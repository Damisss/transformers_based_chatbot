from flask import Blueprint, request, jsonify
import sys
import json

from intent_recognition.model_module.model import get_model
from api.utils.web_scraper import Scraper
from utils.helper import get_weather, get_city

sys.path.insert(0, "")

app = Blueprint('app', __name__)

@app.route('/intent-recognition', methods=['POST'])
def prediction():
    try:
        if request.method == "POST":
            user_intent = request.json['query']
            user_intent = user_intent.strip()
           
            if user_intent:
                model = get_model()
                results = model.predict(user_intent)
                if results['confidence'] > .8:
                    with open('api/utils/intents_map.json', 'r') as f:
                        data = json.load(f)
                        
                        intent = results['predicted_class']
                        if intent:
                            if intent == 'GetWeather':
                                city = get_city()
                                return get_weather(city=city)

                            return jsonify(
                                    {   "type": "bot",
                                        "message": data[intent],
                                        "status_code": 200,
                                    }
                                )

                else: 
                    scraper = Scraper()
                    results = scraper.search_query(user_intent)

                    return results
            
            return jsonify(
                        {
                            "message": "Please provide user's intent text ",
                            "status_code": 400,
                        }
                    )
        

    except:
        return jsonify(
                        {
                            "message": "Internal server error ",
                            "status_code": 500,
                        }
                    )
    