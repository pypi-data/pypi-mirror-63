from typing import Dict, List

from django.utils.text import capfirst, slugify
from django.utils.translation import gettext_lazy as _
from pydantic import BaseModel

from jet import settings
from jet.models import PinnedApplication
from jet.utils import get_admin_site, get_app_list, user_is_authenticated


class MenuItem(BaseModel):
    name: str = None
    label: str = None
    url: str = None
    url_blank = False
    has_perms = False
    object_name: str = None
    current = False


class MenuSection(BaseModel):
    app_label: str = None
    label: str = None
    url: str = None
    url_blank = False
    has_perms = False
    items: List[MenuItem] = []
    pinned = False
    current = False
    models: List[MenuItem] = []


class ItemConfig(BaseModel):
    """
    name - model name (can be either MODEL_NAME or APP_LABEL.MODEL_NAME)
    label - item text label
    url - custom url
    url_blank - open url in new table
    permissions - list of required permissions to display item
    """
    name: str = None
    label: str = None
    url: str = None
    url_blank: bool = None
    permissions: List[str] = None


class AppConfig(BaseModel):
    """
    app_label - application name
    label - application text label
    items - list of children items
    url - custom url
    url_blank - open url in new table
    permissions - list of required permissions to display item
    """
    app_label: str = None
    label: str = None
    items: List[ItemConfig] = None
    url: str = None
    url_blank: bool = None
    permissions: List[str] = None


def get_original_menu_items(context) -> List[MenuSection]:
    if context.get('user') and user_is_authenticated(context['user']):
        pinned_apps = PinnedApplication.objects.filter(user=context['user'].pk).values_list('app_label', flat=True)
    else:
        pinned_apps = []
    return [
        MenuSection(
            app_label=app['app_label'],
            url=app['app_url'],
            label=str(app.get('name', capfirst(_(app['app_label'])))),
            has_perms=app.get('has_module_perms', False),
            pinned=app['app_label'] in pinned_apps,
            models=[
                MenuItem(
                    url=model.get('admin_url'),
                    name=model['model_name'],
                    object_name=model['object_name'],
                    label=str(model.get('name', model['object_name'])),
                    has_perms=any(model.get('perms', {}).values()),
                )
                for model in app['models']
            ]
        )
        for app in get_app_list(context)
    ]

    # return map(lambda app: {
    #     'app_label': app['app_label'],
    #     'url': app['app_url'],
    #     'url_blank': False,
    #     'label': app.get('name', capfirst(_(app['app_label']))),
    #     'has_perms': app.get('has_module_perms', False),
    #     'models': list(map(lambda model: {
    #         'url': model.get('admin_url'),
    #         'url_blank': False,
    #         'name': model['model_name'],
    #         'object_name': model['object_name'],
    #         'label': model.get('name', model['object_name']),
    #         'has_perms': any(model.get('perms', {}).values()),
    #     }, app['models'])),
    #     'pinned': app['app_label'] in pinned_apps,
    #     'custom': False
    # }, app_list)


class MenuBuilder:
    def __init__(self, context):
        self.context = context

    def get_original_menu_item(self, name: str, app_label: str, original_apps):
        parts = name.split('.', 2)
        if len(parts) > 1:
            app_label, name = parts
        if app_label in original_apps:
            for model in original_apps[app_label].models:
                if model.name == name:
                    return model

    def get_menu_item(self, config: ItemConfig, app_label: str, original_apps: Dict[str, MenuSection]):
        item = MenuItem(has_perms=True)
        if config.name:
            original_item = self.get_original_menu_item(config.name, app_label, original_apps)
            if original_item:
                item = original_item.copy()
            else:
                item.has_perms = False
        if config.label is not None:
            item.label = config.label
        if config.url is not None:
            item.url = config.url
        if config.url_blank is not None:
            item.url_blank = config.url_blank
        if config.permissions is not None:
            item.has_perms = item.has_perms and self.context['user'].has_perms(config.permissions)
        return item

    def get_menu_section(self, config: AppConfig, original_apps: Dict[str, MenuSection], pinned_apps: List[str]):
        section = MenuSection(app_label=config.app_label)

        if not config.app_label and not config.label:
            raise ValueError("Custom menu items should at least have 'label' or 'app_label' key")

        # custom section viewable for everyone
        if not config.app_label:
            section.app_label = 'custom_%s' % slugify(config.label, allow_unicode=True)
            section.has_perms = True
        # original section in has_perms=True
        elif section.app_label in original_apps:
            section = original_apps[section.app_label].copy()
        # non-custom, not original - no permissions
        else:
            section.has_perms = False

        if config.label is not None:
            section.label = config.label
        if config.url is not None:
            section.url = config.url
        if config.url_blank is not None:
            section.url_blank = config.url_blank
        if config.permissions is not None:
            section.has_perms = section.has_perms and self.context['user'].has_perms(config.permissions)
        if config.items is not None:
            section.items = [
                self.get_menu_item(item, section.app_label, original_apps)
                for item in config.items
            ]
        section.pinned = section.app_label in pinned_apps
        return section

    def build_from_config(self, custom_apps, original_apps):
        if isinstance(custom_apps, dict):
            admin_site = get_admin_site(self.context)
            custom_apps = custom_apps.get(admin_site.name, [])

        custom_apps = [AppConfig.parse_obj(app) for app in custom_apps]

        pinned_apps = PinnedApplication.objects.filter(user=self.context['user'].pk)
        pinned_apps = pinned_apps.values_list('app_label', flat=True)
        return [
            self.get_menu_section(app, original_apps, pinned_apps)
            for app in custom_apps
        ]

    def build(self):
        original_apps = {
            app.app_label: app
            for app in get_original_menu_items(self.context)
        }
        custom_apps = settings.JET_SIDE_MENU_ITEMS
        if custom_apps not in (None, False):
            app_list = self.build_from_config(custom_apps, original_apps)
        else:
            app_list = list(original_apps.values())
            for app in app_list:
                app.items = app.models
        self.setup_current_app(app_list)
        return app_list

    def setup_current_app(self, apps: List[MenuSection]):
        for app in apps:
            for model in app.items:
                if model.url and self.context['request'].path.startswith(model.url):
                    model.current = True
                    return
            if app.url and self.context['request'].path.startswith(app.url):
                app.current = True
                return


def get_menu_items(context) -> List[MenuSection]:
    b = MenuBuilder(context)
    return b.build()
