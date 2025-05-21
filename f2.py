import streamlit as st
import os, uuid, time

print("re rendering", time.strftime("%H:%M:%S"))
st.set_page_config(
    page_title="Open Sayries", 
    page_icon="📝",
    )

# -------- Side bar Note List ---------
def note_list():
    if not os.path.exists("notes"):
        os.mkdir("notes")    

    def f_(f_name):
        t = os.path.getmtime(f"notes/{f_name}")
        return t

    file_list = os.listdir('notes')
    file_list = sorted(file_list, key=f_, reverse=True)
    for file in file_list:
        with open(f'notes/{file}', 'r') as f:
            lines  = f.readlines()[:3]
        yield file, lines


if "selected_file" not in st.session_state:
    st.session_state.selected_file = str(uuid.uuid4())+'.txt'
if "selected_text" not in st.session_state:
    st.session_state.selected_text = ''

def save_text(inp):
    if len(inp) > 0 :
        with open(f"notes/{st.session_state.selected_file}", 'w') as f:
            f.write(inp)
    elif os.path.exists(f"notes/{st.session_state.selected_file}"):
        os.remove(f"notes/{st.session_state.selected_file}")

inp = st.text_area('Write Shyari Here...', height=400, value=st.session_state.selected_text)
st.button("save", "save", type="primary", use_container_width=True, on_click=save_text, args=(inp, ))

def handle_click(file):
    st.session_state.selected_file = file
    with open(f"notes/{file}", 'r') as fr:
        st.session_state.selected_text = fr.read()

def handle_new():
    st.session_state.selected_file = str(uuid.uuid4())+'.txt'
    st.session_state.selected_text = ''

def is_contain(text, file):
    with open(f"notes/{file}", 'r') as fs:
        if text in fs.read():
            return True
    return False

with st.sidebar:
    hc1, hc2 = st.columns([3,1])
    hc1.subheader("Shayries")
    hc2.button("New", key='new', on_click=handle_new, type='primary')
    search = st.text_input("search...")
    with st.container(height=350, border=False):
        for file, lines in note_list():
            if search and not is_contain(search, file):
                continue
            c1, c2 = st.columns([3,1])
            c1.html(f"<p>{'<br>'.join(lines)}</p>")
            click_ = c2.button("Open", key=file, on_click=handle_click, args=(file, ))