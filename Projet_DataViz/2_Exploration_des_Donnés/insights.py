import pandas as pd

class Insights:
    def __init__(self, df):
        self.df = df.copy()

    def calculer_statistiques(self, groupby_col):
        # Statistiques principales pour 'valeur_fonciere'
        df_stats = self.df.groupby(groupby_col)['valeur_fonciere'].agg(
            median='median',
            mean='mean',
            std='std' 
        ).reset_index()

        # Calculer le coefficient de variation (écart-type / moyenne)
        df_stats['cv'] = df_stats['std'] / df_stats['mean']

        # Calculer le prix au m²
        df_prix_m2_stats = self.df.groupby(groupby_col)['prix_m2'].agg(
            median_prix_m2='median',
            mean_prix_m2='mean'
        ).reset_index()

        # Calculer le nombre de ventes
        df_ventes_stats = self.df.groupby(groupby_col)['valeur_fonciere'].count().reset_index()
        df_ventes_stats.rename(columns={'valeur_fonciere': 'nb_ventes'}, inplace=True)

        # Ajouter l'année de la mutation
        self.df['annee_mutation'] = pd.to_datetime(self.df['date_mutation']).dt.year
        
        # Tendance des prix par année
        df_tendance = self.df.groupby([groupby_col, 'annee_mutation'], observed=False)['valeur_fonciere'].mean().reset_index()
        df_tendance = df_tendance.pivot(index='annee_mutation', columns=groupby_col, values='valeur_fonciere')

        # Nombre de ventes par tranche de prix
        bins = [0, 100000, 200000, 300000, 400000, 500000, float('inf')] 
        labels = ['<100k', '100k-200k', '200k-300k', '300k-400k', '400k-500k', '>500k']
        self.df['tranche_prix'] = pd.cut(self.df['valeur_fonciere'], bins=bins, labels=labels)
        df_tranches = self.df.groupby([groupby_col, 'tranche_prix'], observed=False).size().reset_index(name='count_tranche')

        # Distribution des types locaux et prix médian
        df_type_local_dist = self.df.groupby(groupby_col)['type_local'].value_counts().unstack(fill_value=0).reset_index()
        df_type_local_median = self.df.groupby([groupby_col, 'type_local'])['valeur_fonciere'].median().reset_index()
        df_type_local_median.rename(columns={'valeur_fonciere': 'median_prix_local'}, inplace=True)

        # Fusionner les statistiques principales
        df_stats = df_stats.merge(df_prix_m2_stats, on=groupby_col)
        df_stats = df_stats.merge(df_ventes_stats, on=groupby_col)


        return df_stats, df_tendance, df_tranches, df_type_local_dist,df_type_local_median

    def get_liste_communes_de_departement(self, code_departement):
        # Liste des communes d'un département spécifique
        communes = self.df[self.df['code_departement'] == code_departement]['nom_commune'].unique()
        return communes

    def get_insights_par_departement(self, code_departement, df_stats_par_commune):
        communes = self.get_liste_communes_de_departement(code_departement)
        etude_une_commune = df_stats_par_commune[df_stats_par_commune['nom_commune'].isin(communes)] 
        return etude_une_commune
