import uuid

import pandas as pd
from werkzeug.datastructures import FileStorage

from config import config
from util.logger import log


def handle_file_upload(file_storage: FileStorage):
    file_uuid = f'{str(uuid.uuid4())}.csv'

    log.info(f'Save file {file_uuid}')
    filename = config.custom_input_file(file_uuid)
    file_storage.save(filename)

    log.info(f'Extract CSV headers')
    data = pd.read_csv(filename)

    return {'cols': [col for col in data.columns], 'filename': file_uuid}

