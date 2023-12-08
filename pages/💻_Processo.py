import streamlit as st
import tkinter as tk
from tkinter import filedialog
from models import SelectFilter
from models import Process

def get_root():
    root = tk.Tk()
    root.withdraw()
    root.wm_attributes('-topmost', 1)
    return root

st.markdown("# Processamento")

# Filtros
st.divider()

st.write("Selecionar os filtros")
checks = st.columns(4)

with checks[0]:
    st.session_state['filtro_h_f'] = st.checkbox('Horizontal Flip')
with checks[1]:
    st.session_state['filtro_v_f'] = st.checkbox('Vertical Flip')
with checks[2]:
    st.session_state['filtro_noise'] = st.checkbox('Noise')
with checks[3]:
    st.session_state['filtro_gray_scale'] = st.checkbox('Gray Scale')

st.divider()

st.write("Selecionar os paths")

paths = st.columns(2)

with paths[0]:
    clicked = st.button('Imagens Input', key="folder_1")

    if clicked:
        root = get_root()
        st.session_state['input'] = filedialog.askdirectory(master=root)
        
    
with paths[1]:
    clicked_2 = st.button('Imagens Output', key="folder_2")

    if clicked_2:
        root = get_root()
        st.session_state['output'] = filedialog.askdirectory(master=root)
        
if 'input' in st.session_state:
    st.text_input('Input selecionado: ', st.session_state.input, disabled=True)


if 'output' in st.session_state:
    st.text_input('Output selecionado: ', st.session_state.output, disabled=True)
        
st.divider()

button_right = st.columns(3)

processamento = False

with button_right[2]:
    
    disabled = False
    
    if 'input' not in st.session_state or st.session_state.input == '':
        disabled = True
    
    if 'output' not in st.session_state or st.session_state.output == '':
        disabled = True
    
    processamento = st.button(label="Iniciar processamento", key="process",  use_container_width=True, disabled=disabled)
    
if processamento:
    if st.session_state.input == st.session_state.output:
        st.error("Selecione pastas diferentes para o processamento.")
    else:
        select_filter = SelectFilter(st.session_state)
        process = Process(st.session_state.input, st.session_state.output, select_filter)
        try:
            process.init()
            
            st.info("Iniciando processamento para imagens de teste")
            process.save_test()
            st.success("Finalizado processamento para imagens de teste.")            
            
            st.info("Iniciando processamento para imagens de treinamento")
            process.save_treinament()
            st.success("Finalizado processamento para imagens de treinamento.")
            
            st.success("Processamento finalizado!")
        except Exception as e:
            st.error(e)
