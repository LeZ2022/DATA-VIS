import folium
import requests
import pandas as pd


class CarteFolium:
    def __init__(self, df_stats_par_departement):
        self.df_stats_par_departement = df_stats_par_departement

    def get_color_by_stats(self, code_departement, column_name):
        prix_m2 = self.df_stats_par_departement[self.df_stats_par_departement['code_departement'] == code_departement][column_name].values
        if prix_m2.size > 0:
            prix_m2 = float(prix_m2[0])

            quantiles = self.df_stats_par_departement[column_name].quantile([0.2, 0.4, 0.6, 0.8]).values
            
            if prix_m2 < quantiles[0]:  
                return 'green'
            elif prix_m2 < quantiles[1]: 
                return 'lightgreen'
            elif prix_m2 < quantiles[2]: 
                return 'yellow'
            elif prix_m2 < quantiles[3]: 
                return 'orange'
            else: 
                return 'red'
        
        return 'gray'

    def create_map(self, column_name):
        center_lat, center_lon = 46.603354, 1.888334
        m = folium.Map(location=[center_lat, center_lon], zoom_start=6)

        geojson_url = 'https://france-geojson.gregoiredavid.fr/repo/departements.geojson'
        geojson_data = requests.get(geojson_url).json()

        folium.GeoJson(
            geojson_data,
            name='Départements',
            style_function=lambda feature: {
                'fillColor': self.get_color_by_stats(feature['properties']['code'], column_name),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        ).add_to(m)

        folium.LayerControl().add_to(m)
        return m

