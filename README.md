# tweets-retriever
Retrieve tweets from Twitter API via tweet ID.

Retrieving tweet texts for sentiment classification for 15 European languages. Human annotated sentiment label for each tweet is from Mozetic et. al. (2016).

For each of following languages, around 15k positive/negative Tweets are retrived. No neutral tweets.

Languages - ISO 639-3 code:
 * Albanian - sqi
 * Bosnian - bos
 * Bulgarian - bul
 * Croatian - hrv
 * English - eng
 * German - deu
 * Hungarian - hun
 * Polish - pol
 * Portuguese - por
 * Russian - rus 
 * Serbian - srp
 * Slovak - slk
 * Slovenian -slv
 * Spanish - spa
 * Swedish - swe

## Portocal

For each language, retrieve annotated tweets from the _same annotator_ for consistency. 

## Format

Retrieved tweets are in follwoing format (per row) :

TweetID \t Polarity \t Tweet-texts

A sample row (Swedish):

508925618311135232	Positive	@BrittaBostrm Är ledig o ensam hemma, såå skönt! 😊☕️☀️💕



## References
```
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
