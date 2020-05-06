import os

import dill as dill

from api import errors
from cluster_analytics.clustered_data_structure import ClusterIO
from cluster_analytics.k_means_clusterer import KMeansCluster
from config import config
from data_import.data_handler import DataHandler
from util.logger import log


def __get_filename(prefix: str, model_id: str) -> str:
    return config.model_data_file(f'{prefix}-{model_id}.sav')


def __load_file(filename):
    if not os.path.isfile(filename):
        log.error(f"File '{filename}' does not exist")
        errors.not_found_response()
    with open(filename, "rb") as f:
        return dill.load(f)


def __dump_file(content, filename):
    with open(filename, 'wb') as f:
        dill.dump(content, f)


def is_model_present(uuid, data):
    return os.path.isfile(__get_filename(data, uuid))


def save_model_to_disk(model: ClusterIO, data: str):
    if not config.SAVE_TO_FILE:
        return
    __dump_file(model, __get_filename(data, model.uuid))


def load_model_from_disk(uuid: str, data: str) -> ClusterIO:
    return __load_file(__get_filename(data, uuid))


def save_data_to_disk(data_handler: DataHandler, data: str):
    if not config.SAVE_TO_FILE:
        return
    __dump_file(data_handler, __get_filename("data", data))


def load_data_from_disk(data: str) -> DataHandler:
    return __load_file(__get_filename("data", data))
