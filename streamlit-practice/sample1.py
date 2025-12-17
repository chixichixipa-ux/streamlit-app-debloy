import streamlit as st
st.title("サンプルアプリ①：簡単なWebアプリ")
input_message = st.text_input(label="文字数のカウント対象となるテキストを入力してください")
Text_count = len(input_message)
if st.button("実行"):
    st.write(f"入力されたテキストの文字数は{Text_count}文字です")
