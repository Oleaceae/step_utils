import os

import argparse
import glob
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation
from tqdm import tqdm


def get_parser():
    parser = argparse.ArgumentParser(description="Convert mesh to point cloud")
    parser.add_argument("-s", default="./mesh", type=str, help="Source directory")
    parser.add_argument("-e", default="off", type=str, help="Mesh extension name")
    parser.add_argument("-d", default="./pcd", type=str, help="Destination directory")
    parser.add_argument("-n", default=True, type=bool, help="Normalize point cloud")
    parser.add_argument("-p", default=1024, type=int, help="Number of points sampled")
    parser.add_argument("-r", default=0, type=int, help="Times a point cloud is rotated")
    return parser


def normalize_pnts(pnts):
    centroid = np.mean(pnts, axis=0)
    pnts = pnts - centroid
    m = np.max(np.linalg.norm(pnts, ord=2, axis=1))
    pnts = pnts / m
    return pnts


def get_random_rmat():
    euler_angle = np.random.uniform(0, 2 * np.pi, (3, ))
    rmat = Rotation.from_euler('xyz', euler_angle).as_matrix()
    return rmat


def save_pnts(pnts, save_path):
    os.makedirs(os.path.dirname(save_path), exist_ok=True) 
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pnts)
    o3d.io.write_point_cloud(save_path, pcd)


if __name__ == "__main__":
    args = get_parser().parse_args()
    
    mesh_fdir, pcd_fdir = args.s, args.d
    mesh_fpaths = sorted(glob.glob(f"{mesh_fdir}/**/*.{args.e}", recursive=True))
    normalize = args.n
    number_of_points = args.p
    rotation_num = args.r
    
    for mesh_fpath in tqdm(mesh_fpaths):
        mesh = o3d.io.read_triangle_mesh(mesh_fpath)
        
        pcd_fpath = mesh_fpath.replace(mesh_fdir, pcd_fdir).replace(args.e, "pcd")

        pcd = mesh.sample_points_uniformly(number_of_points=number_of_points)
        pnts = np.array(pcd.points)

        if normalize:
            pnts = normalize_pnts(pnts)
        
        save_pnts(pnts, pcd_fpath)
        
        for i in range(rotation_num):
            rmat = get_random_rmat()
            save_pnts(pnts @ rmat, f"{pcd_fpath[:-4]}_rot{i}.pcd")
