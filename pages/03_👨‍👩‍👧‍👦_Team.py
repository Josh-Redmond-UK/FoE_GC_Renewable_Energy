import streamlit as st


st.markdown('''
### Meet our team:''')

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('josh-redmond-photo.jpg')
    with c2:
        st.markdown('''Josh Redmond: *"I am a PhD student at Exeter University studying the use of satellite images as forensics in Human Rights Cases within a participatory design framework"*''')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('arthur_vandervoort.jpeg')
    with c2:
        st.markdown('''Arthur Vandervoort: *"I'm a PhD student at the University of Exeter's CDT in Environmental Intelligence, researching the impact of gender on urban mobility patterns."*' ''')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('Ellie_Fox.jpg')
    with c2:
        st.markdown('Ellie Fox: *"I am a PhD student in Environmental Intelligence at the University of Exeter, researching how melting glaciers impact downstream communities."*')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('alice_lake.jpg')
    with c2:
        st.markdown('Alice Lake: *"I am a Foundation Scientist at the Met Office, working in the Post-processing Applications team."*')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('Danielle Waters.jpg')
    with c2:
        st.markdown('Danielle Waters: *"I work as a freelance hydrographic surveyor, primarily working within the offshore wind renewable sector."*')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('Matthew Hayslep.jpg')
    with c2:
        st.markdown('Matthew Hayslep: *"I am a PhD student at the University of Exeter, researching leakage in water distribution systems using machine learning."*')


with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.image('Rodrigo_Arce.png')
    with c2:
        st.markdown('Rodrigo Arce: *"I work at Google in the Google Cloud Platform team, giving support to clients who use data analysis products."*')

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        pass
    with c2:
        st.markdown('''Elizabeth Galloway: ''')
