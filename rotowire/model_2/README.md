Data used in [Challenges in Data-to-Document Generation](https://arxiv.org/abs/1707.08052) (Wiseman, Shieber, Rush; EMNLP 2017).

# Model 2
Text-to-text model. No original input. Text tagged with generic values for names and stats. Captures essence of summaries then replaces tags with values.


## Files
This project is made up of the following files:

* infoextract2.py     - Reads each sentence in the training data (../train.json) and tries to find pairs of names and stats present in both the sentence and the box score. If found, words are replaced with tags such as "*lastname*" or "*rebval*". If any pair is found the sentence is written to tagged_summaries_no_names.txt.
* main2.py     - Create and train model. Reads tagged_summaries_no_names.txt and creates sequences of 16 words that are split into 15 word input and a target word. The model then goes through 35 training epochs with a batch size of 1024. Saves model and tokenizer then attempts to use the model on a sample input.
* test2.py     - Tests model by generating one sentence from sample input. Prints result.
* full-test.py     - Tests model more throughly by reading from ../test.json. Generates sentences for each game in the test set. Tags are then replaced with values from game box score. Writes generated sentence to results.txt.
* tagged_summaries_no_names.txt     - Output of infoextract2.py Input for main2.py
* results.txt     - Output of full-test.py
* nonamemodel.h5     - Saved binary of model
* nonametokenizer.pkl     - Saved binary of tokenizer
