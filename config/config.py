import os


class Config:
    API_KEY = os.getenv('API_KEY')
    API_PREFIX = '/api/v1'
    API_DESCRIPTION = 'API Rest for the use of the CometaIAC prototype. By Jairo Martínez 🐶🐈‍⬛'
    API_TITLE = 'CometaIAC 🤖'
    API_VERSION = '1.0'
    LOG_FILE = 'app.log'


class MessagesNamespace:
    ID = 'Messages'
    DESCRIPTION = 'Message processing'
    PATH = '/process_message'


class ActuatorNamespace:
    ID = 'Actuator'
    DESCRIPTION = 'Verify the status of the application'
    PATH = '/actuator/health'


class DevelopmentConfig(Config):
    LOG_LEVEL = 'DEBUG'
    DEBUG = True
    PORT = 5000


class ProductionConfig(Config):
    LOG_LEVEL = 'INFO'
    DEBUG = False
    PORT = 5000


class OpenIAConfig:
    API_KEY = os.getenv('OPENAI_API_KEY')
    THREAD_ID = os.getenv('THREAD_ID')
    ASSISTANT_ID = os.getenv('ASSISTANT_ID')
    COMPLETE_STATUS = 'completed'
    STANDBY = 9
    RETRIES = 5


class TerraformConfig:
    RANDOM_INIT = 1000
    RANDOM_END = 99999
    TEMP_PATH = 'data'
    BASE_DIRECTORY = 'workspace'
    TF_FILE_NAME = 'main_generated.tf'
    AZURE_PROVIDER = 'azurerm'
    AWS_PROVIDER = 'aws'
    AZURE = 'az'
    AWS = 'aws'
