import pandas as pd
import geopandas as gpd

munitions = pd.read_csv(r'data/munitions.csv')
offshore_installations = pd.read_csv(r'data/offshore_installations.csv')
ports = pd.read_csv(r'data/ports.csv')
shipwrecks = pd.read_csv(r'data/shipwrecks.csv')
windfarms = pd.read_csv(r'data/windfarms.csv')