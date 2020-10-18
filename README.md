# Projects and having fun

### Installation

You will need:

- Latest version of Google Chrome.
- Python 3.
- A facebook account.

```bash
# Clone project:
> git clone https://github.com/Simokod/Projects-and-Having-Fun.git
> cd Projects-and-Having-Fun

# Set up a virtual env
> pip install virtualenv
> virtualenv venv

# Open venv:
# Linux:
> source venv/bin/activate
# Windows:
> venv\Scripts\activate.bat
  
# Install Python requirements
(venv) > pip install -e .
(venv) > pip install webdriver_manager
(venv) > pip install Flask
(venv) > pip install -U flask-cors

```

### How to Run
- Add profile urls you'd like to scrape in [input.txt](input.txt)
- Run Flask server - Run the `python server.py` command in the project folder.
- Open your browser on http://127.0.0.1:5000/ and scan your friends!

---
## Progress:
Currently the program can scrape only profiles, and extract posts.
"# FB_Profile_analyzer" 
