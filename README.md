# Python scripts to talk to ManGO

This repository contains a few scripts with boilerplate code to:

- [List the contents of a ManGO project](./list_contents.py)

- [Upload a local file to a directory in ManGO](./upload_file.py)

- [Download data objects from a ManGO collection](./download_file.py)

- [Add schema metadata to a data object in ManGO](./add_metadata.py)

- [Query data objects based on metadata and download them](./query_metadata.py)

## How to run these scripts

1. You should have Python installed and some virtual environment with the packages `python-irodsclient` and `mango-mdschema`. This can be set up as follows:

**Linux, WSL2**
```sh
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install python-irodsclient mango-mdschema # or pip install -r requirements.txt
```

**Windows (PowerShell)**
```pwsh
python -m venv venv
.\venv\Scripts\activate.ps1 # .\venv\Scripts\activate.bat in Command Prompt instead
python -m pip install --upgrade pip
python -m pip install python-irodsclient mango-mdschema # or python -m pip install -r requirements.txt
```

2. In order to run the code in these scripts, the virtual environment should be activated

**Linux, WSL2**
```sh
source venv/bin/activate # or . venv/bin/activate
```

**Windows PowerShell**
```pwsh
.\venv\Scripts\activate.ps1
```

**Windows Command Prompt**
```sh
.\venv\Scripts\activate.bat
```

3. Authenticate by opening an interactive session (with `python` or `ipython`) and copy-pasting the snippet in the "How to connect" tab of the ManGO Portal. This session lasts 7 days; to run code again within these 7 days, if you don't need to change users or zones, authenticating again is not necessary.


<details>
<summary>Example</summary>

```python
Python 3.12.4 | packaged by Anaconda, Inc. | (main, Jun 18 2024, 15:12:24) [GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> config = """
... {
...     "irods_host": "<ZONE>.irods.icts.kuleuven.be",
...     "irods_port": 1247,
...     "irods_zone_name": "<ZONE>",
...     "irods_authentication_scheme": "native",
...     "irods_encryption_algorithm": "AES-256-CBC",
...     "irods_encryption_salt_size": 8,
...     "irods_encryption_key_size": 32,
...     "irods_encryption_num_hash_rounds": 8,
...     "irods_user_name": "<USER>",
...     "irods_ssl_ca_certificate_file": "",
...     "irods_ssl_verify_server": "cert",
...     "irods_client_server_negotiation": "request_server_negotiation",
...     "irods_client_server_policy": "CS_NEG_REQUIRE",
...     "irods_default_resource": "default",
...     "irods_cwd": "/<ZONE>/home",
...     "irods_authentication_uid": 1000
... }
... """
>>> password = "<PASSWORD>"
>>> 
>>> import os, os.path, irods
>>> from irods.password_obfuscation import encode
>>> 
>>> if irods.__version__.startswith(("1.", "0.")):
...   print("You are using an outdated version of the python irods client. Please update to 2.0.0 as soon as possible")
... 
>>> def put(file, contents):
...   os.makedirs(os.path.dirname(file), exist_ok=True)
...   with open(file, "w") as f:
...     f.write(contents)
... 
>>> env_file = os.getenv('IRODS_ENVIRONMENT_FILE', os.path.expanduser('~/.irods/irods_environment.json'))
>>> put(env_file, config)
>>> put(iRODSSession.get_irods_password_file(), encode(password, uid=1000))
```

</details>

