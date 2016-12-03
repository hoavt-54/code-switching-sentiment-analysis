#!/usr/bin/env python2
#from vaderSentiment import sentiment as vaderSentiment
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import sys

err, emo, pos, neu, neg = 0, 0, 0, 0, 0

with open (sys.argv[1], 'r') as f:
    for line in f:
        try:
            tweetId, text = line.strip().split('\t')
            vs = vaderSentiment(text)

            vpos, vneg, vneu = vs["pos"], vs["neg"], vs["neu"]
            # if pos score is highest then this tweet's classified as pos
            if(vpos > vneu and vpos > vneg):
                pos = pos + 1
		print "pos\t", text
            # if neg score is highest
            if (vneg > vpos and vneg > vneu):
                neg = neg + 1
		print "neg\t", text
            # this tweet is classified as emotional if 
            if(vpos > vneu or vneg > vneu):
                emo = emo +1				
            # otherwise it's neutral
            elif(vneu > vneg and vneu > vpos):
                neu = neu + 1
		print "neu\t", text
	    
        except:
            err = err + 1
            pass
			
#print ("emo: %d \tpos: %d\t neu: %d\t neg: %d\t err: %d" % (emo, pos, neu, neg, err))

