import os
from dotenv import load_dotenv

load_dotenv()  # reads variables from a .env file and sets them in os.environ


def main():
    MY_ENV_VAR = os.getenv("EXAMPLE", "UNKNOWN ENVIRONMENT VARIABLE")
    print(f"HELLO {MY_ENV_VAR}!")


if __name__ == "__main__":
    main()
