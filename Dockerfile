FROM pytorch/pytorch:latest

RUN apt-get install -y \
 wget \
 curl \
 bzip2 \
 python-dev \

RUN chmod 777 .

RUN git clone https://github.com/facebookresearch/DrQA.git

RUN cd DrQA

RUN pip install -r requirements.txt

RUN python setup.py develop

RUN ./install_corenlp.sh

RUN export CLASSPATH=$CLASSPATH:data/corenlp/*

RUN python

RUN from drqa.tokenizers import CoreNLPTokenizer
RUN tok = CoreNLPTokenizer()
RUN tok.tokenize('hello world').words()  # Should complete immediately
RUN exit()

RUN ./download.sh

# Manually download our dataset from google drive link

RUN python scripts/pipeline/interactive.py --retriever-model data/web/db-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz --doc-db data/web/db.db