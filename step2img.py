import argparse
import os

import glob
from occwl.io import load_step
from occwl.viewer import Viewer
from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser("Convert step to image")
    parser.add_argument("-s", default="./step", type=str, help="Source directory")
    parser.add_argument("-d", default="./img", type=str, help="Destination directory")
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    stp_fdir = args.s
    img_fdir = args.d
    stp_fpaths = sorted(glob.glob(f"{stp_fdir}/**/*.stp", recursive=True))

    v = Viewer()
    v.hide_axes()
    for stp_fpath in tqdm(stp_fpaths):
        img_fpath = stp_fpath.replace(stp_fdir, img_fdir).replace("stp", "png")
        os.makedirs(os.path.dirname(img_fpath), exist_ok=True)
        solid = load_step(stp_fpath)[0]
        v.clear()
        v.display(solid)
        v.fit()
        v.save_image(img_fpath)