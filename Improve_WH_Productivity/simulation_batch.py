from mapping_batch import *
from routes import *

def simulation_wave(y_low, y_high, origin_loc, orders_number, df_orderlines, list_wid, list_dst, list_route, list_ord):
	'''Simulo il totale della distanza di picking con n orders per wave'''
	distance_route = 0
	# Creo le waves
	df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)
	for wave_id in range(waves_number):

		# Listing di tutte le locazioni per questa wave
		list_locs, n_locs = locations_listing(df_orderlines, wave_id)
		# Risultati
		wave_distance, list_chemin = create_picking_route(origin_loc, list_locs, y_low, y_high)
		distance_route = distance_route + wave_distance
		list_wid.append(wave_id)
		list_dst.append(wave_distance)
		list_route.append(list_chemin)
		list_ord.append(orders_number)
	return list_wid, list_dst, list_route, list_ord, distance_route

def simulate_batch(n1, n2, y_low, y_high, origin_loc, orders_number, df_orderlines):
	''' Loop con diversi scenari di n ordini per wave '''
	# Liste dei vari risultati
	list_wid, list_dst, list_route, list_ord = [], [], [], []

	# Test di diversi valori di orders per wave
	for orders_number in range(n1, n2 + 1):
		list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, origin_loc, orders_number,
		df_orderlines, list_wid, list_dst, list_route, list_ord)
		print("Total distance covered for {} orders/wave: {:,} m".format(orders_number, distance_route))

	# By Wave
	df_waves = pd.DataFrame({'wave': list_wid,'distance': list_dst,'routes': list_route,'order_per_wave': list_ord})

	# Aggrego i risultati
	df_results = pd.DataFrame(df_waves.groupby(['order_per_wave'])['distance'].sum())
	df_results.columns = ['distance']
	return df_waves, df_results.reset_index()