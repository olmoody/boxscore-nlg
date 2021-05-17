Data used in [Challenges in Data-to-Document Generation](https://arxiv.org/abs/1707.08052) (Wiseman, Shieber, Rush; EMNLP 2017).

# Model 3
Full box score to text model. Input in form of lists of stats. Text tagged with generic values for names and stats with index.


## Files
This project is made up of the following files:

* infoextract3.py     - Reads each sentence in the training data (../train.json) and tries to find pairs of names and stats present in both the sentence and the box score. If found, words are replaced with tags such as "*lastname{index}*" or "*rebval{index}*" where index is the index of the stat in its given list. The list of points, rebounds, assists, first names, and last names are then appended to the sentence. If any pair is found the sentence is written to tagged_summaries_noname_dicts.txt.
* main3.py     - Create and train model. Reads tagged_summaries_noname_dicts.txt and creates sequences of 16 words that are split into 15 word input and a target word. The stats lists are placed at the front of the input sequence. The model then goes through 50 training epochs with a batch size of 256. Saves model and tokenizer.
* test3.py     - Tests model by generating one sentence from sample input. Prints result.
* tagged_summaries_noname_dicts.txt     - Output of infoextract3.py Input for main3.py
* datafullmodel.h5     - Saved binary of model
* datatokenizer.pkl     - Saved binary of tokenizer
