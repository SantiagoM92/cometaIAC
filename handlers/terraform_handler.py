import logging
import os
import random
import subprocess

from config import TerraformConfig
from exceptions import TerraformInitError, TerraformPlanError, TerraformDestroyError


def run_terraform_command(command, working_dir):
    try:
        result = subprocess.run(command, check=True, cwd=working_dir, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, text=True)
        return {"success": True, "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"success": False, "error": e.stderr}


class TerraformHandler:
    def __init__(self, provider, credentials, hcl_content):
        self.provider = provider
        self.credentials = credentials
        self.hcl_content = hcl_content
        self.workspace = self.create_workspace()
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_workspace(self):
        try:
            home_dir = os.path.expanduser("~")
            random_number = random.randint(TerraformConfig.RANDOM_INIT, TerraformConfig.RANDOM_END)
            tf_workspace = os.path.join(home_dir,
                                        f"{TerraformConfig.TEMP_PATH}/{TerraformConfig.BASE_DIRECTORY}{random_number}")
            os.makedirs(tf_workspace, exist_ok=True)
            return tf_workspace
        except Exception as e:
            self.logger.error("Error creating workspace:\n", e)
            raise TerraformInitError("Error creating workspace, try again")

    def set_env_variables(self):
        if self.provider == TerraformConfig.AZURE:
            os.environ["ARM_CLIENT_ID"] = self.credentials["arm_client_id"]
            os.environ["ARM_CLIENT_SECRET"] = self.credentials["arm_client_secret"]
            os.environ["ARM_TENANT_ID"] = self.credentials["arm_tenant_id"]
            os.environ["ARM_SUBSCRIPTION_ID"] = self.credentials["arm_subscription_id"]
        elif self.provider == TerraformConfig.AWS:
            os.environ["AWS_ACCESS_KEY_ID"] = self.credentials["aws_access_key_id"]
            os.environ["AWS_SECRET_ACCESS_KEY"] = self.credentials["aws_secret_access_key"]
            os.environ["AWS_DEFAULT_REGION"] = self.credentials["aws_region"]

    def run_init(self):
        init_command = ["terraform", "init"]
        init_output = run_terraform_command(init_command, self.workspace)

        if init_output["success"]:
            self.logger.info("terraform init successfully executed:\n")
            self.logger.debug(init_output["output"])
            return init_output["output"]
        else:
            self.logger.error("Error running Terraform Terraform Init:\n", init_output["error"])
            raise TerraformInitError("Error running terraform init, try again")

    def run_plan(self):
        plan_command = ["terraform", "plan"]
        plan_output = run_terraform_command(plan_command, self.workspace)

        if plan_output["success"]:
            self.logger.info("terraform plan successfully executed:\n")
            self.logger.debug(plan_output["output"])
            return plan_output["output"]

        else:
            self.logger.error("Error running Terraform Plan:\n", plan_output["error"])
            raise TerraformPlanError("Error running terraform plan, check the generated template reformulate your "
                                     "request and try again")

    def run_apply(self):
        apply_command = ["terraform", "apply", "-auto-approve"]
        apply_output = run_terraform_command(apply_command, self.workspace)

        if apply_output["success"]:
            self.logger.info("terraform apply successfully executed:\n")
            self.logger.debug(apply_output["output"])
            return {"result": 200, "output": apply_output["output"]}
        else:
            self.logger.error("Error running Terraform Apply:\n", apply_output["error"])
            return {"result": 500, "output": apply_output["error"]}

    def run_destroy(self):
        destroy_command = ["terraform", "destroy", "-auto-approve"]
        destroy_output = run_terraform_command(destroy_command, self.workspace)

        if destroy_output["success"]:
            self.logger.info("terraform destroy successfully executed:\n")
            self.logger.debug(destroy_output["output"])
            return destroy_output["output"]
        else:
            self.logger.error("Error running terraform destroy:\n", destroy_output["error"])
            raise TerraformDestroyError("Error running terraform destroy, check the generated template")

    def save_hcl_content(self):
        full_path = os.path.join(self.workspace, TerraformConfig.TF_FILE_NAME)
        with open(full_path, "w") as archivo:
            archivo.write(self.hcl_content)