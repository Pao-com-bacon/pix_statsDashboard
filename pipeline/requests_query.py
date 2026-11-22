#================================================================================================================================
# IMPORTING EXTRA PACKAGES AND FUNCTIONS
#================================================================================================================================

import duckdb as db
from pathlib import Path
from src import req_get

#================================================================================================================================
# URL + ENDPOINT (BRAZIL CENTRAL BANK)
#================================================================================================================================

# info about the evolution of Pix users over the years
cad_url = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/PixUsuariosCadastradosDICT?%24format=json"

# info about the frauds occurred in the Pix system
frd_url = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/EstatisticasFraudesPix(Database=@Database)?%40Database='202501'&%24format=json"

# info about the type of transactions and users in the Pix system, like transactions between Person to Person, or Government to Person
cnae_url = "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/CnaePorteRecebedor(Database=@Database)?%40Database='202501'&%24format=json"

#================================================================================================================================
# DATABASE IN DUCKDB AND VIEWS
#================================================================================================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

db_path = str(ROOT_DIR / "pix.duckdb")
con = db.connect(db_path, config={'storage_compatibility_version': 'v1.4.0'}) # creation of a DuckDB database.
                                                                              # use the DuckDB extension to see the datasets

try: # if the extraction process fails, the database file is closed, even if an error in the API occurs
    cad_items = req_get(cad_url, "cadastre", con) # using the function in the src.py file for reading and storing data
    frd_items = req_get(frd_url, "frauds", con)
    cnae_items = req_get(cnae_url, "economic_activity", con)

    views_dir = ROOT_DIR / "views_query"
    vw_files = ["vw_pix_cad.sql", "vw_pix_fraud.sql", "vw_pix_economic.sql"]

    for file in vw_files: # execute the queries in SQL files to create the views used for data viz

        with open(views_dir / file, "r", encoding="utf-8") as f:
            con.execute(f.read())

finally:
    con.close()