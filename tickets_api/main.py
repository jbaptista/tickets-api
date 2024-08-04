from .app_factory import create_app
from .config import Config
from .utils.logging import config_logging

config = Config()

config_logging(version=config.version, level=config.log_level, is_local=config.is_local)

app = create_app(config)
