# Create an RO-Crate following the in-development BGE profile
from datetime import datetime
import os
import uuid
import requests

from rocrate.model import ContextEntity, Entity, Person
from rocrate.rocrate import ROCrate
from rocrate_validator import services, models

from utils import (
    validate_crate,
)

#########
# setup #
#########


def add_authors_and_affiliations(crate: ROCrate) -> None:

    # authors and affiliations
    # TODO update this
    # institutions
    wsi = crate.add(
        ContextEntity(
            crate,
            "https://ror.org/05cy4wa09",
            properties={
                "@type": "Organization",
                "name": "Wellcome Sanger Institute",
                "url": "https://www.sanger.ac.uk",
            },
        )
    )
    cambridge = crate.add(
        ContextEntity(
            crate,
            "https://www.geonames.org/2653941",
            properties={"@type": "Place", "name": "Cambridge, UK"},
        )
    )
    wsi["location"] = cambridge


##################
# analysis stage #
##################


def add_analysis_stage(crate: ROCrate, analysis_accessions: str) -> Entity:

    workflow_assembly = crate.add_workflow(
        dest_path=f"#assembly-workflow-{uuid.uuid4()}",
        properties={
            "name": f"Assembly workflow (placeholder)",
            "description": "A placeholder for a workflow that could exist on WorkflowHub (etc) or be directly contained within the crate",
            "sdDatePublished": str(datetime.now()),
        },
    )

    return


def main():
    crate = ROCrate()
    output_dir = "fl-crate/"

    ##################
    # core metadata  #
    ##################

    crate.name = f"TODO"
    crate.description = f"TODO"
    license = crate.add(
        ContextEntity(
            crate,
            "https://spdx.org/licenses/CC0-1.0",
            properties={
                "@type": "CreativeWork",
                "name": "Creative Commons Zero v1.0 Universal",
                "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
            },
        )
    )
    crate.license = license

    crate.root_dataset["identifier"] = ["TODO"]

    # add_authors_and_affiliations(crate=crate)

    ###########
    # process #
    ###########

    # instrument - Flower
    flower = crate.add(
        ContextEntity(
            crate,
            "https://flower.ai",
            properties={
                "@type": "SoftwareApplication",
                "name": "Flower",
                "description": "Flower federated learning framework",
                "version": "1.26.1",
            },
        )
    )

    flower_project = crate.add_dataset(
        source="example-data",
        dest_path="quickstart-pytorch",
        properties={
            "name": "Flower project folder",
            "description": "A Flower project based on the quickstart-pytorch tutorial",
        },
    )
    client_app_file = crate.add_file(
        source="example-data/pytorchexample/client_app.py",
        dest_path="quickstart-pytorch/pytorchexample/client_app.py",
        properties={
            "name": "Flower client app",
            "description": "Client-side code for the federated learning process",
        },
    )
    server_app_file = crate.add_file(
        source="example-data/pytorchexample/server_app.py",
        dest_path="quickstart-pytorch/pytorchexample/server_app.py",
        properties={
            "name": "Flower server app",
            "description": "Server-side code for the federated learning process",
        },
    )
    model_file = crate.add_file(
        source="example-data/final_model.pt",
        dest_path="quickstart-pytorch/final_model.pt",
        properties={
            "name": "Output model",
            "description": "Model trained using Flower federated learning process",
            # TODO encoding format
        },
    )
    flower_project.append_to("hasPart", [client_app_file, server_app_file, model_file])

    execution = crate.add_action(
        instrument=flower,
        identifier=f"#action-{uuid.uuid4()}",
        object=[client_app_file, server_app_file],  # TODO also include config files?
        result=[model_file],
        properties={
            "name": "Execution of federated learning process",
            "description": "Execution of the federated learning process using `flwr run`",
            # TODO "startTime"
            # TODO "endTime"
            # TODO "agent"
        },
    )

    #################
    # write & check #
    #################
    crate.root_dataset["hasPart"] = [flower_project, model_file]  # TODO
    crate.root_dataset.append_to("mentions", execution)  # TODO
    # the output model is the focus of the crate
    crate.root_dataset["mainEntity"] = model_file  # TODO
    # conforms to process run crate
    process_run_crate = crate.add(
        ContextEntity(
            crate,
            "https://w3id.org/ro/wfrun/process/0.5",
            properties={
                "name": "Process Run Crate",
                "@type": "CreativeWork",
                "version": "0.5",
            },
        )
    )
    crate.root_dataset.append_to("conformsTo", process_run_crate)

    # Writing the RO-Crate metadata:
    crate.write(output_dir)

    validate_crate(
        output_dir,
        profile_identifier="process-run-crate-0.5",
        requirement_severity=models.Severity.RECOMMENDED,
    )


if __name__ == "__main__":
    main()
