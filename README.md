# Facebook Profile Analyzer

### Installation

You will need:

- Latest version of Google Chrome.
- Python 3.
- A facebook account.

```bash
# Clone project:
> git clone https://github.com/Simokod/Facebook-Profile-Analyzer.git
> cd Facebook-Profile-Analyzer

# Set up a virtual env:
> pip install virtualenv
> virtualenv venv

# Open venv:
# Linux:
> source venv/bin/activate
# Windows:
> venv\Scripts\activate.bat
  
# Install Python requirements:
(venv) > pip install -r requirements.txt
(venv) > pip install webdriver_manager

# Download nltk data:
(venv) > python
(venv) > import nltk
(venv) > nltk.download('vader_lexicon')

```

### How to Run
- Run the `python server.py` command in the project folder.
- Scrape away! - Open your browser at http://127.0.0.1:5000/ and start scraping and analyzing profiles
