# Gaussian Splat Alignment in Visible Space

This project focuses on aligning two Gaussian splats within either the visible or X-ray domain. The current implementation supports alignment of two 3DGS datasets in the visible RGB space. This work was conducted while affiliated with the National Institute of Informatics, Tokyo.

## Workflow

**Note:** The query map is always denoted with a subscript of **2**, while the closest map is denoted with a subscript of **1**.

### 1. Extract Frames from the Video
Run `extract_img_frames.py` to extract image frames from the video.

### 2. Run COLMAP
- Define the path to the images and specify the output directory.
- Set the camera model to **pinhole**.
- Place images directly in the directory; **do not** create an `images` folder, as this may cause issues with dense reconstruction.
- Ensure the directory structure follows this format. If necessary, create a folder named `0` and move the `.bin` files into it:

```
project/
├── images/
├── sparse/
│   └── 0/
│       ├── cameras.bin
│       ├── images.bin
│       └── points3d.bin
├── stereo/
├── db.db
├── frame_0000.jpg
├── frame_0001.jpg
...
├── frame_0042.jpg
├── Fused.ply
├── Fused.ply.vis
├── run-colmap-geometric.sh
└── run-colmap-photometric.sh
```

### 3. Retrieve the Closest Images
Select a query image from **M2** $( I_{\text{query}}^{M2} )$ and run `image_retrieval_efficient_net_annoy.py` to find the closest corresponding images from **M1**.

### 4. Project 3D Points onto the Closest Image
Run `project_2_image.py` to project $X_1$ onto $I_{\text{close}}^{M1}$.

### 5. Find Matching Points Between the Query and Closest Image
- Run `calc_m2_X1.py` to detect matching points between $I_{\text{query}}^{M2}$ and the projected points in $I_{\text{close}}^{M1}$.
- The script first detects feature matches between `image_query` and `image_closest`. It then filters matches that are within a 5-pixel distance from the projected points and uses these correspondences to estimate $X$ for the Perspective-n-Point (PnP) problem.

### 6. Estimate Scale
Run `scale_pcd.py` to estimate the scaling factor for **M2**. At least one pair of query and closest images is required to compute this. Since the camera poses in both maps are known, the ratio of distances between the camera centers provides the scaling factor.

### 7. Estimate Transformation Using PnP
Run `global_reg.py` to estimate the rotation and translation vectors. *(Further testing is required, as results are inconsistent.)*

### 8. Refine Transformation Using ICP
Run `fine_reg.py` to refine the rotation and translation vectors using Iterative Closest Point (ICP). *(Results are dependent on threshold values; further validation is needed.)*

---

## To-Do List

- **Verify Scaling Factor:** The manually measured scaling factor between `2_b` and `1_b` datasets is approximately **3.262**, but the computed value is around **1**. Further investigation is required.
- ~~**Apply Transformation to Gaussian Splats:**~~ Implemented under `gaussian_splatting-lightning` in `apply_transform.py`. Link: [apply_transform.py](https://github.com/RishabhBajaj25/gaussian-splatting-lightning/blob/gaussian_tf/apply_transform.py).

---

## Additional Tools

- **SuperSplat**: Used for visualizing Gaussian splats. [GitHub Repository](https://github.com/RishabhBajaj25/supersplat/tree/main)
- **3DGS Converter**: Converts Gaussian splats to point clouds, facilitating visualization in MeshLab and comparison of COLMAP localization results with Gaussian splat localization. [GitHub Repository](https://github.com/RishabhBajaj25/3dgsconverter)
