
import webbrowser
from urllib.parse import quote


def search_google(query):
    query = query.strip()

    if not query:
        return False

    url = f"https://www.google.com/search?q={quote(query)}"

    try:
        webbrowser.open(url)
        return True
    except Exception as e:
        print(f"Browser search error: {e}")
        return False
