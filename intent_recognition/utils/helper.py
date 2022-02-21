import logging
import shutil
import sys
import os
import mlflow
from mlflow.tracking import MlflowClient
from pytorch_lightning.callbacks import TQDMProgressBar

from intent_recognition.config.core import config
FORMATTER = logging.Formatter(
    "%(asctime)s — %(name)s — %(levelname)s —" "%(funcName)s:%(lineno)d — %(message)s"
)

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler

class LitProgressBar(TQDMProgressBar):

  def init_validation_tqdm(self):
      bar = super().init_validation_tqdm()
      bar.set_description('running validation ...')
      refresh_rate=30,
      return bar

def rename_best_checkpoints(*, source:int, destination:int, new_name:int)->None:
    shutil.move(source, destination)
    os.rename(destination, new_name)

def grab_registered_models (client, filter_string):
    models=[]
    registered_models = [dict(mv) for mv in client.search_model_versions(filter_string)]
    for reqiestered_model in registered_models:
        mv_to_dict = dict(reqiestered_model)
        models.append(mv_to_dict)
    return models

def load_prod_model(*, experiment_ids:int, checkpoints:str):

    mlflow.set_tracking_uri(config.app_config.mlflow_config['remote_server_uri'])

    df = mlflow.search_runs([experiment_ids])
    sorted_df = mlflow.search_runs([experiment_ids], order_by=["metrics.f1_score DESC"])
 
    client = MlflowClient()

    artifact_path = "model"
    model_name = 'pytorch'
    filter_string = "name='{}'".format(model_name)
    models_versions = grab_registered_models(client, filter_string)
    run_ids = df['run_id'].values
    run_ids = run_ids.tolist()

    for run_id in run_ids:
        model_uri = "runs:/{run_id}/{artifact_path}".format(run_id=run_id, artifact_path=artifact_path)

        if  run_ids.index(run_id) == 0  and run_id not in [ mv['run_id'] for mv in  models_versions] or len(models_versions) == 0:
            model_details = [dict(mlflow.register_model(model_uri=model_uri, name=model_name))]
    
        else:
            model_details =  [dict(mv) for mv in  models_versions if mv['run_id'] == run_id]

        if len(model_details):
            if run_id == sorted_df['run_id'][0]:
                best_checkpoints_version = model_details[0]['version']
                client.transition_model_version_stage(
                    name=model_name, 
                    version = model_details[0]['version'], 
                    stage="Production"
                    )
            else:
                client.transition_model_version_stage(
                    name=model_name, 
                    version = model_details[0]['version'], 
                    stage="Staging"
     
                    )
    # rename checkpoint in order to make a link between our best-checkpoint povided by pytorch_lighning trainer and the model registered on mlflow
    prod_checkpoint_dir = 'intent_recognition/registered_models_checkpoints'
    prod_model_best_checkpoints = f'{prod_checkpoint_dir}/best-checkpoint_{best_checkpoints_version}.ckpt' if best_checkpoints_version else ''
    previous_checkpoints = os.listdir(prod_checkpoint_dir)
    is_same_version = prod_model_best_checkpoints not in previous_checkpoints
    checkpoints_dest = f'{prod_checkpoint_dir}/best-checkpoint.ckpt'

    if os.path.isdir(checkpoints) and len(os.listdir(checkpoints)):
        
        if  prod_model_best_checkpoints and is_same_version:
            rename_best_checkpoints(
                source=f'{checkpoints}/best-checkpoint.ckpt',
                destination=checkpoints_dest,
                new_name=prod_model_best_checkpoints
            )
         
        elif prod_model_best_checkpoints and len(previous_checkpoints)==0:
            rename_best_checkpoints(
                source=f'{checkpoints}/best-checkpoint.ckpt',
                destination=checkpoints_dest,
                new_name=prod_model_best_checkpoints
            )
           