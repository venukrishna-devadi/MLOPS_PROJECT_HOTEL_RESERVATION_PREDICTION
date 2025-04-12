from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_num(a,b):
    try:
        result = a/b
        logger.info("Dividing 2 numbers a and b")
        return result
    except Exception as e:
        logger.error("Error Occured")
        raise CustomException("Custom Error: Cannot Devide", sys)
        # here we are not creating any object to use custom exception class
        # its because of static method

if __name__ == "__main__":
    # when we do python name.run, all the things below the line runs
    try:
        logger.info("Starting main programme")
        divide_num(10,2)
    except CustomException as ce:
        logger.error(str(ce))



    