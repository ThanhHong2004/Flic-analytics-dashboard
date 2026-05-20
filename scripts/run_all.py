import subprocess
import time
import sys
import os
scripts = [
    "scripts/clear_data.py",
    "scripts/Dim_ThiSinh.py",
    "scripts/Dim_LichThi.py",
    "scripts/Dim_Khoa.py",
    "scripts/Dim_KhoaHoc.py",
    "scripts/Dim_ChuongTrinh.py",
    "scripts/Fact_KQCB.py",
    "scripts/Fact_KQNC.py"
]

def run_scripts():
    overall_start_time = time.time()
    print("BẮT ĐẦU QUÁ TRÌNH NẠP DỮ LIỆU TỔNG THỂ...")
    print("=" * 60)
    custom_env = os.environ.copy()
    custom_env["PYTHONIOENCODING"] = "utf-8"
    for script in scripts:
        script_start = time.time()
        print(f"Đang thực thi: {script}...")
        try:
            result = subprocess.run(
                [sys.executable, script], 
                capture_output=True, 
                text=True, 
                encoding='utf-8',
                env=custom_env
            )   
            if result.stdout:
                print(result.stdout.strip())
            if result.returncode == 0:
                duration = time.time() - script_start
                print(f"Thành công: {script} ({duration:.2f}s)")
                print("-" * 30)
            else:
                print(f"LỖI NGHIÊM TRỌNG tại file: {script}")
                print("Chi tiết lỗi hệ thống:")
                print(result.stderr)
                print("Dừng quá trình nạp để bảo vệ tính toàn vẹn dữ liệu!")
                return  
        except Exception as e:
            print(f"Không thể thực thi file {script}: {e}")
            return

    total_duration = time.time() - overall_start_time
    print("=" * 60)
    print(f"TẤT CẢ ĐÃ HOÀN TẤT! Tổng thời gian: {total_duration:.2f} giây.")
    print("Kiểm tra SQL Server để xác nhận số dòng đã nạp.")

if __name__ == "__main__":
    run_scripts()