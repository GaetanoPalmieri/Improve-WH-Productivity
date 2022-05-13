import numpy as np
import pandas as pd
import ast
from ast import literal_eval


def distance_picking(Loc1, Loc2, y_low, y_high):
    '''Calcolare Picker Route Distance fra 2 locations'''
    # Punto di Partenza
    x1, y1 = Loc1[0], Loc1[1]
    # Punto di Destinazione
    x2, y2 = Loc2[0], Loc2[1]
    # Distanza asse x
    distance_x = abs(x2 - x1)
    # Distanza asse y
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y2 = distance_y1
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)
    # Distanza minina sull'asse y
    distance_y = min(distance_y1, distance_y2)
    # Distanza Totale
    distance = distance_x + distance_y
    return int(distance)


def next_location(start_loc, list_locs, y_low, y_high):
    '''Trovare la closest next location'''
    # Distanza per ogni prossimo punto candidato
    list_dist = [distance_picking(start_loc, i, y_low, y_high) for i in list_locs]
    # Distanza Minima
    distance_next = min(list_dist)
    # Location della Distanza Minima
    index_min = list_dist.index(min(list_dist))
    next_loc = list_locs[index_min]
    list_locs.remove(next_loc)
    return list_locs, start_loc, next_loc, distance_next


def centroid(list_in):
    '''Centroid function'''
    x, y = [p[0] for p in list_in], [p[1] for p in list_in]
    centroid = [round(sum(x) / len(list_in), 2), round(sum(y) / len(list_in), 2)]
    return centroid


def centroid_mapping(df_multi):
    '''Mapping Centroids'''
    # Mapping multi
    df_multi['Coord'] = df_multi['Coord'].apply(literal_eval)
    # Raggruppo le coordinate per ordine
    df_group = pd.DataFrame(df_multi.groupby(['OrderNumber'])['Coord'].apply(list)).reset_index()
    # Calcolo i Centroid
    df_group['Coord_Centroid'] = df_group['Coord'].apply(centroid)
    # Definisco un dizionario per il mapping
    list_order, list_coord = list(df_group.OrderNumber.values), list(df_group.Coord_Centroid.values)
    dict_coord = dict(zip(list_order, list_coord))
    # Final mapping
    df_multi['Coord_Cluster'] = df_multi['OrderNumber'].map(dict_coord).astype(str)
    df_multi['Coord'] = df_multi['Coord'].astype(str)
    return df_multi


def distance_picking_cluster(point1, point2):
    y_low, y_high = 5.5, 50
    # Punto di Partenza
    x1, y1 = point1[0], point1[1]
    # Punto di Arrivo
    x2, y2 = point2[0], point2[1]
    # Distanza x-axis
    distance_x = abs(x2 - x1)
    # Distanza y-axis
    if x1 == x2:
        distance_y1 = abs(y2 - y1)
        distance_y2 = distance_y1
    else:
        distance_y1 = (y_high - y1) + (y_high - y2)
        distance_y2 = (y1 - y_low) + (y2 - y_low)
    # Distanza Minima sull- y-axis
    distance_y = min(distance_y1, distance_y2)
    # Distanza Totale
    distance = distance_x + distance_y
    return distance
