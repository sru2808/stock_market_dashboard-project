import requests

API_KEY = "939411fbfe7c408e87884761537524a6"

def get_news():

    url = f"https://newsapi.org/v2/top-headlines?category=business&language=en&apiKey={API_KEY}"

    response = requests.get(url)

    data = response.json()

    articles = []

    if "articles" in data:

        for article in data["articles"][:5]:

            articles.append({
                "title": article["title"],
                "description": article["description"],
                "url": article["url"]
            })

    return articles