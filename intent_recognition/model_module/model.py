import torch
import torch.nn.functional as F
from transformers import BertTokenizerFast as BertTokenizer
import numpy as np
from pathlib import Path
from .core import ModelModule
from intent_recognition.config.core import config

# if torch.cuda.is_available():
#     map_location=lambda storage, loc: storage.cuda()
# else:
#     map_location='cpu'
class Model:
    def __init__(self):

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        self.tokenizer = BertTokenizer.from_pretrained(config.model_config.model_config)

        intent_recognizer = ModelModule()
        paths = list(Path(config.app_config.best_checkpoints_path).glob('best-*'))
        for path in paths:
            checkpoint = torch.load(path, map_location=torch.device('cpu'))
        
        intent_recognizer.load_state_dict(checkpoint['state_dict'])
        intent_recognizer = intent_recognizer.eval()
        self.intent_recognizer = intent_recognizer.to(self.device)

    def predict(self, text):
        encoded_text = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=config.model_config.max_sentence_length,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )
        input_ids = encoded_text["input_ids"].to(self.device)
        attention_mask = encoded_text["attention_mask"].to(self.device)

        with torch.no_grad():
            pred = self.intent_recognizer(input_ids, attention_mask)
            probabilities = pred[1].flatten().cpu().numpy()
            confidence = max(probabilities)
            indx = np.argmax(probabilities)
            predicted_class  = config.model_config.intents[indx]

        return dict(
            predicted_class = predicted_class,
            confidence = confidence
        )


model = Model()


def get_model():
    return model
