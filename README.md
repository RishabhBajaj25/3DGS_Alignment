# R2Gaussian Renders in Blender

* This branch is for aligning R2Gaussians with a 3D model of an object (Stanford Bunny) using manual points picked in cloud compare.
* It generates files that utils/apply_transform.py can use to apply the transformation to the R2Gaussian. 
* The transformation is applied to the Gaussian splats in the `gaussian_splatting_lightning` repository.
* This work was conducted while affiliated with the National Institute of Informatics.

---

## Working in Blender
1. This part of the project is done in collaboration with [Watanabe Lab](https://www.vision.ict.e.titech.ac.jp/).
2. The project starts with a 3D model of an object (Stanford Bunny) and a blender file containing stereo cameras. The blender file is provided by Watanabe Lab.
3. The goal is to align the R2Gaussian with the 3D model using manual points picked in cloud compare.
4. After this alignment, we can generate stereo image renders which can be used for projection mapping and visualizing the internal structure onto a 3D printed object (of the Stanford Bunny).
4. **Export 3D mesh from blender**: Export the 3D model from Blender in `.ply` format. This will be used for alignment with R2Gaussian in CloudCompare.
5. **Convert mesh to point cloud**: This can be done in either meshlab or CloudCompare. The point cloud makes it easier to visualize the alignment with R2Gaussian.
6. **Pick points in CloudCompare**: Use CloudCompare to pick points on the 3D model and the R2Gaussian. This will help in aligning the two datasets.
7. **Save the scale and transformation**: After picking the points, save the scale and transformation parameters (manually). 
8. **Estimate Scale**: Either make a file `scale.txt` and manually paste the scale obtained from CloudCompare here OR Run `scale_pcd.py` to generate the txt file.
9. **Estimate Transformation Using PnP**: Run `global_reg.py` to generate the files for the transformation. This will be run with `gaussian_splatting_lightning` repository.
10. **Refine Transformation Using ICP**: Run `fine_reg.py` to generate using Iterative Closest Point (ICP). In this case, this transformation doesn't exist, so it needs to be set as $I$ since no ICP is done in case of manual alignment using CloudCompare. Still this file needs to be generated.
11. **Apply transformation to the splat**: Once these files are generated, head to `gaussian_splatting_lightning` [repository](https://github.com/RishabhBajaj25/gaussian-splatting-lightning) and run `apply_transform.py` [script](https://github.com/RishabhBajaj25/gaussian-splatting-lightning/blob/main/utils/apply_transform.py) to apply the transformation to the R2Gaussian. This will align the R2Gaussian with the 3D model of the object.
12. **Convert algined R2Gaussian to 3DGS**: Use the file in `r2_gaussian` [repository](https://github.com/RishabhBajaj25/r2_gaussian) to convert the aligned R2Gaussian to 3DGS format. This will allow you to visualize the aligned R2Gaussian in 3DGS viewer.
13. **Install Blender plugin for 3DGS****: Install Kiri's 3DGS plugin for Blender from [here](https://www.kiriengine.app/blender-addon/3dgs-render). This will allow you to visualize the aligned R2Gaussian in Blender.
14. **Import the file generated from step** 12**: Import the aligned R2Gaussian file into Blender and adjust the colors and lighting to enhance the visualization. 
15. Render images as pleased. Enjoy!

---


## Additional Tools

- **SuperSplat**: Used for visualizing Gaussian splats. [GitHub Repository](https://github.com/RishabhBajaj25/supersplat/tree/main)
- **3DGS Converter**: Converts Gaussian splats to point clouds, facilitating visualization in MeshLab and comparison of COLMAP localization results with Gaussian splat localization. [GitHub Repository](https://github.com/RishabhBajaj25/3dgsconverter)