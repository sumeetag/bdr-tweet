"""

split data into training data and testing data in two separated files
"""
import numpy as np
import re
INPUT = '10KLabeledTweets.txt'
OUTPUT = '10KLabeledTweets_formatted.txt'
TRAIN = 'training_tweets.txt'
TEST = 'testing_tweets.txt'

k_fold = 5  # k-fold cross-validation

# properly format the data
output = open(OUTPUT, 'w')
output.write('Tweet ID\tInformation Source\tInformation Type\tDisaster-related\tTweet Text')
tweets_count = 0
with open(INPUT) as f:
    for line in f.readlines():
        # check if this line as a proper formatted tweet
        if len(line.split('\t')) == 5:
            output.write('\n')
            output.write(line.strip())
            tweets_count = tweets_count + 1
        else:
            output.write(' ' + line.strip().replace('\t', ' '))

# data = np.loadtxt(OUTPUT, dtype='str', delimiter='\t', skiprows=1)
# print data.shape

#
# # for i in range(20):
# #     print data[i]
# np.savetxt(TEST, data[:test_set_count], fmt='%s', delimiter='\t')
# np.savetxt(TRAIN, data[test_set_count:], fmt='%s', delimiter='\t')

test_set_count = tweets_count/k_fold
train_set_count = tweets_count - test_set_count
test_output = open(TEST, 'w')
train_output = open(TRAIN, 'w')
with open(OUTPUT) as f:
    data = f.readlines()
    for line in data[1:test_set_count]:
        test_output.write(line)
    for line in data[train_set_count:]:
        train_output.write(line)