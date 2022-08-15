from peewee import SqliteDatabase
from werkzeug.security import check_password_hash, generate_password_hash

budget_db = SqliteDatabase("budget_db.db")
budget_db.connect()

username = "hichaza"
password = "haha20"

login_user = budget_db.execute_sql('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
check = check_password_hash(login_user[2], password)

print(check)
