import sys
from src.logic.constants import SKIN_TYPES, BENEFITS, FEATURES, PRICES, BRANDS, ORIGINS
from src.logic.knowledge_base import RULE_MAP, PRODUCT_DB

class ExpertSystemEngine:
    def __init__(self):
        self.rules = RULE_MAP
        self.products = PRODUCT_DB

    def consult(self, skin, benefit, feature, price, brand, origin):
        """
        Hàm suy luận: Nhận vào 6 mã (inputs) -> Trả về thông tin sản phẩm
        """
        # 1. Tạo khóa tìm kiếm (Tuple)
        query_key = (skin, benefit, feature, price, brand, origin)
        
        # 2. Tìm kiếm trong tập luật
        product_id = self.rules.get(query_key)

        if product_id:
            # 3. Nếu tìm thấy ID -> Lấy thông tin chi tiết
            product_info = self.products.get(product_id)
            return {
                "status": "SUCCESS",
                "id": product_id,
                "data": product_info,
                "key": query_key
            }
        else:
            return {
                "status": "FAIL",
                "id": None,
                "data": None,
                "key": query_key
            }

def get_input_from_user(label, options_dict):
    """
    Hàm hỗ trợ: Hiển thị danh sách tùy chọn và bắt buộc người dùng nhập đúng key
    """
    print(f"\n--- CHỌN {label.upper()} ---")
    # In ra danh sách các lựa chọn (VD: L1: Da thường, L2: Da dầu...)
    for key, value in options_dict.items():
        print(f"  [{key}]: {value}")
    
    while True:
        user_input = input(f"➤ Mời nhập mã (VD: {list(options_dict.keys())[0]}): ").strip().upper()
        if user_input in options_dict:
            return user_input
        else:
            print(f"❌ Mã '{user_input}' không hợp lệ. Vui lòng nhập lại.")

# --- PHẦN CHẠY TƯƠNG TÁC (INTERACTIVE TEST) ---
if __name__ == "__main__":
    engine = ExpertSystemEngine()

    print("=======================================================")
    print("   HỆ CHUYÊN GIA TƯ VẤN SỮA RỬA MẶT (CONSOLE MODE)")
    print("=======================================================")

    while True:
        try:
            # 1. Thu thập dữ liệu từ bàn phím
            l_input = get_input_from_user("Loại Da (L)", SKIN_TYPES)
            c_input = get_input_from_user("Công Dụng (C)", BENEFITS)
            d_input = get_input_from_user("Đặc Tính (D)", FEATURES)
            g_input = get_input_from_user("Khoảng Giá (G)", PRICES)
            h_input = get_input_from_user("Thương Hiệu (H)", BRANDS)
            x_input = get_input_from_user("Xuất Xứ (X)", ORIGINS)

            # 2. Gọi engine để suy luận
            print("\n" + "-"*40)
            print("ĐANG TRA CỨU DỮ LIỆU...")
            result = engine.consult(l_input, c_input, d_input, g_input, h_input, x_input)

            # 3. Hiển thị kết quả
            if result["status"] == "SUCCESS":
                p_data = result["data"]
                print(f"✅ TÌM THẤY SẢN PHẨM PHÙ HỢP!")
                print(f"   ► Mã SP:      {result['id']}")
                print(f"   ► Tên SP:     {p_data['name']}")
                print(f"   ► Giá:        {p_data['price']}")
                print(f"   ► Ảnh:        {p_data['img']}")
            else:
                print("❌ KHÔNG TÌM THẤY KẾT QUẢ.")
                print(f"   Lý do: Chưa có luật nào khớp với bộ tiêu chí: {result['key']}")
                print("   Gợi ý: Hãy kiểm tra lại file knowledge_base.py xem đã thêm luật này chưa.")

            # 4. Hỏi xem có muốn tiếp tục không
            print("-" * 40)
            cont = input("Bạn có muốn thử lại không? (y/n): ").lower()
            if cont != 'y':
                print("Cảm ơn bạn đã sử dụng chương trình!")
                break

        except KeyboardInterrupt:
            print("\nĐã thoát chương trình.")
            sys.exit()