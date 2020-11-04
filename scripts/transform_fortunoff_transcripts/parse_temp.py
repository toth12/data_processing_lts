import pandas as pd
import constants
import pdb

names=pd.read_csv(constants.INPUT_FOLDER_FORTUNOFF_METADATA+'Fortunoff_first_names.csv' )
names['surname']=names.primary_name.apply(lambda x: x.split(',')[0].strip())
names[names.Identifier=='HVT-6']['surname'].values[0]
pdb.set_trace()
