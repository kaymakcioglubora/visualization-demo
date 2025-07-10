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
from codecarbon import OfflineEmissionsTracker

tracker = OfflineEmissionsTracker(country_iso_code="TUR", project_name="Plotting", measure_power_secs=10)
tracker.start_task("init_streamlit")

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

init_emissions = tracker.stop_task()
tracker.start_task("plot_values")

for i in range(100):
    new_time = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    new_value = np.random.randn() * 10 + 50
    new_row = pd.DataFrame({"Time": [new_time], "Value": [new_value]})
    df = pd.concat([df, new_row], ignore_index=True)
    df = df.tail(100)

    fig = px.line(df, x="Time", y="Value", line_shape='spline')
    fig.update_traces(line=dict(color='crimson', width=3))

    chart_placeholder.plotly_chart(fig, use_container_width=True)
    chart_placeholder_2.line_chart(df.set_index("Time")["Value"])

    table_placeholder.dataframe(df)

    time.sleep(0.1)

plot_emissions = tracker.stop_task()
tracker.stop()

print(f"\nCarbon emissions from computation: {tracker.final_emissions * 1000:.4f} g CO2eq")
print("\nDetailed emissions data:", tracker.final_emissions_data)
