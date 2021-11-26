""" This module returns a list of COVID news """
from pip._vendor import requests
import json

articles:list
accepted_articles:list = []
deleted_articles:list = []

""" Opens config.json file to import news API key """
with open('config.json', 'r') as f:
    config = json.load(f)
    keys = config["API-keys"]
    news_key = keys["news"]

""" Returns list of articles containing COVID terms """
def get_accepted_articles():
    return accepted_articles

""" Deletes article that matches the article the user clicked the cross on """
def delete_news(article_title_to_delete):
    deleted_articles.append(article_title_to_delete)
    for article in accepted_articles:
            if article['title'] == article_title_to_delete:
                accepted_articles.remove(article)

""" When articles are reloaded, this function checks for any articles that were previously deleted or repeats """
def check_for_deleted_news():
    for article in accepted_articles:
        for deleted_article in deleted_articles:
            if article['title'] == deleted_articles:
                accepted_articles.remove(article)
                
    for i in range(0,len(accepted_articles) - 1):
        for j in range(0,len(accepted_articles) - 1):
            if accepted_articles[i]['title'] == accepted_articles[j]['title']:
                accepted_articles.remove(accepted_articles[j])



""" Checks through a given article contents for a given term """
def in_article(article,keyword:str):
    if keyword.lower() in str(article['title']).lower():
        return True
    elif keyword.lower() in str(article['description']).lower():
        return True
    elif keyword.lower() in str(article['content']).lower():
        return True
    else:
        return False

""" Returns a list of articles containing given terms """
def news_api_request(covid_terms = ['Covid','COVID-19','coronavirus']):
    complete_url = "https://newsapi.org/v2/top-headlines?country=gb&apiKey=" + news_key
    response = requests.get(complete_url)
    response2 = response.json()
    articles = response2["articles"]
    term:str

    for article in articles:
        for term in covid_terms:
            if in_article(article,term):
                accepted_articles.append(article)

    check_for_deleted_news()

    return accepted_articles