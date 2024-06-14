import os
import pathlib
from collections import OrderedDict


class DotEnv:
    def __init__(self, dotenv_path):
        self.dotenv_path = dotenv_path
        self._dict = None

    def read_env_file(self):
        """Reads and returns the .env contents
        self.dotenv_path: file path to the to .env file, if not provided, try to find it in the cwd
        """
        if self.dotenv_path is None or self.dotenv_path == ".":
            # Get the .env file from the current working directory
            parent = os.getcwd()
            self.dotenv_path = pathlib.Path(parent) / ".env"
        else:
            # Use the path provided
            self.dotenv_path = pathlib.Path(self.dotenv_path)

        if not self.dotenv_path.exists():
            raise FileNotFoundError(
                f"File does not exist in the path provided: {self.dotenv_path}"
            )

        with open(self.dotenv_path, "r", encoding="utf-8") as file:
            data = file.read()
        return data

    def parse_env_data(self):
        """
        Parse .env file content and return a dictionary of environment variables.
        """
        env_data = self.read_env_file()
        lines = env_data.splitlines()

        env_vars = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()

            # Remove quotes around values, if any
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]

            env_vars[key] = value
        return env_vars

    def dict(self):
        if self._dict:
            return self._dict

        env_values = self.parse_env_data()
        self._dict = OrderedDict(env_values)

        return self._dict

    def set_as_environment_variables(self):
        if not self.dict():
            return False

        for key, value in self.dict().items():
            if key in os.environ:
                continue
            if value is not None:
                os.environ[key] = value

        return True

    def get(self, key: str):
        data = self.dict()

        if key in data:
            return data[key]

        return None


def load_dotenv(dotenv_path="."):
    """
    Load and set .env values to the environment variable.
    Params:
        dotenv_path: Absolute or relative path to .env file.
    """
    dotenv = DotEnv(dotenv_path)
    dotenv.set_as_environment_variables()


if __name__ == "__main__":
    load_dotenv()
