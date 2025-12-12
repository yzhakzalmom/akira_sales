import os
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
        return file_client.download_file().readall()

    def list(self, path: str = ""):
        return [p.name for p in self.fs_client.get_paths(path=path)]
