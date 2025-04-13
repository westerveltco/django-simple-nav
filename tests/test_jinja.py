from .jinja2.environment import environment


def test_derp():
    """Render the template"""
    template = environment.from_string('<p>{{ django_simple_nav("tests.navs.DummyNav", "dummy_nav.html") }}</p>')
    print(template.render(some_var=[1, 2, 3]))
    assert True
