from typing import Type

from django.apps import apps
from django.core.checks import Error, Tags, register

from . import settings
from .dashboard import AppIndexDashboard, Dashboard
from .utils import get_app_dashboard_config, import_value


def check_dashboard(key, path, base_cls):
    try:
        dashboard_csl: Type[base_cls] = import_value(path)
    except ImportError:
        error = Error(
            f"Failed to import {key}: {path!r}",
            hint=f"Fix {key} value in settings.",
            id='jet.dashboard.E001',
        )
        return [error]
    if not issubclass(dashboard_csl, base_cls):
        error = Error(
            f"Invalid {key}. "
            f"Expected subclass of {base_cls.__name__} got {type(dashboard_csl).__name__}",
            id='jet.dashboard.E002',
        )
        return [error]
    return []


@register(Tags.compatibility)
def check_index_dashboard(app_configs, **kwargs):
    return check_dashboard('JET_INDEX_DASHBOARD', settings.JET_INDEX_DASHBOARD, Dashboard)


@register()
def check_app_index_dashboard(app_configs, **kwargs):
    app_labels = {a.label for a in apps.get_app_configs()}
    errors = []
    config = get_app_dashboard_config(settings.JET_APP_INDEX_DASHBOARD)
    for key in config.keys():
        if key is None:
            continue
        if key not in app_labels:
            errors.append(
                Error(
                    f"{key} is not in the app list.",
                    hint=f"Choose from {', '.join(app_labels)}.",
                    id='jet.dashboard.E003',
                )
            )
    for key, path in config.items():
        es = check_dashboard(f'JET_APP_INDEX_DASHBOARD[{key}]', path, AppIndexDashboard)
        errors.extend(es)
    return errors


@register(Tags.compatibility)
def check_yandex_metrika_creds(app_configs, **kwargs):
    if (
        settings.JET_MODULE_YANDEX_METRIKA_CLIENT_ID and
        not settings.JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET or
        settings.JET_MODULE_YANDEX_METRIKA_CLIENT_SECRET and
        not settings.JET_MODULE_YANDEX_METRIKA_CLIENT_ID
    ):
        error = Error(
            f"You need to specify both client_id and client_secret for yandex metrika.",
            id='jet.dashboard.E003',
        )
        return [error]
    return []
