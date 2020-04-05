import os
import uuid

import iso639
import pandas as pd
from langdetect import detect
from werkzeug.datastructures import FileStorage

from api.errors import error_response
from config import config
from data_import.data_handler import calculate_n_clusters_by_category
from util.logger import log


def handle_file_upload(file_storage: FileStorage, upload_type: str):
    file_uuid = f'{str(uuid.uuid4())}_{file_storage.filename}.csv'

    log.info(f'Save file {file_uuid}')
    filename = config.custom_input_file(file_uuid)
    file_storage.save(filename)

    log.info(f'Extract {upload_type}')

    data = None
    detected_language = None

    try:
        if upload_type == 'csv':
            data = pd.read_csv(filename)
        elif upload_type == 'txt':
            data = convert_txt_to_csv(filename)
        elif upload_type == 'whatsapp':
            data = convert_whats_app_to_csv(filename)
        else:
            error_response(f"Not supported yet")

        sample_text = " ".join(map(str, data.iloc[0].tolist()))
        detected_language = iso639.to_name(detect(sample_text)).lower()
    except Exception as e:
        log.error(f'Remove file due to an error: {filename}')
        os.remove(filename)
        log.error('An exception occurred: %r', e)
        error_response(f"Wrong data format")

    return {
        'cols': [col for col in data.columns],
        'filename': file_uuid,
        'language': detected_language,
        'recommendationSet': calculate_n_clusters_by_category(data.shape[0])
    }


def convert_txt_to_csv(filename):
    rows = []
    with open(filename) as fp:
        while True:
            line = fp.readline()
            if not line:
                break

            striped_line = line.strip()
            if striped_line and striped_line != '':
                rows.append(striped_line)

    data = pd.DataFrame(rows, columns=['text-content'])

    # Override file
    data.to_csv(filename)

    return data


def convert_whats_app_to_csv(filename):
    columns = ['From', 'Content']
    rows = []

    with open(filename) as fp:
        while True:
            row = [''] * 2

            line = fp.readline()
            if not line:
                break
            line = ''.join(line.split("]")[1:]).strip()
            row[0] = line.split(":")[0]
            row[1] = ''.join(line.split(":")[1:]).strip()

            rows.append(row)

    data = pd.DataFrame(rows, columns=columns)
    data['Combined'] = data['From'].astype(str) + ': ' + data['Content']
    data.fillna('')

    # Override file
    data.to_csv(filename)

    return data
