import json
import re
import numpy as np
import glob

INPUT_FOLDER = './data/input/'
OUTPUT_FOLDER = './data/output/'
DISASTER_LIST = './data/disasters_grid_listing.csv'
TWEET_MINIMUM_LENGTH = 3

"""
remove tab, \n, hyperlinks from tweets
"""
def clean_line(row):
    row = re.sub(r"RT @\S+", "", row)
    row = re.sub(r"MT @\S+", "", row)
    row = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", row).split())  # remove hyperlinks
    row = row.lower()
    row.replace('\t', ' ')
    return row

"""
parse a data file, return a list of dictionary, each dictionary corresponds to one tweet
"""
def parse_tweet_json(file):
    data_dict = {}
    with open(INPUT_FOLDER + file) as f:
        lines = f.readlines()
    for line in lines:
        json_tweet = json.loads(line)
        id = json_tweet['id']
        uid = json_tweet['user']['id']
        timestamp_ms = json_tweet['timestamp_ms']
        created_at = json_tweet['created_at']
        text = json_tweet['text'].encode('utf-8').strip()
        text = clean_line(text)
        if len(text) < TWEET_MINIMUM_LENGTH:
            continue
        loc = json_tweet['geo']['coordinates']
        if id and uid and timestamp_ms and created_at and loc:
            tweet_dict = {'uid' : uid, 'timestamp_ms' : timestamp_ms, 'created_at' : created_at, 'text' : text, 'lat' : loc[0], 'lon' : loc[1]}
            data_dict[id] = tweet_dict

    file_out = open(OUTPUT_FOLDER + file, 'w')
    for key in data_dict.keys():
        val = data_dict[key]
        line = '\t'.join(map(str, [key, val['uid'], val['lat'], val['lon'], val['timestamp_ms'], val['created_at'], val['text']])) + '\n'
        file_out.write(line)
    file_out.close()
    return len(lines)

# obtain a list of dates for disaster response
# dates = np.loadtxt(DISASTER_LIST, dtype = 'str', delimiter='\",\"', usecols = ([1]), skiprows=1)
# disasters_date = [date.split('/')[2] + date.split('/')[0] + date.split('/')[1] for date in dates]
# print 'Extracting data from the following dates: ', dates
#
# for file in glob.glob(INPUT_FOLDER + "/*"):
#     filename = re.findall('[^\\\\/]+', file)[-1]
#     date = filename.split('.')[0]
#     total_tweets = 0
#     if date in disasters_date:
#         tweet_count = parse_tweet_json(filename)
#         print 'Date ' + date + ' has ' + str(tweet_count ) + ' tweets'
#         total_tweets += tweet_count
#         print '..... total ' + str(total_tweets) + ' tweets extracted...'
#
# print 'Done!'

min_lat, max_lat, min_lon, max_lon = 33, 39, -101, -93

data = np.loadtxt(OUTPUT_FOLDER + './20160903.txt', dtype= float, delimiter='\t', usecols = (2,3))
valid_rows = np.all([min_lat <= data[:,0], data[:,0] <= max_lat, min_lon <= data[:,1],  data[:,1]<= max_lon], axis=0)

data = np.loadtxt(OUTPUT_FOLDER + './20160903.txt', dtype= 'str', delimiter='\t')
data = data[valid_rows]

print type(data), data.shape
np.savetxt(OUTPUT_FOLDER + './20160903_filtered.txt', data, fmt='%s', delimiter='\t')