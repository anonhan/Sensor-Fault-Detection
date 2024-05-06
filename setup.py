from setuptools import find_packages, setup
from typing import List

def list_requirements()->List[str]:
    """
    This function reads the requirements.txt and prepares a list of all requirements and returns it.
    """
    list_reqs = []
    with open(file="requirements.txt",mode='r') as f:
        f = f.readlines()
        list_reqs = [i.strip() for i in f]
    return list_reqs

setup(
    name="Sensor_Fault_Detection",
    version="0.0.0",
    author="Sahil Sharma",
    author_email="sahiltheanalyst@gmail.com",
    packages=find_packages(),
    install_requires=list_requirements()
)
# print(list_requirements())