Data used in [Challenges in Data-to-Document Generation](https://arxiv.org/abs/1707.08052) (Wiseman, Shieber, Rush; EMNLP 2017).

# Getting Started
Upon cloning this repository you should first extract the data as detailed in the parent directory: run `tar -jxvf rotowire.tar.bz2` to add data to rotowire/ directory. You can optionally create a virtual environment to run python scripts using "virtualenv venv" and "source  venv/bin/activate". Then run "pip install -r requirements.txt". If you run into the error of the tensorflow version not being available (I encountered on linux), you can comment out the first line of requirements.txt and run pip install tensorflow separately.

## Files and Directories
This project is made up of the following files and directories:

* model_1/     - Specific stats to text model. Input in the form of [Player 1, player 1 pts, Player 2, player 2 pts, Player 3, player 3 pts, Player 4, player 4 ast, Player 5, player 5 ast, Player 6, player 6 ast, Player 7, player 7 reb, Player 8, player 8 reb, Player 9, player 9 reb]
* model_2/     - Text-to-text model. No original input. Text tagged with generic values for names and stats. Captures essence of summaries then replaces tags with values.
* model_3/     - Full box score to text model. Input in form of lists of stats. Text tagged with generic values for names and stats with index.
* old_models/     - Back-up models. Out-of-date.
* old_tokenizers/     - Back-up tokenizers. Out-of-date.
* venv/     -Optional virtual environment. (Make yourself)
* requirements.txt      - Required python libraries.
