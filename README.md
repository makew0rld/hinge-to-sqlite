# hinge-to-sqlite

This repo contains some Python scripts for doing analysis on your data export from Hinge.

The first script, `hinge-to-sqlite.py`, parses your Hinge match data and creates an SQLite database.
The second script, `analysis.py`, reads the SQLite database and outputs some basic statistics. You
can extend this script (or just use the `sqlite` CLI) to do further data analysis.

## Usage

```
python3 hinge-to-sqlite.py hinge.db matches.json
python3 analysis.py hinge.db
```

- `hinge.db` is the path to your SQLite database file, it doesn't have to exist yet
- `matches.json` is the path to your `matches.json` file from your Hinge export

## License

This code is licensed under the MIT license.
