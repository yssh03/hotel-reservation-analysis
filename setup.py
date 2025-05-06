from setuptools import setup, find_packages
import os

folder_list = ["artifacts", "config", "src",
               "notebook", "utils", "templates", "static", "logs"]


for folder in folder_list:
    if folder in ["src", "utils", "config"]:
        os.makedirs(folder, exist_ok=True)
        with open(os.path.join(os.getcwd(), folder, "__init__.py"), "w") as fp:
            pass
    else:
        os.makedirs(folder, exist_ok=True)

# with open(os.path.join(os.getcwd(), "logger.py"), "w"):
#     pass

# with open("requirements.txt") as txt:
#     requirements = txt.read().splitlines()

# setup(
#     name="Hotel Reservation",
#     version="0.1",
#     author="Yash Patel",
#     packages=find_packages(),
#     install_requires=requirements

# )
