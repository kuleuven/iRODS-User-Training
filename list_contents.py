import os
from irods.session import iRODSSession

env_file = os.getenv(
    "IRODS_ENVIRONMENT_FILE", os.path.expanduser("~/.irods/irods_environment.json")
)

project_home = "/<ZONE>/home/<PROJECT_FOLDER>/"
with iRODSSession(irods_env_file=env_file) as session:
    print(session.collections.get(project_home).data_objects)
