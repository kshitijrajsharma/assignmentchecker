import os
import shutil
import subprocess

import streamlit as st
from git import Repo

st.title("Assignment Checker")
st.write(
    "This application checks assignments using Otter Grader. Source GitHub must be set up accordingly to how Otter Grader works with tests."
)

github_url = st.text_input("Enter source GitHub URL:")
uploaded_file = st.file_uploader("Upload the Python file to be checked:", type=["py"])

if github_url:
    st.write(f"GitHub URL: {github_url}")

if st.button("Check Assignment"):
    if github_url and uploaded_file:
        with st.spinner("Cloning repository and checking assignment..."):
            repo_dir = "/tmp/repo"
            if os.path.exists(repo_dir):
                shutil.rmtree(repo_dir)
            Repo.clone_from(github_url, repo_dir)

            os.chdir(repo_dir)

            requirements_path = os.path.join(repo_dir, "requirements.txt")
            # if os.path.exists(requirements_path):
            #     subprocess.run(["pip", "install", "-r", requirements_path])

            uploaded_file_path = os.path.join(repo_dir, uploaded_file.name)
            with open(uploaded_file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            result = subprocess.run(
                ["otter", "check", uploaded_file_path], capture_output=True, text=True
            )

        st.success("Assignment check completed!")
        st.text(result.stdout)
        st.text(result.stderr)
    else:
        st.error("Please provide both a GitHub URL and a Python file.")
