class Config:
    API_KEY = '5078799b-c729-4150-9cb9-22f1b24f5b23'
    API_PREFIX = '/api/v1'
    API_DESCRIPTION = 'API Rest for the use of the CometaIAC prototype. By Jairo Martínez 🐶🐈‍⬛'
    API_TITLE = 'CometaIAC 🤖'
    API_VERSION = '1.0'


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
    API_KEY = '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'
    THREAD_ID = 'thread_sJ6ZNANbfYSdYemBRVaObopJ'
    ASSISTANT_ID = 'asst_7bYaPBJuBoweykJEH8krITXX'
    COMPLETE_STATUS = 'completed'
    STANDBY = 9
    RETRIES = 3


class TerraformConfig:
    RANDOM_INIT = 1000
    RANDOM_END = 99999
    TEMP_PATH = '.cmt'
    BASE_DIRECTORY = 'workspace'
    TF_FILE_NAME = 'main_generated.tf'
    AZURE_PROVIDER = 'azurerm'
    AWS_PROVIDER = 'aws'
    AZURE = 'az'
    AWS = 'aws'
