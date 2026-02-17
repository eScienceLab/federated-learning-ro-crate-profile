# Developer Notes

These notes are relevant to the GitHub repository for the profile: https://github.com/eScienceLab/federated-learning-ro-crate-profile.

## Code

The `make_crate.py` script creates an example crate that represents the profile.

Currently the scripts are more defined than the profile text.

To run the scripts you must install the requirements listed in `requirements.txt`.

The scripts automatically run validation against the RO-Crate 1.1 specification when generating the RO-Crate. This should tell you if you did anything wrong according to the base spec (but does not mean that all entities are linked correctly). 

The script generates an RO-Crate in the `fl-crate` folder. To generate a HTML preview of the crate (useful for checking things are linked as intended):
```
npm install ro-crate-html
rochtml fl-crate/ro-crate-metadata.json
```

## Where to find useful metadata and identifiers

* People: https://orcid.org/
* Organizations: https://ror.org/
* Places: https://www.geonames.org/v3/
