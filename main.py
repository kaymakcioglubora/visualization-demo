import argparse
import logging
import streamlit as st
import pandas as pd
import numpy as np
import time
from config.app_settings import ApplicationSettings
import config.db_config as db
import config.log_config as log
import plotly.express as px


parser = argparse.ArgumentParser()

parser.add_argument(
    "--env",
    default="default",
    help="default, dev, prod",
)
args = parser.parse_args()

env_file = f".env.{args.env}"
settings = ApplicationSettings(_env_file=env_file)

log.init_logging(settings)

_logger = logging.getLogger(__name__)
_logger.info(f"Loaded env variables from env={settings.ENVIRONMENT}")

client = db.init_db(settings)

st.set_page_config(page_title="Real-Time Chart", layout="wide")

st.title("Real-Time Network Chart Example")

chart_placeholder = st.empty()
chart_placeholder_2 = st.empty()
table_placeholder = st.empty()

df = pd.DataFrame(columns=["Time", "Value"])

for _ in range(100):
    new_time = pd.Timestamp.now().strftime("%H:%M:%S")
    new_value = np.random.randn() * 10 + 50
    new_row = pd.DataFrame({"Time": [new_time], "Value": [new_value]})
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.tail(100)

    fig = px.line(df, x="Time", y="Value", line_shape='spline')
    fig.update_traces(line=dict(color='crimson', width=3))

    chart_placeholder.plotly_chart(fig, use_container_width=True)
    chart_placeholder_2.line_chart(df.set_index("Time")["Value"])

    table_placeholder.dataframe(df)

    time.sleep(1)
