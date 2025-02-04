import os
from irods.session import iRODSSession
from irods.models import Collection, DataObject, DataObjectMeta
from irods.column import Criterion

env_file = os.getenv(
    "IRODS_ENVIRONMENT_FILE", os.path.expanduser("~/.irods/irods_environment.json")
)

project_home = "/<ZONE>/home/<PROJECT_FOLDER>/"
schema_prefix = "mgs.analysis"  # mgs + . + schema name

with iRODSSession(irods_env_file=env_file) as session:
    # find all data objects that
    results = (
        session.query(Collection, DataObject)
        .filter(
            Criterion(
                "like", Collection.name, f"{project_home}%"
            )  # live under the project collection
        )
        .filter(
            Criterion(
                "like", DataObjectMeta.name, "mgs.analysis%"
            )  # have been annotated with the analysis schema
        )
    )

    # find all data objects that
    # results = session.query(Collection, DataObject).filter(
    #     Criterion("=", DataObjectMeta.name, "mgs.analysis.analyst") # have an 'analyst' field from the analysis schema
    # ).filter(
    #     Criterion("=", DataObjectMeta.value, "fulana") # and the 'analyst' is 'fulana'
    # )
    for item in results:
        path = f"{item[Collection.name]}/{item[DataObject.name]}/"
        session.data_objects.get(path)
