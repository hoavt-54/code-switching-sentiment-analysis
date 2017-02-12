### SENTIMENT CLASSIFIER

from nltk.classify import MaxentClassifier
import pickle
from nltk.corpus import sentiwordnet as swn
from nltk.classify.util import apply_features
import re
import random
from nltk.tokenize import TweetTokenizer
from statistics import mean

''' This script contains a sentiment classifier for our tweets together with all other
resources needed for that (reading the tweets, mapping the tags to SENT/NONE), extracting
the feature from a tweet and calculating the accuracy of the classifier.
The code is ready to run in the "if __name__ == '__main__':" part.
If left as such, the script will take all tweets (monolingual and CS) from the files 500_cs and 500_mono.annotated,
learn a classifier with 90% of the data (training) and evaluate it on the 10%. 
The CS feature is included.
This is done 100 times and the mean accuracy is printed at the end.
In order to change features, go to function senti_features.
'''


def read_tweets(file):
	'''
	This function takes a file of tweets with sentiment
	P	tweet_ID	tweet-text
	and outputs a list of tweets represented as tuples (tweet, sentiment label)
	'''
	pattern = re.compile('(.*?)\t(.*?)\t(.*?)\n')
	tweets = []
	with open(file, 'r') as fil:
		for line in fil:
			if re.search(pattern, line):
				match = re.search(pattern, line)
				sent = match.group(1)	# take the tweet's sentiment
				tweet = match.group(3)	# take the tweet's content

				tweets.append((tweet, sent))
	return tweets


def map_sentiment(tweets):
	'''
	This function takes a list of tweets (in the form of the read_tweets function's output) and maps
	positive, negative and mixed sentiment to a unique label called SENT.
	This is used for the SENT vs NONE analysis.
	It outputs the same tweet list with the desired mapping.
	'''
	new_tweets = []
	for tweet in tweets:
		if tweet[1] == 'P' or tweet[1] == 'N' or tweet[1] == 'M':
			tw = tweet[0]
			tag = 'SENT'
			new_tweets.append((tw, tag))
		else:
			new_tweets.append(tweet)

	return new_tweets


def senti_features(tweet_string):
	'''
	This function takes a tweet string as input and outputs a dictionary with its features	
	'''
	
	features = dict()
	features['emoticons'] = 0 # Number of exclamations
	features['exclamations'] = 0 # Number of exclamations
	features['positivism']= 0 # SentiWordNet feature
	features['negativism'] = 0 # SentiWordNet feature
	features['prop_caps'] = 0 # proportion of capital letters
	
	features['CS'] = False # Whether the tweet is a CS tweet (comment this line and its extraction in order not to use it)
	# The CS feature is extracted by checking that the two first characters of the tweet are CS
	# These two characters are added in the "main" part at the end. 
	# Once checked, it is removed:
	if tweet_string.startswith('CS'):
                features['CS'] = True
                tweet_string = tweet_string[2:]	
	
	tokenizer = TweetTokenizer()	# tokenize the tweet with the tweet tokenizer (should be better than just splitting)
	tweet = tokenizer.tokenize(tweet_string)  # this is now a list of words

	# Remove mentions of people starting with @, we assume they are useless (do not convey sentiment)
	for word in tweet:
		if word.startswith('@'):
			tweet.remove(word)

	# Set of emoticons taken from the data containing both good and bad emoticons and expressions like "lol"
	# which refer to laughing
	emoticons = set(['😠', '😭', ':)', ':(', ';D', ':D',':o', ':p', 'xD', 'lol', 'lmao', '...', 'lmfao','😂', '😋', '😎', '❤', '😏', '👌', '😍','😊','😁','😐','💕', '😛', 'Wtf', 'haha'])

	# Adding the bag of words feature:
	for word in tweet:
		features[word] = 1 		
		# SentiWordNet features:
		if list(swn.senti_synsets(word)):   # If this word exists in SentiWordNet:
			word_sents = list(swn.senti_synsets(word))
			pos = word_sents[0].pos_score()
			neg = word_sents[0].neg_score()
			obj = word_sents[0].obj_score()
			if pos > neg:
				features['positivism'] +=1
			elif pos < neg:
				features['negativism'] +=1        

		# filling the emoticon feature
		if word in emoticons:
			features['emoticons'] += 1 
            
	# exclamation and capital letter features
	up = 0
	length = len(tweet_string)
	for char in tweet_string:
		if char == '!':
			features['exclamations'] += 1
		if char.isupper():
			up +=1
	prop_caps = up / length
	features['prop_caps'] = prop_caps	

	return features


def evaluate_classifier(classifier, test_data):
    '''
    This function takes as input a classifier and test data (as a list of tuples) 
    and outputs the accuracy of the classifier
    '''
    correct = 0
    incorrect = 0
    for instance in test_data:
        features = instance[0]
        real_tag = instance[1]
        guessed_tag = classifier.classify(features)
        if real_tag == guessed_tag:
            correct +=1
        else:
            incorrect +=1

    accuracy = correct / (correct + incorrect)
    return accuracy


if __name__ == '__main__':
    
    #mono_tweets = read_tweets('500_mono.annotated.txt') # monolingual tweets without mapping sentiment
    #cs_tweets = read_tweets('500_cs.txt') # CS tweets without mapping sentiment
    cs_tweets = map_sentiment(read_tweets('500_cs.txt')) # cs tweets with sentiment mapping
    mono_tweets = map_sentiment(read_tweets('500_mono.annotated.txt')) # monolingual tweets with sentiment mapping

    # adding the CS mark to identify CS tweets. This is needed for the feature extraction. 
    for idx, (tweet, label)  in enumerate(cs_tweets):
        tweet = 'CS' + tweet
        cs_tweets[idx] = (tweet,label)
        mono_tweets.append((tweet, label))
    
    accuracies = []
    tweets = mono_tweets
    for i in range(100):
        
        random.shuffle(tweets)
        
        # Splitting into train and test, FOR 1000 tweets (Change it according to data size!!)
        train = tweets[:900]
        test = tweets[900:]
        
        # Applying features to our data
        train_feat, test_feat = [],[]
        for instance in train:
            x = (senti_features(instance[0]), instance[1])
            train_feat.append(x)
        for instance in test:
            x = (senti_features(instance[0]), instance[1])
            test_feat.append(x)
		
        print('Training...')	
        # Training the classifier
        me = MaxentClassifier.train(train_feat, max_iter=10)
        
	
        print('Evaluating...')
	# Store all accuracies for different runs
        accuracies.append(evaluate_classifier(me,test_feat))
        me.show_most_informative_features()
	# Get final, mean accuracy
    print ("accuracy: %.3f" % mean(accuracies))
