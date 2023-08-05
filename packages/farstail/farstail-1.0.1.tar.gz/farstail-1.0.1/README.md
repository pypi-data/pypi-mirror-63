# FarsTail
This package is for loading FarsTail Persian Natural Language Inference (NLI) and Question Answering (QA) dataset.

## install
```ruby
pip install farstail
```

## using
```ruby
from farstail.datasets import farstail
(p_train, h_train, l_train), (p_dev, h_dev, l_dev), (p_test, h_test, l_test) = farstail.load_data()
```
Downloading data ...  
333973/333973 [==============================] - 13s 38us/step

```ruby
farstail_word_index = farstail.get_word_index()
```
Downloading data ...  
421737/421737 [==============================] - 18s 42us/step
