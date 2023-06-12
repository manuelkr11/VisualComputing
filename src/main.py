# Used Python Version 3.6 for Open3D
import os
import open3d as o3d
import numpy as np
from preprocessing import preprocessing


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


def visualisation(point_cloud, point_size=2, zoom=False):
    # Create a visualizer object
    visualizer = o3d.visualization.Visualizer()
    visualizer.create_window()
    # Add the PointCloud to the visualizer
    visualizer.add_geometry(point_cloud)
    # Get the rendering option and modify the point size
    render_option = visualizer.get_render_option()
    render_option.point_size = point_size  # Set point size
    # Set camera (used for comparison pictures in document)
    if zoom:
        ctr = visualizer.get_view_control()
        parameters = o3d.io.read_pinhole_camera_parameters("data\\ScreenCamera_01.json")
        ctr.convert_from_pinhole_camera_parameters(parameters)
    # Run the visualizer
    visualizer.run()
    visualizer.destroy_window()


if __name__ == '__main__':
    point_size = 2
    # Loading data from model.pts file
    points, colors = load_points('model.pts')
    # Preprocessing
    points, colors = preprocessing(points, colors, eps=0.05, min_samples=40, subset_size=10000)
    # Converting the numpy arrays to a point_cloud
    point_cloud = convert_to_pointcloud(points, colors)
    # Visualisation using the Open3D library, zoom=True will put camera in front of dinosaur
    visualisation(point_cloud, point_size=point_size, zoom=False)
