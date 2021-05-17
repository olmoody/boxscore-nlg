Data used in [Challenges in Data-to-Document Generation](https://arxiv.org/abs/1707.08052) (Wiseman, Shieber, Rush; EMNLP 2017).

# Model 1
Specific stats to text model. Input in the form of [Player 1, player 1 pts, Player 2, player 2 pts, Player 3, player 3 pts, Player 4, player 4 ast, Player 5, player 5 ast, Player 6, player 6 ast, Player 7, player 7 reb, Player 8, player 8 reb, Player 9, player 9 reb]


## Files
This project is made up of the following files:

* infoextract.py     - Reads each sentence in the training data (../train.json) and tries to find pairs of names and stats present in both the sentence and the box score. If found, this pair would be added to the correct dictionary (points, rebounds, assists). The dictionaries are then added to the beginning of the sentence. If any pair is found the sentence is written to tagged_summaries.txt. (This file can also be used on ../test.json to create tagged_test_summaries.txt)
* main.py     - Create and train model. Reads tagged_summaries.txt and creates sequences of 16 words that are split into 15 word input and a target word. The stats dictionaries are converted to a list and placed at the front of the input sequence. The model then goes through 50 training epochs with a batch size of 256. Saves model and tokenizer then attempts to use the model on a sample input.
* test.py     - Tests model by generating one sentence from sample input. Prints result.
* full-data-test.py     - Tests model more throughly by reading from tagged_test_summaries. Generates 500 sentences by randomly selecting sentence from tagged_test_summaries. Writes generated sentence and original input to results-stats.txt. Counts names and stats referenced in generated sentence and prints stats.
* tagged_summaries.txt     - Output of infoextract.py Input for main.py
* tagged_test_summaries.txt     - Output of infoextract.py Input for full-data-test.py
* results-stats.txt     - Output of full-data-test.py
* model.h5     - Saved binary of model
* tokenizer.pkl     - Saved binary of tokenizer
