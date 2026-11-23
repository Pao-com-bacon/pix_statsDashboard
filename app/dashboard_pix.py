import streamlit as st
from pathlib import Path
import duckdb as db

#================================================================================================================================
# CONECTION TO THE DATABASE FUNCTION
#================================================================================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
db_path = str(ROOT_DIR / "pix.duckdb")

@st.cache_resource 
def get_connection(path_db): # conect the script into de db and returns the con of the db, using resource to set an global instance
    con = db.connect(path_db, read_only=True)

    return con

#================================================================================================================================
# TRANSFORMING VIEWS INTO DF FUCTION
#================================================================================================================================

@st.cache_data 
def load_view (_con, view): # load the views from an db and transform them into df. We are going to use the df's into filters and other things in streamlit
    #_con is the return of the last function above
    data = _con.execute(f"""SELECT *
                    FROM {view}""").df()
    return data

#================================================================================================================================
# IMPORTING DATASETS AND CHECKING IN STREAMLIT
#================================================================================================================================

pix_con = get_connection(db_path)

df_cad = load_view(pix_con, "vw_pix_cad")
df_economic = load_view(pix_con, "vw_pix_economic")
df_fraud = load_view(pix_con, "vw_pix_fraud")


st.dataframe(df_cad) # used to check if the pipeline is running okay. And it is
st.dataframe(df_economic)
st.dataframe(df_fraud)



