# Cấu trúc Key: (L, C, D, G, H, X) -> Value: Product_ID

RULE_MAP = {
    # Luật 1: Da dầu, Sạch sâu, Không xà phòng, 350-500k, Cerave, Mỹ -> S15
    ("L2", "C3", "D1", "G3", "H1", "X3"): "S15",

    # Luật 263:
    ("L4", "C5", "D7", "G1", "H7", "X2"): "S25",

    # Luật 2: Da khô, Dưỡng ẩm, Không hương liệu, 350-500k, Cerave, Mỹ -> S16
    ("L4", "C2", "D6", "G3", "H1", "X3"): "S16",

    # Luật 4: Da dầu, Giảm mụn, Không hương liệu, 150-350k, Simple, Anh -> S18
    ("L2", "C1", "D6", "G2", "H2", "X7"): "S18",
    
    # Luật 7: Da thường, Sạch sâu, Không cồn, Dưới 150k, Senka, Nhật -> S4
    ("L1", "C3", "D2", "G1", "H13", "X2"): "S4",

    # Luật 13: Da mụn, Giảm dầu mụn, Thuần chay, 150-350k, Cocoon, VN -> S23
    ("L6", "C1", "D3", "G2", "H5", "X4"): "S23",

    # Luật 19: Da dầu, Giảm mụn, Không xà phòng, 350-500k, La Roche-Posay, Pháp -> S24
    ("L2", "C1", "D1", "G3", "H6", "X1"): "S24",

    # Luật 22: Da khô, Dưỡng ẩm, Ngày đêm, Dưới 150k, Hada Labo, Nhật -> S25
    ("L4", "C2", "D7", "G1", "H7", "X2"): "S25",
    
    # ... Bạn tiếp tục thêm các luật còn lại vào đây ...
}

# Dữ liệu sản phẩm (Output Data) để hiển thị
PRODUCT_DB = {
    "S4":  {"name": "Senka Perfect Whip", "price": "80.000 - 150.000", "img": "senka_whip.png"},
    "S15": {"name": "CeraVe Foaming Cleanser", "price": "350.000 - 400.000", "img": "cerave_foaming.png"},
    "S16": {"name": "CeraVe Hydrating Cleanser", "price": "350.000 - 400.000", "img": "cerave_hydrating.png"},
    "S18": {"name": "Simple Cleanser Purify+", "price": "190.000 - 250.000", "img": "simple_purify.png"},
    "S23": {"name": "Gel Rửa Mặt Cocoon Bí Đao", "price": "140.000 - 180.000", "img": "cocoon_bi_dao.png"},
    "S24": {"name": "La Roche-Posay Effaclar Gel", "price": "~400.000", "img": "laroche_effaclar.png"},
    "S25": {"name": "Hada Labo Advanced Nourish", "price": "~60.000", "img": "hada_labo.png"},
}