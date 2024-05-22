import os
from dotenv import dotenv_values

def load_env(path=None) -> dict:
    if not path:
        path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    return {
        **dotenv_values(
            os.path.join(path, ".env")
        ),
        **dotenv_values(os.path.join(path, ".env.local")) # load local variable
        **os.environ, # override loaded values with env variables
    }