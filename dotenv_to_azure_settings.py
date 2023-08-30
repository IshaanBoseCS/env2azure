import json
import os
from argparse import ArgumentParser

parser = ArgumentParser(
    prog="env2azure",
    description=(
        "Converts a .env to file to the equivalent json file which can"
        " be used to configure an Azure App Service."
    ),
)
parser.add_argument("file_path", help="Absolute path to the .env file to be converted")
parser.add_argument(
    "--add",
    nargs="*",
    help=("Adds additional environment variables. Should follow format" ' VAR="value"'),
)
parser.add_argument(
    "--o",
    nargs="?",
    default=os.path.join(os.getcwd(), "azure_settings.json"),
    help=(
        "Path to the output file. By default, creates a JSON file named"
        " azure_settings.json in the current directory."
    ),
)


def convert_dotenv_to_json(file_path: str, extras: list[str], output_file_path: str):
    json_data = []

    if len(extras) != 0:
        for extra in extras:
            var, value = extra.split("=", 1)
            json_data.append({"name": var, "value": value, "slotSetting": False})

    with open(file_path, "r") as file:
        for line in file.readlines():
            line = line.strip()
            line = line.strip("\n")

            # ignoring new lines and comments
            if len(line) > 0 and line[0] != "#":
                var, value = line.split("=", 1)
                value = value.strip()
                var = var.strip()

                # removing quotes to avoid weird strings
                if value[0] == '"':
                    value = value[1:-1]

                json_data.append(
                    {"name": var, "value": str(value), "slotSetting": False}
                )

    if output_file_path is None:
        output_file_path = os.path.join(os.getcwd(), "azure_settings.json")

    with open(output_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


if __name__ == "__main__":
    args = parser.parse_args()
    convert_dotenv_to_json(args.file_path, args.add, args.o)
