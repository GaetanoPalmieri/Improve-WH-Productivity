import pandas as pd

def process_lines(df_orderlines):
    ''' Processing del dataframe '''
    # Mapping Order lines
    df_nline = pd.DataFrame(df_orderlines.groupby(['OrderNumber'])['SKU'].count())

    # Lists
    list_ord = list(df_nline.index.astype(int).values)
    list_lines = list(df_nline['SKU'].values.astype(int))

    # Mapping
    dict_nline = dict(zip(list_ord, list_lines))
    df_orderlines['N_lines'] = df_orderlines['OrderNumber'].map(dict_nline)

    # Processing
    df_mono, df_multi = df_orderlines[df_orderlines['N_lines'] == 1], df_orderlines[df_orderlines['N_lines'] > 1]
    del df_orderlines

    return df_mono, df_multi

def monomult_concat(df_mono, df_multi):
    ''' Concateno mono-line and multi-lines orders'''
    # Coordinate originali per il mono
    df_mono['Coord_Cluster'] = df_mono['Coord']
    # Dataframe Concat
    df_orderlines = pd.concat([df_mono, df_multi])
    # Conto il numero dei Waves
    waves_number = df_orderlines.WaveID.max() + 1

    return df_orderlines, waves_number