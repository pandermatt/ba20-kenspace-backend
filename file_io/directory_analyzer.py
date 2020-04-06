import os
import uuid
from zipfile import ZipFile

import PyPDF2
import pandas as pd

from config import config
from util.logger import log

ZIP_DIR_DEPTH = 3


def generate_df_and_read_file_content(analytic_list):
    data = {'full_path': [], 'filename': [], 'directory': [], 'content': []}
    for current in analytic_list:
        for filename, string_path in zip(current.data_list, current.string_path_list):
            dir_name, clean_filename = os.path.split(filename)

            data['full_path'].append(string_path)
            data['filename'].append(clean_filename)
            data['directory'].append(os.path.basename(string_path))

            _, file_extension = os.path.splitext(clean_filename)
            data['content'].append(read_content(filename, file_extension))
    return pd.DataFrame(data)


def read_content(path_to_file, ending):
    if ending == '.txt':
        with open(path_to_file, 'r') as file:
            return file.read().replace('\n', '')
    elif ending == '.csv':
        with open(path_to_file, 'r') as content_file:
            return content_file.read()
    elif ending == '.pdf':
        return pdf_content(path_to_file)


def pdf_content(path_to_file):
    pdf_file_obj = open(path_to_file, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)
    data = []
    for number in range(pdf_reader.numPages):
        page_obj = pdf_reader.getPage(number)
        data.append(page_obj.extractText())
    pdf_file_obj.close()
    return ' '.join(data)


class AnalyticsHelper:
    __slots__ = ['root_path', 'data_list', 'string_path_list']

    def __init__(self, root_path, data_list, string_path_list):
        self.root_path = root_path
        self.data_list = data_list
        self.string_path_list = string_path_list


class DirectoryAnalytics:
    def __init__(self, path_zip, filter_option_list):
        zip_root_path = config.zip_input_data_dir(uuid.uuid4())

        log.info(f'Analyse Zip: {zip_root_path}')
        with ZipFile(path_zip, 'r') as zipObj:
            zipObj.extractall(path=zip_root_path)

        path_as_string = ""

        self.filter_option_list = filter_option_list
        all_files, all_strings = self.__list_of_files(zip_root_path, path_as_string, 0, True)
        self.pandas_data = generate_df_and_read_file_content([AnalyticsHelper(zip_root_path, all_files, all_strings)])

        #########################
        # WARNING: DELETES FOLDER
        #########################
        log.info(f'Remove Folder: {zip_root_path}')
        import shutil
        shutil.rmtree(zip_root_path)

    def __list_of_files(self, dir_name, dir_name_as_string, count, root_dir=False):
        if count > ZIP_DIR_DEPTH:
            return [], []
        list_of_file = os.listdir(dir_name)
        all_files_as_string = list()
        all_files = list()
        for entry in list_of_file:
            full_path = os.path.join(dir_name, entry)
            current_dir_name_as_string = os.path.basename(dir_name)

            if current_dir_name_as_string == "__MACOSX":
                log.info(f'Skipping __MACOSX folder')
                continue

            if not root_dir:
                new_dir_as_string = f'{dir_name_as_string}/{current_dir_name_as_string}'
            else:
                new_dir_as_string = ""

            if os.path.isdir(full_path):
                files, strings = self.__list_of_files(full_path, new_dir_as_string, count + 1)
                all_files = all_files + files
                all_files_as_string = all_files_as_string + strings
            elif os.path.isfile(full_path) and self.__check_file_type(full_path):
                all_files.append(full_path)
                all_files_as_string.append(new_dir_as_string)
        return all_files, all_files_as_string

    def __check_file_type(self, full_path):
        entries = full_path.split('.')
        if len(entries) > 1:
            # get data ending
            data_type = entries[len(entries) - 1]
            if data_type in self.filter_option_list:
                return True
        return False

    @staticmethod
    def __top_level(dir_name):
        top_level = []
        top = os.listdir(dir_name)
        for entry in top:
            full_path = os.path.join(dir_name, entry)
            if os.path.isdir(full_path):
                top_level.append(full_path)
        return top_level
