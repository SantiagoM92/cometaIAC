import logging

from config import OpenIAConfig, TerraformConfig
from exceptions import MissingCredentialsError, InvalidProviderError, OpenAIError
from handlers import OpenAIHandler, TerraformHandler


class MessageProcessor:
    def __init__(self, message, credentials):
        self.message = message
        self.credentials = credentials
        self.logger = logging.getLogger(self.__class__.__name__)

    def process_message(self):

        try:
            hcl_content = self.process_openai()
            terraform_result = self.process_terraform(hcl_content)

            if terraform_result["result"] == 200:
                return {"result": 200,
                        "response": "Your request was successfully processed, please check the output",
                        "tf": hcl_content,
                        "output": terraform_result["output"]}
            else:
                return {"result": 500,
                        "response": "Error processing your request, please check the output and generated template."
                                    "Reformulate your request and try again",
                        "tf": hcl_content,
                        "output": terraform_result["output"]}

        except Exception as e:
            return {"result": 500, "response": str(e), "tf": None, "output": None}

    def process_openai(self):

        try:
            open_ia_handler = OpenAIHandler(OpenIAConfig.API_KEY, OpenIAConfig.THREAD_ID, OpenIAConfig.ASSISTANT_ID)

            open_ia_handler.send_message(self.message)

            run = open_ia_handler.run_thread()

            run_steps = open_ia_handler.get_run_steps(run.id)

            current_message_id = run_steps.data[0].step_details.message_creation.message_id

            message = open_ia_handler.get_message_retrieve(current_message_id)

            content = message.content[0].text.value

            content = content.replace("```hcl\n", "").replace("\n```", "")

            self.logger.info("Content successfully retrieved:\n")
            self.logger.debug(content)

        except Exception as e:
            self.logger.error("Error processing openAI:\n", e)
            raise OpenAIError("Error processing openIA, reformulate your request and try again")

        return content

    def process_terraform(self, hcl_content):

        provider = self.validate_credentials(hcl_content)

        terraform_handler = TerraformHandler(provider, self.credentials, hcl_content)

        terraform_handler.save_hcl_content()

        terraform_handler.set_env_variables()

        terraform_handler.run_init()

        terraform_plan = terraform_handler.run_plan()

        if terraform_plan["result"] == 500:
            return terraform_plan
        else:
            return terraform_handler.run_apply()

    def validate_credentials(self, hcl_content):
        if TerraformConfig.AZURE_PROVIDER in hcl_content:
            required_keys = ['arm_client_id', 'arm_client_secret', 'arm_tenant_id', 'arm_subscription_id']
            missing_keys = [key for key in required_keys if key not in self.credentials]
            if missing_keys:
                raise MissingCredentialsError(f"Missing Azure credentials: {', '.join(missing_keys)}")
            provider = TerraformConfig.AZURE

        elif TerraformConfig.AWS_PROVIDER in hcl_content:
            required_keys = ['aws_access_key_id', 'aws_secret_access_key', 'aws_region']
            missing_keys = [key for key in required_keys if key not in self.credentials]
            if missing_keys:
                raise MissingCredentialsError(f"Missing AWS credentials: {', '.join(missing_keys)}")
            provider = TerraformConfig.AWS

        else:
            raise InvalidProviderError("The provider is not valid")

        return provider
