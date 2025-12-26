import os
from typing import Dict


class ScormUploader:
    """
    Uploads extracted SCORM directory into Alfresco,
    preserving folder structure.
    """

    def __init__(self, alfresco_client):
        self.client = alfresco_client

    def upload_directory(self, local_root: str, parent_node_id: str):
        """
        Recursively uploads a directory to Alfresco.

        :param local_root: Extracted SCORM root directory
        :param parent_node_id: Alfresco folder node id
        """
        folder_map: Dict[str, str] = {local_root: parent_node_id}

        for root, dirs, files in os.walk(local_root):
            alfresco_parent_id = folder_map[root]

            for dirname in dirs:
                local_path = os.path.join(root, dirname)

                node_id = self.client.create_folder(
                    name=dirname,
                    parent_id=alfresco_parent_id,
                )

                folder_map[local_path] = node_id

            for filename in files:
                file_path = os.path.join(root, filename)

                self.client.upload_file(
                    parent_id=alfresco_parent_id,
                    file_path=file_path,
                    file_name=filename,
                )
