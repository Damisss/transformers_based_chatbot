import requests 
import json
from rake_nltk import Rake
from flask import jsonify
import os
#import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
# nltk.download('stopwords')
# nltk.download('punkt')

class Scraper():
    def keyword_extractor(self, text):
        try:
            
            r = Rake()
            r.extract_keywords_from_text(text)
            res = r.get_ranked_phrases()
            
            res = ' + '.join(res)

            return res
        except Exception as e:
            raise e
    
    def search_query(self, text):
        try:
            keywords =  self.keyword_extractor(text)
            url = "https://google-search3.p.rapidapi.com/api/v1/search/q={}&num=3".format(keywords)
            headers = {
                    'x-rapidapi-key': os. environ['XRAPIDAPIKEY'],
                    'x-rapidapi-host': os.environ['XRAPIDAPIHOST']
                    }

            response = requests.request("GET", url, headers=headers)
            data = json.loads(response.text)
            search_results= list()
            item = dict()
            for result in data['results']:
                item['title'] = result['title']
                item['description'] = result['description']
                item['url'] = [result['link']]
                search_results.append(item)

            if len(search_results):
                return jsonify({
                    "message": search_results,
                    "status_code": 200,
                    "intent":"Not identified",
                    "type": "bot",
                })
            else:
                return jsonify({
                    "message": "Sorry!! we are unable to process your request at this time. Please try again later.",
                    "status_code": 500,
                })
        except Exception as e:
            raise e 