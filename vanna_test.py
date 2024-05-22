import vanna
import pandas as pd
import mysql.connector
from vanna.remote import VannaDefault


def run_sql(sql: str) -> pd.DataFrame:
    cnx = mysql.connector.connect(user='root',password='',host='localhost',database='TTS')
    cursor = cnx.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    columns = cursor.column_names
    df = pd.DataFrame(result, columns=columns)
    return df


api_key = 'ff271480a5114f0493b7706fe1010ba1'
vanna_model_name = 'tts'
vn = VannaDefault(model=vanna_model_name, api_key=api_key)
vn.run_sql = run_sql
vn.run_sql_is_set = True

vn.train(question='统计不同民族数量？', sql='SELECT nation, COUNT(*) as count FROM customer GROUP BY nation ORDER BY count DESC;')

vn.ask('统计不同民族数量？')

from vanna.flask import VannaFlaskApp
app = VannaFlaskApp(vn, allow_llm_to_see_data=True)
app.run()
