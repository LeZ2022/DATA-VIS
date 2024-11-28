from sklearn.preprocessing import LabelEncoder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class CorrelationAnalyzer:

    def __init__(self, df):
        """Initialise la classe avec un DataFrame."""
        self.df = df

    def encode_categorical_columns(self):
        """Encodes categorical columns in the DataFrame."""
        df_encoded = self.df.copy()
        for column in df_encoded.columns:
            if df_encoded[column].dtype == 'object' or df_encoded[column].dtype.name == 'category' or df_encoded[column].nunique() < 50:
                df_encoded[column] = df_encoded[column].apply(str)
                le = LabelEncoder()
                df_encoded[column] = le.fit_transform(df_encoded[column])
        return df_encoded

    def plot_correlation_matrix(self):
        """Plots the correlation matrix heatmap."""
        df_encoded = self.encode_categorical_columns()
        correlation_matrix = df_encoded.corr()
        num_columns = len(correlation_matrix.columns)
        figsize = (num_columns * 0.8, num_columns * 0.6)
        plt.figure(figsize=figsize)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.2)
        plt.title('Correlation Matrix')
        plt.show()

    def find_high_correlation_pairs(self, threshold=0.90):
        """Finds pairs of variables with correlation above the given threshold."""
        df_encoded = self.encode_categorical_columns()
        correlation_matrix = df_encoded.corr()

        high_corr_pairs = []
        for column in correlation_matrix.columns:
            for row in correlation_matrix.index:
                if abs(correlation_matrix.loc[row, column]) > threshold and row != column:
                    high_corr_pairs.append((row, column, correlation_matrix.loc[row, column]))

        high_corr_pairs = list(set([tuple(sorted(pair[:2])) + (pair[2],) for pair in high_corr_pairs]))

        if high_corr_pairs:
            print(f"Pairs of variables with correlation greater than {threshold}:")
            for pair in high_corr_pairs:
                print(f"{pair[0]} and {pair[1]}: {pair[2]:.2f}")
        else:
            print(f"No pairs with correlation greater than {threshold}")

    def plot_correlation_with_column(self, column_name):
        """Plots the correlation of the given column with all other columns."""
        df_encoded = self.encode_categorical_columns()
        correlation_matrix = df_encoded.corr()

        correlation_column = correlation_matrix[column_name]
        correlation_column_filtered = correlation_column[correlation_column != 1]
        correlation_column_sorted = correlation_column_filtered.sort_values(ascending=False)

        plt.figure(figsize=(15, 10))
        sns.barplot(x=correlation_column_sorted.index, y=correlation_column_sorted.values, color='cornflowerblue')
        plt.xticks(rotation=90)
        plt.title(f'Correlation of {column_name} with other columns', fontsize=20)
        plt.xlabel('Columns', fontsize=15)
        plt.ylabel('Correlation coefficient', fontsize=15)
        plt.tight_layout()
        plt.show()

    def plot_correlation_between_dfs(self, df2):
        """Plots the correlation matrix between two DataFrames."""
        df_encoded = self.encode_categorical_columns()
        df2_encoded = CorrelationAnalyzer(df2).encode_categorical_columns()

        combined_df = pd.concat([df_encoded, df2_encoded], axis=1)
        correlation_matrix = combined_df.corr()

        num_columns = len(correlation_matrix.columns)
        figsize = (num_columns * 0.8, num_columns * 0.6)
        plt.figure(figsize=figsize)
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.2)
        plt.title('Correlation Matrix between DataFrames', fontsize=20)
        plt.show()

    def print_correlation_between_columns(self, column1, column2):
        """Prints the correlation between two specific columns."""
        df_encoded = self.encode_categorical_columns()
        correlation_value = df_encoded[[column1, column2]].corr().iloc[0, 1]
        print(f"The correlation between '{column1}' and '{column2}' is: {correlation_value:.2f}")

