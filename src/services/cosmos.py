import os
from typing import Any, Optional
from azure.cosmos import CosmosClient
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from datetime import date, datetime
from copy import deepcopy


class CosmosDBClient:
    def __init__(
        self,
        endpoint: Optional[str] = None,
        database: Optional[str] = None,
    ):
        load_dotenv()
        self.endpoint = endpoint or os.getenv("CONFIGURATION__AZURECOSMOSDB__ENDPOINT")
        self.database_name = database or os.getenv(
            "CONFIGURATION__AZURECOSMOSDB__DATABASENAME", "cricketdb"
        )
        if not self.endpoint:
            raise EnvironmentError("Cosmos DB endpoint not set.")
        # Use managed identity (DefaultAzureCredential)
        credential = DefaultAzureCredential()
        self.client = CosmosClient(url=self.endpoint, credential=credential)
        self.database = self.client.get_database_client(self.database_name)

    def get_container(self, container_name: str) -> Any:
        return self.database.get_container_client(container_name)

    def upsert_item(self, container_name: str, item: dict) -> dict:
        container = self.get_container(container_name)
        # Cosmos SDK expects JSON-serializable objects. Convert date/datetime
        # objects to ISO-format strings before upserting.
        serializable = self._make_json_serializable(deepcopy(item))
        return container.upsert_item(serializable)

    def _make_json_serializable(self, obj: Any) -> Any:
        """Recursively convert date/datetime objects to ISO strings so
        the Cosmos SDK can serialize the payload.

        Leaves other types unchanged. Works for dicts, lists, and primitives.
        """
        if isinstance(obj, dict):
            return {k: self._make_json_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._make_json_serializable(v) for v in obj]
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return obj

    def read_item(self, container_name: str, item_id: str, partition_key: str) -> dict:
        container = self.get_container(container_name)
        return container.read_item(item=item_id, partition_key=partition_key)

    def query_items(
        self, container_name: str, query: str, parameters: list = []
    ) -> list:
        container = self.get_container(container_name)
        return list(
            container.query_items(
                query=query, parameters=parameters, enable_cross_partition_query=True
            )
        )

    def delete_item(
        self, container_name: str, item_id: str, partition_key: str
    ) -> None:
        container = self.get_container(container_name)
        container.delete_item(item=item_id, partition_key=partition_key)


# Dependency injection for FastAPI
def get_db():
    return CosmosDBClient()
