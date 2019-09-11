#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 08:39:16 2019

@author: JeffHalley
"""

from bs4 import BeautifulSoup
from bs4 import NavigableString
import requests
import unicodedata
import pandas as pd


#page = requests.get('reddit.com/r/ListOfSubreddits/wiki/listofsubreddits')

page = "/Users/JeffHalley/Downloads/list_of_subreddits.htm"

def get_subreddit_topics_df(page):
    soup = BeautifulSoup(open(page), 'html.parser')
    subreddit_topics = pd.DataFrame(columns=['topic', 'subreddit'])
    h2s_and_h3s = soup.find_all(['h2','h3'])
    for h2 in h2s_and_h3s:
        header = h2.strong
        if header is not None:
            topic = header.text
        
        node = h2.next_element.next_element.next_element.next_element
        if isinstance(node, NavigableString):
            continue
        if node is not None:
            subreddit = node.text.splitlines()
        subreddits_df = pd.DataFrame(subreddit, columns = ['subreddit'])
        subreddits_df['topic'] = topic
        subreddit_topics = pd.concat([subreddit_topics, subreddits_df], ignore_index=True, sort=True)
    
    for h2 in h2s_and_h3s:
        header = h2.em
        if header is not None:
            topic = header.text
        
        node = h2.next_element.next_element.next_element.next_element
        if isinstance(node, NavigableString):
            continue
        if node is not None:
            subreddit = node.text.splitlines()
        subreddits_df = pd.DataFrame(subreddit, columns = ['subreddit'])
        subreddits_df['topic'] = topic
        subreddit_topics = pd.concat([subreddit_topics, subreddits_df], ignore_index=True, sort=True)
    return subreddit_topics

def get_vg_subs(list_page):
    vg_subreddits = []
    vg_soup = BeautifulSoup(open(list_page), 'html.parser')
    wiki = vg_soup.find("div", {"class": "md wiki"})        # Get all the html within the div with class "md wiki"
     
    for p in wiki.find_all('p'):                         # For every paragraph tag within...
        for a in p.find_all('a', {'rel': 'nofollow'}):   # If it contains an anchor (<a>) tag with rel = "nofollow...
     
            tag_text = str(a.text)                       # Get the text of the anchor tag
     
            if tag_text.startswith('/r/'):               # If it starts with "/r/"....
                vg_subreddits.append(tag_text)                 
    
    vg_subs = pd.DataFrame(columns=['topic', 'subreddit'])
    vg_subs['subreddit'] = vg_subreddits
    vg_subs['topic'] = "video games"
    return vg_subs



page = "/Users/JeffHalley/Downloads/list_of_subreddits.htm"
subreddit_topics_df = get_subreddit_topics_df(page)
video_game_page = "/Users/JeffHalley/Downloads/video_game_list_reddit.htm"
vg_subs_df = get_vg_subs(video_game_page)
subreddit_topics_df = pd.concat([subreddit_topics_df, vg_subs_df], ignore_index=True, sort=True)
