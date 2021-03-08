import base64

import streamlit as st
import os
import pandas as pd
import pdfplumber
import numpy as np

# def file_selector(folder_path='.'):
#     filenames = os.listdir(folder_path)
#     selected_filename = st.selectbox('Select a file', filenames)
#     return os.path.join(folder_path, selected_filename)

st.title('PDF to Excel Converter')

uploaded_file = st.file_uploader("Upload Files",type=['pdf'])
if uploaded_file is not None:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    st.write(file_details)

# filename = file_selector()
# st.write('You selected `%s`' % filename)


try:
    pdffile=uploaded_file     #pdf檔路徑及檔名
    pdf = pdfplumber.open(pdffile)
    p = pdf.pages

    df_stack = []
    for i in range(len(p)):
        p_text = p[i].extract_text()
        table = p[i].extract_table()
        df = pd.DataFrame(table[1:], columns=table[0])
        df_clean = df.replace({r'\s+$': '', r'^\s+': ''}, regex=True).replace(r'\n',  ' ', regex=True)
        df_clean.columns = df.columns.str.replace('\n', '')
        df_stack.append(df_clean)
        
    df_concat = pd.concat(df_stack)
    st.write(df_concat)

    ragic_version = st.checkbox("CSV For Ragic版本")
    if ragic_version:
        column_names = ["材料編號", "材料名稱", "物料名稱(英)", "材料規範", "單位", "備           註", "分類", "主要來源", "品牌", "原廠型號", "原廠規格"]
        df_new = df_concat.reindex(columns=column_names)
        df_new_clean = df_new.replace(np.nan, '', regex=True)
        df_new_clean_column = df_new_clean.rename(columns={"材料名稱": "物料名稱(中)", "材料規範": "客戶規格", "備           註":"備註"})
        df_new_clean_column["分類"]  = "銷售商品"
        df_new_clean_column["主要來源"]  = "採購"
        st.write(df_new_clean_column)
        csv = df_new_clean_column.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
        href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
        st.markdown(href, unsafe_allow_html=True)
except AttributeError:
    st.write("選擇上傳公告")
