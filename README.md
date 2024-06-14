Python version - 3.10.4

# SETUP

## Creating Python Virtual Environment

```sh
python3 -m venv env $(pwd)
```

## Activating the virtual environment

```sh
source ./env/bin/activate
```

## Installing the packages

```sh
pip3 install -r requirements.txt
```

## Enable formatting on commit

```sh
pre-commit install
```

## Starting the server in virtual env

```sh
source ./env/bin/activate && nodemon --exec python3 --ext py index.py
```

# Auto Formatter

Install the extension `Black Formatter` by Microsoft in VSCode.

Make sure to set it as default formatter for Python on save.
To do this open VSCode settings.json and add the following field in the JSON object.

```json
    "[python]": {
		"editor.defaultFormatter": "ms-python.black-formatter"
	}
```

# VSCode recommended extensions

- Python by Microsoft
- Pylance by Microsoft
