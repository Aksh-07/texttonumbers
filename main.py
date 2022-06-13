import numpy as np
import sqlite3
import time
import io

st = time.time()


def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sqlite3.Binary(out.read())


def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out, allow_pickle=True)


#  When inserting data, the array Convert to text Insert
sqlite3.register_adapter(np.ndarray, adapt_array)

#  When querying data, the text Convert to array
sqlite3.register_converter("array", convert_array)


batch = [
    "My name is Aksh,",
    "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
    "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,",
    "when an unknown printer took a galley of type and scrambled it to make a type specimen book.",
    "It has survived not only five centuries, but also the leap into electronic typesetting,",
    "remaining essentially unchanged.",
    "My name is Aksh.",
    "It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,",
    "and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."
]


def convert_to_numbers(data):
    text_list = [t for t in data]
    batch_token_list = [t.split() for t in data]
    num_list = [[[ord(char) for char in token] for token in token_list] for token_list in batch_token_list]
    num_array_list = [np.array([items], dtype=object) for items in num_list]
    sum_array_list = [np.array([sum(single_word) for single_word in sentence], dtype=object) for sentence in num_list]
    return text_list, num_array_list, sum_array_list


def search(data):
    search_text, search_numbers, search_sum = convert_to_numbers([data])
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    c.execute("SELECT rowid, text FROM vectors WHERE numbers = ?", search_numbers)
    items = c.fetchall()
    for item in items:
        print(f"{item[0]}, {item[1]}")
    con.close()


def create_table():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("""CREATE TABLE vectors (
    text TEXT,
    numbers array,
    sum_of_words array
    )""")
    con.commit()
    con.close()


def delete_table():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("DROP TABLE vectors")
    con.commit()
    con.close()


def insert(t, n, s):
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.executemany("INSERT INTO vectors VALUES (?,?,?)", zip(t, n, s))
    con.commit()
    con.close()


def fetch():
    con = sqlite3.connect("vectorized.db", detect_types=sqlite3.PARSE_DECLTYPES)
    c = con.cursor()
    c.execute("SELECT rowid, text FROM vectors")
    items = c.fetchall()
    print(items)
    con.close()


delete_table()
create_table()
text, num, sum_ = convert_to_numbers(batch)
insert(text, num, sum_)
# fetch()
search("My name is Aksh.")

f = time.time()
print(f"total time: {f - st}")

