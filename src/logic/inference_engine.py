import sqlite3
from src.logic.knowledge_base import RULE_MAP
from src.utils.resource_manager import get_db_path

class ExpertSystem:
    def __init__(self):
        # Đường dẫn đến database sử dụng resource manager
        self.db_path = get_db_path()
        self.rules = RULE_MAP

    def get_product_details(self, product_id):
        """Kết nối SQLite để lấy thông tin chi tiết sản phẩm"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, origin, price, description, image_path, product_link FROM products WHERE id = ?", (product_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return {
                "name": row[0],
                "origin": row[1],
                "price": row[2],
                "description": row[3],
                "image_path": row[4],
                "product_link": row[5],
            }
        return None

    def consult(self, inputs):
        """
        inputs: list hoặc tuple gồm [L, C, D, G, H, X]
        """
        # 1. Tra bảng luật để lấy ID sản phẩm (VD: "S15")
        query_key = tuple(inputs)
        product_id = self.rules.get(query_key)

        # 2. Nếu tìm thấy ID, vào Database lấy chi tiết
        if product_id:
            details = self.get_product_details(product_id)
            if details:
                details['id'] = product_id
                return details
        
        return None