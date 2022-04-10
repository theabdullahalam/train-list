import os
import csv
import sys

MOSR_FILE = 'mosr-train-list.csv'
FAX_SHEET = sys.argv[1]
UPDATED_SHEET = 'updated-sheet.csv'
CCG_SHEET = 'ccg-sheet.csv'
EMPT_ROWS = 14

def get_origin_divn(train_no):

    with open(MOSR_FILE, 'r') as mosr_file:
        mosr_reader = csv.DictReader(mosr_file)
        
        for row in mosr_reader:
            if row['TRAIN NO.'] == train_no:
                return row['ORIGIN DIVN']
    
    return 'Not Found'

def generate_updated_sheet():
  with open(FAX_SHEET, 'r') as f:
      reader = csv.DictReader(f)
      field_names = ['S.No.','Train no','Division','Class','Date','FROM','TO','PNR NO.','NAME &NO. OF BERTHS','REFERENCE','Remarks','MOB.NO.']
      updated_rows = []

      for row in reader:
        new_row = row
        new_row['Division'] = get_origin_divn(row['Train no'])

        # handle BCT case
        if new_row['Division'] == 'BCT':
          if new_row['Class'] == 'SL' or new_row['Class'] == '2S':
            pass
          else:
            new_row['Division'] = 'CCG'


        updated_rows.append(new_row)

      with open(UPDATED_SHEET, 'w') as u:
          writer = csv.DictWriter(u, fieldnames=field_names)
          writer.writeheader()
          writer.writerows(updated_rows)

def generate_ccg_sheet():
  with open(UPDATED_SHEET, 'r') as u:
      reader = csv.DictReader(u)
      field_names = ['S.No.','Train no','Division','Class','Date','FROM','TO','PNR NO.','NAME &NO. OF BERTHS','REFERENCE','Remarks','MOB.NO.']
      ccg_rows = []
      final_rows = []

      for row in reader:
        new_row = row
        if row['Division'] == 'CCG':
          ccg_rows.append(new_row)

      for row in ccg_rows:
        for i, key in enumerate(row.keys()):
          newrow = list([field_names[i], row[key]])
          final_rows.append(newrow)
        
        for i in range(0, EMPT_ROWS):
          final_rows.append(['', ''])

      with open(CCG_SHEET, 'w') as c:
          writer = csv.writer(c)
          writer.writerows(final_rows)

def check_files():
  if not os.path.isfile(MOSR_FILE):
    print_fancy('MOSR file not found')
    sys.exit()

def print_fancy(string):
  print(f'\n--------------------\n{string}\n--------------------\n')

# check if the required files are present
check_files()

# generate updated sheet
generate_updated_sheet()
print_fancy('Updated sheet generated')

# generate ccg sheet
generate_ccg_sheet()
print_fancy('Generated CCG sheet')