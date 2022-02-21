from pathlib import Path
from strictyaml import YAML, load
from pydantic import BaseModel
import typing as t

ROOT_PATH = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT_PATH / 'config.yml'

class AppConfig(BaseModel):
    data_folder: str
    best_checkpoints_path: str
    mlflow_config: t.Dict[str, str]

class ModelConfig(BaseModel):
    num_class: int
    seed_value: int
    test_size: float
    epochs: int
    batch_size: int
    max_sentence_length: int
    model_config: str
    intents: t.List[str]
    

class Config(BaseModel):
    app_config: AppConfig
    model_config: ModelConfig

def get_config_path()->Path:
    if CONFIG_PATH.is_file:
        return CONFIG_PATH
    raise Exception('Config file not found.')

def parse_ymal(file_path:str=None)->YAML:
    if file_path is None:
        file_path = get_config_path()

    if file_path:
        with open(file_path, 'r') as f:
            data = load(f.read())
        return data

    raise Exception('Config file not found.')

def create_config(parsed_data:YAML=None)->Config:
    if parsed_data is None:
        parsed_data = parse_ymal()
    
    _config = Config(
        app_config= AppConfig(**parsed_data.data),
        model_config= ModelConfig(**parsed_data.data)
    )
    return _config

config = create_config()