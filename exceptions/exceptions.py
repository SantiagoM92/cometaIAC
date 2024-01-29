class InvalidProviderError(Exception):
    """Exception when the supplier is invalid or missing."""
    pass


class MissingCredentialsError(Exception):
    """Exception when necessary credentials are missing."""
    pass


class MaxRetriesError(Exception):
    """Exception when number of attempts reached."""
    pass


class TerraformInitError(Exception):
    """Exception when terraform init fail."""
    pass


class TerraformPlanError(Exception):
    """Exception when terraform plan fail."""
    pass


class TerraformApplyError(Exception):
    """Exception when terraform apply fail."""
    pass


class TerraformDestroyError(Exception):
    """Exception when terraform destroy fail."""
    pass


class OpenAIError(Exception):
    """Exception when request to OpenAI fail."""
    pass
