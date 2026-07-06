# Thay đoạn này:
feature_cols = ['pl_orbper', 'pl_radj', 'pl_bmasse', 'pl_orbincl', 'st_teff', 'st_logg']
X = df[feature_cols].copy()

# Thành đoạn này (tự động tìm cột gần đúng):
import re
def find_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name
    # Nếu không tìm thấy, thử tìm gần đúng
    for col in df.columns:
        for name in possible_names:
            if name.lower() in col.lower():
                return col
    return None

col_mapping = {
    'pl_orbper': ['pl_orbper', 'orbper', 'period'],
    'pl_radj': ['pl_radj', 'radj', 'radius'],
    'pl_bmasse': ['pl_bmasse', 'bmasse', 'mass'],
    'pl_orbincl': ['pl_orbincl', 'orbincl', 'inclination'],
    'st_teff': ['st_teff', 'teff', 'temp'],
    'st_logg': ['st_logg', 'logg']
}

X = pd.DataFrame()
for key, names in col_mapping.items():
    col = find_column(df, names)
    if col:
        X[key] = df[col]
    else:
        st.error(f"❌ Không tìm thấy cột cho '{key}'. Vui lòng kiểm tra file CSV.")
        st.stop()
