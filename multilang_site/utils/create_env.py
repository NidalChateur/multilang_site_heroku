import os
from pathlib import Path

from django.core.management.utils import get_random_secret_key

from .encryptor import Encryptor

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env_file = BASE_DIR / ".env"


def create_environment_variables_file():
    if not os.path.exists(env_file):
        with open(env_file, "w") as f:
            f.write(f"SECRET_KEY={get_random_secret_key()}\n")
            f.write(f"FERNET_KEY={Encryptor.generate_key()}\n")
            f.write("JWT_PASSWORD=password\n")

            f.write("\n\n")

            f.write("# set your mail config here (used by reset password)\n")
            f.write("EMAIL_PORT=\n")
            f.write("EMAIL_HOST=\n")
            f.write("EMAIL_HOST_USER=\n")
            f.write("EMAIL_HOST_PASSWORD=\n")

            f.write("\n\n")
            f.write("# set your openAI API KEY here (used by chatbot)\n")
            f.write("# visit https://platform.openai.com/ \n")
            f.write("OPENAI_API_KEY=\n")
