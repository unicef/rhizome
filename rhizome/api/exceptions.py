class RhizomeApiException(Exception):

    defaultMessage = "Sorry, this request could not be processed."
    defaultCode = -1

    def __init__(self, message=defaultMessage, code=defaultCode):

        self.message = message
        self.code = code


class InputException(Exception):

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        if data is not None:
            self.data = data
