import os

import joblib

from api import errors
from cluster_analytics.k_means_clusterer import KMeansCluster
from config import config
from util.logger import log


def save_model_to_disk(model: KMeansCluster):
    filename = config.model_data_file(f'{model.uuid}.sav')
    joblib.dump(model, filename)


def load_model_from_disk(uuid: str):
    filename = os.path.join(config.model_data_dir(), f'{uuid}.sav')
    if not os.path.isfile(filename):
        log.error(f"File '{filename}' does not exist")
        errors.not_found_response()
    return joblib.load(filename)
