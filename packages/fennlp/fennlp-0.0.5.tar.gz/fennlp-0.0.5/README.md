# fennlp 0.0.5

[![Build Status](https://travis-ci.org/kyzhouhzau/fennlp.svg?branch=master)](https://travis-ci.org/kyzhouhzau/fennlp/branches)
[![PyPI version](https://badge.fury.io/py/fennlp.svg)](https://badge.fury.io/py/fenlp)
[![GitHub version](https://badge.fury.io/gh/kyzhouhzau%2Ffennlp.svg)](https://badge.fury.io/gh/kyzhouhzau%2Ffennlp)
[![Maintainability](https://api.codeclimate.com/v1/badges/d587092245542684c80b/maintainability)](https://codeclimate.com/github/kyzhouhzau/fennlp/maintainability)
[![License](https://img.shields.io/github/license/kyzhouhzau/fennlp)](https://github.com/kyzhouhzau/fennlp/blob/master/LICENSE)
[![Coverage Status](https://coveralls.io/repos/github/kyzhouhzau/fennlp/badge.svg)](https://coveralls.io/github/kyzhouhzau/fennlp)

# Package description
An out-of-the-box NLP toolkit can easily help you solve tasks such as
Entity Recognition, Text Classification, Relation Extraction and so on.
Currently it contain the following models (see "tests" dictionary for more details):

Models:
* BERT
* ALBERT
* TextCNN
* TucKER
* GCN

Examples (See tests for more details):

* BERT-NER (Chinese and English Version)
* BERT-CRF-NER (Chinese and English Version)
* BERT-Sentence-Classification (Chinese and English Version)
* ALBERT-NER (Chinese and English Version)
* TextCNN(Chinese and English Version)
* GCN (2 Layer, CORA data set)
* TuckER (English Version, WN18 data set)

All the above experiments were tested on GTX 1080 GPU with memory 8000MiB.

# Status
2020/3/19: add test example "albert_ner_train.py" "albert_ner_test.py"

2020/3/16: add model for training sub word embedding based on bpe methods.
The trained embedding is used in TextCNN model for improve it's improvement.
See "tran_bpe_embeding.py" for more details.

2020/3/8: add test example "run_tucker.py" for train TuckER on WN18.

2020/3/3: add test example "tran_text_cnn.py" for train TextCNN model. 

2020/3/2: add test example "train_bert_classification.py" for text classification based on bert.

2020/2/26: add GCN example on cora data.

2020/2/25: add test example "bert_ner_train.py" and "bert_ner_test.py".

# Requirement
* tensorflow-gpu>=2.0
* typeguard
* gensim
* tqdm
* sentencepiece

# Usage

1. clone source
```
git clone https://github.com/kyzhouhzau/fennlp.git
```
2. install package
```
python setup.py install
```
or 
```
pip install fennlp
```
3. run model
```
python bert_ner_train.py
```

# For NER：

## Input
* put train, valid and test file in "Input" dictionary.
* data format: reference data in  "tests\NER\InputNER\train"

    e.g. "拮 抗 RANKL 对 破 骨 细 胞 的 作 用 。	O O O O B-Anatomy I-Anatomy I-Anatomy E-Anatomy O O O O"
    
    For each line in train contains two parts, the first part "拮 抗 RANKL 对 破 骨 细 胞 的 作 用 。" is a sentence.
    The second part "O O O O B-Anatomy I-Anatomy I-Anatomy E-Anatomy O O O O" is the tag for each word in the sentence.
    Both of them use '\t' to concatenate.

### 1、bert

```python
from fennlp.models import bert
bert = bert.BERT()
```

```
python bert_ner_train.py
```

```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
bert (BERT)                  multiple                  101677056 
_________________________________________________________________
dense (Dense)                multiple                  35374     
=================================================================
Total params: 101,712,430
Trainable params: 101,712,430
Non-trainable params: 0
_________________________________________________________________
```

### 2、bert + crf
```python
from fennlp.models import bert
from fennlp.metrics.crf import CrfLogLikelihood
bert = bert.BERT()
crf = CrfLogLikelihood()
```

```
python bert_ner_crf_train.py
```
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
bert (BERT)                  multiple                  101677056 
_________________________________________________________________
dense (Dense)                multiple                  35374     
_________________________________________________________________
crf (CrfLogLikelihood)       multiple                  2116      
=================================================================
Total params: 101,714,546
Trainable params: 101,714,546
Non-trainable params: 0
_________________________________________________________________
```

### 3、albert (base, large, xlage, xxlage)
```python
from fennlp.models import albert
bert = albert.ALBERT()
```

```
python albert_ner_train.py 
```
```
large
Model: "albert_ner"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
albert (ALBERT)              multiple                  11092992  
_________________________________________________________________
dense (Dense)                multiple                  6921      
=================================================================
Total params: 11,099,913
Trainable params: 11,099,913
Non-trainable params: 0
_________________________________________________________________

```

Using the default parameters, we get the following results on "中文糖尿病标注数据集" and "CoNLL-2003" valid data.

|model    | macro-F1| macro-P| macro-R|  lr    |epoch   |maxlen  |batch_size| data|
| ------- |  -------| -------| -------| ------- |------- |------- |------- |-------   |
| bert+crf| -       | -      | -      | -       |-       |    -   |  -   |中文糖尿病标注数据集    |
|   bert  |  -      | -      | -      | -       |-       |    -   |  -   |中文糖尿病标注数据集    |
|   bert  | 0.9007  | 0.9067 | 0.9132 | 2e-5    |8       |   128  |  8   |    CoNLL-2003    |
|albert+base| 0.8367  | 0.8527 | 0.8462 | 2e-5  |10      |   128  |  16 |    CoNLL-2003    |
|albert+large| 0.8670  | 0.8778 | 0.8731 | 2e-5 |10     |   128  |  4 |    CoNLL-2003    |

# For Sentence Classfication
                 
## Input
* put train, valid and test file in "Input" dictionary.
* data format: reference data in "\tests\CLS\BERT( or TextCNN)\Input".

    e.g. "作 为 地 球 上 曾 经 最 强 的 拳 王 之 一 ， 小 克 里 琴 科 谈 自 己 是 否 会 复 出    2"
    
    For each line in train(test,valid) contains two parts, the first part "作 为 地 球 上 曾 经 最 强 的 拳 王 之 一 ，
    小 克 里 琴 科 谈 自 己 是 否 会 复 出" is the sentence, and second part "2" is the label.

### 1、bert

```python
from fennlp.models import bert
bert = bert.BERT()
```

``` 
python train_bert_classification.py
```
```
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
bert (BERT)                  multiple                  102267648 
_________________________________________________________________
dense (Dense)                multiple                  11535     
=================================================================
Total params: 102,279,183
Trainable params: 102,279,183
Non-trainable params: 0
_________________________________________________________________

```


### 2、TextCNN

```python
from fennlp.models import TextCNN
model = TextCNN.TextCNN()
```

``` 
python train_text_cnn.py
```

```
Use "WordPiece embedding" to Initialize word embedding. Train your embeddings.
python train_bpe_embedding.py
```
For more detail reference [WordPiece](https://mp.weixin.qq.com/s/Il8sh66TUCEPskbypDZLAg) 


Using the default parameters, we get the following results on "新闻标题短文本分类" valid data.

|model    | macro-F1| macro-P| macro-R| ACC     |  lr    |epoch   |maxlen  |batch_size|lr_decay|
| ------- |  -------| -------| -------| ------- |------- |------- |------- |-------   |-------|
| bert+softmax|0.8470|0.8618 |0.8625  |0.8899   |1e-5     |    5   |  50    |    32    |False|
| TextCNN+BPE| 0.8105 | 0.8193 | 0.8223| 0.8382|0.001  |  5     | 50     |   128    |False|
|  TextCNN   | 0.8029 | 0.8196 | 0.8104| 0.8308|0.001  |  5     | 50     |   128    |False|
# For GCN：

## Input
data format: see files in "tests/GCN/data/README.md" for more detail.


```python
from fennlp.models import GCN
model = GCN.GCN2Layer()
```

```
python train_gcn.py
```


关系的展示不是很好
生物上的应用








