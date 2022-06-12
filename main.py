import sqlite3
import time

s = time.time()
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
    batch_token_list = [text.split() for text in data]
    return [[[ord(char) for char in token] for token in token_list] for token_list in batch_token_list]


def convert_to_string(data):
    char_list = [[chr(n) for n in num_list] for num_list in data]
    words_list = ["".join(items) for items in char_list]
    return " ".join(words_list)


def search(data):
    search_list = convert_to_numbers([data])
    converted_data = []
    for items in search_list:
        converted_data.append(str(items))
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    c.execute("SELECT rowid, * FROM vectors WHERE vector = ?", converted_data)
    items = c.fetchall()
    for item in items:
        numbers_list = eval(item[1])
        string = convert_to_string(numbers_list)
        print(f"{item[0]}, {string}")
    con.close()


def create_table():
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    c.execute("""CREATE TABLE vectors (
    vector TEXT
    )""")
    con.commit()
    con.close()


def delete_table():
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    c.execute("DROP TABLE vectors")
    con.commit()
    con.close()


def insert(data):
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    converted_data = []
    for items in data:
        converted_data.append(str(items))
    c.executemany("INSERT INTO vectors VALUES (?)", zip(converted_data))
    con.commit()
    con.close()


def fetch():
    con = sqlite3.connect("vectorized.db")
    c = con.cursor()
    c.execute("SELECT rowid, * FROM vectors")
    items = c.fetchall()
    for item in items:
        numbers_list = eval(item[1])
        string = convert_to_string(numbers_list)
        print(string)

    con.close()


delete_table()
create_table()
num = convert_to_numbers(batch)
insert(num)
# fetch()
search("My name is Aksh.")

f = time.time()
print(f"total time: {f - s}")

