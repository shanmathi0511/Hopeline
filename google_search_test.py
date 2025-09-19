import requests

API_KEY = "AIzaSyDUMMY_KEY_1234567890abcdef"
CSE_ID = "dummy_cse_id_1234567890"
query = "mental health support"

url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={CSE_ID}"
response = requests.get(url)

results = response.json()
for item in results.get("items", []):
    print(item["title"], item["link"])
