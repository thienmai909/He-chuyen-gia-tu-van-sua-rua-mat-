"""
Resource Manager Module
Quản lý đường dẫn tài nguyên (resources) một cách tập trung và an toàn.
Đảm bảo đường dẫn luôn đúng bất kể working directory hoặc khi đóng gói với PyInstaller.
"""

import os
import sys
from pathlib import Path


def get_base_dir():
    """
    Lấy thư mục gốc của project.
    
    Returns:
        Path: Đối tượng Path trỏ đến thư mục gốc của project
        
    Note:
        - Khi chạy từ source code: trả về thư mục chứa main.py
        - Khi chạy từ PyInstaller executable: trả về thư mục tạm (_MEIPASS)
    """
    if getattr(sys, 'frozen', False):
        # Nếu chạy từ PyInstaller executable
        return Path(sys._MEIPASS)
    else:
        # Nếu chạy từ source code
        # __file__ là resource_manager.py -> parent là utils -> parent là src -> parent là project root
        return Path(__file__).parent.parent.parent


def get_resource_path(*paths):
    """
    Chuyển đổi đường dẫn tương đối thành đường dẫn tuyệt đối.
    
    Args:
        *paths: Các phần của đường dẫn (VD: "assets", "images", "logo.png")
        
    Returns:
        str: Đường dẫn tuyệt đối đến resource
        
    Examples:
        >>> get_resource_path("assets", "images", "logo.png")
        'd:\\project\\assets\\images\\logo.png'
        
        >>> get_resource_path("data", "mypham.db")
        'd:\\project\\data\\mypham.db'
    """
    base = get_base_dir()
    resource_path = base / Path(*paths)
    return str(resource_path)


def resource_exists(*paths):
    """
    Kiểm tra xem một resource có tồn tại hay không.
    
    Args:
        *paths: Các phần của đường dẫn
        
    Returns:
        bool: True nếu resource tồn tại, False nếu không
        
    Examples:
        >>> resource_exists("assets", "images", "logo.png")
        True
    """
    path = get_resource_path(*paths)
    return os.path.exists(path)


def get_db_path():
    """
    Lấy đường dẫn tuyệt đối đến database.
    
    Returns:
        str: Đường dẫn tuyệt đối đến file mypham.db
        
    Note:
        - Khi chạy từ source code: Lưu trong thư mục project/data/
        - Khi chạy từ exe (frozen): Lưu BÊN NGOÀI exe trong thư mục data/
          để có thể chỉnh sửa database sau khi build
        - Tự động copy database mẫu từ exe ra ngoài lần đầu chạy
    """
    if getattr(sys, 'frozen', False):
        # Khi chạy từ exe - lưu database BÊN NGOÀI exe (cùng thư mục với exe)
        base_dir = Path(sys.executable).parent
        data_dir = base_dir / "data"
        data_dir.mkdir(exist_ok=True)
        
        db_path = data_dir / "mypham.db"
        
        # Lần đầu chạy exe: Copy database mẫu từ bên trong exe ra ngoài
        if not db_path.exists():
            # Database được PyInstaller đóng gói vào _MEIPASS
            bundled_db = Path(sys._MEIPASS) / "data" / "mypham.db"
            if bundled_db.exists():
                import shutil
                print(f"Đang copy database mẫu ra ngoài...")
                shutil.copy(bundled_db, db_path)
                print(f"Đã tạo database tại: {db_path}")
            else:
                print(f"Cảnh báo: Không tìm thấy database mẫu trong exe!")
        
        return str(db_path)
    else:
        # Khi chạy từ source code - lưu trong thư mục project
        base_dir = get_base_dir()
        data_dir = base_dir / "data"
        
        # Tạo thư mục data nếu chưa tồn tại
        data_dir.mkdir(exist_ok=True)
        
        db_path = data_dir / "mypham.db"
        return str(db_path)


def validate_resource(resource_path, resource_name="Resource"):
    """
    Kiểm tra và validate một resource path.
    
    Args:
        resource_path (str): Đường dẫn đến resource
        resource_name (str): Tên của resource (để hiển thị trong error message)
        
    Returns:
        bool: True nếu resource hợp lệ
        
    Raises:
        FileNotFoundError: Nếu resource không tồn tại
        
    Examples:
        >>> validate_resource("/path/to/image.png", "Logo Image")
        True
    """
    if not os.path.exists(resource_path):
        raise FileNotFoundError(
            f"{resource_name} không tồn tại tại: {resource_path}"
        )
    return True


def get_asset_path(asset_type, filename):
    """
    Lấy đường dẫn đến asset theo loại.
    
    Args:
        asset_type (str): Loại asset ('images', 'icons', 'fonts')
        filename (str): Tên file
        
    Returns:
        str: Đường dẫn tuyệt đối đến asset
        
    Examples:
        >>> get_asset_path("images", "logo.png")
        'd:\\project\\assets\\images\\logo.png'
        
        >>> get_asset_path("fonts", "Nunito-ExtraBold.ttf")
        'd:\\project\\assets\\fonts\\Nunito-ExtraBold.ttf'
    """
    return get_resource_path("assets", asset_type, filename)
