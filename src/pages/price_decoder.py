import streamlit as st
import awesome_streamlit as ast

def write():
    code_lst = {"a":"1", "b":"2", "c":"3", "d":"4",\
        "e":"5", "f":"6", "g":"7", "h":"8", "i":"9", "j":"0"}

    code_input = st.text_input("輸入英文編碼: (英文小寫)")

    code_stack = []
    for code in code_input:
        if code in code_lst:
            code_stack += code_lst[code]
        else:
            st.write(f"{code} is not available. Try again.")

    result = "".join(code_stack)

    st.write("NT$ " + str(result))