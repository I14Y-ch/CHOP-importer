from io import BytesIO
from math import ceil
import traceback
import requests as r
import urllib3
import json
import os

from config import CHOP_API_BASE_URL, CHOP_REVISION, CHOP_YEAR, CLIENT_KEY, CLIENT_SECRET, GET_TOKEN_URL, I14Y_API_BASE_URL, RESPONSIBLE_DEPUTY_JSON, RESPONSIBLE_PERSON_JSON, TEMPLATES_DIR

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class CHOPImporter:

    def __init__(self, year, revision, chunk_size=250):
        self.token = self.get_access_token()
        self.year = year
        self.revision = revision
        self.chunk_size = chunk_size
        self.concept_id = None

    def get_access_token(self):
        """Generated an access token from client key and client secret"""
        data = {"grant_type": "client_credentials"}
        response = r.post(
            GET_TOKEN_URL,
            data=data,
            verify=False,
            auth=(CLIENT_KEY, CLIENT_SECRET),
        )
        if response.status_code >= 400:
            raise Exception("Failed to get token")
        return "Bearer " + response.json()["access_token"]

    def post_codeListEntries(self, concept_id):
        all_codelists = self.get_chop_codeListEntries()["codeListEntries"]

        total = len(all_codelists)
        print(f"Total codelist entries: {total}")

        num_chunks = ceil(total / self.chunk_size)

        headers = {"Authorization": self.token}

        for i in range(num_chunks):
            start = i * self.chunk_size
            end = start + self.chunk_size
            chunk = all_codelists[start:end]

            payload = {"data": chunk}
            file_content = json.dumps(payload, ensure_ascii=False).encode("utf-8")

            files = {"file": ("import.json", BytesIO(file_content), "application/json")}

            print(f"Uploading chunk {i+1}/{num_chunks} ({len(chunk)} entries)...")

            response = r.post(
                f"{I14Y_API_BASE_URL}/concepts/{concept_id}/codelist-entries/imports/Json",
                headers=headers,
                files=files,
                verify=False,
            )

            try:
                response.raise_for_status()
                print(f"\tChunk {i+1} uploaded successfully")
            except r.exceptions.HTTPError as e:
                print(f"\tChunk {i+1} failed: {e}")
                print(f"\tResponse: {response.text}")
                importer.debug_delete_concept(concept_id)

    def publish_i14y(self, public=False):

        chop_data = self.build_data()
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        response = r.post(
            I14Y_API_BASE_URL + "/concepts",
            json={"data": chop_data},
            headers=headers,
            verify=False,
        )

        if response.status_code >= 400:
            print("Status code:", response.status_code)
            try:
                print("Response JSON:", response.json())
            except ValueError:
                print("Response text:", response.text)
            response.raise_for_status()

        concept_id = response.text.strip('"')
        self.concept_id = concept_id
        print(f"Newly created concept id: {concept_id}")

        if public:
            self.change_publication_level(concept_id, "Public")

        self.post_codeListEntries(concept_id)

        return concept_id

    def change_publication_level(self, concept_id, publication_level):
        response = r.put(
            url=f"{I14Y_API_BASE_URL}/concepts/{concept_id}/publication-level",
            params={"level": publication_level},
            headers={
                "Authorization": self.token,
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Accept-encoding": "json",
            },
            verify=False,
        )
        response.raise_for_status()

    def debug_delete_concept(self, concept_id):
        headers = {"Authorization": self.token, "Content-Type": "application/json"}
        self.change_publication_level(concept_id, "Internal")
        response = r.delete(I14Y_API_BASE_URL + "/concepts/" + concept_id, headers=headers, verify=False)
        response.raise_for_status()
        print(f"Deleted concept with id {concept_id}")

    def get_chop_codeListEntries(self):
        """
        returns {
            'codeListEntries':
                {...}
            }
        """
        url = f"{CHOP_API_BASE_URL}/chop/{self.year}/{self.revision}"
        response = r.get(url, verify=False)
        response.raise_for_status()

        data = response.json()

        return data

    def parse_templates(self):
        """
        Parse Markdown template files in the templates/ folder and return a dict:
        {
            'name': {'fr': ..., 'de': ..., 'en': ..., 'it': ...},
            'description': {'fr': ..., 'de': ..., 'en': ..., 'it': ...}
        }
        Replaces {YEAR} with the provided year.
        """
        result = {"name": {}, "description": {}}

        # Mapping between language codes and filenames
        lang_files = {"de": "de.md", "fr": "fr.md", "en": "en.md", "it": "it.md"}

        for lang, filename in lang_files.items():
            filepath = os.path.join(TEMPLATES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                # Replace {YEAR} placeholder with the actual year
                content = content.replace("{YEAR}", str(self.year))

                # Extract # Title section
                name = ""
                description = ""
                if "# Title" in content:
                    parts = content.split("# Title", 1)[1]  # everything after # Title
                    lines = parts.splitlines()
                    name_lines = []
                    for line in lines:
                        if line.startswith("# Description"):
                            break  # stop at Description section
                        name_lines.append(line)
                    name = " ".join(name_lines).strip()

                # Extract # Description section
                if "# Description" in content:
                    parts = content.split("# Description", 1)[1]  # everything after # Description
                    lines = parts.splitlines()
                    description_lines = []
                    for line in lines:
                        if line.startswith("# "):
                            break  # stop at next header
                        description_lines.append(line)
                    description = "\n".join(description_lines).strip()

                # Store results under the correct language
                result["name"][lang] = name
                result["description"][lang] = description

        return result

    def build_data(self):
        data = self.parse_templates()
        data["identifier"] = "DV_CHOP"
        data["version"] = f"{self.year}.{self.revision}.0"
        data["themes"] = [{"code": "114"}]
        data["validFrom"] = f"{self.year-1}-12-31T23:00:00+00:00"
        data["validTo"] = f"{self.year}-12-30T23:00:00+00:00"
        data["codeListEntryDefaultSortProperty"] = "Position"
        data["codeListEntryValueMaxLength"] = 8
        data["codeListEntryValueType"] = "String"
        data["conceptType"] = "CodeList"
        data["publisher"] = {"identifier": "CH1"}

        data["responsibleDeputy"] = json.loads(RESPONSIBLE_DEPUTY_JSON)
        data["responsiblePerson"] = json.loads(RESPONSIBLE_PERSON_JSON)

        return data

if __name__ == "__main__":
    importer = CHOPImporter(int(CHOP_YEAR), int(CHOP_REVISION))
    try:
        importer.publish_i14y(public=True)
    except Exception as e:
        traceback.print_exc()
        importer.debug_delete_concept(importer.concept_id)
    print(f"Concept id: {importer.concept_id}")
