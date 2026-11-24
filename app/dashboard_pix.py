import streamlit as st
import plotly.express as px
from pathlib import Path
import duckdb as db

#================================================================================================================================
# PAGE CONFIG & GLOBAL STYLES
#================================================================================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent
icon_asset = str(ROOT_DIR / "app" / "assets" / "pix_logo.svg")

st.set_page_config(
    page_title="Dashboard Pix",
    page_icon=icon_asset,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/Pao-com-bacon/pix_statsDashboard",
        "About": """
        ### Pix Stats: The Brazil eletronic payment system
        Dashboard about the principal statistics about the Pix

        **Source Code:** [Repositório no GitHub](https://github.com/Pao-com-bacon/pix_statsDashboard)
        **Data Source:** [Dados Abertos BCB](https://dadosabertos.bcb.gov.br/dataset/pix)
        **Dev by:** [João Pedro Lima (LinkedIn)](https://www.linkedin.com/in/joao-pedro-limads)
        """,
    },
)

col_logo, col_title = st.columns([0.06, 0.94], vertical_alignment="center")
with col_logo:
    st.image(icon_asset, width=55)
with col_title:
    st.title("Pix Stats Dashboard")

st.html("""
<style>
    /* Navegation buttons */
    [data-testid="stButtonGroup"] button {
        border-width: 2px !important;
    }

    /* Filters and SideBar */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-baseweb="base-input"],
    [data-testid="stSidebar"] button {
        border-width: 2px !important;
    }

    /* Cards */
    [data-testid="stVerticalBlockBorderWrapper"],
    [data-testid="stMetric"] {
        border-width: 2px !important;
    }
</style>
""")

#================================================================================================================================
# CONECTION TO THE DATABASE FUNCTION
#================================================================================================================================

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
# INITIAL SETTINGS OF THE APP
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

    with st.sidebar:

        st.logo(icon_asset, size='large')

        st.header("Pix Registration Filters")
        st.divider()

        person_radio = st.radio(
            "Chosse an type of people to see the evolution",
            ('All', 'Persons', 'Enterprises', 'Total')
        )

        avaliable_data = sorted(df_cad["reference_data_cad"].unique()) # get the distinct dates in the dataset of registration

        start_date, end_date = st.select_slider(
            "Select a range of data in the dataset",
            options=avaliable_data,
            value= (avaliable_data[0], avaliable_data[-1])
        )

        csv_cad = df_cad.to_csv(index=False).encode("utf-8") # get the dataset used to

        st.download_button(
            label="Download Registration Data (CSV)",
            data=csv_cad,
            file_name="pix_registration_data.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    df_filtered = (
        df_cad[df_cad["reference_data_cad"].between(start_date, end_date)]
        .sort_values("reference_data_cad")
        .reset_index(drop=True)
    )

    with st.sidebar:
        csv_cad = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Data (CSV)",
            data=csv_cad,
            file_name="pix_registration_data.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    def get_kpi_stats(series):
        current = int(series.iloc[-1])
        initial = int(series.iloc[0])
        pct_change = ((current - initial) / initial) * 100 if initial != 0 else 0.0
        return f"{current:,}", f"{pct_change:+.2f}%"

    total_val, total_delta = get_kpi_stats(df_filtered["qtdUsuariosCadastradosDICTTotal"])
    pf_val, pf_delta = get_kpi_stats(df_filtered["qtdUsuariosPessoaFisica"])
    pj_val, pj_delta = get_kpi_stats(df_filtered["qtdUsuariosPessoaJuridica"])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Registered Users",
            value=total_val,
            delta=total_delta,
            border=True,
            chart_data=df_filtered["qtdUsuariosCadastradosDICTTotal"],
            chart_type="area",
        )

    with col2:
        st.metric(
            label="Individuals",
            value=pf_val,
            delta=pf_delta,
            border=True,
            chart_data=df_filtered["qtdUsuariosPessoaFisica"],
            chart_type="area",
        )

    with col3:
        st.metric(
            label="Companies",
            value=pj_val,
            delta=pj_delta,
            border=True,
            chart_data=df_filtered["qtdUsuariosPessoaJuridica"],
            chart_type="area",
        )

    st.subheader("Evolution of Registered Pix Users")

    df_line = df_filtered.rename(columns={
        "qtdUsuariosPessoaFisica": "Persons",
        "qtdUsuariosPessoaJuridica": "Enterprises",
        "qtdUsuariosCadastradosDICTTotal": "Total",
    })

    categories = ["Enterprises", "Persons", "Total"]
    y_cols = categories if person_radio == "All" else [person_radio]

    fig_line = px.line(
        df_line,
        x="reference_data_cad",
        y=y_cols,
        markers=True,
        text="value",
        color_discrete_sequence=["#32BCAD", "#2E6D61", "#0F2E28"],
        labels={
            "reference_data_cad": "Reference Date",
            "value": "Registered Users",
            "variable": "User Type",
        },
    )

    for i, trace in enumerate(fig_line.data):
        trace.fill = "tozeroy" if i == 0 else "tonexty"

    fig_line.update_traces(
        textposition="top center",
        texttemplate="%{y:.3s}",
        cliponaxis=False,
    )

    st.plotly_chart(fig_line)
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



