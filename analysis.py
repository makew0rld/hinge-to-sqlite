#!/usr/bin/env python3

import sqlite3
import sys
from datetime import datetime

con = sqlite3.connect(sys.argv[1], isolation_level=None)
cur = con.cursor()

res = cur.execute("SELECT COUNT(*) FROM matches")
print("Interactions:", res.fetchone()[0])

res = cur.execute("SELECT COUNT(*) FROM matches WHERE like_from = 'them'")
print("Likes received:", res.fetchone()[0])
res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE like_from = 'them' AND type = 'match'"
)
print("\tMatches:", res.fetchone()[0])
res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE like_from = 'them' AND type = 'remove'"
)
print("\tRemoved:", res.fetchone()[0])

res = cur.execute("SELECT COUNT(*) FROM matches WHERE like_from = 'me'")
print("Likes sent:", res.fetchone()[0])
res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE like_from = 'me' AND type = 'match'"
)
print("\tMatches:", res.fetchone()[0])
res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE like_from = 'me' AND type !='match'"
)
print("\tNo response:", res.fetchone()[0])

res = cur.execute("SELECT COUNT(*) FROM matches WHERE type = 'match'")
print("Total matches:", res.fetchone()[0])

res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE type = 'match' AND we_met_bool = TRUE"
)
print("\tDates:", res.fetchone()[0])

res = cur.execute("SELECT COUNT(*) FROM matches WHERE type = 'match' AND chats IS NULL")
print("\tNo chatting:", res.fetchone()[0])

res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE type = 'match' AND json_array_length(chats) = 1"
)
print("\tNo reply:", res.fetchone()[0])

# All non-met people, minus the previous queries (no chat, no reply)
res = cur.execute(
    "SELECT COUNT(*) FROM matches WHERE we_met_bool = FALSE AND type = 'match' and chats IS NOT NULL AND json_array_length(chats) != 1"
)
print("\tFizzled out:", res.fetchone()[0])

# Time span
# Example timestamp: "2023-05-10 03:06:14", sometime contains fractional seconds too
res = cur.execute("SELECT MIN(timestamp) FROM matches")
start = datetime.fromisoformat(res.fetchone()[0])
res = cur.execute("SELECT MAX(timestamp) FROM matches")
end = datetime.fromisoformat(res.fetchone()[0])
print(f"\nFirst activity: {start}\nLast activity:  {end}\nTime span: {end - start}")

cur.close()
con.close()
