from twython import Twython
from collections import Counter

import tqdm
import twython
import time


CONSUMER_KEY = ""
CONSUMER_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


class TwitterRetriever(object):
    def __init__(self):
        self.twitter = Twython(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    def retrive_texts(self, tweet_id):
        return self.twitter.show_status(id=tweet_id)["text"]


class DatasetLang(object):
    """ For each of the 13 language dataset, use annotated tweets 
    from the most-annotate annotator.
    Skip all neutral tweets.
    """
    def __init__(self, lang, csvpath):
        self.lang = lang
        self.id2poar, self.which_annotator, self.max_annotations = self._parse_csv(csvpath)
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
        print ("[INFO]: using results from annotator {}, with {} annotations.".format(
            which_annotator, max_annotations
        ))
        annos = annoor2annoes[which_annotator]
        labels = [x[1] for x in annos]
        print ("[INFO]: loading {} valid tweets.".format(len(annos)))
        print ("[INFO]: tweets distribution {}".format(Counter(labels)))
        return dict(annos), which_annotator, max_annotations


class RetrievedData(object):
    OUTPATH = "./retrieved_dataset/"
    def __init__(self, para):
        self.lang, csvpath = para[0], para[1]
        self.identifiers = DatasetLang(self.lang, csvpath)
        self.retriever = TwitterRetriever()
        self.retrieve_it()

    def retrieve_it(self):
        num_writes, met_id = 0, set()
        while num_writes < 1000:
            for myid, mypolar in self.identifiers.id2poar.items():
                if myid in met_id: continue
                time.sleep(59)
                try:
                    mytext = self.retriever.retrive_texts(myid)
                except twython.exceptions.TwythonError as e:
                    print (e)
                    continue
                with open(RetrievedData.OUTPATH+"{}.data".format(self.lang), "a") as f:
                    f.write("{}\t{}\t{}\n".format(myid, mypolar, mytext.encode("utf-8")))
                print ("[INFO]: ! writeen following row !")
                print (self.lang, myid, mypolar, mytext)
                num_writes += 1
                met_id.add(myid)
        print ("[INFO]: finish retrieving tweets for {}".format(self.lang))


if __name__ == "__main__":
    locate = lambda x: "./dataset/{}_Twitter_sentiment.csv".format(x)
    myretrievers = RetrievedData(("swe", locate("Swedish")))
