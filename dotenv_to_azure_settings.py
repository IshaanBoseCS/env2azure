import json
import os
import re
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


def convert_dotenv_to_env_dict(file_path: str, extras: list[str]):
    env_dict = {}

    if len(extras) != 0:
        for extra in extras:
            var, value = extra.split("=", 1)
            env_dict[var] = value
    
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
                
                env_dict[var] = value
    
    return env_dict


def format_variables(env_dict: dict[str, str]):
    for key in env_dict:
        if "${" in env_dict[key]:
            key_list = re.findall(r'\$\{(?P<keys>[A-Z_]+)\}', env_dict[key])
            env_dict[key] = env_dict[key].replace("${", "{")
            format_dict = { i: env_dict[i] for i in key_list }
            value = env_dict[key].format(**format_dict)
            env_dict[key] = value
    return env_dict


def convert_dotenv_to_json(file_path: str, extras: list[str], output_file_path: str):
    json_data = []
    env_dict = convert_dotenv_to_env_dict(file_path, extras)
    env_dict = format_variables(env_dict)

    for key, value in env_dict.items():
        json_data.append({
            "name": key,
            "value": value,
            "slotSetting": False
        })

    if output_file_path is None:
        output_file_path = os.path.join(os.getcwd(), "azure_settings.json")

    with open(output_file_path, "w") as json_file:
        json.dump(json_data, json_file, indent=4)


if __name__ == "__main__":
    args = parser.parse_args()
    convert_dotenv_to_json(args.file_path, args.add, args.o)
