import pickle
from pathlib import Path

import streamlit_authenticator as stauth

staff_names = ["roohi", "heydari", "jamali", "seydi", "hassan_nejad", "sheykh", "shahriar"]
usernames = ["roohi", "heydari", "jamali", "seydi", "hassan_nejad", "sheykh", "shahriar"]
passwords = ["123", "123", "123", "123", "123", "123", "0"]

hashed_passwords = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "data/hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_passwords, file)
