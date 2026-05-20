import pandas as pd
from ketnoi_sql import engine, file_path
try:
    df_dmkh = pd.read_excel(file_path, sheet_name='DMKH')
    df_dmkh.columns = df_dmkh.columns.str.strip()
    df_dmkh['KeyMatch'] = df_dmkh['Họ và tên'].astype(str).str.upper().str.replace(" ", "")
    sheets_diem = ['11-12.01_CB', '25-26.01_CB', '11-12.01_NC', '25-26.01_NC']
    list_namsinh = []

    for s in sheets_diem:
        try:
            temp = pd.read_excel(file_path, sheet_name=s)
            temp.columns = temp.columns.str.replace('\n', ' ').str.strip()
            t_xl = temp[['HỌ VÀ TÊN', 'Ng/SINH']].copy()
            t_xl['KeyMatch'] = t_xl['HỌ VÀ TÊN'].astype(str).str.upper().str.replace(" ", "")
            t_xl['NamSinh'] = t_xl['Ng/SINH'].astype(str).str.strip().str[-4:]
            
            list_namsinh.append(t_xl[['KeyMatch', 'NamSinh']])
        except Exception as e:
            print(f"Bỏ qua sheet {s} do: {e}")
    df_lookup_namsinh = pd.concat(list_namsinh).drop_duplicates(subset=['KeyMatch'])
    df_gop = pd.merge(df_dmkh, df_lookup_namsinh, on='KeyMatch', how='left')
    
    def lay_khoa_hoc(dong):
        ten_lop = str(dong['Lớp']).strip()
        doi_tuong = str(dong['Đối tượng']).strip()
        nam_sinh = str(dong['NamSinh']).strip()
        
        if ten_lop != 'nan' and ten_lop != '' and len(ten_lop) >= 3:
            return ten_lop[0:3]
        if nam_sinh != 'nan' and nam_sinh != 'None' and len(nam_sinh) == 4 and nam_sinh.isdigit():
            if "Người đi làm" in doi_tuong:
                return f"NDL_{nam_sinh}"
            if "Sinh viên - UD" in doi_tuong:
                return f"UD_{nam_sinh}"
            return f"SVK_{nam_sinh}"
        return "Khác" 
    
    df_gop['KhoaHoc'] = df_gop.apply(lay_khoa_hoc, axis=1)
    df_dim_khoahoc = df_gop[['KhoaHoc']].drop_duplicates().reset_index(drop=True)

    df_dim_khoahoc.to_sql('Dim_KhoaHoc', con=engine, if_exists='append', index=False)
    print(f"Dim_KhoaHoc loaded successfully! Total categories: {len(df_dim_khoahoc)}")

except Exception as e:
    print("Errors:", e)