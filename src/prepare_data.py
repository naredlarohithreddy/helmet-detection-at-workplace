import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
import glob

CLASS_MAPPING = {
    'helmet': 0,
    'head': 1,
    'person': 2
}

OUTPUT_DIR = '../data/interim_labels'

def convert_voc_to_yolo(xml_file):

    tree = ET.parse(xml_file)
    root = tree.getroot()

    size = root.find('size')
    img_width = int(size.find('width').text)
    img_height = int(size.find('height').text)

    yolo_lines = []
    for obj in root.findall('object'):
        class_name = obj.find('name').text
        if class_name not in CLASS_MAPPING:
            print(f"Warning: Class '{class_name}' in {xml_file} is not in CLASS_MAPPING. Skipping.")
            continue
        
        class_id = CLASS_MAPPING[class_name]

        bndbox = obj.find('bndbox')
        xmin = float(bndbox.find('xmin').text)
        ymin = float(bndbox.find('ymin').text)
        xmax = float(bndbox.find('xmax').text)
        ymax = float(bndbox.find('ymax').text)

        dw = 1.0 / img_width
        dh = 1.0 / img_height
        x_center = ((xmin + xmax) / 2.0) * dw
        y_center = ((ymin + ymax) / 2.0) * dh
        width = (xmax - xmin) * dw
        height = (ymax - ymin) * dh

        yolo_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
    
    return yolo_lines


def main():

    raw_annotations_dir = '../data/raw/annotations'
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    xml_files = glob.glob(os.path.join(raw_annotations_dir, '*.xml'))
    if not xml_files:
        print("Error: No XML files found. Did you place the 'annotations' folder in 'data/raw/'?")
        return
    
    for xml_file in tqdm(xml_files, desc="Converting VOC to YOLO"):
        yolo_data = convert_voc_to_yolo(xml_file)
        
        base_filename = os.path.splitext(os.path.basename(xml_file))[0]
        output_path = os.path.join(OUTPUT_DIR, base_filename + '.txt')

        with open(output_path, 'w') as f:
            f.write('\n'.join(yolo_data))
            
    print(f"Conversion complete. All YOLO label files are in '{OUTPUT_DIR}'.")

if __name__ == '__main__':
    main()