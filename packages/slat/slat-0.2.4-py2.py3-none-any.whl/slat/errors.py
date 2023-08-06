"""
Exception to through that ensures all needed information is gathered in order to return
a well formed lambda response
"""
import json


class LambdaResponseException(Exception):
    """
    Build a custom Exception to ensure we get predictable responses back to APIG
    see: https://aws.amazon.com/blogs/compute/error-handling-patterns-in-amazon-api-gateway-and-aws-lambda/
    """

    def __init__(self, message: str, exception_type: str, error_code: str, status_code: int):
        # Call the base class constructor with the parameters it needs
        super(LambdaResponseException, self).__init__(message)
        self.message = message
        self.exception_type = exception_type
        self.error_code = error_code
        self.status_code = status_code

    def __str__(self):
        my_error_obj = {
            'errorType': self.error_code,
            'httpStatus': self.status_code,
            'message': self.message
        }
        return json.dumps(my_error_obj)
