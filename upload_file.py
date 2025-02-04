import os
from irods.session import iRODSSession

env_file = os.getenv(
    "IRODS_ENVIRONMENT_FILE", os.path.expanduser("~/.irods/irods_environment.json")
)

project_home = "/<ZONE>/home/<PROJECT_FOLDER>/"
with iRODSSession(irods_env_file=env_file) as session:
    source_path = "output.txt"  # provide a valid existing path
    dest_path = (
        f"{project_home}filename_new.txt"  # provide a path that does not exist yet
    )
    session.data_objects.put(source_path, dest_path)
