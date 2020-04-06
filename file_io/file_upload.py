import os
import uuid

import iso639
import pandas as pd
from langdetect import detect
from werkzeug.datastructures import FileStorage

from api.errors import error_response
from config import config
from data_import.data_handler import calculate_n_clusters_by_category
from file_io.directory_analyzer import DirectoryAnalytics
from util.logger import log

CSV_FILE = 'csv'
TXT_FILE = 'txt'
WHATS_APP_TXT_FILE = 'whatsapp'
ZIP = 'zip'


def handle_file_upload(file_storage: FileStorage, upload_type: str):
    filename, file_extension = os.path.splitext(file_storage.filename)
    file_uuid = f'{str(uuid.uuid4())}_{filename}'

    log.info(f'Save file {file_uuid}')
    original_filename = config.custom_input_file(f'{file_uuid}{file_extension}')
    csv_filename = config.custom_input_file(f'{file_uuid}.csv')
    file_storage.save(original_filename)

    log.info(f'Extract {upload_type}')

    data = None
    detected_language = None

    try:
        if upload_type == CSV_FILE:
            data = pd.read_csv(original_filename)
        elif upload_type == TXT_FILE:
            data = convert_txt_to_csv(original_filename)
        elif upload_type == WHATS_APP_TXT_FILE:
            data = convert_whats_app_to_csv(original_filename)
        elif upload_type == ZIP:
            data = DirectoryAnalytics(original_filename, [CSV_FILE, TXT_FILE]).pandas_data
        else:
            error_response(f"{file_extension} not supported yet")

        sample_text = " ".join(map(str, data.iloc[0].tolist()))
        detected_language = iso639.to_name(detect(sample_text)).lower()
    except Exception as e:
        log.error(f'Remove file due to an error: {original_filename}')
        os.remove(original_filename)
        log.error('An exception occurred: %r', e)
        error_response(f"Wrong data format")

    if upload_type != CSV_FILE:
        log.info(f'Remove file: {original_filename}')
        os.remove(original_filename)
        data.to_csv(csv_filename)

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

    return pd.DataFrame(rows, columns=['text-content'])


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

    return data
