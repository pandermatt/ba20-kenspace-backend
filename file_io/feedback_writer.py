import csv


def save_feedback(*args):
    fields = [item for item in args]
    with open(r'feedback.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(fields)
