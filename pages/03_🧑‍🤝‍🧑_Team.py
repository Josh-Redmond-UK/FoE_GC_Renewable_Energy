import streamlit as st
import random
st.set_page_config(page_title = "The Team")

st.markdown('''
### Meet our team:''')
def josh():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/josh-redmond-photo.jpg')
        with c2:
            st.markdown('''Josh Redmond: *"I am a PhD student at Exeter University studying the use of satellite images as forensics in Human Rights Cases within a participatory design framework"*''')

def arthur():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/arthur_vandervoort.jpeg')
        with c2:
            st.markdown('''Arthur Vandervoort: *"I'm a PhD student at the University of Exeter's CDT in Environmental Intelligence, researching the impact of gender on urban mobility patterns."*' ''')

def ellie():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/Ellie_Fox.jpg')
        with c2:
            st.markdown('Ellie Fox: *"I am a PhD student in Environmental Intelligence at the University of Exeter, researching how melting glaciers impact downstream communities."*')

def alice():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/alice_lake.jpg')
        with c2:
            st.markdown('Alice Lake: *"I am a Foundation Scientist at the Met Office, working in the Post-processing Applications team."*')

def danielle():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/Danielle Waters.jpg')
        with c2:
            st.markdown('Danielle Waters: *"I work as a freelance hydrographic surveyor, primarily working within the offshore wind renewable sector."*')

def matthew():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/Matthew Hayslep.jpg')
        with c2:
            st.markdown('Matthew Hayslep: *"I am a PhD student at the University of Exeter, researching leakage in water distribution systems using machine learning."*')

def rodrigo():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/Rodrigo_Arce.png')
        with c2:
            st.markdown('Rodrigo Arce: *"I work at Google in the Google Cloud Platform team, giving support to clients who use data analysis products."*')
def lizzy():
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            st.image('website and profiles/Final profile photos/Elizabeth_Galloway_Square.jpg')
        with c2:
            st.markdown('''Elizabeth Galloway: I am a PhD student in the Environmental Intelligence CDT at the University of Exeter, working on predicting the impacts of tropical cyclones.''')

team = [josh, arthur, danielle, alice, matthew, rodrigo, lizzy, ellie]

random.shuffle(team)

for i in team:
    i()
