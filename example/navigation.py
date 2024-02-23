from __future__ import annotations

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavItem


class ExampleListNav(Nav):
    template_name = "navs/example_list.html"
    items = [
        NavItem(title="Tailwind CSS", url="/tailwind/"),
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
