### SENTIMENT CLASSIFIER

from nltk.classify import MaxentClassifier
import pickle
from nltk.corpus import sentiwordnet as swn
from nltk.classify.util import apply_features
import re
import random
from nltk.tokenize import TweetTokenizer

# You should pull before doing this because the cs_tweet had a format incompatibility, 
# I replaced it, it is now fixed. Get the new one.

# This has no sys.argvs, everything is in the name-main part.


def read_tweets(file):
	'''
	This function takes a file of tweets with sentiment
	P	tweet_ID	tweetblablablabla
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
	This function takes a list of tweets (like read_tweet's output) and maps
	positive, negative and mixed sentiment to a unique label called SENT.
	This is used for the SENT vs NONSENT analysis.
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
	This function takes as input a tuple containing a tweet and its sentiment
	and extracts its features.
	The features have the form of a dictionary where the key is the name
	of the feature. 
	The function outputs the feature dictionary.
	This is later fed as input for the nltk apply_features function, which
	takes care of all the dirty work (like turning these features into
	numbers if I am not mistaken).
	ITS BETTER TO LOOK AT SENTI_FEATURES2, THE ONE USED FOR MIXED CS AND MONO DATA.
	'''

	tweet_string = tweet_string[0]	# take the tweet text
	features = dict()
	tokenizer = TweetTokenizer()	# tokenize it with the tweet tokenizer (better than splitting, probably...)
	tweet = tokenizer.tokenize(tweet_string)	#tweet_string.split() # this is now a list of words

	# Remove mentions of people, we assume they are useless
	for word in tweet:
		if word.startswith('@'):
			tweet.remove(word)

	# some default feature values (will change later if necessary)
	#features['positivism'] = 0 # Removed features for SentiWordNet
	#features['negativism'] = 0
	features['contains_emoticon'] = 0
	features['exclamation'] = 0

	emoticons = ['😠', '😭', ':)', ':(', ';D', ':D',':o', ':p', 'xD', 'lol', 'lmao', '...', 'lmfao','😂', '😋', '😎', '❤', '😏', '👌', '😍','😊','😁','😐','💕', '😛', 'Wtf', 'haha']

	# Adding word features and SentiWordNet features
	for word in tweet:
		#word = nltk.stem.WordNetLemmatizer().lemmatize(word) # APPARENTLY, LEMMATIZING IS NOT A GOOD IDEA: ACCURACY DECREASED

		features[word] = 1 # This is the bag of words feature. Tried removing uppercase and it was worse for some reason

		''' SENTIWORDNET, NOT USING
		if list(swn.senti_synsets(word)):	# If this word exists in SentiWordNet:
			word_sents = list(swn.senti_synsets(word))
			pos = word_sents[0].pos_score()
			neg = word_sents[0].neg_score()
			obj = word_sents[0].obj_score()
			if pos > neg:
				features['positivism'] +=1
			elif pos < neg:
				features['negativism'] +=1
		'''

		# filling emoticon feature
		if word in emoticons:
			features['contains_emoticon'] += 1


	for char in tweet_string:
		if char == '!':
			features['exclamation'] += 1



	# other possible features: loooooong words?

	return features




def senti_features2(tweet_string):
	'''
	This is almost the same as senti_features but with mixed input (cs and monolingual)
	
	'''

	tweet_string = tweet_string[0]
	features = dict()
	features['contains_emoticon'] = 0
	features['exclamation'] = 0
	features['CS'] = False
	features['prop_caps'] = 0 # proportion of capital letters


	# The CS feature is extracted by checking that the two first characters of the tweet are CS
	# (In the name-main part I add CS to all of them. Once checked, it is removed:)
	# (I didnt have time to think of a better way to do this xd)
	if tweet_string.startswith('CS'):
		features['CS'] = True
		tweet_string = tweet_string[2:]	
	
	tokenizer = TweetTokenizer()	# tokenize it with the tweet tokenizer (better than splitting, probably...)
	tweet = tokenizer.tokenize(tweet_string)	#tweet_string.split() # this is now a list of words

	# Remove mentions of people, we assume they are useless
	for word in tweet:
		if word.startswith('@'):
			tweet.remove(word)

	# Yes, I know not all of them are emoticons as such...
	# these could be split into laughing and some other categories maybe...
	emoticons = ['😠', '😭', ':)', ':(', ';D', ':D',':o', ':p', 'xD', 'lol', 'lmao', '...', 'lmfao','😂', '😋', '😎', '❤', '😏', '👌', '😍','😊','😁','😐','💕', '😛', 'Wtf', 'haha']

	# Adding word features 
	for word in tweet:
		
		features[word] = 1 # This is the bag of words feature
		
		# filling emoticon feature
		if word in emoticons:
			features['contains_emoticon'] += 1

	# exclamation and capital letter features
	up = 0
	length = len(tweet_string)
	for char in tweet_string:
		if char == '!':
			features['exclamation'] += 1
		if char.isupper():
			up +=1
	prop_caps = up / length
	features['prop_caps'] = prop_caps


	# other possible features: loooooong words?

	return features



def evaluate_classifier(classifier, test_data):
	'''
	Outputs the accuracy of the classifier
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


	#tweets = map_sentiment(read_tweets('tweets.txt'))
	#mono_tweets = read_tweets('tweets.txt')
	#cs_tweets = read_tweets('cs_tweets.txt')
	
	mono_tweets = map_sentiment(read_tweets('tweets.txt'))
	cs_tweets = map_sentiment(read_tweets('cs_tweets.txt'))

	# adding the CS mark to code switching tweets. This is needed for the feature extraction. It's ugly, I know.
	for tweet, label in cs_tweets:
		tweet = 'CS' + tweet

	tweets = mono_tweets + cs_tweets
	
	# this is only necessary if mono and cs are mixed
	random.shuffle(tweets)

	# Splitting into train and test, FOR 1000 TWEETS (CHANGE IT ACCORDINGLY)
	train = tweets[:450]
	test = tweets[450:]
	print(len(test))

	# Applying features to our data. 
	train_feat = apply_features(senti_features2, train)
	test_feat = apply_features(senti_features2, test)

	print('Training...')

	# Training the classifier
	me = MaxentClassifier.train(train_feat, max_iter=10)


	print('Evaluating...')

	print(evaluate_classifier(me,test_feat))

	print('Best features:')

	me.show_most_informative_features()