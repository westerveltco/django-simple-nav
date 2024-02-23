from __future__ import annotations

from django_simple_nav.nav import Nav
from django_simple_nav.nav import NavItem


class TailwindMainNav(Nav):
    template_name = "navs/tailwind_main.html"
    items = [
        NavItem(title="Dashboard", url="/tailwind/"),
        NavItem(title="Team", url="/team/"),
        NavItem(title="Projects", url="/projects/"),
        NavItem(title="Calendar", url="/calendar/"),
    ]


class TailwindProfileNav(Nav):
    template_name = "navs/tailwind_profile.html"
    items = [
        NavItem(title="Your Profile", url="/profile/"),
        NavItem(title="Settings", url="/settings/"),
        NavItem(title="Sign out", url="/sign-out/"),
    ]
