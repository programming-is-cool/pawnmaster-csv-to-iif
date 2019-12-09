import sys
import csv


def main(input_file_name):
    head = "!TRNS,TRNSTYPE,DATE,ACCNT,MEMO,AMOUNT,CLASS\r\n!SPL,TRNSTYPE,DATE,ACCNT,MEMO,AMOUNT,CLASS\r\n!ENDTRNS,,,,,,"
    trans_start_template = "\nTRNS,GENJRN,{0},,,,"
    trans_body_template = "\nSPL,GENJRN,{0},{1},{2},{3},PAWNIT"
    trans_end_template = "\nENDTRNS,,,,,,"
    last_date_processed = None

    with open(input_file_name, 'r') as input_file:
        csv_reader = csv.DictReader(input_file)
        trans_num = 0

        for trans in csv_reader:
            trans_date = trans.get("glh_date").split(None, 1)[0]
            trans_account = trans.get("gld_acct_posted")
            trans_memo = trans.get("glh_reference")
            trans_amount = trans.get("gld_amt")
            
            if last_date_processed != trans_date:
                if last_date_processed is not None:
                    with open(f'general_ledger_{ trans_num }.iif', mode='a', newline='') as output_file:
                        output_file.write(trans_end_template)
                trans_num += 1
                with open(f'general_ledger_{ trans_num }.iif', mode='a', newline='') as output_file:
                    output_file.write(head)
                    output_file.write(trans_start_template.format(trans_date))
                    output_file.write(trans_body_template.format(trans_date, trans_account, trans_memo, trans_amount))
                    last_date_processed = trans_date
            elif last_date_processed == trans_date:
                with open(f'general_ledger_{ trans_num }.iif', mode='a', newline='') as output_file:
                    output_file.write(trans_body_template.format(trans_date, trans_account, trans_memo, trans_amount))
        with open(f'general_ledger_{ trans_num }.iif', mode='a', newline='') as output_file:
            output_file.write(trans_end_template)


if __name__ == '__main__':
    if len(sys.argv) > 2:
        print('Only one argument is allowed.\nProvide only the file name to be cleaned as the argument.')
    elif len(sys.argv) <= 1:
        print('The file name to be cleaned is required as an argument.')
    else:
        try:
            main(sys.argv[1])
            print('The provided CSV file has been converted into multiple .iif files based on the transaction date.  '
                  'Please verify that all data is correct before importing into Quickbooks.')
        except FileNotFoundError:
            print(f'No file with the name: "{ sys.argv[1] }".  Please check the name and try again.')
