import logging

from flask import request
from models import RequestMessage, ResponseMessage
from processor import MessageProcessor


class ProcessMessageService:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_request(self):
        request_data = request.get_json()

        if not request_data or 'message' not in request_data or 'credentials' not in request_data:
            response_message = ResponseMessage("Incomplete request, check it and retry 😥", None, None)
            return response_message.to_dict(), 400
        else:

            request_message = RequestMessage.from_dict(request_data)

            self.logger.info("Starting processing message")
            message_processor = MessageProcessor(request_message.message, request_message.credentials)
            response = message_processor.process_message()
            self.logger.info("End processing message")

            if response["result"] == 200:
                response_message = ResponseMessage(response["response"].join(" 🚀"), response["output"], response["tf"])
                return response_message.to_dict(), 200
            else:
                response_message = ResponseMessage(response["response"].join(" 💥"), response["output"], response["tf"])
                return response_message.to_dict(), 500
