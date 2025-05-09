import os
from dotenv import load_dotenv
load_dotenv()
print(os.getenv("AWS_ACCESS_KEY_ID"))