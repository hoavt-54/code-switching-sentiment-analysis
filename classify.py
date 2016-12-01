#!/usr/bin/env python2
#from vaderSentiment import sentiment as vaderSentiment
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import sys

err, pos, neu, neg = 0, 0, 0, 0
vs = vaderSentiment("I love all Erasmus LCT students")
print(str(vs))
print ()
with open (sys.argv[1], 'r') as f:
    for line in f:
        try:
            tweetId, text = line.strip().split('\t')
            print (text), 
            vs = vaderSentiment(text)
            print ("\n\t" + str(vs))
        except:
            print "Unexpected error:", sys.exc_info()[0]
            print line.strip().split('\t')
            exit()

