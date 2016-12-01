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

    def download(self, tweetIds):
        for status in self.api.statuses_lookup(tweetIds):
                print(status.id, "\t",status.text)
        


if(__name__ == "__main__"):
    import tweepy, sys, time
    from tweepy import OAuthHandler
    downloader = TweetDownloader(consumer_key,\
            consumer_secret, access_token, access_secret)
    chunk = []
    with open(sys.argv[1], 'r') as f:
        for line in f:
            if (len(chunk) < 2):
                chunk.append(line.rstrip())
            else:
                chunk.append(line.rstrip())
                downloader.download(chunk)
                chunk = []
                time.sleep(2)
        if (len(chunk) > 0): download(chunk)







