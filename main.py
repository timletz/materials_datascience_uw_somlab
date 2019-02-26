import FOM_SOM
import train_model
import pandas as pd

def properties_dataframe_from_file(path: str):
    property_lists = FOM_SOM.parsing_refined_data(path)
    return pd.DataFrame({'name': property_lists[0], 'density': property_lists[1],
    'melting point': property_lists[2], 'thermal conductivity': property_lists[3], 'heat capacity': property_lists[4]})
    

