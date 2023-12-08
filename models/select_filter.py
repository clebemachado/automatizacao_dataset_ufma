import streamlit as st

class SelectFilter:
    def __init__(self, session: st.session_state) -> None:
        self.horizontal = False
        self.vertical = False
        self.noise = False
        self.gray = False

        self.init_(session)
        
    def init_(self, session):
        
        if "filtro_h_f" in session:
            self.horizontal = session['filtro_h_f']
            
        if "filtro_v_f" in session:
            self.vertical = session['filtro_v_f']
            
        if "filtro_noise" in session:
            self.noise = session['filtro_noise']
            
        if "filtro_gray_scale" in session:
            self.gray = session['filtro_gray_scale']
            
        