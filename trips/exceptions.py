from rest_framework.exceptions import APIException

class MissingParameters(APIException):
    status_code = 400
    default_detail = "Data, origin and destination must be given."
    
class BadDate(APIException):
    status_code = 400
    default_detail = "Data must be greater than now."