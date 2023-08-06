from typing import Any, Dict, List

from django.template import loader
from django.template.context import BaseContext

from .config import get_menu_items


class Section:
    template_name = None

    def __init__(self, template_name=None):
        self.template_name = self.template_name or template_name
        self.context = None  # will be populated in render()

    def get_context_data(self, context) -> Dict[str, Any]:
        if isinstance(context, BaseContext):
            context = context.flatten()
        return {**context, 'self': self}

    def get_extra_context(self):
        return {}

    def init_with_context(self, context):
        """Hook which will be called before rendering."""

    def render(self, context):
        self.context = self.get_context_data(context)
        self.init_with_context(self.context)
        self.context.update(self.get_extra_context())
        return loader.render_to_string(self.template_name, self.context)

    def popups(self) -> List['Section']:
        return []

    def render_popups(self):
        for section in self.popups():
            yield section.render(self.context)


class NavSection(Section):
    template_name = 'jet/sidebar/section_nav.html'


class AppPopup(Section):
    template_name = 'jet/sidebar/popup_app.html'

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = app

    def get_extra_context(self):
        return {'app': self.app}


class AppsSection(Section):
    template_name = 'jet/sidebar/section_apps.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apps = []

    def get_extra_context(self):
        return {'app_list': self.apps}

    def init_with_context(self, context):
        self.apps = [
            app for app in get_menu_items(context)
            if app.has_perms
        ]

    def popups(self):
        return [AppPopup(app) for app in self.apps]


class BookmarkSection(Section):
    template_name = 'jet/sidebar/section_bookmarks.html'


class Sidebar(Section):
    template_name = 'jet/sidebar/sidebar.html'

    def __init__(self, *args, **kwargs):
        super(Sidebar, self).__init__(*args, **kwargs)
        self.sections: List[Section] = []

    def init_with_context(self, context):
        self.sections = [
            NavSection(),
            AppsSection(),
        ]
        if context['request'].user.has_perm('jet.change_bookmark'):
            self.sections.append(BookmarkSection())

    def popups(self):
        for item in self.sections:
            yield from item.popups()

    def render_sections(self):
        for section in self.sections:
            yield section.render(self.context)
