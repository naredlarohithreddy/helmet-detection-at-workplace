import os
import glob
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import shutil

RAW_IMAGE_DIR = '../data/raw/images'
INTERIM_LABEL_DIR = '../data/interim_labels'
PROCESSED_DATA_DIR = '../data/processed'

TRAIN_RATIO = 0.80
VAL_RATIO = 0.10
TEST_RATIO = 0.10

def copy_files(file_list, image_dest_dir, label_dest_dir):

    os.makedirs(image_dest_dir, exist_ok=True)
    os.makedirs(label_dest_dir, exist_ok=True)
    
    for img_path in tqdm(file_list, desc=f"Copying to {os.path.basename(image_dest_dir)}"):
        try:

            shutil.copy(img_path, image_dest_dir)

            base_filename = os.path.splitext(os.path.basename(img_path))[0]
            label_filename = base_filename + '.txt'
            label_path = os.path.join(INTERIM_LABEL_DIR, label_filename)
            
            if os.path.exists(label_path):
                shutil.copy(label_path, label_dest_dir)
            else:
                print(f"Warning: Label file not found for {img_path}")
        except Exception as e:
            print(f"Error copying {img_path}: {e}")

def main():

    image_paths = glob.glob(os.path.join(RAW_IMAGE_DIR, '*.png'))
    if not image_paths:
        print("Error: No PNG images found. Did you place the 'images' folder in 'data/raw/'?")
        return

    train_val_files, test_files = train_test_split(
        image_paths, test_size=TEST_RATIO, random_state=42
    )

    val_size_adjusted = VAL_RATIO / (TRAIN_RATIO + VAL_RATIO)
    train_files, val_files = train_test_split(
        train_val_files, test_size=val_size_adjusted, random_state=42
    )
    
    print(f"Total images: {len(image_paths)}")
    print(f"Training set size: {len(train_files)}")
    print(f"Validation set size: {len(val_files)}")
    print(f"Test set size: {len(test_files)}")

    # 4. Define destination paths
    train_img_dest = os.path.join(PROCESSED_DATA_DIR, 'images/train')
    train_lbl_dest = os.path.join(PROCESSED_DATA_DIR, 'labels/train')
    val_img_dest = os.path.join(PROCESSED_DATA_DIR, 'images/val')
    val_lbl_dest = os.path.join(PROCESSED_DATA_DIR, 'labels/val')
    test_img_dest = os.path.join(PROCESSED_DATA_DIR, 'images/test')
    test_lbl_dest = os.path.join(PROCESSED_DATA_DIR, 'labels/test')

    # 5. Copy files to their final destinations
    copy_files(train_files, train_img_dest, train_lbl_dest)
    copy_files(val_files, val_img_dest, val_lbl_dest)
    copy_files(test_files, test_img_dest, test_lbl_dest)
    
    print("\nData splitting and copying complete.")
    print(f"Processed data is ready in '{PROCESSED_DATA_DIR}'")

if __name__ == '__main__':
    main()