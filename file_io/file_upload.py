import uuid

import pandas as pd
from werkzeug.datastructures import FileStorage

from config import config


def handle_file_upload(file_storage: FileStorage):
    file_uuid = f'{str(uuid.uuid4())}.csv'
    filename = config.custom_input_file(file_uuid)
    file_storage.save(filename)

    data = pd.read_csv(filename)

    return {'cols': [col for col in data.columns], 'filename': file_uuid}

