# -*- encoding:utf-8 -*-
# @Time    : 2019/6/19 19:35
# @Author  : gfjiang
# @Site    : 
# @File    : dota_to_coco.py
# @Software: PyCharm
import json
import os.path as osp
from tqdm import tqdm
import cv2.cv2 as cv
from PIL import Image
import numpy as np

import cvtools
from cvtools.evaluation.class_names import get_classes


class DOTA2COCO(object):
    """convert DOTA labels to coco-like format labels.

    Args:
        label_root (str): label file path,
            for example, '/home/data/DOTA/train/labelTxt'
        image_root (str): image path,
            for example, '/home/data/DOTA/train/images'
        classes (str or list): class name in a file or a list.
        path_replace (dict): replace same things in images path,
            if not needed, you can just ignore it.
        box_form (str): coco bbox format, default 'x1y1wh'.
    """

    def __init__(self,
                 label_root,
                 image_root,
                 classes=get_classes('dota'),
                 path_replace=None,
                 box_form='x1y1wh'):
        self.label_root = label_root
        self.image_root = image_root
        self.path_replace = path_replace
        self.box_form = box_form
        self.files = []
        self.files += cvtools.get_files_list(
            label_root, basename=True)
        if cvtools._DEBUG:
            self.files = self.files[:10]
        self.lines = []
        if isinstance(classes, str):
            self.cls_map = cvtools.read_key_value(classes)
        else:
            self.cls_map = {name: i + 1 for i, name in enumerate(classes)}
        self.coco_dataset = {
            "info": {
                "description": "This is stable 1.0 version of the DOTA.",
                "url": "http://captain.whu.edu.cn/DOTAweb/index.html",
                "version": "1.0", "year": 2018,
                "contributor": "DOTA",
                "date_created": cvtools.get_time_str()
            },
            "categories": [],
            "images": [], "annotations": []
        }
        self.imageID = 1
        self.annID = 1
        self.run_timer = cvtools.Timer()

    def convert(self, use_crop=False):
        for key, value in self.cls_map.items():
            self.coco_dataset['categories'].append({
                'id': int(value),
                'name': key,
                'supercategory': key
            })
        for file in tqdm(self.files):
            with open(osp.join(self.label_root, file), 'r') as f:
                lines = f.readlines()
            # !only do once for one file label
            image_name = file.replace('.txt', '.png')
            if use_crop:
                image_name = file.split('_')[0] + '.png'
            image_file = osp.join(self.image_root, image_name)
            try:
                "PIL: Open an image file, without loading the raster data"
                im = Image.open(image_file)
                if im is None:
                    print('Waring: !!!can\'t read %s, continue this image'
                          % image_file)
                    continue
                width, height = im.size
            except (FileNotFoundError, Image.DecompressionBombError) as e:
                print(e)
                continue

            # add image information to dataset
            if self.path_replace:
                for key, value in self.path_replace.items():
                    image_name = image_name.replace(key, value)
            img_info = {
                'file_name': image_name,    # relative path
                'id': self.imageID,
                'width': width,
                'height': height,
            }
            if use_crop:
                # get crop coor
                crop_str = osp.splitext(osp.basename(file))[0].split('_')[2:]
                crop = list(map(int, crop_str))
                img_info['width'] = crop[2] - crop[0]
                img_info['height'] = crop[3] - crop[1]
                img_info['crop'] = crop
            self.coco_dataset["images"].append(img_info)

            ignore = 0
            if height * width > 100000000:
                ignore = 1

            for line in lines:
                line = line.strip().split()
                if len(line) != 10:
                    continue
                polygon = list(map(float, [item.strip() for item in line[:8]]))
                # prepare for Polygon class input
                a = np.array(polygon).reshape(4, 2)
                # the clockwise output convex hull in the Cartesian coordinate
                # system
                a_hull = cv.convexHull(a.astype(np.float32), clockwise=False)

                if self.box_form == 'x1y1wh':
                    box = cv.boundingRect(a_hull)
                    area = box[2] * box[3]
                elif self.box_form == 'xywha':
                    xywha = cv.minAreaRect(a_hull)
                    area = xywha[1][0] * xywha[1][1]
                    box = list(xywha[0]) + list(xywha[1]) + [xywha[2]]
                elif self.box_form == 'x1y1x2y2x3y3x4y4':
                    area = cv.contourArea(a_hull)
                    box = list(a_hull.reshape(-1).astype(np.float))
                else:
                    raise TypeError("not support {} box format!".format(
                        self.box_form))

                if not self.check_box(box, width, height):
                    print('{}: box {} out of the image {}x{}'.format(
                        image_name, box, width, height))
                    continue

                box = list(map(lambda x: round(x, 2), box))
                cat = line[8].strip()
                difficult = int(line[9].strip())
                try:
                    self.coco_dataset['annotations'].append({
                        'area': area,
                        'bbox': box,
                        # 0 for background
                        'category_id': int(self.cls_map[cat]),
                        'id': self.annID,
                        'image_id': self.imageID,
                        'iscrowd': 0,
                        'ignore': ignore,
                        'difficult': difficult,
                        'segmentation': [polygon]
                    })
                except KeyError:
                    print("{} not in classes".format(cat))
                    continue
                self.annID += 1
            self.imageID += 1

    def check_box(self, box, w, h):
        if box[0] > w or box[1] > h:    # for P1872.png
            return False
        return True

    def save_json(self, to_file='cocolike.json'):
        # save json format results to disk
        cvtools.utils.makedirs(to_file)
        with open(to_file, 'w') as f:
            json.dump(self.coco_dataset, f)
        print('!save {} finished'.format(to_file))
