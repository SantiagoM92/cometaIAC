from flask import Flask
from flask_restx import Api, Namespace, Resource
from logging.handlers import TimedRotatingFileHandler
from config import DevelopmentConfig, Config, MessagesNamespace, ActuatorNamespace
from models import RequestMessage, ResponseMessage
from security import require_apikey
from services import ProcessMessageService
import logging
import sys

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

logger = logging.getLogger()
logger.setLevel(app.config['LOG_LEVEL'])

file_handler = TimedRotatingFileHandler(app.config['LOG_FILE'], when="midnight", interval=1, backupCount=6)
file_handler.setLevel(app.config['LOG_LEVEL'])
file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(app.config['LOG_LEVEL'])
console_handler.setFormatter(file_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

api = Api(app, version=Config.API_VERSION, title=Config.API_TITLE, description=Config.API_DESCRIPTION)
api_message = Namespace(MessagesNamespace.ID, description=MessagesNamespace.DESCRIPTION)
api.add_namespace(api_message, path=Config.API_PREFIX)


@api_message.route(MessagesNamespace.PATH)
class ProcessRequest(Resource):
    @require_apikey
    @api_message.doc(MessagesNamespace.PATH)
    @api_message.expect(RequestMessage.get_request_model(api))
    @api_message.marshal_with(ResponseMessage.get_response_model(api))
    def post(self):
        process_message_service = ProcessMessageService()
        return process_message_service.process_request()


api_actuator = Namespace(ActuatorNamespace.ID, description=ActuatorNamespace.DESCRIPTION)
api.add_namespace(api_actuator, path=Config.API_PREFIX)


@api_actuator.route(ActuatorNamespace.PATH)
class HealthCheck(Resource):
    def get(self):
        return {'status': 'UP'}, 200


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'], host='0.0.0.0', port=app.config['PORT'])
