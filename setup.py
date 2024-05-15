from setuptools import find_packages, setup
from typing import List

def list_requirements()->List[str]:
    """
    This function reads the requirements.txt and prepares a list of all requirements and returns it.
    """
    requirement_list:List[str] = []

    """
    Write a code to read requirements.txt file and append each requirements in requirement_list variable.
    """
    return requirement_list

setup(
    name="Sensor_Fault_Detection",
    version="0.0.0",
    author="Sahil Sharma",
    author_email="sahiltheanalyst@gmail.com",
    packages=find_packages(),
    install_requires=list_requirements()
)