import glob
import os
import sys
import pdb
import os.path as osp
sys.path.append(os.getcwd())
os.environ['PYOPENGL_PLATFORM'] = 'egl'

import cv2
import time
import torch
import joblib
import shutil
import colorsys
import argparse
import yaml
import numpy as np
from tqdm import tqdm
from multi_person_tracker import MPT
from torch.utils.data import DataLoader


from meva.lib.meva_model import MEVA, MEVA_demo
from meva.utils.renderer import Renderer
from meva.utils.kp_utils import convert_kps
from meva.dataloaders.inference import Inference
from meva.utils.video_config import parse_args, update_cfg
from meva.utils.demo_utils import (
    convert_crop_cam_to_orig_img,
    prepare_rendering_results,
    video_to_images,
    images_to_video,
    download_ckpt,
)

mesh_folder = 'results/mesh/Sout'
frame_results = joblib.load("results/output/Sout_meva_output_dammit.pkl")
## this is where to give the pkl name

## pkl should be just like [{'verts': ...,'cam': ..., '...'}] for frames in order 

orig_height = 720
orig_width = 720

fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')  # 编码器
fps = 30  # 帧率
videoWrite = cv2.VideoWriter('move_frame_01.mp4', fourcc, fps, (720, 720))

renderer = Renderer(resolution=(orig_width, orig_height), orig_img=False, wireframe=False)

mc = colorsys.hsv_to_rgb(np.random.rand(), 0.5, 1.0)

for (idx, frame_data) in enumerate(frame_results):
    side_img = np.zeros((orig_width, orig_height, 3))
    frame_verts = frame_data['verts']
    frame_cam = frame_data['cam']
    frame_cam = np.array([ 0.5,  1., 0,  0]) ## you can turn it around
    mesh_filename = os.path.join(mesh_folder, f'{idx:06d}.obj')
    side_img = renderer.render(
                        side_img,                       # black
                        frame_verts,                    # verts of body
                        cam=frame_cam,                  # cam loc
                        color=mc,                       # model_data
                        mesh_filename=mesh_filename,    # meshsaver
                        # angle=270,
                        # axis=[0,1,0],
                    )
    saveimgname = 'results/mesh/out/' + str(idx) + '.jpg'
    cv2.imwrite(saveimgname, side_img) ## to write the saveimgname
    videoWrite.write(side_img)
videoWrite.release()

###林弘扬交给你了
