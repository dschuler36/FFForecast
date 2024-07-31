import os
from src.data_prep.data_prep_base import DataPrep

filenames_to_process = os.listdir('data/')
files_to_process = [f'data/{f}' for f in filenames_to_process]

for file_name in files_to_process:
    if file_name.endswith('.csv'):
        dp = DataPrep(file_name)
        print(file_name)