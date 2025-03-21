from dataclasses import dataclass
from .common import Config


@dataclass
class DevConfig(Config):
  GOOGLE_AUTH_CLIENT_ID: str = ('1031677911940-gp2bacdvs6maimm540hor9g9k6aadmsj.apps.googleusercontent.com')
  GOOGLE_AUTH_CLIENT_SECRET: str = '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'