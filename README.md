# Learning PostgreSQL with Python

Hey, I am learning how to use PostgreSQL with Python for backend development. Soon will implement integration with FastAPI.

```bash
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

## Before running the code don't forget to create a `.env` file

```bash
cp .env.example .env
```

### Your .env file looks as follows

```env
host="your-host-name-here"
database="your-database-name-here"
user="your-username-here"
password="your-password-here"
port=your-port-number-here
```

Change all the environment variables in the code and then try to run the program uisng the below command

```bash
# To run any code sample
uv run main.py
```
