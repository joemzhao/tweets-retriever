# tweets-retriever
Retrieve tweets from Twitter API with tweet ID.

Retrieving tweet texts for Twitter sentiment classification for 13 European languages. Human annotated sentiment label for each tweet is from [1].

Languages:
 * Albanian
 * Bosnian
 * Bulgarian
 * Croatian
 * English
 * German
 * Hungarian
 * Polish
 * Portuguese
 * Russian
 * Serbian
 * Slovak
 * Slovenian
 * Spanish
 * Swedish

The goal is to gradually retrieve 1000 tweets in each of the 13 languages. It consume significant amount of time due to restrictions from the Twitter API rate limit. 

In total there are 1.6 million tweets. For simplicity all netrual tweets are skipped and output row format is:

TweetID \t Polarity \t Tweet-texts

A sample row (Swedish):

508925618311135232	Positive	@BrittaBostrm Är ledig o ensam hemma, såå skönt! 😊☕️☀️💕

## References
```
[1]
@article{DBLP:journals/corr/MozeticGS16,
  author    = {Igor Mozetic and
               Miha Grcar and
               Jasmina Smailovic},
  title     = {Multilingual Twitter Sentiment Classification: The Role of Human Annotators},
  journal   = {CoRR},
  volume    = {abs/1602.07563},
  year      = {2016},
  url       = {http://arxiv.org/abs/1602.07563},
  archivePrefix = {arXiv},
  eprint    = {1602.07563},
  timestamp = {Mon, 13 Aug 2018 16:48:40 +0200},
  biburl    = {https://dblp.org/rec/bib/journals/corr/MozeticGS16},
  bibsource = {dblp computer science bibliography, https://dblp.org}
}
```
