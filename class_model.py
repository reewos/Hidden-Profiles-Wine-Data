import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import (AgglomerativeClustering,
                             AffinityPropagation,
                             SpectralClustering,
                             DBSCAN,
                             KMeans)

# Model
class ModelClusterVoting:
    def __init__(self, num_clusters=3, random_state=42):
        self.num_clusters = num_clusters
        self.random_state = random_state
        self.dict_equivalents_model = None
        self.clustering_models = None
        self.scaler = None
        self.pca = None

    def preprocess_fit_transform(self, df):
        # Standardize and reduce dimensionality using PCA during training
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)

        X = df.values
        X_standard = self.scaler.fit_transform(X)
        X_pca_standard = self.pca.fit_transform(X_standard)
        return X_standard, X_pca_standard
    
    def preprocess_transform(self, df):
        # Standardize and reduce dimensionality using PCA during prediction
        X = df.values
        X_standard = self.scaler.transform(X)
        X_pca_standard = self.pca.transform(X_standard)
        return X_standard, X_pca_standard

    def fit(self, df):
        print("\n\nStart training....")
        # Preprocess and fit-transform the input data
        X_standard, X_pca_standard = self.preprocess_fit_transform(df)
        
        column_count = df.shape[1]
        # Initialize clustering models
        self.clustering_models = {
            "kmeans": KMeans(n_clusters=self.num_clusters, random_state=self.random_state),
            "agglom": AgglomerativeClustering(n_clusters=self.num_clusters),
            "dbscan": DBSCAN(eps=0.55, min_samples=5),
            "affini": AffinityPropagation(damping=0.9, preference=-200.0, random_state=self.random_state),
            "spectr": SpectralClustering(n_clusters=self.num_clusters, random_state=self.random_state, affinity='nearest_neighbors'),
        }

        # Train each clustering model
        for name, model in self.clustering_models.items():
            # print(f"Model {name} starting training")
            if name == 'dbscan':        #It's only dbscan because with pca reduction have less outliers
                model.fit(X_pca_standard)
            else:
                model.fit(X_standard)

        df_temp = df.copy()
        # Assign cluster labels to the original dataframe
        for name, model in self.clustering_models.items():
            df_temp[name] = model.labels_

        # Create a dictionary to map equivalent values in each cluster for each column
        self.dict_equivalents_model = {col: {df_temp[col][df_temp['kmeans'] == cluster_i].mode().iloc[0]: cluster_i
                                             for cluster_i in range(self.num_clusters)}
                                       for col in df_temp.columns[column_count:]}
        print("\n\nEnd training....")
       

    def predict(self, df):
        # Preprocess and transform the input data during prediction
        X_standard, X_pca_standard = self.preprocess_transform(df)
        df_temp = df.copy()
        column_count = df.shape[1]

        # Predict cluster labels for each model
        for name, model in self.clustering_models.items():
            if name == 'dbscan':
                df_temp[name] = model.fit_predict(X_pca_standard)
            elif name in ('agglom', 'spectr'):
                df_temp[name] = model.fit_predict(X_standard)
            else:
                df_temp[name] = model.predict(X_standard)
        
        # Replace cluster labels with equivalent values based on the trained model
        for col in df.columns[column_count:]:
            df_temp[col].replace(self.dict_equivalents_model[col], inplace=True)

        # Create a 'Voting' column based on the mode of cluster labels across models
        df_temp['Voting'] = df_temp.iloc[:, column_count:].mode(axis=1)[0].astype(int)
        self.labels_ = df.iloc[:, column_count:].values

        return df_temp['Voting'].values
    
    def fit_predict(self, df):
        # Train the model and make predictions
        self.fit(df)
        predicted_values = self.predict(df)
        return predicted_values

    def save_model(self, ruta):
        # Save the model using pickle
        with open(ruta, 'wb') as archivo:
            pickle.dump(self, archivo)

    @classmethod
    def load_model(cls, ruta):
        # Load a saved model using pickle
        with open(ruta, 'rb') as archivo:
            return pickle.load(archivo)


if __name__ == '__main__':
    # Example usage
    df = pd.read_csv("./datasets/wine-clustering.csv")

    # Create an instance of the ModelClusterVoting class
    model = ModelClusterVoting()

    # Fit the model and predict cluster labels
    df['Clusters_Voting'] = model.fit_predict(df)

    # Save the trained model to a file
    model.save_model('./models/voting_model.pkl')

    # Load the saved model
    model_new = ModelClusterVoting()
    model_new.load_model('./models/voting_model.pkl')
