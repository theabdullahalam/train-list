import os
import csv
import sys

MOSR_FILE = 'database.csv'
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
  field_names = []
  train_no_column = ''
  class_column = ''

  with open(FAX_SHEET, 'r') as f:
    # field names
    row_list = list(csv.reader(f))
    field_names = row_list[0]
    field_names.insert(2, 'Division')
    train_no_column = field_names[1]
    class_column = field_names[3]

  with open(FAX_SHEET, 'r') as f:

    # processing
    reader = csv.DictReader(f)
    updated_rows = []

    for row in reader:
      print(row)
      new_row = row
      new_row['Division'] = get_origin_divn(row[train_no_column])

      # handle BCT case
      if new_row['Division'] == 'BCT':
        if new_row[class_column] == 'SL' or new_row[class_column] == '2S':
          pass
        else:
          new_row['Division'] = 'CCG'


      updated_rows.append(new_row)

    with open(UPDATED_SHEET, 'w', newline='') as u:
        writer = csv.DictWriter(u, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(updated_rows)

def generate_ccg_sheet():
  field_names = []
  
  with open(UPDATED_SHEET, 'r') as u:
      
      # field names
      row_list = list(csv.reader(u))
      field_names = row_list[0]

  with open(UPDATED_SHEET, 'r') as u:

      reader = csv.DictReader(u)
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

      with open(CCG_SHEET, 'w', newline='') as c:
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