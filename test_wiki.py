import requests

def get_wiki_image(term):
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "pageimages",
        "titles": term,
        "pithumbsize": 500
    }
    headers = {
        "User-Agent": "EducationalApp/1.0 (contact@example.com)"
    }
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    pages = data.get("query", {}).get("pages", {})
    for page_id, page in pages.items():
        if "thumbnail" in page:
            return page["thumbnail"]["source"]
    return None

terms = ["Dog", "Watermelon", "Car", "Red", "Hand"]
for t in terms:
    print(f"{t}: {get_wiki_image(t)}")
