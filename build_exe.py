"""
Script tự động build file .exe cho Hệ Chuyên Gia Tư Vấn Sữa Rửa Mặt
Sử dụng PyInstaller để đóng gói thành ONE-FILE executable
"""

import os
import subprocess
import sys
from pathlib import Path

def check_pyinstaller():
    """Kiểm tra PyInstaller đã cài đặt chưa"""
    try:
        import PyInstaller
        print("✅ PyInstaller đã được cài đặt.")
        return True
    except ImportError:
        print("❌ PyInstaller chưa được cài đặt.")
        print("Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ Đã cài đặt PyInstaller thành công!")
        return True

def build_exe():
    """Build file .exe"""
    base_dir = Path(__file__).parent
    
    print("\n" + "="*60)
    print("🚀 BẮT ĐẦU BUILD FILE THỰC THI")
    print("="*60 + "\n")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--name=SuaRuaMat",                    # Tên file exe
        "--onefile",                           # Đóng gói thành 1 file duy nhất
        "--windowed",                          # Không hiện console (GUI app)
        "--icon=assets/icons/logo.jpg",        # Icon cho exe
        
        # Thêm toàn bộ thư mục assets
        "--add-data=assets;assets",
        
        # Thêm database
        "--add-data=data;data",
        
        # Hidden imports (để PyInstaller biết import các module này)
        "--hidden-import=PySide6",
        "--hidden-import=PySide6.QtCore",
        "--hidden-import=PySide6.QtGui",
        "--hidden-import=PySide6.QtWidgets",
        "--hidden-import=sqlite3",
        
        # File entry point
        "main.py"
    ]
    
    print("📝 Lệnh build:")
    print(" ".join(cmd))
    print()
    
    # Chạy PyInstaller
    try:
        subprocess.check_call(cmd, cwd=base_dir)
        print("\n" + "="*60)
        print("✅ BUILD THÀNH CÔNG!")
        print("="*60)
        print(f"\n📂 File .exe nằm tại: {base_dir / 'dist' / 'SuaRuaMat.exe'}")
        print(f"📦 Kích thước: ~{get_file_size(base_dir / 'dist' / 'SuaRuaMat.exe')} MB")
        print("\n💡 Lưu ý:")
        print("   - Lần đầu chạy exe sẽ tự động tạo thư mục data/ và copy database")
        print("   - Có thể chỉnh sửa database bằng cách chạy create_db.py")
        print("   - Chia sẻ toàn bộ thư mục dist/ cho người dùng khác")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ LỖI KHI BUILD: {e}")
        sys.exit(1)

def get_file_size(file_path):
    """Lấy kích thước file theo MB"""
    try:
        size_bytes = file_path.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f}"
    except:
        return "?"

def main():
    print("🔧 CÔNG CỤ BUILD FILE THỰC THI - HỆ CHUYÊN GIA SỮA RỬA MẶT")
    print()
    
    # Bước 1: Kiểm tra PyInstaller
    check_pyinstaller()
    
    # Bước 2: Xác nhận build
    print("\n⚠️  Cảnh báo: Quá trình build có thể mất 1-3 phút.")
    confirm = input("Bạn có muốn tiếp tục? (y/n): ").lower()
    
    if confirm != 'y':
        print("Đã hủy build.")
        sys.exit(0)
    
    # Bước 3: Build
    build_exe()
    
    print("\n✨ Hoàn tất!")

if __name__ == "__main__":
    main()
