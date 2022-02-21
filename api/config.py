class Config:
    TESTING = False
    DEBUG = False
    SERVER_PORT = 3000

class DevelopementConfig(Config):
    DEVELOPEMENT = True
    DEBUG = True

class TestingConfig(Config):
    TESTING = False
