import open3d as o3d

# Specify the path to your PLY file
ply_file_path = "/home/sky/realsense_image_2.ply"  # Replace with the actual path to your .ply file

# Load the point cloud from the PLY file
pcd = o3d.io.read_point_cloud(ply_file_path)

# Print information about the loaded point cloud (optional)
print(pcd)
print(f"Number of points: {len(pcd.points)}")

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd])
