from pathlib import Path
import json
import pandas as pd 
import logging

_logger = logging.getLogger(__name__)

class DataPreprocessing():
    def _get_data_paths(self, data_folder_path:str,  data_type:str):
        paths = Path(data_folder_path).glob(f'{data_type}_*')
  
        return list(paths)

    def fit(self, data_folder_path:str, data_type:str):
        _logger.info('starting data preprocessing...')
        try:
            sentences = []
            intents= []

            for path in self._get_data_paths(data_folder_path, data_type):
                
                with path.open() as f:
                    data = json.load(f)
                
                for k, v in data.items():

                    for a in v:
                        sentence=''
                        for i in a['data']:
                            sentence += i['text']
                        sentences.append(sentence)
                        intents.append(k)
            
            df = pd.DataFrame({'sentences': sentences, 'intents': intents})
            
            return df
            
        except Exception as e:
            _logger.info('Something went wrong file while preprocessing data')
            raise e
    
    def transform (self, data:pd.DataFrame):
        try:
            unique_intent = data['intents'].unique()
            unique_intent_dict = dict()
            for i, intent in enumerate(unique_intent):
                unique_intent_dict[intent] = i

            data['labels'] = data.intents.replace(unique_intent_dict)

            _logger.info('Data preprocessing completed.')
            return data
            
        except Exception as e: 
            _logger.info('Something went wrong file while preprocessing data')
            raise e
      