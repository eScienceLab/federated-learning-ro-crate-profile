# Helper functions for Federated Learning RO-Crate creation
from datetime import datetime
import os
import uuid
import requests

from rocrate.model import ContextEntity, Person
from rocrate.rocrate import ROCrate
from rocrate_validator import services, models


#####################
#  crate validation #
#####################
def validate_crate(crate_uri):
    # Create an instance of `ValidationSettings` class to configure the validation
    settings = services.ValidationSettings(
        # Set the path to the RO-Crate root directory
        rocrate_uri=crate_uri,
        # Set the identifier of the RO-Crate profile to use for validation.
        # If not set, the system will attempt to automatically determine the appropriate validation profile.
        profile_identifier="ro-crate-1.1",
        # Set the requirement level for the validation
        requirement_severity=models.Severity.REQUIRED,
        # requirement_severity=models.Severity.RECOMMENDED, # use for best practices!
    )

    # Call the validation service with the settings
    result = services.validate(settings)

    # Check if the validation was successful
    if not result.has_issues():
        print("RO-Crate is valid!")
    else:
        print("RO-Crate is invalid!")
        # Explore the issues
        for issue in result.get_issues():
            # Every issue object has a reference to the check that failed, the severity of the issue, and a message describing the issue.
            print(
                f'Detected issue of severity {issue.severity.name} with check "{issue.check.identifier}": {issue.message}'
            )


####################
# helper functions #
####################

# add helper functions here
