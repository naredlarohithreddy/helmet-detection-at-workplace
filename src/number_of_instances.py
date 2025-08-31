import xml.etree.ElementTree as ET
import os
from tqdm import tqdm
import glob

CLASS_MAPPING = {
    'helmet': 0,
    'head': 1,
    'person': 2
}

person = 0
helmet = 0
head = 0

def convert_voc_to_yolo(xml_file):

    global helmet
    global head
    global person
    
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for obj in root.findall('object'):
        class_name = obj.find('name').text

        if class_name=='helmet':
            helmet+=1

        if class_name=='head':
            head+=1

        if class_name=='person':
            person+=1


def main():

    raw_annotations_dir = '../data/raw/annotations'

    xml_files = glob.glob(os.path.join(raw_annotations_dir, '*.xml'))
    if not xml_files:
        print("Error: No XML files found. Did you place the 'annotations' folder in 'data/raw/'?")
        return
    
    for xml_file in tqdm(xml_files, desc="Converting VOC to YOLO"):
        convert_voc_to_yolo(xml_file)

    print(f"total person annotation : {person}")
    print(f"total helmet annotation : {helmet}")
    print(f"total head annotation : {head}")

if __name__ == '__main__':
    main()