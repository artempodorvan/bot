import sqlite3 as sq

def sign_up(name, password):
    db = sq.connect('Kesha_db.db')
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users
                (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)""")
    db.commit()

    cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", (name, password))
    db.commit()
    cur.execute("SELECT * FROM users")
    admins = cur.fetchall()

    if admins:
        admin_name = name
        admin_password = password
        if admin_name == 'Artem' and admin_password == '20090905':
            db.close()
            return 'U passed'
        else:
            db.close()
            return 'U did not'
    else:
        db.close()
        return 'U did not find any users'

def log_in(name1, password1):
    db = sq.connect('Kesha_db.db')
    cur = db.cursor()

    cur.execute("SELECT * FROM users")
    admins1 = cur.fetchall()

    if admins1:
        admin_name1 = name1
        admin_password1 = password1
        if admin_name1 == 'Artem' and admin_password1 == '20090905':
            db.close()
            return 'U passed'
        else:
            db.close()
            return 'U did not'
    else:
        db.close()
        return 'U did not find any users'

def users():
    db = sq.connect('Kesha_db.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()

    user_list = []

    if users:
        for user in users:
            username, user_password = user[1], user[2]
            user_list.append(f"Name: {username}, Password: {user_password}")

        return user_list
    else:
        return ['Database is empty']


def delete_user(username, password):
    db = sq.connect('Kesha_db.db')
    cur = db.cursor()

    cur.execute("DELETE FROM users WHERE username = ? AND password = ?", (username, password))
    db.commit()

    if cur.rowcount > 0:
        return f"User {username} with this password {password} was deleted from database"
    else:
        return f"this user {username} wasn't found by u with password {password} in database"

    db.close()
