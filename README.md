# CHOP-importer

This repo contains a script that imports CHOP as a concept in I14Y.

The required pip modules are listed in the `requirements.txt` file.

You have to create a `.env` file with the same variables as in `.env.example`.

The following env variables are needed:
- `I14Y_API_BASE_URL`: i14y api url (different for ABN/DEV/PROD)
- `GET_TOKEN_URL`: url to generate i14y token (different for ABN/DEV/PROD)
- `CLIENT_ID`: client id to generate i14y token
- `CLIENT_SECRET`: client secret to generate i14y token
- `CHOP_API_BASE_URL`: MCT API url
- `CHOP_YEAR`: Chop year
- `CHOP_REVISION`: Chop revision (usually 99)
- `RESPONSIBLE_DEPUTY_GIVENNAME`: Given name for responsible deputy
- `RESPONSIBLE_DEPUTY_FAMILYNAME`: Family name for responsible deputy
- `RESPONSIBLE_DEPUTY_EMAIL`: Email for responsible deputy
- `RESPONSIBLE_PERSON_GIVENNAME`: Given name for responsible person
- `RESPONSIBLE_PERSON_FAMILYNAME`: Family name for responsible person
- `RESPONSIBLE_PERSON_EMAIL`: Email for responsible person
- `TEMPLATES_DIR`: Folder containing description and title in different languages in `.md` files

The CHOP API provides the codeListEntries. The title and description for the concept are defined in the `templates` folder for different languages as `.md` files. The placeholder `{YEAR}` in those file will be replaced by the provided `CHOP_YEAR` env variable.

Parameters for the I14Y concept that are unlikely to change are defined in the `build_data` function in `CHOPImporter.py` file.