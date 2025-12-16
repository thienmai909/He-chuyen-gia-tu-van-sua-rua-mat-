import sqlite3
import os

# Đường dẫn file database
DB_PATH = os.path.join("data", "mypham.db")

# Đảm bảo thư mục data tồn tại
if not os.path.exists("data"):
    os.makedirs("data")

def create_database():
    # 1. Kết nối (sẽ tự tạo file nếu chưa có)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 2. Tạo bảng products
    # id: Mã sản phẩm (S1, S2...) dùng để khớp với Logic
    # name: Tên hiển thị
    # price: Giá tiền (dạng chuỗi để hiển thị khoảng giá)
    # description: Công dụng/Mô tả
    # image_path: Đường dẫn ảnh (Bạn cần đổi tên ảnh thật khớp với cái này)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT,
        price TEXT,
        description TEXT,
        image_path TEXT
    )
    """)

    # 3. Dữ liệu chuẩn (Trích xuất từ tài liệu của bạn)
    products_data = [
        ("S1", "Caryophy Portulaca Cleansing Foam", "180.000 - 230.000", 
         "Chiết xuất rau má, rau sam. Kháng khuẩn, giảm viêm mụn, mờ thâm, ngừa lão hóa.", "assets/images/s1.png"),
         
        ("S2", "Tia'm Snail & Azulene Low pH Cleanser", "150.000 - 250.000", 
         "pH 5.5 dịu nhẹ, chiết xuất ốc sên & hoa cúc. Làm dịu đỏ rát, bảo vệ hàng rào ẩm.", "assets/images/s2.png"),
         
        ("S3", "Pond's Age Miracle", "100.000 - 200.000", 
         "Chứa Retinol-C và Niacinamide. Mờ đốm nâu, giảm nếp nhăn, tái tạo tế bào, chống lão hóa.", "assets/images/s3.png"),
         
        ("S4", "Senka Perfect Whip (Xanh)", "80.000 - 150.000", 
         "Bọt tơ tằm trắng siêu dày. Làm sạch sâu bụi mịn PM2.5, giữ ẩm với Aqua In Pool.", "assets/images/s4.png"),
         
        ("S5", "Senka Perfect Whip Acne Care", "80.000 - 150.000", 
         "Chứa BHA và hoa cúc Kyoto. Chuyên giảm mụn, kháng viêm, kiểm soát nhờn.", "assets/images/s5.png"),
         
        ("S6", "Senka Perfect Whip Collagen In", "80.000 - 150.000", 
         "Bổ sung Collagen và 60% tinh chất dưỡng. Giúp da săn chắc, đàn hồi, mờ nhăn.", "assets/images/s6.png"),
         
        ("S7", "Senka Perfect Whip Low pH Calming Cica", "80.000 - 150.000", 
         "pH thấp, chứa Rau má & Đậu nành. Cực kỳ dịu nhẹ cho da nhạy cảm, kích ứng.", "assets/images/s7.png"),
         
        ("S8", "Acnes Oil Control Cleanser", "40.000 - 80.000", 
         "Gel rửa mặt kiểm soát nhờn. Chứa hạt siêu mịn, AHA, Zinc PCA, Niacinamide.", "assets/images/s8.png"),
         
        ("S9", "Klairs Gentle Black Facial Cleanser", "100.000 - 500.000", 
         "Phức hợp đen (đậu đen, nấm truffle). pH 5.5, làm sạch 99.9% bụi mịn, cấp ẩm sâu.", "assets/images/s9.png"),
         
        ("S10", "Nivea Pearl Bright", "50.000 - 100.000", 
         "Tinh chất ngọc trai và 4-Butylresorcinol. Dưỡng sáng gấp 10 lần Vitamin C, mờ thâm.", "assets/images/s10.png"),
         
        ("S11", "Nivea Anti-Acne", "50.000 - 100.000", 
         "Chiết xuất vỏ cây mộc lan. Giảm khuẩn mụn gấp 10 lần, kiểm soát nhờn hiệu quả.", "assets/images/s11.png"),
         
        ("S12", "Garnier Bright Complete 3-in-1 Anti Acne", "50.000 - 120.000", 
         "Kết hợp Salicylic Acid và Vitamin C. Giảm mụn, mờ thâm, sáng da.", "assets/images/s12.png"),
         
        ("S13", "Vichy Normaderm Phytosolution", "~ 510.000", 
         "Dược mỹ phẩm Pháp. Chứa Salicylic Acid, Zinc Oxide, Probiotic. Chuyên trị mụn, se khít lỗ chân lông.", "assets/images/s13.png"),
         
        ("S14", "Obagi Nu-Derm Gentle Cleanser", "200.000 - 500.000", 
         "Dòng cao cấp. Chứa Acid Amin yến mạch, Lô hội. Làm sạch dịu nhẹ cho da khô, lão hóa.", "assets/images/s14.png"),
         
        ("S15", "CeraVe Foaming Cleanser", "~350.000 - 400.000", 
         "Dạng Gel tạo bọt cho da dầu. Chứa 3 loại Ceramides, Niacinamide, HA. Phục hồi màng da.", "assets/images/s15.png"),
         
        ("S16", "CeraVe Hydrating Cleanser", "~350.000 - 400.000", 
         "Dạng kem không tạo bọt cho da khô. Cấp ẩm chuyên sâu, không gây khô căng.", "assets/images/s16.png"),
         
        ("S17", "CeraVe SA Smoothing Cleanser", "~350.000 - 400.000", 
         "Chứa Salicylic Acid (BHA). Làm mịn da sần sùi, giảm mụn ẩn, tẩy tế bào chết nhẹ.", "assets/images/s17.png"),
         
        ("S18", "Simple Cleanser Purify+", "~190.000 - 250.000", 
         "Chiết xuất cây phỉ, Zinc, PHA. Kiểm soát dầu, giảm mụn, thông thoáng lỗ chân lông.", "assets/images/s18.png"),
         
        ("S19", "Simple Cleanser Repair+", "~190.000 - 250.000", 
         "Chứa Pro-Ceramides & HA. Phục hồi da tổn thương, làm dịu da nhạy cảm.", "assets/images/s19.png"),
         
        ("S20", "Simple Cleanser Hydrate+", "~190.000 - 250.000", 
         "Công nghệ Micellar & Glycerin thuần chay. Cấp ẩm sâu cho da khô thiếu nước.", "assets/images/s20.png"),
         
        ("S21", "Cetaphil Gentle Skin Cleanser", "~125.000 - 550.000", 
         "Huyền thoại dịu nhẹ. Không xà phòng, không hương liệu. An toàn tuyệt đối cho da nhạy cảm.", "assets/images/s21.png"),
         
        ("S22", "SVR Sebiaclear Gel Moussant", "~300.000 - 400.000", 
         "Chứa Gluconolactone & Salicylic Acid. Giảm mụn, giảm thâm, không chứa xà phòng.", "assets/images/s22.png"),
         
        ("S23", "Cocoon Bí Đao", "~140.000 - 180.000", 
         "Thương hiệu Việt Nam. Bí đao, rau má, tràm trà. Giảm dầu, giảm mụn ẩn, thuần chay.", "assets/images/s23.png"),
         
        ("S24", "La Roche-Posay Effaclar Gel", "~400.000", 
         "Gel tạo bọt cho da dầu nhạy cảm. Nước khoáng La Roche-Posay + Zinc PCA. Kiềm dầu, giảm kích ứng.", "assets/images/s24.png"),
         
        ("S25", "Hada Labo Advanced Nourish", "~60.000", 
         "Hệ dưỡng ẩm HA, SHA, Nano HA. Cấp ẩm sâu 36h, giúp da mềm mượt.", "assets/images/s25.png"),
         
        ("S26", "Eucerin ProAcne Solution", "~200.000 - 450.000", 
         "Chứa 6% Ampho-Tensides. Ngừa khuẩn mụn, làm sạch sâu cho da nhờn mụn.", "assets/images/s26.png"),
         
        ("S27", "L'Oréal Revitalift HA Gel", "130.000", 
         "Chứa Hyaluronic Acid. Làm sạch, cấp ẩm, giúp da căng mọng, giảm nếp nhăn.", "assets/images/s27.png"),
         
        ("S28", "Bioderma Sébium Gel Moussant", "~100.000 - 400.000", 
         "Phức hợp D.A.F, Kẽm, Đồng. Kiểm soát bã nhờn, thanh lọc da, không gây khô căng.", "assets/images/s28.png"),
    ]

    # 4. Thực hiện Insert (Dùng INSERT OR REPLACE để chạy lại không bị lỗi trùng lặp)
    cursor.executemany("""
    INSERT OR REPLACE INTO products (id, name, price, description, image_path)
    VALUES (?, ?, ?, ?, ?)
    """, products_data)

    conn.commit()
    conn.close()
    print(">>> Đã khởi tạo Database thành công tại: data/mypham.db")
    print(f">>> Đã thêm {len(products_data)} sản phẩm.")

if __name__ == "__main__":
    create_database()