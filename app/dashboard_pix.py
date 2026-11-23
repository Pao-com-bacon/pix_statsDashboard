import streamlit as st
import plotly.express as px
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


#st.dataframe(df_cad) --used to check if the pipeline is running okay. And it is
#st.dataframe(df_economic)
#st.dataframe(df_fraud)

#================================================================================================================================
# INITIAL SETTINGS OF THE APP AND PAGES DESIGN
#================================================================================================================================

pages_map = {
    0: "Registration Information",
    1: "Economic Information",
    2: "Frauds Information",
    3: "About Pix System",
}

pages = st.segmented_control("Dashboard Pages",
                             options = pages_map.keys(),
                             format_func = lambda page: pages_map[page],
                             selection_mode='single',
                             default=0)

#================================================================================================================================
# REGISTRATION INFORMATION PAGE
#================================================================================================================================

if pages == 0:
    #instrction about Registration
    pass

#================================================================================================================================
# ECONOMIC DATA PAGE
#================================================================================================================================

elif pages == 1:
    #instruction about economic
    pass

#================================================================================================================================
# FRAUDS INFORMATION PAGE
#================================================================================================================================

elif pages == 2:
    #instruction about frauds
    pass

#================================================================================================================================
# ABOUT PIX PAGE
#================================================================================================================================

elif pages == 3:
    #instruction about pix
    pass

else:
    st.info("You must select one of the pages above to visualize the data avaliable")



