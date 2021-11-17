import os
from datetime import datetime 
import pandas as pd
from geopy.distance import geodesic

def engineer(data_dir):

    filenames = os.listdir(data_dir)
    file_paths = [os.path.join(data_dir,f) for f in filenames if not f.startswith('.')]
    
    trip_df = pd.concat([pd.read_csv(filepath) for filepath in file_paths])
    
    trip_df.drop(['start_station_name', 'end_station_name'], axis = 1, inplace = True)
    trip_df.dropna(inplace = True)
    
    str_to_dt = lambda s: datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
    trip_df['start_dt'] = trip_df['started_at'].transform(str_to_dt)
    trip_df['end_dt'] = trip_df['ended_at'].transform(str_to_dt)

    trip_df['month'] = trip_df['start_dt'].apply(lambda x: x.month)
    trip_df['hour'] = trip_df['start_dt'].apply(lambda x: x.hour)
    trip_df['day'] = trip_df['start_dt'].apply(lambda x: x.weekday())
    
    trip_df['duration'] = trip_df['end_dt'] - trip_df['start_dt']
    trip_df['duration(mins)'] = trip_df['duration'].apply(lambda x: int(x.total_seconds()/60))
    
    trip_df['start_coord'] = [(lat,lng) for lat,lng in zip(trip_df['start_lat'],trip_df['start_lng'])]
    trip_df['end_coord'] = [(lat,lng) for lat,lng in zip(trip_df['end_lat'],trip_df['end_lng'])]
    trip_df['dist(m)'] = [geodesic(start,end).meters for start,end in \
                       zip(trip_df['start_coord'], trip_df['end_coord'])]
    
#     bins = pd.IntervalIndex.from_tuples([(-1, 5), (5, 11), (11, 17), (17,23)])
#     labels = ["Small Hours", "Morning", "Afternoon", "Evening"]
#     bin_label = dict(zip(bins,labels))
#     trip_df['time_of_day'] = pd.cut(trip_df['hour'],bins).map(bin_label)

#     trip_df['is_weekend'] = trip_df['day'] >= 5

#     bins = pd.IntervalIndex.from_tuples([(-1, 2), (2, 5), (5, 8), (8,11)])
#     labels = ["Winter", "Spring", "Summer", "Fall"]
#     bin_label = dict(zip(bins,labels))
#     trip_df['season'] = pd.cut(trip_df['month'].apply(lambda x: x%12),bins).map(bin_label)

    #cols = ['ride_id','member_casual','month','day','hour','dist(m)','duration(mins)', 'rideable_type']
    
    #trip_df = trip_df[cols]
    
    trip_df.to_csv('Data/engineered_df2.csv', index = False)