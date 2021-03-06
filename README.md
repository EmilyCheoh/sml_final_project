# Domain Specific Question Answering
Surrounded by overwhelming amount of data everyday, we have never enjoyed more convenience in retriving knowledge. However, most information available online, 
such as web pages, is in full-text, meaning it could be hard for us to get the answer that we are interested in directly. Question Answering systems are hence build to
solve this problem. 

Idealy, given a question, the system will search through it knowledge base and return the correct answer to us directly. 
The task we focus on is domain-specific questions answering.

## How our project solves this problem
![framework](solution.png)
Our model is based on [DrQA](https://github.com/facebookresearch/DrQA), which focuses on Open-domain QA problem. 

With DrQA, the system is searching for an answer for a question in very large corpus of unstructured documents, so it is designed into two parts: a document retriever and a bidirectional RNN document reader. 
In this setting, document retriever is designed to find the five most relevant documents based on bigram hashing and TF-IDF matching, and document reader is designed to achieve machine comprehension of text, identifying the answers from documents retriever found.

However, DrQA is using WIkepedia as the unique knowledge source for documents, which, for our system, is a specific website(https://www.chainstoreage.com). 

Therefore, in our system, there is a web crawler before document retriever to iterativelly scrape all potential documents from that website.

## input&output of your model
Input: Questions users are interested in and the knowledge source

Output: Answers to the questions and according text source

## How to train the model
### Scraping data from website

To get a txt file of documents from website, run:

``` python
python clawer.py
```

Web crawler will generate a txt. file to store the documents. Each file consists of JSON-encoded documents that have id and text fields, one per line:

```
{"id": "doc1", "text": "text of doc1"}
...
{"id": "docN", "text": "text of docN"}
```

### Storing the documents
With those txt. files, the next step will be build a sqlite database to store them.

To create a splite database, run:

```
python build_db.py /path/to/data /path/to/saved/database.db
```

Path to data is the path to a nested directory of generated txt. files by web crawler.

### Building TF-IDF N-grams
To build a TF-IDF matrix from documents stored in your built sqlite database, run:

```
python build_tfidf.py /path/to/doc/db /path/to/output/dir
```

The sparse matrix and its associated metadata will be saved to the output directory under <db-name>-tfidf-ngram=\<N>-hash=\<N>-tokenizer=\<T>.npz
  
### interactively using document retriever

To use document retriever interactively, run:

```
python scripts/retriever/interactive.py --model /path/to/model/(.npz file)
```

```
>>> process('Old Navy', k = 3)
+------+---------+-----------+
| Rank |  Doc Id | Doc Score |
+------+---------+-----------+
|  1   | doc5958 |   97.709  |
|  2   | doc5960 |   90.914  |
|  3   | doc5943 |   73.943  |
+------+---------+-----------+
```


## How to use the trained model
### Installing our system

To clone the repository and install our system, run:

```
git clone https://github.com/EmilyCheoh/sml_final_project.git
cd DrQA; pip install -r requirements.txt; python setup.py develop
```

To Download a CoreNLP, run:

```
./install_corenlp.sh
```

Verify that it runs:

```
from drqa.tokenizers import CoreNLPTokenizer
tok = CoreNLPTokenizer()
tok.tokenize('hello world').words()  # Should complete immediately
```

IMPORTANT: The default tokenizer is CoreNLP so you will need that in your CLASSPATH to run the system.

```
Ex: export CLASSPATH=$CLASSPATH:/path/to/corenlp/download/*.
```

### Trained model and data
To download all provided trained models and data, first run:

```
./download.sh
```

Warning: this downloads a 7.5GB tarball (25GB untarred) and will take some time.

After that, please also download our dataset [here](https://drive.google.com/file/d/1a1wLzWiB4_gWPX0lZNQWBefm3oTM_t0T/view?usp=sharing), and move this file under the path data/ in order to run our model directly.

### Running the whole system
To interactively ask questions using our system, run:

```
python scripts/pipeline/interactive.py --retriever-model data/web/db-tfidf-ngram\=2-hash\=16777216-tokenizer\=simple.npz --doc-db data/web/db.db
```

Optional arguments:

```
--reader-model    Path to trained Document Reader model.
--retriever-model Path to Document Retriever model (tfidf).
--doc-db          Path to Document DB.
--tokenizer       String option specifying tokenizer type to use (e.g. 'corenlp').
--candidate-file  List of candidates to restrict predictions to, one candidate per line.
--no-cuda         Use CPU only.
--gpu             Specify GPU device id to use.
```

## Docker image
### Docker file
You can run our model with this docker file [here](https://github.com/EmilyCheoh/sml_final_project/blob/master/Dockerfile), but you still need to download our dataset [here](https://drive.google.com/file/d/1a1wLzWiB4_gWPX0lZNQWBefm3oTM_t0T/view?usp=sharing).

If it is not working, please go through the whole pipeline to run our model. Thank you.
