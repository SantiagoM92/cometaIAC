import logging
import time
from openai import OpenAI

from config import OpenIAConfig
from exceptions import MaxRetriesError


class OpenAIHandler:
    def __init__(self, api_key, thread_id, assistant_id):
        self.client = OpenAI(api_key=api_key)
        self.thread_id = thread_id
        self.assistant_id = assistant_id
        self.logger = logging.getLogger(self.__class__.__name__)

    def send_message(self, content):
        response = self.client.beta.threads.messages.create(
            self.thread_id,
            role="user",
            content=content
        )
        self.logger.info("Message sent successfully:\n")
        self.logger.debug(response)
        return response

    def run_thread(self):
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )
        self.logger.info("Run create successfully:\n")
        self.logger.debug(run)

        run_retrieve = self.client.beta.threads.runs.retrieve(
            thread_id=self.thread_id,
            run_id=run.id
        )
        self.logger.info("Run retrieve successfully:\n")
        self.logger.debug(run_retrieve)

        retry = 0
        while run_retrieve.status != OpenIAConfig.COMPLETE_STATUS and retry < OpenIAConfig.RETRIES:
            retry += 1
            self.logger.info(f"Run retrieve retry {retry}...")
            time.sleep(OpenIAConfig.STANDBY)
            run_retrieve = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id,
                run_id=run.id
            )
            self.logger.info("Run retrieve successfully:\n")
            self.logger.debug(run_retrieve)

        if run_retrieve.status != OpenIAConfig.COMPLETE_STATUS and retry >= OpenIAConfig.RETRIES:
            self.logger.error(f"Error getting run retrieve in {OpenIAConfig.RETRIES} retries")
            raise MaxRetriesError(f"Error getting run retrieve in {OpenIAConfig.RETRIES} retries")

        self.logger.info("Run successfully:\n")
        self.logger.debug(run_retrieve)
        return run_retrieve

    def get_run_steps(self, run_id):
        response = self.client.beta.threads.runs.steps.list(
            thread_id=self.thread_id,
            run_id=run_id
        )
        self.logger.info("Get run steps successfully:\n")
        self.logger.debug(response)
        return response

    def get_message_retrieve(self, message_id):
        response = self.client.beta.threads.messages.retrieve(
            message_id=message_id,
            thread_id=self.thread_id,
        )
        self.logger.info("Get message retrieve successfully:\n")
        self.logger.debug(response)
        return response
