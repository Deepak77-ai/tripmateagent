from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from backend import run_travel_agent

#results = search_flights("give me a list of flights from delhi to mumbai on 2024-06-15")

#print(results)

import os
from dotenv import load_dotenv

load_dotenv(override=True)

print("Tracing enabled:", os.getenv("LANGSMITH_TRACING"))
print("Endpoint:", os.getenv("LANGSMITH_ENDPOINT"))
print("Project:", os.getenv("LANGSMITH_PROJECT"))
print("API key loaded:", bool(os.getenv("LANGSMITH_API_KEY")))

user_input = input("Enter your travel query: ")

response = run_travel_agent(user_input = user_input,
                            thread_id ="test_user")

print("Flight Results:\n", response["flight_results"])
print(response["answer"])
