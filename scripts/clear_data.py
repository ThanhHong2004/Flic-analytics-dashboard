from ketnoi_sql import engine
import sqlalchemy as sa

def clear_all():
    tables = ["Fact_KQNC", "Fact_KQCB", "Dim_ThiSinh", "Dim_LichThi", "Dim_Khoa", "Dim_KhoaHoc", "Dim_ChuongTrinh"]
    
    with engine.connect() as conn:
        print("Dang don dep kho du lieu")
        for table in tables:
            try:
                conn.execute(sa.text(f"DELETE FROM {table}"))
                conn.execute(sa.text(f"DBCC CHECKIDENT ('{table}', RESEED, 0)"))
                print(f"Da xoa du lieu bang: {table}")
            except Exception as e:
                print(f"Khong the xoa bang: {table}: {e}")
        conn.commit()

if __name__ == "__main__":
    clear_all()