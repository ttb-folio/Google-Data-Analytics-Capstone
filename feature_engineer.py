import os
from datetime import datetime 
import pandas as pd

def engineer(data_dir):

    filenames = os.listdir(data_dir)
    file_paths = [os.path.join(data_dir,f) for f in filenames if not f.startswith('.')]
    
    trip_df = pd.concat([pd.read_csv(filepath) for filepath in file_paths])
    
    str_to_dt = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')

    trip_df['started_at'] = trip_df['started_at'].transform(str_to_dt)
    trip_df['ended_at'] = trip_df['ended_at'].transform(str_to_dt)
    
    trip_df['year'] = trip_df['started_at'].apply(lambda x: x.year)
    trip_df['month'] = trip_df['started_at'].apply(lambda x: x.month)
    trip_df['weekday'] = trip_df['started_at'].apply(lambda x: x.weekday())
    
    trip_df['duration'] = trip_df['ended_at'] - trip_df['started_at']
    trip_df['duration_mins'] = trip_df['duration'].apply(lambda x: int(x.total_seconds()/60))
    
    trip_df.to_csv('Data/engineered_df.csv', index = False)