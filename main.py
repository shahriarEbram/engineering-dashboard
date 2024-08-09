import streamlit as st
import pandas as pd
import cons
import jdatetime
import datetime
from code_validator import validate_code
import pickle
from pathlib import Path
import streamlit_authenticator as stauth
from generate_keys import staff_names, usernames

st.set_page_config(layout="wide")

# load hashed passwords
file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(staff_names, usernames, hashed_passwords,
                                    "eng_dash", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

col1row_1, col2row_1, col3row_1 = st.columns(3)
if authentication_status:
    staff = cons.engineers_names.get(username)

    with st.sidebar:
        st.write("welcome", username)
    authenticator.logout("Logout", "sidebar")


    # *** Date Setting *** #
    # Gregorian To Shamsi
    def miladi_to_shamsi(date):
        return jdatetime.date.fromgregorian(date=date)


    # Today date in Shamsi
    today_shamsi = miladi_to_shamsi(jdatetime.datetime.now().togregorian())
    # *** Date Setting *** #

    # *** Dataframe Setting *** #

    # Load the dataframe and store it in the session state if not already there
    if "df" not in st.session_state:
        df = pd.read_csv("test.csv")
        df['task_name'] = df['task_name'].astype(pd.CategoricalDtype(cons.task_name.values()))
        st.session_state.df = df

    # Store the initial value of widgets in session state
    if "visibility" not in st.session_state:
        st.session_state.visibility = "visible"
        st.session_state.disabled = False

    # *** Dataframe Setting *** #

    with st.form("my_form"):

        col1row1, col2row1, col3row1 = st.columns(3)
        with col1row1:
            # ****** Tasks SelectBox
            tasks = st.selectbox(
                "Task:",
                (cons.task_name.values()),
            )
            selected_index_of_tasks = list(cons.task_name.values()).index(tasks)


        with col2row1:
            # ****** Project Code
            pcode = st.text_input(
                "Code:",
                max_chars=9,
                key=0,
                label_visibility=st.session_state.visibility,
                disabled=st.session_state.disabled,
            )
            pcode = pcode.upper()
            # Display an error message if the input is invalid
            if pcode and not validate_code(pcode):
                st.error("Invalid code format. Please ensure the code follows this format:\n"
                         "- First character: D, C, F, G, M, T, V, Q, R\n"
                         "- Characters 2-5: Four digits\n"
                         "- Character 6: N or X\n"
                         "- Character 7: P, S, or R\n"
                         "- Characters 8-9: 01-99")
        with col3row1:

            duration = st.select_slider(
                "Duration:",
                options=[i * 0.5 for i in range(1, 17)]
            )

        # Date Container ********************************
        with st.container(border=True):
            col1row0, col2row0, col3row0 = st.columns(3)
            with col1row0:
                year = st.number_input('Year', min_value=1300, max_value=1500, value=today_shamsi.year, disabled=True)
            with col2row0:
                month = st.number_input('Month', min_value=1, max_value=12, value=today_shamsi.month)
            with col3row0:
                day = st.number_input('Day', min_value=1, max_value=31, value=today_shamsi.day)
        task_date = datetime.date(year, month, day)
        # Date Container ********************************


        project_description = st.text_area('Enter Project Description', height=100)


        submitted = st.form_submit_button("Submit")
        if submitted:
            if len(pcode) < 9:
                st.error("Project Code must be exactly 9 characters long.")
            else:
                new_row = {
                    'start_date': task_date,
                    'person_name': staff,
                    'project_code': pcode,
                    'duration': duration,
                    'task_name': tasks,
                    'project_description': project_description,

                }
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                st.write("Submitted!")

    edited_df = st.data_editor(st.session_state.df,
                               use_container_width=True,
                               num_rows="dynamic",
                               hide_index=True,
                               disabled=["person_name", "project_code"])

    edited_df.to_csv("test.csv", index=False)
