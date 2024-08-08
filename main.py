import streamlit as st
import pandas as pd
import cons
import re
import streamlit.components.v1 as components

# Load the dataframe and store it in the session state if not already there
if "df" not in st.session_state:
    df = pd.read_csv("test.csv")
    st.session_state.df = df

# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False


# Define the validation function
def validate_code(code):
    # Regular expression pattern for the code format
    pattern = re.compile(
        r"^[DCFGRMTVQ](\d{4})(N|X)(P|S|R)(0[1-3])$"
    )
    # Check if the code matches the pattern
    return bool(pattern.match(code))


with st.form("my_form"):
    col1row1, col2row1, col3row1 = st.columns(3)
    with col1row1:
        # ****** Project Code
        pcode = st.text_input(
            "Code:",
            max_chars=9,
            key=0,
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled,
        )
        # Display an error message if the input is invalid
        if pcode and not validate_code(pcode):
            st.error("Invalid code format. Please ensure the code follows this format:\n"
                     "- First character: D, C, F, G, M, T, V, Q, R\n"
                     "- Characters 2-5: Four digits\n"
                     "- Character 6: N or X\n"
                     "- Character 7: P, S, or R\n"
                     "- Characters 8-9: 01, 02, or 03")

    with col2row1:
        # ****** Tasks SelectBox
        tasks = st.selectbox(
            "Task:",
            (cons.task_name.values()),
        )
        selected_index_of_tasks = list(cons.task_name.values()).index(tasks)
        st.write("You selected:", tasks, selected_index_of_tasks)

    with col3row1:
        # ****** Staff SelectBox
        staff = st.selectbox(
            "Name:",
            (cons.staff_names.values()),
        )
        selected_index_of_staff = list(cons.staff_names.values()).index(staff)
        st.write("You selected:", staff, selected_index_of_staff)

    col1row2, col2row2 = st.columns(2)
    with col1row2:
        project_description = st.text_area('Enter text', height=100)
        if project_description:
            st.write("You entered: ", project_description)

    with col2row2:
        duration = st.select_slider(
            "Duration:",
            options=[i * 0.5 for i in range(1, 17)]
        )
        st.write("Duration is", duration)

    submitted = st.form_submit_button("Submit")
    if submitted:
        if len(pcode) < 9:
            st.error("Project Code must be exactly 9 characters long.")
        else:
            new_row = {
                'pid': 0,
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
                           disabled=["person_name", "pid", "project_code"])

edited_df.to_csv("test.csv", index=False)

components.html(
    "<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>"
)

