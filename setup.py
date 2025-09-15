from setuptools import find_packages,setup

setup (
    name="Mcqgenerator",
    version="0.0.1",
    author="Odusanya Kayode",
    author_email="Odusanykayode25@gmail.com",
    install_requires=["transformers","huggingface_hub","langchain","streamlit","python-dotenv","pyPDF2"],
    packages=find_packages()
)