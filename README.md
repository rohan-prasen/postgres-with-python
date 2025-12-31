# Learning PostgreSQL with Python

Hey, I am learning how to use PostgreSQL with Python for backend development. Soon will implement integration with FastAPI.

```
# For those who prefer HTTPS
git clone https://github.com/rohan-prasen/postgres-with-python.git

# For those who prefer SSH
git clone git@github.com:rohan-prasen/postgres-with-python.git
```

```bash
# I used uv as my venv manager
uv init .
uv sync

# Normal python venv usage
# For windows users
python -m venv .venv
./.venv/Scripts/activate
pip install -r requirements.txt

# For macOS/Linux users
python3 -m venv .venv
source ./.venv/bin/activate
pip3 install -r requirements.txt
```

```bash
# To run any code sample
uv run main.py
```
