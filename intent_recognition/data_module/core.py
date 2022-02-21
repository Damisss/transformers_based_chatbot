import pytorch_lightning as pl
from torch.utils.data import DataLoader 
from transformers import BertTokenizerFast as BertTokenizer
from sklearn.model_selection import train_test_split
import pandas as pd
import os 
import typing as t
import logging

from intent_recognition.data_utils.core import DatasetModule
from intent_recognition.config.core import config

_logger = logging.getLogger(__name__)

class DataLoaderModule(pl.LightningDataModule):
    def __init__(
        self, train_data:pd.DataFrame, 
        test_data:pd.DataFrame,
        maxlen:int, 
        batch_size:int, 
        tokenizer:BertTokenizer) -> None:

            super().__init__()
            self.train_data = train_data
            self.test_data = test_data
            self.maxlen = maxlen
            self.tokenizer = tokenizer
            self.batch_size = batch_size
    
    def setup(self, stage:t.Optional[str]=None):
        self.train_df, self.val_df = train_test_split(
            self.train_data, 
            test_size=config.model_config.test_size, 
            random_state=config.model_config.seed_value
            )
    
    def train_dataloader(self):
        _logger.info('loading train data...')
        return DataLoader(
            dataset=DatasetModule(data=self.train_df, maxlen=self.maxlen, tokenizer=self.tokenizer),
            shuffle=True,
            batch_size=self.batch_size,
            num_workers=os.cpu_count()
        )
    
    def val_dataloader(self):
        _logger.info('loading validation data...')
        return DataLoader(
            dataset=DatasetModule(data=self.val_df, maxlen=self.maxlen, tokenizer=self.tokenizer),
            shuffle=False,
            batch_size=self.batch_size,
            num_workers=os.cpu_count()
        )
    
    def test_dataloader(self):
        _logger.info('loading test data...')
        return DataLoader(
            dataset=DatasetModule(data=self.test_data, maxlen=self.maxlen, tokenizer=self.tokenizer),
            shuffle=False,
            batch_size=self.batch_size,
            num_workers=os.cpu_count()
        )