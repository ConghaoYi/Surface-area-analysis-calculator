import surface_area_funcs
import os
import pandas as pd
import numpy as np

def main(
        image_dir,
        output_dir = 'surface_area_data',
        dataset_name = 'my_data.csv',
        c1_name = 'Site', 
        c2_name = 'Contamination_rate%'
):
    surface_area_funcs.data_init(dir_name = output_dir,
                                 dataset_name = dataset_name,
                                 c1_name= c1_name, 
                                 c2_name=c2_name)
    os.makedirs(os.path.join(output_dir,'processed_photos'),exist_ok=True)
    image_list = os.listdir(image_dir)
    for file in image_list:
        print('\n',file)
        image_path = os.path.join(image_dir,file)
        print('\n',image_path)
        surface_area_funcs.clip_big_roi(image_path,output_dir,file)
        df = pd.read_csv(os.path.join(output_dir,dataset_name))
        df.loc[len(df), c2_name] = np.load(os.path.join(output_dir,file+'rate.npy'))
        df.loc[len(df)-1, c1_name] = file
        df.to_csv(os.path.join(output_dir,dataset_name), index=False)
main(
    image_dir=
    
)