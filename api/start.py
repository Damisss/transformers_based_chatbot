from app import create_app
from config import Config 

app = create_app(config_object=Config())

if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0", port=3001)