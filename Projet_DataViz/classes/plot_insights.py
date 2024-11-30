import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

class VisualisationStats:
    
    def __init__(self, df_stats_par_departement, df_stats_par_commune, etude):
        self.df_stats_par_departement = df_stats_par_departement
        self.df_stats_par_commune = df_stats_par_commune
        self.etude = etude

    def setup_barplot(self, data, x, y, hue, title, xlabel, ylabel):
       
        fig = px.bar(
            data_frame=data,
            x=x,
            y=y,
            color=hue,
            color_continuous_scale="Viridis",
            title=title,
            labels={x: xlabel, y: ylabel, hue: hue}, 
        )

        # Ajustements de style
        fig.update_layout(
            title=dict(font=dict(size=20), x=0.5),  # Centrer le titre
            xaxis=dict(tickangle=45, title=dict(font=dict(size=14))),
            yaxis=dict(title=dict(font=dict(size=14))),
            margin=dict(l=50, r=50, t=50, b=50),  # Marges
            plot_bgcolor="rgba(0,0,0,0)",  # Fond transparent
        )

        # Afficher le graphique
        fig.show()

    def plot_median_prix_m2_par_departement(self):
        self.setup_barplot(
            data=self.df_stats_par_departement,
            x="code_departement",
            y="median_prix_m2",
            hue="code_departement",
            title="Prix Médian au m² des Valeurs Foncières par Département",
            xlabel="Département",
            ylabel="Valeur Foncière Médiane (€)"
        )


    def plot_mean_prix_m2_par_departement(self):
        self.setup_barplot(
            data=self.df_stats_par_departement.dropna(),
            x="code_departement",
            y="mean_prix_m2",
            hue="code_departement",
            title="Prix Moyen au m² par Département",
            xlabel="Département",
            ylabel="Prix Moyen au m² (€)"
        )

    def plot_nb_ventes_par_departement(self):
        self.setup_barplot(
            data=self.df_stats_par_departement,
            x="code_departement",
            y="nb_ventes",
            hue="code_departement",
            title="Nombre de Ventes par Département",
            xlabel="Département",
            ylabel="Nombre de Ventes"
        )

    def plot_tranches_prix_par_departement(self, df_tranches_par_departement, code_departement):
        df_filtered = df_tranches_par_departement[df_tranches_par_departement['code_departement'] == code_departement]
        self.setup_barplot(
            data=df_filtered,
            x="tranche_prix",
            y="count_tranche",
            hue="tranche_prix",
            title=f"Répartition des Prix par Tranche pour le Département {code_departement}",
            xlabel="Tranche de Prix",
            ylabel="Nombre de Transactions"
        )

    def plot_median_prix_m2_par_commune(self, code_departement):
        etude_une_commune = self.etude.get_insights_par_departement(code_departement, self.df_stats_par_commune)
        self.setup_barplot(
            data=etude_une_commune,
            x="nom_commune",
            y="median_prix_m2",
            hue="nom_commune",
            title=f"Prix Médian au m² des Valeurs Foncières par Commune pour le Département {code_departement}",
            xlabel="Commune",
            ylabel="Valeur Foncière Médiane (€)"
        )

    def plot_mean_prix_m2_par_commune(self, code_departement):
        etude_une_commune = self.etude.get_insights_par_departement(code_departement, self.df_stats_par_commune)
        self.setup_barplot(
            data=etude_une_commune,
            x="nom_commune",
            y="mean_prix_m2",
            hue="nom_commune",
            title=f"Prix Moyen au m² par Commune pour le Département {code_departement}",
            xlabel="Commune",
            ylabel="Prix Moyen au m² (€)"
        )

    def plot_nb_ventes_par_commune(self, code_departement):
        etude_une_commune = self.etude.get_insights_par_departement(code_departement, self.df_stats_par_commune)
        self.setup_barplot(
            data=etude_une_commune,
            x="nom_commune",
            y="nb_ventes",
            hue="nom_commune",
            title=f"Nombre de Ventes par Commune pour le Département {code_departement}",
            xlabel="Commune",
            ylabel="Nombre de Ventes"
        )



    def afficher_nombre_et_prix_median_par_type_local(self, df_nombre, df_prix_median, code_departement):
        selected_columns = ['Appartement', 'Local industriel. commercial ou assimilé', 'Maison']
        df_nombre_filtered = df_nombre[df_nombre['code_departement'] == code_departement][selected_columns]
        
        df_prix_filtered = df_prix_median[df_prix_median['code_departement'] == code_departement][['type_local', 'median_prix_m2_local']]
        
    
        rows = []
        for col in selected_columns:
            nombre = df_nombre_filtered[col].iloc[0] if not df_nombre_filtered.empty else 0
            prix_median = df_prix_filtered[df_prix_filtered['type_local'] == col]['median_prix_m2_local'].iloc[0] if not df_prix_filtered[df_prix_filtered['type_local'] == col].empty else "N/A"
            rows.append([col, nombre, prix_median])

        
        fig = go.Figure(data=[go.Table(
            header=dict(values=["Type de Local", "Nombre", "Prix Médian au m²(€)"],
                        fill_color='#4CAF50',
                        font=dict(color='white', size=12),
                        align='center'),
            cells=dict(values=list(zip(*rows)), 
                    fill=dict(color=['#f9f9f9', '#f9f9f9', '#f9f9f9']),  
                    align='center',
                    font=dict(color=['black', 'black', 'black'], size=12))  
        )])

       
        fig.update_layout(
            height=400,
            width=800,
            title=f"Données pour le Département {code_departement}",
            title_x=0.5,
            title_font=dict(size=20),
            template="plotly_dark",  
        )

        fig.show()