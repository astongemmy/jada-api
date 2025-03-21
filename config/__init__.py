from config.common import ENVIRONMENT
from .development import DevConfig


configs = {
  'development': DevConfig,
  'production': DevConfig,
  'staging': DevConfig,
  'test': DevConfig
}

config = configs[ENVIRONMENT]()