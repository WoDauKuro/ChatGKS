"""This module extracts information from the `.env` file
for using the AplhaVantage API key.
"""

# For communicating with computer's
# operating system
import os

# For data validation
from pydantic_settings import BaseSettings


def return_full_path(filename: str = ".env") -> str:
    """Uses os to return the correct path of the `.env` file."""
    absolute_path = os.path.abspath(__file__)
    directory_name = os.path.dirname(absolute_path)
    full_path = os.path.join(directory_name, filename)
    return full_path


class Settings(BaseSettings):
    """Uses pydantic to define settings for project."""

    groq_api_key: str


    class Config:
        env_file = return_full_path(".env")


# Creating an instance of `Settings` class
# to be imported in notebook.
settings = Settings()
