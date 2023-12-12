#these are the database tools
#note: search lib is kept in gui_libsearch.py
import sqlite3

#drops tables in existing DB for testing
def drop_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    # tables = cursor.fetchall()

    # Drop each table
    # for table in tables:
    #     table_name = table[0]
    #     cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    cursor.execute("DROP TABLE IF EXISTS alas")
    conn.commit()
    conn.close()
    

#alas_db is the ALAS database storing the main ID and details of the ALAS itself
def create_alas_db():
    conn = sqlite3.connect('alas.db')
    c = conn.cursor()
    # this is to init the various tables in the DB

    c.execute('''CREATE TABLE IF NOT EXISTS alas (
        id TEXT PRIMARY KEY UNIQUE,
        title TEXT,
        severity TEXT,
        component TEXT,
        cve TEXT,
        pubdate datetime,
        updated datetime,
        link TEXT
    )''')

    conn.commit()
    conn.close()
    print("ALAS Database created successfully")
    print("DB closed")

def write_to_alas_db(id, title, severity, component, cve, pubdate, updated, link):
    conn = sqlite3.connect('alas.db')
    c = conn.cursor()
    #reference: 
        # id TEXT PRIMARY KEY,
        # title TEXT,
        # severity TEXT,
        # component TEXT,
        # cve TEXT,
        # pubdate datetime,
        # updated datetime,
        # link TEXT
    c.execute("INSERT INTO alas VALUES (?,?,?,?,?,?,?,?)", (id, title, severity, component, cve, pubdate, updated, link))
    conn.commit()
    conn.close()
    # print("write_to_alas_db written")
    # print("DB closed")


#lib_db is the library database storing the library ID and details of the library
def create_lib_db():
    conn = sqlite3.connect('alas_lib.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS alas (
        head TEXT PRIMARY KEY UNIQUE,
        library TEXT,
        id TEXT
    )''')

    conn.commit()
    conn.close()
    print("Library Database created successfully")
    print("DB closed")

def write_to_lib_db(library, id):
    # print("db_tools write lib.py library and ID", library, id)

    conn = sqlite3.connect('alas_lib.db')
    c = conn.cursor()
    # reference
    #     library TEXT PRIMARY KEY,
    #     id TEXT SECONDARY KEY
    head = library + " " + id
    c.execute("INSERT INTO alas VALUES (?,?,?)", (head, library, id))
    conn.commit()
    conn.close()
    # print("Data written to DB")
    # print("DB closed")

def del_existing(db_name,id):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    #note, both alas and alas_lib use the same main table "alas"
    c.execute("DELETE FROM alas WHERE id=?", (id,))
    conn.commit()
    conn.close()
    print("Data deleted from DB:",db_name, id)

def search_library_by_id(search_id):
    connection = sqlite3.connect("alas.db")
    cursor = connection.cursor()
    cursor.execute("SELECT severity, component, cve, pubdate, updated, link FROM alas WHERE id=?", (search_id,))
    results = cursor.fetchall()
    connection.close()
    return results


def search_entries_by_component_and_date(component, date):
    connection = sqlite3.connect("alas.db")
    cursor = connection.cursor()

    # Use SQL query to find entries based on component and date
    # Assuming 'pubdate' is stored as a string in the format 'YYYY-MM-DD HH:MM:SS'
    cursor.execute("SELECT severity, substr(pubdate, 1, 10) FROM alas WHERE component=? AND substr(pubdate, 1, 10) > ?", (component, date))
    results = cursor.fetchall()
    connection.close()

    return results



def main():
    drop_db('alas.db')
    drop_db('alas_lib.db')
    print("dropped")
    create_alas_db()
    create_lib_db()
    pass



if __name__ == '__main__':
    main()
