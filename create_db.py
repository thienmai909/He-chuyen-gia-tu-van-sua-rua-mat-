import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import os

DB_PATH = os.path.join("data", "mypham.db")

class CosmeticManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý Sản phẩm Mỹ phẩm")
        self.root.geometry("1200x700")
        
        # Khởi tạo database nếu chưa có
        self.init_database()
        
        # Tạo giao diện
        self.create_widgets()
        
        # Load dữ liệu ban đầu
        self.load_data()
        
    def init_database(self):
        """Khởi tạo database nếu chưa tồn tại"""
        if not os.path.exists("data"):
            os.makedirs("data")
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT,
            origin TEXT,
            price TEXT,
            description TEXT,
            image_path TEXT
        )
        """)
        conn.commit()
        conn.close()
    
    def create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # Frame chính chia làm 2 phần: Trái (Form) và Phải (Danh sách)
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # === PHẦN TRÁI: FORM NHẬP LIỆU ===
        left_frame = tk.LabelFrame(main_frame, text="Thông tin sản phẩm", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # ID sản phẩm
        tk.Label(left_frame, text="Mã SP:").grid(row=0, column=0, sticky="w", pady=5)
        self.id_entry = tk.Entry(left_frame, width=40)
        self.id_entry.grid(row=0, column=1, pady=5, padx=5)
        
        # Tên sản phẩm
        tk.Label(left_frame, text="Tên SP:").grid(row=1, column=0, sticky="w", pady=5)
        self.name_entry = tk.Entry(left_frame, width=40)
        self.name_entry.grid(row=1, column=1, pady=5, padx=5)
        
        # Xuất xứ
        tk.Label(left_frame, text="Xuất xứ:").grid(row=2, column=0, sticky="w", pady=5)
        self.origin_entry = tk.Entry(left_frame, width=40)
        self.origin_entry.grid(row=2, column=1, pady=5, padx=5)
        
        # Giá
        tk.Label(left_frame, text="Giá:").grid(row=3, column=0, sticky="w", pady=5)
        self.price_entry = tk.Entry(left_frame, width=40)
        self.price_entry.grid(row=3, column=1, pady=5, padx=5)
        
        # Mô tả (Text widget với scrollbar)
        tk.Label(left_frame, text="Mô tả:").grid(row=4, column=0, sticky="nw", pady=5)
        desc_frame = tk.Frame(left_frame)
        desc_frame.grid(row=4, column=1, pady=5, padx=5, sticky="ew")
        
        self.desc_text = tk.Text(desc_frame, width=40, height=10, wrap=tk.WORD)
        desc_scrollbar = tk.Scrollbar(desc_frame, command=self.desc_text.yview)
        self.desc_text.config(yscrollcommand=desc_scrollbar.set)
        
        self.desc_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        desc_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Đường dẫn ảnh
        tk.Label(left_frame, text="Đường dẫn ảnh:").grid(row=5, column=0, sticky="w", pady=5)
        image_frame = tk.Frame(left_frame)
        image_frame.grid(row=5, column=1, pady=5, padx=5, sticky="ew")
        
        self.image_entry = tk.Entry(image_frame, width=30)
        self.image_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        tk.Button(image_frame, text="Chọn...", command=self.browse_image).pack(side=tk.LEFT, padx=(5, 0))
        
        # Các nút chức năng
        button_frame = tk.Frame(left_frame)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        tk.Button(button_frame, text="Thêm mới", bg="#4CAF50", fg="white", 
                 width=12, command=self.add_product).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cập nhật", bg="#2196F3", fg="white", 
                 width=12, command=self.update_product).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Xóa", bg="#f44336", fg="white", 
                 width=12, command=self.delete_product).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Làm mới", bg="#FF9800", fg="white", 
                 width=12, command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # === PHẦN PHẢI: DANH SÁCH SẢN PHẨM ===
        right_frame = tk.LabelFrame(main_frame, text="Danh sách sản phẩm", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Thanh tìm kiếm
        search_frame = tk.Frame(right_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(search_frame, text="Tìm kiếm:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_data())
        
        tk.Button(search_frame, text="Tải lại", command=self.load_data).pack(side=tk.LEFT)
        
        # Treeview để hiển thị danh sách
        tree_frame = tk.Frame(right_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars
        tree_scroll_y = tk.Scrollbar(tree_frame)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, 
                                 columns=("ID", "Tên", "Xuất xứ", "Giá"),
                                 show="headings",
                                 yscrollcommand=tree_scroll_y.set,
                                 xscrollcommand=tree_scroll_x.set)
        
        tree_scroll_y.config(command=self.tree.yview)
        tree_scroll_x.config(command=self.tree.xview)
        
        # Định nghĩa các cột
        self.tree.heading("ID", text="Mã SP")
        self.tree.heading("Tên", text="Tên sản phẩm")
        self.tree.heading("Xuất xứ", text="Xuất xứ")
        self.tree.heading("Giá", text="Giá")
        
        self.tree.column("ID", width=80)
        self.tree.column("Tên", width=250)
        self.tree.column("Xuất xứ", width=100)
        self.tree.column("Giá", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Sự kiện click vào một dòng
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)
        
        # Thông tin số lượng
        self.status_label = tk.Label(right_frame, text="Tổng: 0 sản phẩm", anchor="w")
        self.status_label.pack(fill=tk.X, pady=(5, 0))
    
    def browse_image(self):
        """Chọn file ảnh"""
        filename = filedialog.askopenfilename(
            title="Chọn ảnh sản phẩm",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All files", "*.*")]
        )
        if filename:
            self.image_entry.delete(0, tk.END)
            self.image_entry.insert(0, filename)
    
    def load_data(self):
        """Load dữ liệu từ database vào Treeview"""
        # Xóa dữ liệu cũ
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Lấy từ khóa tìm kiếm
        search_term = self.search_entry.get().strip().lower()
        
        # Truy vấn database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        if search_term:
            cursor.execute("""
            SELECT id, name, origin, price 
            FROM products 
            WHERE LOWER(id) LIKE ? OR LOWER(name) LIKE ? OR LOWER(origin) LIKE ?
            ORDER BY id
            """, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        else:
            cursor.execute("SELECT id, name, origin, price FROM products ORDER BY id")
        
        rows = cursor.fetchall()
        conn.close()
        
        # Thêm vào Treeview
        for row in rows:
            self.tree.insert("", tk.END, values=row)
        
        # Cập nhật status
        self.status_label.config(text=f"Tổng: {len(rows)} sản phẩm")
    
    def on_tree_select(self, event):
        """Khi click vào một sản phẩm trong danh sách"""
        selected = self.tree.selection()
        if not selected:
            return
        
        # Lấy ID của sản phẩm được chọn
        item = self.tree.item(selected[0])
        product_id = item['values'][0]
        
        # Load chi tiết sản phẩm
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if product:
            # Điền vào form
            self.clear_form()
            self.id_entry.insert(0, product[0])
            self.name_entry.insert(0, product[1])
            self.origin_entry.insert(0, product[2])
            self.price_entry.insert(0, product[3])
            self.desc_text.insert("1.0", product[4])
            self.image_entry.insert(0, product[5])
    
    def clear_form(self):
        """Xóa toàn bộ form"""
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.origin_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.image_entry.delete(0, tk.END)
    
    def add_product(self):
        """Thêm sản phẩm mới"""
        # Lấy dữ liệu từ form
        product_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        origin = self.origin_entry.get().strip()
        price = self.price_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        image_path = self.image_entry.get().strip()
        
        # Validate
        if not product_id or not name:
            messagebox.showerror("Lỗi", "Vui lòng nhập Mã SP và Tên SP!")
            return
        
        # Kiểm tra trùng ID
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM products WHERE id = ?", (product_id,))
        if cursor.fetchone():
            conn.close()
            messagebox.showerror("Lỗi", f"Mã sản phẩm '{product_id}' đã tồn tại!")
            return
        
        # Insert
        try:
            cursor.execute("""
            INSERT INTO products (id, name, origin, price, description, image_path)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (product_id, name, origin, price, description, image_path))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", "Đã thêm sản phẩm thành công!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            conn.close()
            messagebox.showerror("Lỗi", f"Không thể thêm sản phẩm: {str(e)}")
    
    def update_product(self):
        """Cập nhật sản phẩm"""
        product_id = self.id_entry.get().strip()
        
        if not product_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm cần cập nhật!")
            return
        
        name = self.name_entry.get().strip()
        origin = self.origin_entry.get().strip()
        price = self.price_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        image_path = self.image_entry.get().strip()
        
        if not name:
            messagebox.showerror("Lỗi", "Tên sản phẩm không được để trống!")
            return
        
        # Update
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE products 
            SET name = ?, origin = ?, price = ?, description = ?, image_path = ?
            WHERE id = ?
            """, (name, origin, price, description, image_path, product_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm thành công!")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {str(e)}")
    
    def delete_product(self):
        """Xóa sản phẩm"""
        product_id = self.id_entry.get().strip()
        
        if not product_id:
            messagebox.showerror("Lỗi", "Vui lòng chọn sản phẩm cần xóa!")
            return
        
        # Xác nhận
        confirm = messagebox.askyesno("Xác nhận", 
                                      f"Bạn có chắc muốn xóa sản phẩm '{product_id}'?")
        if not confirm:
            return
        
        # Delete
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Thành công", "Đã xóa sản phẩm thành công!")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xóa: {str(e)}")

def main():
    root = tk.Tk()
    app = CosmeticManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()