# Kaboom Import Scripts

Python scripts that can import comics/cartoons from external services such as TMDb and ComicVine.

## Setup

Before running any of the scripts make sure to run `pip install -r requirements/[service]_requirements.txt` depending on what service you are importing from.

Enter your API credentials into `var.example.py`. Rename it to `var.py` and move it to the `scripts` directory.

## Notes

Make sure to change the api urls and access tokens.

You will also need an API key from whatever service you are using (TMDb, ComicVine etc).

If you are importing to the live server, please be sure to check if the comic/cartoon already exists in the database.