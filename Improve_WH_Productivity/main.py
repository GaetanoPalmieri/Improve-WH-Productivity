import pandas as pd
import numpy as np

from simulation_batch import (simulate_batch)
from simulation_cluster import (simulation_cluster)
from plot import (plot_simulation1, plot_simulation2)
import streamlit as st

# Set page di config
st.set_page_config(page_title="Improve Warehouse Productivity using Order Batching",initial_sidebar_state="expanded",layout='wide')

# Set up page
@st.cache(persist=False,allow_output_mutation=True,suppress_st_warning=True,show_spinner=True)

# Preparazione dei dati
def load(filename, n):
    df_orderlines = pd.read_csv(IN + filename).head(n)
    return df_orderlines

# Allineo le coordinate su y-axis
y_low, y_high = 5.5, 50

# Location di origine
origin_loc = [0, y_low]

# Distanza di Threshold (m)
distance_threshold = 35
distance_list = [1] + [i for i in range(5, 100, 5)]
IN = 'static/in/'

# Conservo i risultati per WaveID
list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]  # Group in list

# Conservo i risultati per la Simulation (Order_number)
list_ordnum, list_dstw = [], []

# Simulation 1: Order Batch

st.header("**Impatto della wave size negli ordini (Orders/Wave)**")
st.subheader(''' Quante Orders Lines vuoi includere nella tua analisi? ''')
col1, col2 = st.columns(2)
with col1:
    n = st.slider(
        'SIMULATION 1 (1000 ORDERS)', 1, 200, value=5)
with col2:
    lines_number = 1000 * n
    st.write('''{:,} \
        order lines'''.format(lines_number))

# SIMULATION PARAMETERS
st.subheader('''SIMULO ORDER PICKING BY WAVE PER N ORDERS PER WAVE CON N IN [N_MIN, N_MAX] ''')
col_11, col_22 = st.columns(2)

with col_11:
    n1 = st.slider(
        'SIMULATION 1: N_MIN (ORDERS/WAVE)', 0, 20, value=1)
    n2 = st.slider(
        'SIMULATION 1: N_MAX (ORDERS/WAVE)', n1 + 1, 20, value=int(np.max([n1 + 1, 10])))
with col_22:
    st.write('''[N_MIN, N_MAX] = [{:,}, {:,}]'''.format(n1, n2))

# START
start_1 = False
if st.checkbox('SIMULATION 1: START', key='show', value=False):
    start_1 = True

# Calcolo
if start_1:
    df_orderlines = load('df_lines.csv', lines_number)
    df_waves, df_results = simulate_batch(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines)
    plot_simulation1(df_results, lines_number)

# Simulation 2: Order Batch using Spatial Clustering
st.header("**Impatto del metodo di order batching**")
st.subheader('''Quante Orders Lines vuoi includere nella tua analisi?''')
col1, col2 = st.columns(2)
with col1:
    n_ = st.slider( s   w
        'SIMULATION 2 (1000 ORDERS)', 1, 200, value=5)
with col2:
    lines_2 = 1000 * n_
    st.write('''{:,} \
    order lines'''.format(lines_2))
# START
start_2 = False
if st.checkbox('SIMULATION 2: START ', key='show_2', value=False):
    start_2 = True
# Calcolo
if start_2:
    df_orderlines = load('df_lines.csv', lines_2)
    df_reswave, df_results = simulation_cluster(y_low, y_high, df_orderlines, list_results, n1, n2,
                                                distance_threshold)
    plot_simulation2(df_reswave, lines_2, distance_threshold)
