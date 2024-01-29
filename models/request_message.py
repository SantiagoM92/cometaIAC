from flask_restx import fields, Api


class RequestMessage:
    def __init__(self, message, credentials):
        self.message = message
        self.credentials = credentials

    @staticmethod
    def from_dict(data):
        return RequestMessage(data['message'], data['credentials'])

    @staticmethod
    def get_request_model(self: Api):
        return self.model('RequestModel', {
            'message': fields.String(required=True, description='Message to process', example='Create a virtual '
                                                                                              'machine with ...'),
            'credentials': fields.Raw(required=True, description='Credentials to use in the cloud provider',
                                      example={"ARM_CLIENT_ID": "809ce2f8-bd6f-4637-b227-XXXXXX",
                                               "ARM_CLIENT_SECRET": "ncY8Q~Efpub6PjxkfIkp8i3u5sb0iER~XXXXXX",
                                               "ARM_TENANT_ID": "9396c2e5-4534-4b93-827f-7471bdXXXXXX",
                                               "ARM_SUBSCRIPTION_ID": "02b9c0e0-8708-46b2-90f1-c26c6XXXXXX"})
        })
