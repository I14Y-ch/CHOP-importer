# CHOP-importer

This repo contains a script that imports CHOP as a concept in I14Y.

The CHOP API provides the codeListEntries. The title and description for the concept are defined in the `templates` folder for different languages as `.md` files.

The names for the responsible deputy and person are stored in github secrets to avoid personal info leak. They are in json format like this:

- RESPONSIBLE_DEPUTY
    - `{"givenName":"John","familyName":"Doe","email":"john.doe@example.com"}`
- RESPONSIBLE_PERSON
    - `{"givenName":"Jacques","familyName":"Dupont","email":"jacques.dupont@example.com"}`

The year and revision are defined in Github env variables (`Settings` -> `Security` -> `Secret and variables` -> `Actions` -> `Variables`) this way we don't need to change the code each year:
- CHOP_YEAR
- CHOP_REVISION

The url for the CHOP API (`CHOP_API_BASE_URL`) is defined in `config.py`.

`GET_TOKEN_URL` and `I14Y_API_BASE_URL` are defined in the workflow yaml files because they change between ABN and Prod.

Parameters for the I14Y concept that are unlikely to change are defined in the `build_data` function in `CHOPImporter.py` file.