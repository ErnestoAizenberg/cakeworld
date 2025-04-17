from .config import Config

class DevelopmentConfig(Config):
  PORT = 5000
  HOST = '127.0.0.1'
