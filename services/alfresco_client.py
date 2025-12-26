import requests
import shutil
from requests.auth import HTTPBasicAuth


class AlfrescoClient:
    def __init__(self, base_url: str, username: str, password: str):
        self.base_url = base_url.rstrip("/")
        self.auth = HTTPBasicAuth(username, password)

    def download_content(self, node_id: str, target_path: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{node_id}/content"

        with requests.get(url, auth=self.auth, stream=True) as r:
            r.raise_for_status()
            with open(target_path, "wb") as f:
                shutil.copyfileobj(r.raw, f)

    def create_folder(self, name: str, parent_id: str) -> str:
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{parent_id}/children"

        payload = {"name": name, "nodeType": "cm:folder"}
        r = requests.post(url, json=payload, auth=self.auth)
        r.raise_for_status()
        return r.json()["entry"]["id"]

    def upload_file(self, parent_id: str, file_path: str, file_name: str):
        url = f"{self.base_url}/alfresco/api/-default-/public/alfresco/versions/1/nodes/{parent_id}/children"

        with open(file_path, "rb") as f:
            files = {"filedata": (file_name, f)}
            data = {"name": file_name, "nodeType": "cm:content", "autoRename": "true"}
            r = requests.post(url, files=files, data=data, auth=self.auth)
            r.raise_for_status()
            return r.json()["entry"]["id"]
