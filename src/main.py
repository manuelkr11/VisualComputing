# Used Python Version 3.6 for Open3D
import os
import open3d as o3d
import numpy as np


def load_points(file_name):
    # Get full file path
    main_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    pts_file_path = os.path.join(main_dir, 'data', file_name)
    # Load the points and RGB values from the file
    points = []
    colors = []
    with open(pts_file_path, 'r') as file:
        for line in file:
            values = line.strip().split(' ')
            x, y, z = map(float, values[:3])
            r, g, b = map(int, values[3:])
            points.append([x, y, z])
            colors.append([r, g, b])
    # Convert the lists to numpy arrays and return them
    points = np.asarray(points)
    colors = np.asarray(colors)
    print("Points loaded successfully!")
    return points, colors


def convert_to_pointcloud(points, colors):
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors / 255.0)  # Normalize RGB values to [0, 1]
    print("PointCloud created!")
    return point_cloud


if __name__ == '__main__':
    # Loading data from model.pts file
    points, colors = load_points('model.pts')
    # Converting the numpy arrays to a point_cloud
    point_cloud = convert_to_pointcloud(points, colors)
    # Visualisation using the Open3D library
    o3d.visualization.draw_geometries([point_cloud])
