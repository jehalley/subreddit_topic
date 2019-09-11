from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import unicodedata
from pandas import DataFrame


#page = requests.get('https://www.reddit.com/r/ListOfSubreddits/wiki/listofsubreddits')

page = "/Users/JeffHalley/Downloads/list_of_subreddits.htm"

soup = BeautifulSoup(open(page), 'html.parser')

#topic headers are h2 tagged
h2s = soup.find_all('h2')
for h2 in h2s:
    header = h2.strong
    if header is not None:
        category = header.text
    print(category)
    
    node = h2.next_element.next_element.next_element.next_element
    if isinstance(node, NavigableString):
        continue
    if node is not None:
        subreddit = node.text.splitlines()
        print(subreddit)
