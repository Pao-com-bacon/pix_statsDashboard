#================================================================================================================================
# IMPORTING EXTRA PACKAGES
#================================================================================================================================

import requests

#================================================================================================================================
# REQUEST FUNCTION
#================================================================================================================================

def req_get (url, type, con_db):

    response = requests.get(url, stream=True)
    response.close() # this is necessary to close the connection and lower the local memory usage

    print("="*100)
    print(f"{type} RESPONSE")
    status = response.status_code
    print(status)

    if status == 200:
        print(f"Success on {type} requisition")
        print("="*100)
        print("\n")

        con_db.execute(f"""CREATE OR REPLACE TABLE raw_{type} AS 
                   SELECT unnest(value, recursive := true)
                   FROM read_json_auto($${url}$$)""")

    elif status == 400:
        print(f"Failure on {type} requisition.")
        print("="*100)
        print("\n")

        return None
    
    else:
        print(f"Consult the following link for more information:\n https://www.semrush.com/blog/http-status-codes/?g_network=g&g_campaign=BR_POR_SRCH_DSA_Blog_EN&g_acctid=888-874-7704&g_keyword=&g_keywordid=dsa-2185834088336&g_adtype=search&g_adid=676514000793&g_campaignid=18361973175&g_adgroupid=153796425585&kw=&cmp=BR_POR_SRCH_DSA_Blog_EN&label=dsa_pagefeed&Network=g&Device=c&utm_content=676514000793&kwid=dsa-2185834088336&cmpid=18361973175&agpid=153796425585&BU=Core&extid=279904347073&adpos=&matchtype=&gad_source=1&gad_campaignid=18361973175&gclid=EAIaIQobChMI-f_isaKQmAMVSUFIAB06NwkAEAAYASAAEgL_F_D_BwE")
        print("="*100)
        print("\n")

        return None

    return None

  