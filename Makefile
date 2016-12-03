en_monolingual_tweet_text.txt: id_monolingual_english.txt
	./download.py id_monolingual_english.txt > en_monolingual_tweet_text.txt
id_monolingual_english.txt: id_containing_lang2.txt
	cat en_es_training_offsets.tsv | grep -v -f id_containing_lang2.txt | grep lang1 | cut -f1 | uniq > id_monolingual_english.txt
id_containing_lang2.txt:
	cat en_es_training_offsets.tsv | grep -E'mixed|lang2' | cut -f1 | uniq > id_containing_lang2.txt
list_tweets_uniq.txt:
	./unique_tweet.sh
en_es_training_offsets.tsv:
	wget http://emnlp2014.org/workshops/CodeSwitch/data/Spanish_English/training/en_es_training_offsets.tsv
