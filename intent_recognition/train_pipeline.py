import os
import sys
import shutil
from transformers import  BertTokenizerFast as BertTokenizer
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
import mlflow
import logging
import pytorch_lightning as pl
from utils.helper import LitProgressBar, load_prod_model
import warnings

from config.core import config 
from data_preprocessors.preprocessors import DataPreprocessing
from data_module.core import DataLoaderModule
from model_module.core import ModelModule

warnings.filterwarnings('ignore')

_logger = logging.getLogger(__name__)
sys.path.insert(0, "")

def run_training()->None:
    data_preprocessors = DataPreprocessing()
    # preprocess train data
    train_data = data_preprocessors.fit(
        data_folder_path=config.app_config.data_folder, 
        data_type='train'
        )
    train_data =  data_preprocessors.transform(data=train_data)
    
    #preprocess test data
    test_data = data_preprocessors.fit(
        data_folder_path=config.app_config.data_folder, 
        data_type='validate'
        )
    test_data =  data_preprocessors.transform(data=test_data)
    #initialize tokenizer
    tokenizer=BertTokenizer.from_pretrained(config.model_config.model_config, do_lower_case=True)
    #initialize dataloader module
    data_loader_module = DataLoaderModule(
        train_data=train_data.iloc[:4000], 
        test_data=test_data[:300], 
        maxlen=config.model_config.max_sentence_length, 
        batch_size=config.model_config.batch_size, 
        tokenizer= tokenizer
        )
    
    #initialize model module
    step_per_epoch = len(train_data) // config.model_config.batch_size
    model_module = ModelModule(step_per_epoch=step_per_epoch)
    #initialize progress bar list
    pro_bar = LitProgressBar()
    
    # check point configuration
    checkpoint_callback = ModelCheckpoint(
    save_top_k=1,
    dirpath='checkpoints',
    filename='best-checkpoint',
    monitor='val_loss',
    mode='min',
    verbose=True)

    early_stopping = EarlyStopping(
        monitor='val_loss',
        mode='min',
        verbose=True,
        patience=1,
    )
  
    mlflow.set_tracking_uri(config.app_config.mlflow_config['remote_server_uri'])
    mlflow.set_experiment(config.app_config.mlflow_config['experiment_name'])
    #Auto log all MLflow entities
    mlflow.pytorch.autolog()

    with mlflow.start_run(run_name="bert-intent-recognition") as run:
        if os.path.isdir('checkpoints'):
            shutil.rmtree('checkpoints')
        trainer = pl.Trainer(
        callbacks=[checkpoint_callback, early_stopping, pro_bar],
        max_epochs=config.model_config.epochs,
        gpus=0)
        trainer.fit(model_module, data_loader_module)

        trainer.test(dataloaders=data_loader_module)

        load_prod_model(experiment_ids=1, checkpoints='checkpoints')

        
if __name__== '__main__':
    run_training()
