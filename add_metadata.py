import os
from irods.session import iRODSSession
from mango_mdschema import Schema

env_file = os.getenv(
    "IRODS_ENVIRONMENT_FILE", os.path.expanduser("~/.irods/irods_environment.json")
)

project_home = "/<ZONE>/home/<PROJECT_FOLDER>/"
training_schema = Schema(".metadata-schema.json")  # local path to existing json file

with iRODSSession(irods_env_file=env_file) as session:
    obj_with_metadata = session.data_objects.get(
        f"{project_home}file_with_md.txt"
    )  # path to existing data object
    print(training_schema.extract(obj_with_metadata))

    obj_md = {
        "some_key": "some_value"
    }  # metadata that should match the schema requirements
    training_schema.validate(obj_md)

    obj_without_metadata = session.data_objects.get(
        f"{project_home}file_for_md.txt"
    )  # path to existing data object
    training_schema.apply(obj_without_metadata, obj_without_metadata)

    print(obj_without_metadata.metadata.items())  # training_schema.validate(obj_md)
