from flask_restx import fields, Api


class ResponseMessage:
    def __init__(self, response, output, tf):
        self.response = response
        self.output = output
        self.tf = tf

    def to_dict(self):
        return {
            "response": self.response,
            "output": self.output,
            "template": self.tf
        }

    def get_response_model(self: Api):
        return self.model('ResponseModel', {
            'response': fields.String(description='Response message'),
            'output': fields.String(description='Processing output'),
            'template': fields.String(description='Processed terraform template')
        })
