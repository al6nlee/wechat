import configparser
import logging
import os

from .const import BASE_DIR


def get_conf_section(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(BASE_DIR, "conf", "conf.ini"))
    if section not in config.sections():
        return None
    try:
        return config.get(section, key)
    except Exception as err:
        log.exception(str(err))
    return None


log = logging.getLogger('django')
