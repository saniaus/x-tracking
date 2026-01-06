import sqlite3

conn = sqlite3.connect("tweets.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tweets (
    source TEXT,
    tweet_id TEXT,
    PRIMARY KEY (source, tweet_id)
)
""")
conn.commit()

def is_new(source, tweet_id):
    cur.execute(
        "SELECT 1 FROM tweets WHERE source=? AND tweet_id=?",
        (source, tweet_id)
    )
    if cur.fetchone():
        return False

    cur.execute(
        "INSERT INTO tweets VALUES (?,?)",
        (source, tweet_id)
    )
    conn.commit()
    return True
