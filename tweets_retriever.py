from collections import Counter

import tweepy
import random

random.seed(3)

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


def batches(it, size):
	batch = []
	for item in it:
		batch.append(item)
		if len(batch) == size:
			yield batch
			batch = []
	if len(batch) > 0: yield batch 


class DatasetLang(object):
    """ For each of the 13 language dataset, use annotated tweets 
    from the most-annotate annotator.
    Skip all neutral tweets and only use 15000 tweets for each language.
    """
    def __init__(self, lang, csvpath):
        self.lang = lang
        self.id2polar, self.which_annotator, self.max_annotations = self._parse_csv(csvpath)
        print ("[INFO]: ! finish init the dataset object for {} !\n".format(lang))
    
    def _parse_csv(self, csvpath):
        annoor2annoes = {}
        with open(csvpath, "r") as f:
            for line in f.readlines()[1:]:
                myid, polar, anno_id = line.strip().split(",")
                if polar == "Neutral": continue
                if anno_id in annoor2annoes:
                    annoor2annoes[anno_id].append((myid, polar))
                else:
                    annoor2annoes[anno_id] = [(myid, polar)]
        max_annotations = max(map(lambda x: len(x), annoor2annoes.values()))
        for anno_id, annos in annoor2annoes.iteritems():
            if len(annos) == max_annotations:
                which_annotator = anno_id
                break
        print ("[INFO]: use results of annotator {}, with {} annotations.".format(
            which_annotator, max_annotations
        ))
        annos = annoor2annoes[which_annotator]
        random.shuffle(annos)
        annos = annos[:15000]
        labels = [x[1] for x in annos]
        print ("[INFO]: loading {} valid tweets.".format(len(annos)))
        print ("[INFO]: tweets distribution {}".format(Counter(labels)))
        return dict(annos), which_annotator, max_annotations


class TwitterRetriever(object):
    def __init__(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        self.twitter = tweepy.API(
            auth, 
            wait_on_rate_limit=True, 
            wait_on_rate_limit_notify=True
        )
    
    def retrive_texts(self, tweet_ids):
        tweet_status = self.twitter.statuses_lookup(id_=tweet_ids)
        return tweet_status


class RetrievedData(object):
    OUTPATH = "./retrieved_dataset/"
    def __init__(self, para):
        self.lang, csvpath = para[0], para[1]
        self.num_written = 0
        self.identifiers = DatasetLang(self.lang, csvpath)
        self.retriever = TwitterRetriever()
        self.retrieve_it()

    def retrieve_it(self):
        num_writes, met_id = 0, set()
        all_ids = self.identifiers.id2polar.keys()
        for batch_ids in batches(all_ids, 100):
            mystatus = self.retriever.retrive_texts(batch_ids)
            batch_id2txt = []
            for sta in mystatus:
                batch_id2txt.append((sta.id, sta.text))
            self.write_batch(batch_id2txt)

    def write_batch(self, batch_id2txt):
        print (len(batch_id2txt))
        with open(RetrievedData.OUTPATH + "{}.txt".format(self.lang), "a") as f:
            for myid, mytext in batch_id2txt:
                myid = str(myid)
                if myid not in self.identifiers.id2polar: 
                    continue
                mypolar = self.identifiers.id2polar[myid]
                f.write("{}\t{}\t\{}\n".format(myid, mypolar, mytext.encode("utf-8")))
                self.num_written += 1
        print ("[INFO]: finish written {} tweets for {}".format(self.num_written, self.lang))


if __name__ == "__main__":
    locate = lambda x: "./dataset/{}_Twitter_sentiment.csv".format(x)
    myretrievers = RetrievedData(("eng", locate("English")))
