import os 
import shutil

config = r'C:\Users\bs\DLC\PRT-Benj-2024-01-30\config.yaml'

deeplabcut.analyze_videos(config = config, videopath = videopath, videotype = '.mp4' , shuffle = 3, save_as_csv=True, robust_nframes = True )

import os
import shutil

def move_all_csv(source_folder, destination_folder):
    # Ensure the destination folder exists
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # List all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.csv'):
            source_path = os.path.join(source_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.move(source_path, destination_path)
            print(f"Moved {filename} to {destination_folder}")

# Example usage
source_folder = '/path/to/source/folder'
destination_folder = '/path/to/destination/folder'

move_all_csv(source_folder, destination_folder)