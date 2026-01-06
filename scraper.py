import requests
import random
from lxml import html

HEADERS = [
    {"User-Agent": "Mozilla/5.0 Chrome/120"},
    {"User-Agent": "Mozilla/5.0 Firefox/122"},
]

def _fetch(url):
    r = requests.get(
        url,
        headers=random.choice(HEADERS),
        timeout=10
    )
    r.raise_for_status()
    return html.fromstring(r.text)

def fetch_account(username):
    tree = _fetch(f"https://nitter.net/{username}")
    tweet = tree.xpath('//div[@class="timeline-item"]')[0]

    tid = tweet.xpath('.//a[@class="tweet-link"]/@href')[0]
    text = "".join(
        tweet.xpath('.//div[@class="tweet-content"]//text()')
    ).strip()

    return tid, text, f"https://twitter.com{tid}"

def fetch_list(list_id):
    tree = _fetch(f"https://nitter.net/i/lists/{list_id}")
    tweet = tree.xpath('//div[@class="timeline-item"]')[0]

    tid = tweet.xpath('.//a[@class="tweet-link"]/@href')[0]
    text = "".join(
        tweet.xpath('.//div[@class="tweet-content"]//text()')
    ).strip()

    return tid, text, f"https://twitter.com{tid}"
