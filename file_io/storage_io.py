import os

import joblib

from api import errors
from cluster_analytics.k_means_clusterer import KMeansCluster
from config import config
from data_import.data_handler import DataHandler
from util.logger import log


def __get_filename(prefix: str, model_id: str) -> str:
    return config.model_data_file(f'{prefix}-{model_id}.sav')


def save_model_to_disk(model: KMeansCluster, data: str):
    if not config.SAVE_TO_FILE:
        return
    filename = __get_filename(data, model.uuid)
    joblib.dump(model, filename)


def load_model_from_disk(uuid: str, data: str) -> KMeansCluster:
    filename = __get_filename(data, uuid)
    if not os.path.isfile(filename):
        log.error(f"File '{filename}' does not exist")
        errors.not_found_response()
    return joblib.load(filename)


def save_data_to_disk(data_handler: DataHandler, data: str):
    if not config.SAVE_TO_FILE:
        return
    filename = __get_filename("data", data)
    joblib.dump(data_handler, filename)


def load_data_from_disk(data: str) -> DataHandler:
    filename = __get_filename("data", data)
    if not os.path.isfile(filename):
        log.error(f"File '{filename}' does not exist")
        errors.not_found_response()
    return joblib.load(filename)
