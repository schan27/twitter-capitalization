# Social and Emotional Correlates of Capitalization on Twitter
Disclaimer - these are the scripts that were used for the project, but this was back in 2016 when organization was not a priority for me. I hope to organize these scripts in the future, but for now they're here for reference. :) 

The scripts here are meant to reproduce the results in [this workshop paper (Chan & Fyshe, 2018)](http://www.aclweb.org/anthology/W18-1102), and are organized by the section of the paper they correspond to.

The input dataset is from [Exploring Demographic Language Variations to Improve Multilingual Sentiment Analysis in Social Media (Volkova, Wilson, & Yarowsky, 2013)](https://www.cs.jhu.edu/~svitlana/papers/VWY-emnlp2013.pdf) and can be downloaded [here](https://www.cs.jhu.edu/~svitlana/data/data_emnlp2013.tar.gz). Since Twitter restricts the sharing of data, the dataset lists tweet ids but you will need to fetch the actual tweets (see [this resource](https://gwu-libraries.github.io/sfm-ui/posts/2017-09-14-twitter-data)). Only English tweets were used.

The tweets were tagged using [TweeboParser](https://github.com/ikekonglp/TweeboParser), and [Google Books English 1-grams](http://storage.googleapis.com/books/ngrams/books/datasetsv2.html) were used to approximate true frequency distributions.
