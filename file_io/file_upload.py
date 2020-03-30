import uuid

import iso639
import pandas as pd
from langdetect import detect
from werkzeug.datastructures import FileStorage

from config import config
from data_import.data_handler import calculate_n_clusters_by_category
from util.logger import log


def handle_file_upload(file_storage: FileStorage):
    file_uuid = f'{str(uuid.uuid4())}.csv'

    log.info(f'Save file {file_uuid}')
    filename = config.custom_input_file(file_uuid)
    file_storage.save(filename)

    log.info(f'Extract CSV headers')
    data = pd.read_csv(filename)

    sample_text = " ".join(map(str, data.iloc[0].tolist()))

    return {
        'cols': [col for col in data.columns],
        'filename': file_uuid,
        'language': iso639.to_name(detect(sample_text)).lower(),
        'recommendationSet': calculate_n_clusters_by_category(data.shape[0])
    }
