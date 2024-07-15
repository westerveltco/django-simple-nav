from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.template.backends.django import Template
from django.utils.module_loading import import_string
from model_bakery import baker

from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem
from tests.navs import DummyNav
from tests.utils import count_anchors

pytestmark = pytest.mark.django_db


def test_init():
    nav = DummyNav

    assert nav.template_name == "tests/dummy_nav.html"
    assert len(nav.items) == 12

    for item in nav.items:
        assert item.title


def test_dotted_path_loading():
    nav = import_string("tests.navs.DummyNav")

    assert nav.template_name == "tests/dummy_nav.html"
    assert len(nav.items) == 12


@pytest.mark.parametrize(
    "user, expected_count",
    [
        (AnonymousUser(), 7),
        (None, 10),
    ],
)
def test_nav_render(user, expected_count, req):
    if not isinstance(user, AnonymousUser):
        user = baker.make(get_user_model())

    req.user = user

    rendered_template = DummyNav().render(req)

    assert count_anchors(rendered_template) == expected_count


def test_dotted_path_nav_render(req):
    req.user = baker.make(get_user_model())

    nav = import_string("tests.navs.DummyNav")

    assert nav().render(req)


@pytest.mark.parametrize(
    "permission, expected_count",
    [
        ("", 10),  # regular authenticated user
        ("is_staff", 13),
        ("is_superuser", 19),
        ("tests.dummy_perm", 13),
    ],
)
def test_nav_render_with_permissions(req, permission, expected_count):
    user = baker.make(get_user_model())

    if permission == "tests.dummy_perm":
        dummy_perm = baker.make(
            "auth.Permission",
            codename="dummy_perm",
            name="Dummy Permission",
            content_type=baker.make("contenttypes.ContentType", app_label="tests"),
        )
        user.user_permissions.add(dummy_perm)
    else:
        setattr(user, permission, True)

    user.save()

    req.user = user
    rendered_template = DummyNav().render(req)

    assert count_anchors(rendered_template) == expected_count


def test_nav_render_with_template_name(req):
    req.user = AnonymousUser()

    rendered_template = DummyNav().render(req, "tests/alternate.html")

    assert "This is an alternate template." in rendered_template


def test_extra_context(req):
    item = NavItem(
        title="Test",
        url="/test/",
        extra_context={"foo": "bar"},
    )

    rendered_item = item.get_context_data(req)

    assert rendered_item.get("foo") == "bar"


def test_extra_context_with_no_extra_context(req):
    item = NavItem(
        title="Test",
        url="/test/",
    )

    rendered_item = item.get_context_data(req)

    assert rendered_item.get("foo") is None


def test_extra_context_shadowing(req):
    item = NavItem(
        title="Test",
        url="/test/",
        extra_context={"title": "Shadowed"},
    )

    rendered_item = item.get_context_data(req)

    assert rendered_item.get("title") == "Test"


def test_extra_context_builtins(req):
    item = NavGroup(
        title="Test",
        items=[
            NavItem(
                title="Test",
                url="/test/",
                extra_context={"foo": "bar"},
            ),
        ],
        url="/test/",
        extra_context={"baz": "qux"},
    )

    rendered_item = item.get_context_data(req)

    assert rendered_item.get("title") == "Test"
    assert rendered_item.get("url") == "/test/"
    assert rendered_item.get("baz") == "qux"

    assert rendered_item.get("items") is not None
    assert len(rendered_item.get("items")) == 1

    rendered_group_item = rendered_item.get("items")[0]

    assert rendered_group_item.get("title") == "Test"
    assert rendered_group_item.get("url") == "/test/"
    assert rendered_group_item.get("foo") == "bar"


def test_get_context_data(req):
    req.user = baker.make(get_user_model())

    context = DummyNav().get_context_data(req)

    assert context["items"]


def test_get_context_data_override(req):
    class OverrideNav(DummyNav):
        def get_context_data(self, request):
            return {"foo": "bar"}

    req.user = baker.make(get_user_model())

    context = OverrideNav().get_context_data(req)

    assert context["foo"] == "bar"


def test_get_context_data_override_render(req):
    class OverrideNav(DummyNav):
        def get_context_data(self, request):
            return {"foo": "bar"}

    req.user = baker.make(get_user_model())

    rendered_template = OverrideNav().render(req)

    assert count_anchors(rendered_template) == 0


def test_rendered_nav_item_active(req):
    item = NavItem(title="Test", url="/test/")
    rendered_item = item.get_context_data(req)

    assert rendered_item.get("active") is False

    req.path = "/test/"
    rendered_item = item.get_context_data(req)

    assert rendered_item.get("active") is True


def test_rendered_nav_group_active_no_url(req):
    item = NavGroup(title="Test", items=[NavItem(title="Test", url="/test/")])

    rendered_item = item.get_context_data(req)

    assert rendered_item.get("active") is False


def test_rendered_nav_item_active_named_url(req):
    item = NavItem(title="Test", url="fake-view")

    req.path = "/fake-view/"
    rendered_item = item.get_context_data(req)

    assert rendered_item.get("active") is True


def test_get_template():
    template = DummyNav().get_template()

    assert isinstance(template, Template)


def test_get_template_override_render(req):
    class TemplateOverrideNav(DummyNav):
        def get_template(self, template_name):
            return """\
<h1>Overridden Template</h1>
<ul>
  {% for item in items %}
    <li>
      <a href="{{ item.url }}"
         class="{% if item.active %}text-indigo-500 hover:text-indigo-300{% else %}hover:text-gray-400{% endif %}">
        {{ item.title }}
      </a>
    </li>
  {% endfor %}
</ul>"""

    req.user = baker.make(get_user_model())

    rendered_template = TemplateOverrideNav().render(req)

    assert "<h1>Overridden Template</h1>" in rendered_template
