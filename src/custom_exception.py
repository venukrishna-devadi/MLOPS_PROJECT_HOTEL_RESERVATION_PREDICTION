# for tracking the errors we need traceback library
import traceback
import sys

class CustomException(Exception):
    # we will create our own exception, however we also need exceptions which are predefined
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message) # we need to inherit from exception class
        # if the error is already existing in the predefined Exception we will show that, if not custom exception
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    ### The @staticmethod decorator in Python is used to define a method inside a 
    # class that does not require access to instance (self) or class (cls) attributes. 
    # It behaves like a regular function but is logically grouped within a class.

    #Use Cases of @staticmethod:
	#1.	Utility Methods – Functions related to the class but do not need instance or class data.
	#2.	Code Organization – Keeps helper functions inside relevant classes instead of keeping them outside.
	#3.	Improves Readability – Clearly indicates that the method does not modify instance/class attributes.
    def get_detailed_error_message(error_message, error_detail:sys):

        # exc_info() returns 3 opts, we need only the last thing which return traceback
        _,_, exc_tb = traceback.sys.exc_info()
        # in which file the error occured
        file_name = exc_tb.tb_frame.f_code.co_filename
        # line number
        line_number = exc_tb.tb_lineno

        return f"Error Occured at - {file_name}, line {line_number} : {error_message}"
    
    def __str__(self):
        return self.error_message
