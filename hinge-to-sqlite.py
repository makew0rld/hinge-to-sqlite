#!/usr/bin/env python3

import sqlite3
import sys
import json

db_file = sys.argv[1]
matches_file = sys.argv[2]


def dumps_or_none(v):
    if v is None:
        return None
    return json.dumps(v)


con = sqlite3.connect(db_file, isolation_level=None)
cur = con.cursor()

cur.execute("DROP TABLE IF EXISTS matches")
cur.execute(
    """
CREATE TABLE matches (
    timestamp TEXT NOT NULL,
    type TEXT NOT NULL,
    like_from TEXT,
    we_met_bool INTEGER NOT NULL,
    we_met TEXT,
    match TEXT,
    chats TEXT,
    like TEXT,
    block TEXT
)
"""
)
# Possible matches types:
# like, remove, match (I liked), match (they liked)
# (reports are ignored)
#
# So type field is one of: like,remove,match
# And like_from is one of: me,them
# indicating who sent the like.
#
# like_from is also set for the "like" and "remove" match types for easier querying.
#
# timestamp field is the earliest known timestamp of any event.
# So if I liked someone and then we matched, this is the like timestamp.
#
# we_met_bool is a boolean to simplify answering the question of whether we met.
#
# All other fields just contain JSON from objects from the matches.json file.
# The "match" field contains the "match" object for that person, etc.

with open(matches_file, "r") as f:
    matches = json.load(f)

print(f"Found {len(matches)} entries in matches.json")

for i, match in enumerate(matches):
    print(f"Processing entry {i}")

    # Collect data for each row field

    timestamp = None
    mtype = None
    like_from = None
    we_met_bool = False

    if "match" in match:
        assert len(match["match"]) == 1
        mtype = "match"

        if "like" in match:
            assert len(match["like"]) == 1
            like_from = "me"
            timestamp = match["like"][0]["timestamp"]
        else:
            like_from = "them"
            timestamp = match["match"][0]["timestamp"]

        if "we_met" in match:
            for evt in match["we_met"]:
                if evt["did_meet_subject"] == "Yes":
                    we_met_bool = True
                    break

    elif "like" in match:
        # Like but no match

        # Sometimes there can be multiple likes for one profile
        # So remove this assertion, and just consider the first like for the timestamp
        # assert len(match["like"]) == 1

        mtype = "like"
        timestamp = match["like"][0]["timestamp"]
        # For consistency
        like_from = "me"

    elif "block" in match:
        assert len(match["block"]) == 1
        if match["block"][0]["block_type"] == "remove":
            mtype = "remove"
            timestamp = match["block"][0]["timestamp"]
            # For consistency
            like_from = "them"
        elif match["block"][0]["block_type"] == "report":
            # Ignore
            continue
        else:
            print("Unknown entry type, aborting")
            sys.exit(1)

    else:
        print("Unknown entry type, aborting")
        sys.exit(1)

    # Insert data
    cur.execute(
        "INSERT INTO matches VALUES (?,?,?,?,?,?,?,?,?)",
        (
            timestamp,
            mtype,
            like_from,
            we_met_bool,
            dumps_or_none(match.get("we_met")),
            dumps_or_none(match.get("match")),
            dumps_or_none(match.get("chats")),
            dumps_or_none(match.get("like")),
            dumps_or_none(match.get("block")),
        ),
    )


cur.close()
con.close()
