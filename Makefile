tweet_text.txt:
	./download.py list_tweets_uniq.txt > tweet_text.txt
list_tweets_uniq.txt:
	./unique_tweet.sh
en_es_training_offsets.tsv:
	wget http://emnlp2014.org/workshops/CodeSwitch/data/Spanish_English/training/en_es_training_offsets.tsv
