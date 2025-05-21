import os

import open3d.examples.visualization.draw

from utils import *

# base_dir = "/media/rishabh/SSD_1/Data/Blender_Renders/ct_scan_foot"
# output_name = "project_2_images"

base_dir = "/home/rishabh/projects/gaussian-splatting/output/bunny_v3/point_cloud/iteration_30000"
output_name = "blender_tf"

output_dir = osp.join(base_dir, output_name)

os.makedirs(output_dir, exist_ok=True)

# obtained from manually aligning the 2pcd using point picking in CloudCompare
if "foot" in base_dir:
    result_T_m2_m1 = np.array([
        [ 0.03281417, -0.47197083, -0.08237366, -0.43157973],
        [-0.02093014, -0.08389998,  0.47237842,  0.16128158],
        [-0.4786479 , -0.02868767, -0.0263032 , -0.22229815],
        [ 0.        ,  0.        ,  0.        ,  1.        ]]) # THIS TF matrix from cloud compare contains scaling factor too
elif "bunny" in base_dir:
    result_T_m2_m1 = np.array([
        [-0.005651696119, -0.009304529987, -0.152641370893,  0.026200454682],
        [ 0.152924671769, -0.000424805272, -0.005636291113,  0.040806733072],
        [-0.000081029211, -0.152745380998,  0.009313870221,  0.052693203092],
        [ 0.0,             0.0,             0.0,             1.0]# THIS TF matrix from cloud compare contains scaling factor too (0.480228)
])

rot = R.from_matrix(result_T_m2_m1[:3,:3])

euler_angles = rot.as_euler('zyx', degrees=False)

# test_M2 = o3d.io.read_point_cloud('/home/rishabh/projects/r2_gaussian/output/foot/point_cloud/iteration_30000/density_test.ply')
test_M2 = o3d.io.read_point_cloud("/home/rishabh/projects/gaussian-splatting/output/bunny_v3/point_cloud/iteration_30000/cleaned_point_cloud.ply")
test_M2.transform(result_T_m2_m1)
o3d.io.write_point_cloud(osp.join(output_dir, "scaled_M2_transformed.ply"), test_M2)

# The TF matrix from cloud compare contains scaling factor too (yes, but still need to store it (to apply to gaussians later and not point cloud))
# s =0.480228
scale = np.loadtxt(osp.join(output_dir, "scale.txt"))

# Open the CSV file for writing
with open(osp.join(output_dir, "global_reg_result.csv"), mode='w', newline='') as file:
    writer = csv.writer(file)

    # Write the scale value as a header
    writer.writerow(["scale"])

    # Write matrix result_T_m2_m1
    writer.writerow(["result_T_m2_m1"])
    for row in result_T_m2_m1:
        writer.writerow(row)

    writer.writerow([])  # Blank line separator

    # Write Euler angles
    writer.writerow(["euler_angles_zyx"])
    writer.writerow(euler_angles)

print(f"Matrices and Euler angles saved successfully!")
print("Transformation matrix obtained from manually aligning the 2pcd using point picking in CloudCompare!")