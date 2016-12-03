#!/usr/bin/env python
consumer_key = '8MrDzUPX60SyJuVOlgsvVhTh1'
consumer_secret = '0a74KJMqRIcQm9OYMDdfnq8cSUw2o8VD9VFppZGh5PGIs8p2V2'
access_token = '2988809351-I60HyK4KXr5lPKmb6iucDUCHmhI0mteDPzTQFII'
access_secret = 'zxwo4I22sSxEeB6tDS46ZeOJgkPyCHxjR2On8xTh4hq7i'

class TweetDownloader(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret):
        auth = OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        self.api = tweepy.API(auth)

    def download(self, tweetIds, label_dict):
        for status in self.api.statuses_lookup(tweetIds):
            if(str(status.id) in label_dict):
                print(label_dict[str(status.id)], "\t" ,status.text)
            else: print(status.id, '\t', status.text)
        


if(__name__ == "__main__"):
    import tweepy, sys, time
    from tweepy import OAuthHandler
    downloader = TweetDownloader(consumer_key,\
            consumer_secret, access_token, access_secret)
    chunk = []
    label_dict = {}
    with open(sys.argv[1], 'r') as f:
        for line in f:
            try:
                if(line.startswith('#')) : continue
                tweet_id, label = line.strip().split('\t')
                label_dict[tweet_id] = label
            
                if (len(chunk) < 95):
                    chunk.append(tweet_id)
                else:
                    chunk.append(tweet_id)
                    downloader.download(chunk, label_dict)
                    chunk = []
                    label_dict = {}
                    time.sleep(3)
            except:
                #print (label_dict)
                raise
        if (len(chunk) > 0): download(chunk, label_dict)







