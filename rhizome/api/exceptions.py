class RhizomeApiException(Exception):

    defaultMessage = "Sorry, this request could not be processed."
    defaultCode = -1

    def __init__(self, message=defaultMessage, code=defaultCode):
        '''
        We try to parse and prettify of the exception, otherwise we just
        return to the API whatever error we have caught
        '''

        self.message = message
        self.code = code

        try:
            self.message = self.parse_error_msg()
        except:
            pass

    def parse_error_msg(self):
        '''
        A way for us to parse common django / tastypie error messages
        so that we can return useful information to the API.
        '''

        if self.code == 497:
            detail_msg = self.message.split('DETAIL:  ')[1]
            tmp_column_string, tmp_input_value = detail_msg.split(')=(')
            column_string = tmp_column_string[tmp_column_string.find("(") + 1 :]
            input_value = tmp_input_value[:tmp_input_value.find(")")]
            return 'key: "{0}" with value: "{1}" already exists'\
                .format(column_string, input_value)

        return self.message

    #########################
    ## rhizome error codes ##
    #########################

    # 499
    # 499
    # 497 -- IntegrityError: for instance create an indicator with the same name



class InputException(Exception):

    def __init__(self, code, message, data=None):
        self.code = code
        self.message = message
        if data is not None:
            self.data = data
