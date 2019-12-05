import csv
import sys


def clean_csv(csv_file):
    with open(csv_file) as dirty_csv:
        field_names = ['Date', 'Account', 'Memo', 'Amount']
        csv_reader = csv.DictReader(dirty_csv)

        with open('cleaned_csv.csv', mode='w', newline='') as cleaned_csv:
            cleaned_csv_writer = csv.DictWriter(cleaned_csv, fieldnames=field_names)
            cleaned_csv_writer.writeheader()
            for row in csv_reader:
                cleaned_csv_writer.writerow({'Date': row.get('glh_date').split(None, 1)[0], 'Account': row.get('gld_acct_posted'), 'Memo': row.get('glh_reference'), 'Amount': row.get('gld_amt')})


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Only one argument is allowed.\nProvide only the file name to be cleaned as the argument.')
    elif len(sys.argv) <= 1:
        print('The file name to be cleaned is required as an argument.')
    else:
        try:
            clean_csv(sys.argv[1])
            print('The provided file has been successfully cleaned!  The new file name is "cleaned_csv.csv".')
        except FileNotFoundError:
            print(f'No file with the name: "{ sys.argv[1] }".  Please check the name and try again.')
