#### Page name w/ emoji for you to copy and paste
#### 🏡_Homepage.py



import streamlit as st
import ee
st.set_page_config(page_title = "Homepage")



# Sidebar title
cl1, cl2, cl3 = st.sidebar.columns([1,60,1])
st.markdown("""
<style>
.big-font {
    font-size:30px !important;
    text-align : center;
}
</style>
""", unsafe_allow_html=True)
with cl2:
    #st.markdown("<strong class='big-font'>EIGC22 & FoE:</strong>", unsafe_allow_html=True)
    st.markdown("<strong class='big-font'>Mapping the UK's Renewable Capacity</strong>", unsafe_allow_html=True)

c1, c2, c3 = st.sidebar.columns([1, 6, 1])
with c2:
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Friends_of_the_Earth_%28logo%29.svg/1200px-Friends_of_the_Earth_%28logo%29.svg.png", use_column_width=True)
    st.image("https://www.studiosity.com/hubfs/Exeter%20colour_logo.png", use_column_width = True)


# st.sidebar.image("https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Friends_of_the_Earth_%28logo%29.svg/1200px-Friends_of_the_Earth_%28logo%29.svg.png", width = 150)
# st.sidebar.image("https://www.studiosity.com/hubfs/Exeter%20colour_logo.png", width = 150)

with open("website and profiles/homepage markdown.txt") as f:
    md_body = f.readlines()
md_body = " ".join(md_body)

# Main body text etc
#welcome = "### Welcome to the home page for our project mapping the UK's solar and on-shore wind energy potential!"
st.markdown(md_body, unsafe_allow_html=False)

# subheader = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# st.markdown(subheader, unsafe_allow_html=False)

# whitespace = " "
# st.write(whitespace)

# links = """
# - Find the code for this project in our [Github repository](https://github.com/Josh-Redmond-UK/FoE_GC_Renewable_Energy). 
# - The documentation for the project can be found [here](https://docs.google.com/document/d/1gQbY1mPs2MjZjMS0_X15yEfpNTeCOegEoz4wCTuOxZ8/edit?usp=sharing).
# - Here's a third list item to check if unordered lists work.
# """
# st.markdown(links, unsafe_allow_html=False)