# env2azure
Program to convert .env files configs to a JSON file which can be used in Azure App Service Configuration.

## Usage
Run program in command prompt as follows:
`.\env2azure.exe [--add [ADD ...]] [--o [O]] file_path`

For information about the arguments type `.\env2azure.exe --help`

## Build
### Prerequisites
* python 3.9+
* pyinstaller

To build the executable file, run the `build.bat` file. 