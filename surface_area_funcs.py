import numpy as np
import matplotlib as plt
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.widgets import RectangleSelector
from matplotlib.patches import Rectangle


def data_init(c1_name = 'Site', c2_name = 'Contamination_rate%', dataset_name = 'my_data.csv',dir_name = 'surface_area_data'):
    os.makedirs(dir_name,exist_ok=True)
    if os.path.exists(os.path.join(dir_name,dataset_name)):
        df = pd.read_csv(os.path.join(dir_name,dataset_name))
        print(f"Loaded existing file: {os.path.join(dir_name,dataset_name)}")
    else:
        df = pd.DataFrame(columns=[c1_name,c2_name])
        df.to_csv(os.path.join(dir_name,dataset_name), index=False)

    return df

def clip_big_roi(img_dir,out_dir,image_name):
    def _onselect(eclick, erelease):
        current_ax = eclick.inaxes
        current_fig = current_ax.figure
        current_img = current_ax.get_images()[0].get_array()
        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        xmin, xmax, ymin, ymax = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        width, height = xmax - xmin, ymax - ymin
        print('size is ', width*height)
        np.save('total_area.npy',width*height)
        roi = current_img[ymin:ymax, xmin:xmax]
        if roi.size > 0:
            plt.imsave(os.path.join(out_dir,'selected_roi_temp.png'), roi)
            print(f"Saved ROI! Press 'Enter' to exit.")

    def _on_key(event):
        # if event.key == 'enter':
        #     plt.close(fig)
        #     print("Window closed.")
        current_fig = event.canvas.figure

        if event.key == 'enter':
            plt.close(current_fig)
            print("Window closed.")
    img = plt.imread(img_dir)
    fig, ax = plt.subplots()
    ax.imshow(img)
    fig.canvas.mpl_connect('key_press_event', _on_key)
    rs = RectangleSelector(ax, _onselect, interactive=True)
    plt.show()
    clip_roi(os.path.join(out_dir,'selected_roi_temp.png'),out_dir,image_name)

def clip_roi(img_dir,outdir,image_name):

    def _onselect2(eclick, erelease):
    
        current_ax = eclick.inaxes
        current_fig = current_ax.figure
        current_img = current_ax.get_images()[0].get_array()
        x1, y1 = int(eclick.xdata), int(eclick.ydata)
        x2, y2 = int(erelease.xdata), int(erelease.ydata)
        xmin, xmax, ymin, ymax = min(x1, x2), max(x1, x2), min(y1, y2), max(y1, y2)
        width, height = xmax - xmin, ymax - ymin

        if width > 0 and height > 0:
            rect = Rectangle((xmin, ymin), width, height, 
                            edgecolor='red', facecolor='none', linewidth=2)
            current_ax.add_patch(rect)
            
            current_fig.canvas.draw()
            roi_all.append(width * height)
            total_area = np.sum(np.array(roi_all))
            print("Current ROI ratio is ",total_area/np.load('total_area.npy'))
            np.save(os.path.join(outdir,image_name+'rate.npy'),total_area/np.load('total_area.npy'))
            plt.savefig(os.path.join(outdir+'/processed_photos',image_name+'_all_roi.png'))
        
    def _on_key2(event):
        current_fig = event.canvas.figure

        if event.key == 'enter':
            plt.close(current_fig)
    img = plt.imread(img_dir)
    f,a = plt.subplots()
    roi_all = []
    a.imshow(img)
    rs= RectangleSelector(a, _onselect2, interactive=True)
    f.canvas.mpl_connect('key_press_event', _on_key2)
    plt.show()
    