import pandas as pd
from datetime import datetime

import config
import logging


_logger = logging.getLogger(__name__)


def load_dataset(file_name: str) -> pd.DataFrame:
    _data = pd.read_csv(f'{config.DATASET_DIR}/{file_name}')
    return _data

def save_dataset(df: pd.DataFrame, file_name: str):
    df.to_csv(f'{config.DATASET_DIR}/{create_file_name_version(file_name)}', index=False)

def get_timestamp():
    now = datetime.now()
    return now.strftime("%m%d%Y_%H%M%S")

def create_file_name_version(file_name):
    prefix, extension = file_name.split(".")
    return prefix + "_" + get_timestamp() + "." + extension
