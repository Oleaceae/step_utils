import os

import argparse
import cadquery as cq
import glob
import trimesh
from tqdm import tqdm

parser = argparse.ArgumentParser(description="Convert .stp to .off/.stl")
parser.add_argument("-s", default="./step", type=str, help="Source directory")
parser.add_argument("-d", default="./mesh", type=str, help="Destination directory")
parser.add_argument("-f", default="off", type=str, choices=["off", "stl"], help="Format of output meshs (.stl/.off)")

if __name__ == "__main__":
    args = parser.parse_args()
    src_fdir, dst_fdir = args.s, args.d

    src_fpaths = sorted(glob.glob(f"{src_fdir}/**/*.stp", recursive=True))

    cnt = {}

    for fpath in tqdm(src_fpaths):
        stp = cq.importers.importStep(fpath)
        stl_fpath = os.path.join(dst_fdir, "tmp.stl")
        os.makedirs(os.path.dirname(stl_fpath), exist_ok=True)
        cq.exporters.export(stp, stl_fpath)
        
        final_fpath = fpath.replace(src_fdir, dst_fdir).replace(".stp", f".{args.f}")
        os.makedirs(os.path.dirname(final_fpath), exist_ok=True)
        mesh = trimesh.load_mesh(stl_fpath)
        mesh.export(final_fpath)
        os.remove(stl_fpath)