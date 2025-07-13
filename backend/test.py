import open3d as o3d

mesh = o3d.io.read_triangle_mesh("./temp/21a7a2ae-f9a4-40b0-b2bd-f82cc26eaf9c/models/model.glb")
o3d.visualization.draw_geometries([mesh])
