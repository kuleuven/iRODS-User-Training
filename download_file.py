import os
from irods.session import iRODSSession

env_file = os.getenv(
    "IRODS_ENVIRONMENT_FILE", os.path.expanduser("~/.irods/irods_environment.json")
)

project_home = "/<ZONE>/home/<PROJECT_FOLDER>/"
with iRODSSession(irods_env_file=env_file) as session:
    source_path = f"{project_home}filename.txt"  # provide a valid path
    dest_path = "output.txt"
    session.data_objects.get(source_path, dest_path)
