import csv


def save_stopwords(*args):
    fields = [item for item in args]
    with open(r'used_stopwords.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        f.flush()
