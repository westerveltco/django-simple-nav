from __future__ import annotations

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavGroup
from django_simple_nav.nav import NavItem


class ExampleListNav(Nav):
    template_name = "navs/example_list.html"
    items = [
        NavItem(title="Tailwind CSS", url="/tailwind/"),
        NavItem(title="Bootstrap 4", url="/bootstrap4/"),
        NavItem(title="Bootstrap 5", url="/bootstrap5/"),
    ]


class TailwindMainNav(Nav):
    template_name = "navs/tailwind_main.html"
    items = [
        NavItem(title="Dashboard", url="/tailwind/"),
        NavItem(title="Team", url="#"),
        NavItem(title="Projects", url="#"),
        NavItem(title="Calendar", url="#"),
    ]


class TailwindProfileNav(Nav):
    template_name = "navs/tailwind_profile.html"
    items = [
        NavItem(title="Your Profile", url="#"),
        NavItem(title="Settings", url="#"),
        NavItem(title="Sign out", url="#"),
    ]


class BootstrapNav(Nav):
    template_name = "navs/bootstrap4.html"
    items = [
        NavItem(title="Home", url="#"),
        NavItem(title="Link", url="#"),
        NavItem(title="Disabled", url="#", extra_context={"disabled": True}),
        NavGroup(
            title="Dropdown",
            items=[
                NavItem(title="Action", url="#"),
                NavItem(title="Another action", url="#"),
                NavItem(title="Something else here", url="#"),
            ],
        ),
    ]
