import requests

url = "https://en.wikipedia.org/w/api.php"

params = {
    "action": "query",
    "prop": "extracts",
    "titles": "Python (programming language)",
    "explaintext": True,
    "format": "json"
}

r = requests.get(url, params=params)

data = r.json()

pages = data["query"]["pages"]

for page in pages.values():
    print(page["extract"][:500])