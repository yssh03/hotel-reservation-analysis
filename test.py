from src.custom_exceptions import CustomException
import sys
try:
    print(10/0)

except Exception as e:
    raise CustomException("Not possible", sys)
