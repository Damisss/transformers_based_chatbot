This transformer based chatbot is a chatbot with easy to update, integrated with a frontend (reactjs application). The present application can be extended and used as the first layer of support service. Users can get response of their queries at anytime 24x7 hours without waiting in a queue. If chatbot is unable to directly answer your query. It will automatically perform a web crapping (google search in this case) and shared with you the top three responses.
In order to build this chatbot we have used a dataset that contains various types of user's intents categorized into seven intents. It is hosted on [GitHub](https://github.com/sonos/nlu-benchmark/tree/master/2017-06-custom-intent-engines) and was first presented in [this paper](https://arxiv.org/abs/1805.10190).

We have tried a State of the art natural language processing from BERT-large. Our future plan is to used other transfomers based model like Distilbert, Electra, Albert etc....

<img src="/images/chatbot.gif" width="400" height="400"/>

# Prerequisites
* Docker 

# Start project tests and training
* `open the project` 
* `bash run.sh -b` build docker images
* `bash run.sh -p` starts differeent docker contaires
* `bash runs.sh -c` copy trained model checkpoints to to your the local machine. This will allow you to start the chat boot after training.
* `bash runs.sh -t` turn off and then remove different docker images

# Access Mlflow during taining
* `open browser and type: localhost:1234`

# Run transformer based ChatBot
* `open the project`
* `bash run.sh -a` build docker images
* `bash run.sh -d` starts application
* `bash runs.sh -t` turn off and then remove different docker images
