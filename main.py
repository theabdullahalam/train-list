import os
import csv
import sys

MOSR_FILE = 'mosr-train-list.csv'
FAX_SHEET = sys.argv[1]
UPDATED_SHEET = 'updated-sheet.csv'
CCG_SHEET = 'ccg-sheet.csv'

def get_origin_divn(train_no):

    with open(MOSR_FILE, 'r') as mosr_file:
        mosr_reader = csv.DictReader(mosr_file)
        
        for row in mosr_reader:
            if row['TRAIN NO.'] == train_no:
                return row['ORIGIN DIVN']
    
    return 'Not Found'

with open(FAX_SHEET, 'r') as f:
    reader = csv.DictReader(f)
    field_names = ['S.No.','Train no','Division','Class','Date','FROM','TO','PNR NO.','NAME &NO. OF BERTHS','REFERENCE','Remarks','MOB.NO.']
    updated_rows = []

    for row in reader:
      new_row = row
      new_row['Division'] = get_origin_divn(row['Train no'])

      # handle BCT case
      if new_row['Division'] == 'BCT':
        if new_row['Class'] == 'SL' or new_row['Class'] == '2SL':
          new_row['Division'] = 'CCG'          

      updated_rows.append(new_row)

    with open(UPDATED_SHEET, 'w') as u:
        writer = csv.DictWriter(u, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(updated_rows)