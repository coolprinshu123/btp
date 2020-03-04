import osmium as osm
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# ShopHandler extract restaurant's locations from the osm file
class ShopHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []

    def shops(self, elem):
        if ShopHandler.is_site(elem):
            self.osm_data.append(ShopHandler.getLocation(elem.location))

    def node(self, n):
        self.shops(n)

    @staticmethod
    def is_site(elem):
        for tag in elem.tags:
            if tag.v in ['supermarket','station', 'apartments', 'hospital', 'company']:
            	if tag.v in ['station', 'apartments']:
            		return tag.k in ['railway', 'building']
            	return True
        return False

    @staticmethod
    def getLocation(location):
        return [float(location.lat), float(location.lon)]

# get restaurant locations from the osm file as a pandas dataframe
def get_restaurants(region, csv=False):
    if csv:
        return pd.read_csv(f'csv/{region}.csv')

    shopHandler = ShopHandler()
    shopHandler.apply_file(f'region/{region}.osm')
    print(f'Number of restaurants in the region {region}: {len(shopHandler.osm_data)}')

    data_columns = ["lat", "lon"]
    return pd.DataFrame(shopHandler.osm_data, columns=data_columns)

# draw restaurants locations and save the figure
def draw(df, region):
    sns.jointplot(x="lat", y="lon", data=df)
    plt.savefig(f'fig/{region}.png', format='png')
    plt.show()

# save the result of dataframe to csv file
def to_csv(df, region):
    df.to_csv(f'csv/{region}.csv')
