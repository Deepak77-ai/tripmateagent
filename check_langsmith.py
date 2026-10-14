
import os
from dotenv import load_dotenv
from langsmith import Client

load_dotenv(override=True)

api_key = os.getenv("LANGSMITH_API_KEY")
endpoint = os.getenv("LANGSMITH_ENDPOINT")

print("API key loaded:", bool(api_key))
print("Endpoint:", endpoint)

try:
    client = Client(
        api_key=api_key,
        api_url=endpoint,
    )

    projects = list(client.list_projects(limit=3))
    print("Authentication successful!")
    print("Projects retrieved:", len(projects))

except Exception as e:
    print("Authentication or permission check failed.")
    print(type(e).__name__, str(e))

