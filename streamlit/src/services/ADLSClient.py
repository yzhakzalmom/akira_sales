import os
from io import BytesIO
from utils.constants import MSG_FILE_NOT_FOUND
from utils.helpers import load_env_file
from azure.identity import ClientSecretCredential
from azure.storage.filedatalake import DataLakeServiceClient

# Load .env file from project root
load_env_file()

# Object that connects with ADLS
class ADLSClient:

    def __init__(self):

        # Configure env variables
        self.tenant_id = os.getenv('AZURE_TENANT_ID')
        self.client_id = os.getenv('AZURE_CLIENT_ID')
        self.client_secret = os.getenv('AZURE_CLIENT_SECRET')
        self.account_name = os.getenv('ADLS_ACCOUNT_NAME')
        self.container = os.getenv('ADLS_CONTAINER')

        # Configure Azure credential
        self.credential = ClientSecretCredential(
            tenant_id = self.tenant_id,
            client_id = self.client_id,
            client_secret = self.client_secret
        )

        # Configure Data Lake client
        self.service_client = DataLakeServiceClient(
            account_url = f"https://{self.account_name}.dfs.core.windows.net",
            credential = self.credential 
        )

        # Configure file system client
        self.fs_client = self.service_client.get_file_system_client(self.container)

    # =======================
    # UTILITY METHODS
    # =======================

    def upload(self, path: str, data: bytes):
        file_client = self.fs_client.get_file_client(path)
        file_client.upload_data(data, overwrite=True)

    def read(self, path: str) -> bytes:
        file_client = self.fs_client.get_file_client(path)
        return BytesIO(file_client.download_file().readall())

    def read_folder(self, folder_path: str) -> bytes:
        paths = self.fs_client.get_paths(path=folder_path)

        for path in paths:
            if not path.is_directory:
                file_client = self.fs_client.get_file_client(path.name)
                return BytesIO(file_client.download_file().readall())

        raise FileNotFoundError(f'{MSG_FILE_NOT_FOUND} {folder_path}')

    def list(self, path: str = "") -> list[str]:
        return [p.name for p in self.fs_client.get_paths(path=path)]
