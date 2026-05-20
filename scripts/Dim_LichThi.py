import pandas as pd
from ketnoi_sql import engine, file_path

try:
    sheets_diem = ['11-12.01_CB', '11-12.01_NC', '25-26.01_CB', '25-26.01_NC']
    list_dot_thi = []

    for s in sheets_diem:
        try:
            temp = pd.read_excel(file_path, sheet_name=s)
            temp.columns = temp.columns.str.replace('\n', ' ').str.strip()
            if 'ĐỢT THI' in temp.columns.upper():
                t_xl = temp.copy()
                t_xl.columns = [c.upper() for c in t_xl.columns]
                list_dot_thi.append(t_xl[['ĐỢT THI']]) 
        except:
            pass
    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    def lay_ngay_thi(ma_dot):
        ma_dot = str(ma_dot).strip()
        if '_' in ma_dot:
            try:
                phan_sau = ma_dot.split('_')[-1]
                phan_truoc = ma_dot.split('_')[0]
                nam_thi = "".join(filter(str.isdigit, phan_truoc))[-2:]
                ngay_thang = "".join([c for c in phan_sau if c.isdigit() or c == '.'])
                if '.' in ngay_thang:
                    return pd.to_datetime(f"{ngay_thang}.{nam_thi}", format='%d.%m.%y')
            except:
                pass
        return pd.NaT
    df_unique_dots = df_dmkh[['Lớp FLIC']].drop_duplicates().dropna()
    df_unique_dots.columns = ['MaDotThi']
    df_unique_dots['NgayThi'] = df_unique_dots['MaDotThi'].apply(lay_ngay_thi)
    def map_ten_dot(ma_dot):
        if '11.01' in str(ma_dot): return 'Đợt 1'
        if '25.01' in str(ma_dot): return 'Đợt 2'
        return 'N/A'

    df_unique_dots['TenDotThi'] = df_unique_dots['MaDotThi'].apply(map_ten_dot)
    df_final = df_unique_dots.dropna(subset=['NgayThi']).drop_duplicates()

    try:
        df_sql = pd.read_sql("SELECT MaDotThi, NgayThi, TenDotThi FROM Dim_LichThi", con=engine)
        df_sql['NgayThi'] = pd.to_datetime(df_sql['NgayThi'])
        df_new = pd.merge(df_final, df_sql, on=['MaDotThi', 'NgayThi', 'TenDotThi'], how='left', indicator=True)
        df_new = df_new[df_new['_merge'] == 'left_only'].drop(columns=['_merge'])
    except:
        df_new = df_final

    if not df_new.empty:
        df_new.to_sql('Dim_LichThi', con=engine, if_exists='append', index=False)
        print(f"Thành công: Đã nạp {len(df_new)} đợt thi mới dựa trên cấu trúc sheet điểm.")
    else:
        print("Không có đợt thi mới.")

except Exception as e:
    print('Lỗi: ', e)