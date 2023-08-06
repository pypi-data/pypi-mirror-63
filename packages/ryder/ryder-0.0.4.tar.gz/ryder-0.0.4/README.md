# Scrape any news outlet

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Installing

You can install the method by typing:
```
pip install ryder
```

### Basic usage

```python
import ryder

#: get all valid urls on the homepage
articles = ryder.source("https://lemonde.fr")

for article in articles[:5]:
    #: scrape content of the article
    # lang is True by default: whether to infer the language
    # of the article (using langdetect)
    news = ryder.read(article["url"], lang=True)
    print(news)

```

## Authors

Maixent Chenebaux