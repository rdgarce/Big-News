from os import getenv
import streamlit as st

neo4j_uri = getenv("NEO4J_URI")
neo4j_user = getenv("NEO4J_USER")
neo4j_pass = getenv("NEO4J_PASSWORD")

if not neo4j_uri or not neo4j_user or not neo4j_pass:
    st.error("NEO4J Environment variables not defined")
    st.stop()