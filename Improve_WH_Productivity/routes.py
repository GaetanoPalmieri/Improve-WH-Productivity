from distances import *


def create_picking_route(origin_loc, list_locs, y_low, y_high):
    '''Calcolare la distanza totale per coprire per una lista di locations'''

    # Variabile per la distanza totale
    wave_distance = 0
    # Location corrente variabile
    start_loc = origin_loc
    # Memorizzare i routes
    list_chemin = []
    list_chemin.append(start_loc)

    while len(list_locs) > 0:  # Looping fino a quando tutte le locations vengono scelte
        # Verso la prossima location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        # Update start_loc
        start_loc = next_loc
        list_chemin.append(start_loc)
        # Update distanza
        wave_distance = wave_distance + distance_next

        # Distanza finale dall'ultima storage location dall'origine
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)

    return wave_distance, list_chemin


# Calcolo la distanza totale per coprire la lista di locazioni
def create_picking_route_cluster(origin_loc, list_locs, y_low, y_high):
    # Variabile della distanza totale
    wave_distance = 0
    # Distanza max
    distance_max = 0
    # Variabile che mi definisce la location corrente
    start_loc = origin_loc
    # Memorizzo le routes
    list_chemin = []
    list_chemin.append(start_loc)
    while len(list_locs) > 0:  # Looping finchè tutte le locations sono coperte
        # Ci si sposta verso la prossima location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        # Update start_loc
        start_loc = next_loc
        list_chemin.append(start_loc)
        if distance_next > distance_max:
            distance_max = distance_next
        # Update distanza
        wave_distance = wave_distance + distance_next
        # Distanza finale dalle ultime storage location all origine
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)
    return wave_distance, list_chemin, distance_max