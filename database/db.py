import sqlite3
from typing import List, Tuple

class Database:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row

    def get_menu(self) -> List[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM products").fetchall()
    
    def get_product_info(self, product_id) -> List[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    
    def get_promos(self) -> List[sqlite3.Row]:
        return self.conn.execute("SELECT * FROM products WHERE is_promo = 1").fetchall()

    def add_user(self, user_id: int, username: str, full_name: str):
        query = """
            INSERT OR IGNORE INTO users (user_id, username, full_name)
            VALUES (?, ?, ?)
        """
        self.conn.execute(query, (user_id, username, full_name,))
        self.conn.commit()

    def create_order(self, user_id: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO orders (user_id) VALUES (?)",
            (user_id,)
        )
        self.conn.commit()
        return cursor.lastrowid
    
    def add_order_item(self, order_id: int, product_id: int, quantity: int):
        self.conn.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, product_id, quantity)
        )
        self.conn.commit()
