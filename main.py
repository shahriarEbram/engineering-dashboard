import code_validator
from code_validator import validate_code, decode_code
from generate_keys import staff_names, usernames
import streamlit_authenticator as stauth
from pathlib import Path
import streamlit as st
import pandas as pd
import jdatetime
import datetime
import pickle
import cons
import os

st.set_page_config(layout="wide")

# Load hashed passwords
file_path = Path(__file__).parent / "data/hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)
authenticator = stauth.Authenticate(staff_names, usernames, hashed_passwords,
                                    "eng_dash", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    # Ensure session state reset is done after successful logout
    if 'username' in st.session_state and st.session_state['username'] != username:
        st.session_state.clear()

    # Now assign the new username to session state
    st.session_state['username'] = username

    # Set unique session keys based on username
    df_key = f"df_{username}"
    visibility_key = f"visibility_{username}"
    disabled_key = f"disabled_{username}"

    # Logout button
    with st.sidebar:
        st.write(f"Welcome, {username}")
        authenticator.logout("Logout", "sidebar")

    # Continue with the rest of your application logic
    staff = cons.engineers_names.get(username)


    # st.write(f"Welcome, {username}")

    # *** Date Setting *** #
    def miladi_to_shamsi(date):
        return jdatetime.date.fromgregorian(date=date)


    today_shamsi = miladi_to_shamsi(jdatetime.datetime.now().togregorian())

    # *** Dataframe Setting *** #
    if df_key not in st.session_state:
        filename = f"data/{username}.csv"

        if not os.path.exists(filename):
            df = pd.DataFrame(columns=['person_name', 'task_name',
                                       'project_code', 'project_name',
                                       'date', 'duration',
                                       'project_description'])
            df.to_csv(filename, index=False)
        else:
            df = pd.read_csv(filename)

        df['task_name'] = df['task_name'].astype(pd.CategoricalDtype(cons.task_name.values()))
        st.session_state[df_key] = df

    # if visibility_key not in st.session_state:
    #     st.session_state[visibility_key] = "visible"
    #     st.session_state[disabled_key] = False
    with st.container(border=True):
        col1row1, col2row1, col3row1 = st.columns(3)
        with st.form("my_form", clear_on_submit=False,border=False):
            with col1row1:
                tasks = st.selectbox("Task:", (cons.task_name.values()))
                selected_index_of_tasks = list(cons.task_name.values()).index(tasks)

            with col2row1:
                disable_pcode = 25 <= selected_index_of_tasks <= 31
                if not disable_pcode:
                    pcode = st.text_input("Code:",
                                          max_chars=9,
                                          key=0,
                                          disabled=False
                                          )
                    pcode = pcode.upper()
                    if pcode and len(pcode) == 0 and not validate_code(pcode):
                        st.error("Invalid code format. Please ensure the code follows the correct format.")
                else:
                    pcode = st.text_input("Code:",
                                          max_chars=9,
                                          key=0,
                                          disabled=True,
                                          value="000000000"
                                          )

            with col3row1:
                duration = st.select_slider("Duration:", options=[i * 0.5 for i in range(1, 17)])

            with st.container(border=True):
                col1row0, col2row0, col3row0 = st.columns(3)
                with col1row0:
                    year = st.number_input('Year', min_value=1300, max_value=1500, value=today_shamsi.year, disabled=True)
                with col2row0:
                    month = st.number_input('Month', min_value=1, max_value=12, value=today_shamsi.month)
                with col3row0:
                    day = st.number_input('Day', min_value=1, max_value=31, value=today_shamsi.day)
            task_date = datetime.date(year, month, day)

            project_description = st.text_area('Enter Project Description', height=100)

            submitted = st.form_submit_button("Submit")
            if submitted:
                if len(pcode) < 9:
                    st.error("Project Code must be exactly 9 characters long.")
                elif not validate_code(pcode) and not disable_pcode:
                    st.error("Please check the errors first!")
                elif len(project_description) == 0:
                    st.error("Please enter a project description.")

                else:
                    new_row = {
                        'date': task_date,
                        'person_name': staff,
                        'project_code': pcode,
                        'project_name': decode_code(pcode),
                        'duration': duration,
                        'task_name': tasks,
                        'project_description': project_description,

                    }
                    st.session_state[df_key] = pd.concat([pd.DataFrame([new_row]), st.session_state[df_key]],
                                                         ignore_index=True)

                    st.toast("Submitted!")

    edited_df = st.data_editor(st.session_state[df_key],
                               use_container_width=True,
                               num_rows="dynamic",
                               hide_index=True,
                               disabled=["task_name", "project_code", "start_date", "person_name",
                                         "duration",
                                         "project_description"])

    # Save the updated DataFrame back to the session state and CSV file
    st.session_state[df_key] = edited_df
    filename = f"data/{username}.csv"
    edited_df.to_csv(filename, index=False)  # [st.session_state[df_key] = edited_df]
