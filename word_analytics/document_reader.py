import csv


class DocumentReader:
    def __init__(self, document_path):
        self.column_header = []
        self.rows = []
        self.__read_csv(document_path)

    def __read_csv(self, document_path):
        with open(document_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            is_header = True
            for row in csv_reader:
                if is_header:
                    self.column_header.append([row[0], row[1], row[2]])
                    is_header = False
                else:
                    self.rows.append([row[0], row[1], row[2]])
