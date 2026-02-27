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
    uniman = crate.add(
        ContextEntity(
            crate,
            "https://ror.org/027m9bs27",
            properties={
                "@type": "Organization",
                "name": "The University of Manchester",
                "url": "https://www.manchester.ac.uk",
            },
        )
    )
    eli = crate.add(
        ContextEntity(
            crate,
            "https://orcid.org/0000-0002-0035-6475",
            properties={
                "@type": "Person",
                "name": "Eli Chadwick",
                "givenName": "Eli",
                "familyName": "Chadwick",
            },
        )
    )
    eli["affiliation"] = uniman

    return


##################
# analysis stage #
##################


def main():
    crate = ROCrate()
    output_dir = "fl-crate/"

    ##################
    # core metadata  #
    ##################

    crate.name = (
        f"Training of image categorization model (Federated Learning RO-Crate example)"
    )
    crate.description = f"Training of an image categorization model using Flower and PyTorch. The Flower configuration is based on the quickstart-pytorch tutorial (https://flower.ai/docs/framework/tutorial-quickstart-pytorch.html). This is an example RO-Crate demonstrating the Federated Learning RO-Crate Profile."
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

    add_authors_and_affiliations(crate=crate)

    crate.root_dataset["publisher"] = crate.get("https://ror.org/027m9bs27")
    crate.root_dataset["author"] = crate.get("https://orcid.org/0000-0002-0035-6475")

    ############
    # datasets #
    ############

    training_dataset = crate.add_dataset(
        source="https://huggingface.co/datasets/uoft-cs/cifar10",
        dest_path=None,
        properties={
            "name": "uoft-cs/cifar10 (Hugging Face dataset)",
            "description": "The CIFAR-10 dataset consists of 60000 32x32 colour images in 10 classes, with 6000 images per class. There are 50000 training images and 10000 test images. The dataset is divided into five training batches and one test batch, each with 10000 images. The test batch contains exactly 1000 randomly-selected images from each class. The training batches contain the remaining images in random order, but some training batches may contain more images from one class than another. Between them, the training batches contain exactly 5000 images from each class.",
            "conformsTo": "http://mlcommons.org/croissant/1.1",
            "encodingFormat": "git+https",
            # TODO - could pull out some of the Croissant data, add it to the crate in full, or link it
            # https://huggingface.co/api/datasets/uoft-cs/cifar10/croissant
        },
    )

    #################
    # configuration #
    #################

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
                "url": "https://flower.ai",
            },
        )
    )

    # Flower project files - configuration
    flower_project = crate.add_dataset(
        source="example-data",
        dest_path="quickstart-pytorch",
        properties={
            "name": "Flower project folder",
            "description": "A Flower project based on the quickstart-pytorch tutorial",
        },
    )
    flower_config_scripts = crate.add_dataset(
        source="example-data/pytorchexample",
        dest_path="quickstart-pytorch/pytorchexample",
        properties={
            "name": "Flower configuration scripts",
            "description": "Flower scripts written in Python which configure the client app, server app, datasets, and model",
            "encodingFormat": "text/x-python",
        },
    )
    flower_config_file = crate.add_file(
        source="example-data/pyproject.toml",
        dest_path="quickstart-pytorch/pyproject.toml",
        properties={
            "name": "Flower project configuration TOML",
            "description": "A TOML file which includes the configuration for the Flower project. It's also a Python project configuration file.",
            "encodingFormat": "application/toml",
        },
    )
    readme = crate.add_file(
        source="example-data/README.md",
        dest_path="quickstart-pytorch/README.md",
        properties={
            "name": "Flower project README",
            "description": "A Markdown file containing instructions for how to run the project.",
            "encodingFormat": "text/markdown",
        },
    )
    readme["about"] = flower_project
    flower_project["hasPart"] = [flower_config_scripts, flower_config_file, readme]

    #################
    # output model #
    #################
    pickle_encoding = crate.add(
        ContextEntity(
            crate,
            "https://docs.python.org/3/library/pickle.html",
            properties={
                "@type": "WebPage",
                "name": "Pickle Python library documentation",
                "description": "Pickle Python library documentation. The pickle module implements binary protocols for serializing and de-serializing a Python object structure.",
            },
        )
    )
    model_file = crate.add_file(
        source="example-data/final_model.pt",
        dest_path="quickstart-pytorch/final_model.pt",
        properties={
            "name": "Output model",
            "description": "Model trained using Flower federated learning process",
        },
    )
    model_file["encodingFormat"] = pickle_encoding

    #############
    # execution #
    #############

    execution = crate.add_action(
        instrument=flower,
        identifier=f"#action-{uuid.uuid4()}",
        object=[flower_config_scripts, flower_config_file, training_dataset],
        result=[model_file],
        properties={
            "name": "Execution of federated learning process",
            "description": "Execution of the federated learning process using `flwr run`",
            # TODO "startTime"
            # TODO "endTime"
        },
    )
    execution["agent"] = crate.get("https://orcid.org/0000-0002-0035-6475")

    #################
    # write & check #
    #################
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
