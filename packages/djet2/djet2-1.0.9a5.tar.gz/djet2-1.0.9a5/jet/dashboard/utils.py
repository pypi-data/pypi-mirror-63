import logging
from importlib import import_module
from typing import Union

from jet.dashboard import settings


logger = logging.getLogger(__name__)


def import_value(path: str):
    module, name = path.rsplit('.', 1)
    try:
        module = import_module(module)
        value = getattr(module, name)
    except (ImportError, AttributeError) as e:
        raise ImportError(e)
    return value


def get_app_dashboard_config(config: Union[str, dict]):
    if isinstance(config, str):
        return {None: config}
    return config


def get_app_dashboard(app: str, config: dict):
    if app in config:
        return config[app]
    if None in config:
        return config[None]
    return settings.JET_DEFAULT_APP_INDEX_DASHBOARD


def get_current_dashboard(app_label=None):
    if app_label is None:
        path = settings.JET_INDEX_DASHBOARD
    else:
        config = get_app_dashboard_config(settings.JET_APP_INDEX_DASHBOARD)
        path = get_app_dashboard(app_label, config)
    dashboard_cls = import_value(path)
    return dashboard_cls
