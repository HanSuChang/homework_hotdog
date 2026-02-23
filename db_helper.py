import pymysql

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '0000',
    'db': 'sampledb',
    'charset': 'utf8mb4'
}

class DB:
    def __init__(self, host, user, password, db, charset='utf8mb4'):
        self.conn = pymysql.connect(host=host, user=user, password=password, db=db, charset=charset)

    def verify_user(self, uid, pw):
        with self.conn.cursor() as cursor:
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            cursor.execute(sql, (uid, pw))
            return cursor.fetchone() is not None

    def fetch_hotdogs(self):
        with self.conn.cursor() as cursor:
            sql = "SELECT id, menu_name, price, stock, category, kcal FROM hotdogs"
            cursor.execute(sql)
            return cursor.fetchall()

    def insert_hotdog(self, name, price, stock, category, kcal):
        with self.conn.cursor() as cursor:
            sql = "INSERT INTO hotdogs (menu_name, price, stock, category, kcal) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (name, price, stock, category, kcal))
        self.conn.commit()

    def update_hotdog(self, hotdog_id, name, price, stock, category, kcal):
        with self.conn.cursor() as cursor:
            sql = "UPDATE hotdogs SET menu_name=%s, price=%s, stock=%s, category=%s, kcal=%s WHERE id=%s"
            cursor.execute(sql, (name, price, stock, category, kcal, hotdog_id))
        self.conn.commit()

    def delete_hotdog(self, hotdog_id):
        with self.conn.cursor() as cursor:
            sql = "DELETE FROM hotdogs WHERE id=%s"
            cursor.execute(sql, (hotdog_id,))
        self.conn.commit()

    def deduct_stock(self, menu_name, qty):
        with self.conn.cursor() as cursor:
            sql = "UPDATE hotdogs SET stock = stock - %s WHERE menu_name = %s"
            cursor.execute(sql, (qty, menu_name))
        self.conn.commit()