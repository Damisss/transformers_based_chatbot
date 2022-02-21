from transformers import BertTokenizerFast as BertTokenizer
from torch.utils.data  import Dataset
from torch.nn.functional import one_hot
import torch
import pandas as pd

from intent_recognition.config.core import config

class DatasetModule(Dataset):
    def __init__(self, data:pd.DataFrame, maxlen:int, tokenizer:BertTokenizer) -> None:
        self.data = data
        self.maxlen = maxlen
        self.tokenizer = tokenizer
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        sentence = self.data.iloc[idx]['sentences']
        label = one_hot(torch.tensor(self.data.iloc[idx]['labels']), num_classes=config.model_config.num_class)
        sentence_encoding = self.tokenizer.encode_plus(
            sentence,
            add_special_tokens=True,
            max_length=self.maxlen,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt'
        )

        return dict(
            input_ids=sentence_encoding['input_ids'].flatten(),
            attention_mask=sentence_encoding['attention_mask'].flatten(),
            labels= label.flatten()
        )
       