# R2Gaussian Renders in Blender

This branch is for aligning R2Gaussians with a 3D model of an object and visualizing the X-ray by using 3D projection mapping. It generates files that `utils/apply_transform.py` can use to apply the transformation to the R2Gaussian. The transformation is applied to the Gaussian splats in the [`gaussian_splatting_lightning`](https://github.com/RishabhBajaj25/gaussian-splatting-lightning) repository. This work was conducted while affiliated with the National Institute of Informatics in collaboration with [Watanabe Lab](https://www.vision.ict.e.titech.ac.jp/).

There can be two cases to use and generate files from this branch:
- **Case 1**: When the X-ray and visual RGB data is taken of the same exact object, alignment can be performed using manual points picked in CloudCompare before using projections.
- **Case 2**: When the R2Gaussian is only a visual representative example (not of the exact object on which projection is to be done), for example in the case of using 3D printed objects to project the X-ray onto, the alignment needs to be done in an ad-hoc manner in Blender.

---

## Dependencies

This project uses the following tools:

- [`CloudCompare`](https://github.com/CloudCompare/CloudCompare) (desktop tool for manual alignment)
- [`gaussian_splatting_lightning`](https://github.com/RishabhBajaj25/gaussian-splatting-lightning) (for transforming and rendering splats)
- [`r2_gaussian`](https://github.com/RishabhBajaj25/r2_gaussian) (for converting .pickle to .ply)
- [`3dgsconverter`](https://github.com/RishabhBajaj25/3dgsconverter)
- [`supersplat`](https://github.com/RishabhBajaj25/supersplat) (for visualization and debugging)

---

## Workflow for Case 1

1. **Project Setup:**
  The project starts with a 3D model of an object (Stanford Bunny) and a blender file containing stereo cameras. The blender file is provided by Watanabe Lab.

2. **Alignment Goal:**
  The goal is to align the R2Gaussian with the 3D model using manual points picked in cloud compare.

3. **Final Output:**
  After this alignment, we can generate stereo image renders which can be used for projection mapping and visualizing the internal structure onto a 3D printed object (of the Stanford Bunny).

4. **Export 3D mesh from blender:**
  Export the 3D model from Blender in `.ply` format. This will be used for alignment with R2Gaussian in CloudCompare.

5. **Convert mesh to point cloud:**
  This can be done in either meshlab or CloudCompare. The point cloud makes it easier to visualize the alignment with R2Gaussian.

6. **Convert R2Gaussians to PLY:**
  If using R2Gaussians, convert the `.pickle` files to `.ply` files using [`stricter_pickle2ply.py`](https://github.com/RishabhBajaj25/r2_gaussian/blob/75c129d1653ee6bfdca2ec74b9aa659e225c0019/stricter_pickle2ply.py).

7. **Clean-up in Supersplat:**
  Clean up the R2Gaussian using [Supersplat](https://github.com/RishabhBajaj25/supersplat/tree/main).

8. **Convert to Point Clouds:**
  Convert the ply of R2Gaussians into point cloud using the [3dgs Convertor](https://github.com/RishabhBajaj25/3dgsconverter).

9. **Import into CloudCompare:**
  Import the point cloud of the blender object and of the R2Gaussian into [CloudCompare](https://github.com/CloudCompare/CloudCompare/tree/master).

10. **Manual Alignment:**
   Perform alignment of the 2 point clouds manually in CloudCompare [click here for more information on alignment](https://www.cloudcompare.org/doc/wiki/index.php/Alignment_and_Registration).

11. **Save Alignment Results:**
   Save the results of the alignment from the CloudCompare console.

12. **Scale Point Cloud:**
   Paste the scale value from the alignment in `scale_pcd.py` and run this script.

13. **Apply Transformation Matrix:**
   Paste the transformation matrix from the alignment in `global_reg.py` and run this script.

14. **Perform ICP:**
   Run `fine_reg.py`. In this case, this transformation doesn't exist, so it needs to be set as $I$ since no ICP is done in case of manual alignment using CloudCompare. Still this file needs to be generated.

15. **Apply transformation to the splat:**
   Once these files are generated, head to `gaussian_splatting_lightning` [repository](https://github.com/RishabhBajaj25/gaussian-splatting-lightning) and run `apply_transform.py` [script](https://github.com/RishabhBajaj25/gaussian-splatting-lightning/blob/main/utils/apply_transform.py) to apply the transformation to the R2Gaussian. This will align the R2Gaussian with the 3D model of the object.

16. **Install Blender plugin for 3DGS:**
   Install Kiri's 3DGS plugin for Blender from [here](https://www.kiriengine.app/blender-addon/3dgs-render). This will allow you to visualize the aligned R2Gaussian in Blender.

17. **Import the file generated from step 15:**
   Import the aligned R2Gaussian file into Blender and adjust the colors and lighting to enhance the visualization.

18. **Recommended settings:**
   * Transparent bounces: 1024
   * HQ mode (blended alpha) with 16 Viewport samples and 3050 Render samples.
   * Render: View Transform: Standard, Look: Very High Contrast, Render Samples 3050
   * Render Engine: Cycles
   * Color settings: Brightness: 0.8, Contrast: 4.0, Hue: 0.7, Saturation 1.0

19. **Final Render:**
   Render the left/right eye disparity images as pleased. these images can be sent to Watanabe lab to be used for projection mapping. Enjoy!

20. **Create anaglyph images:**
    Once the images have been rendered, use `create_single anaglyph` [here](https://github.com/RishabhBajaj25/3DGS_PoseRender/blob/main/create_single_anaglyph.py) to create red/cyan anaglyph image which can help perceive depth using the old school 3D glasses.

21. ** Create stereo images:**
    Use the `create_stereo_img_from_blender.py` [here](https://github.com/RishabhBajaj25/3DGS_PoseRender/blob/main/create_stereo_img_from_blender.py) script to create stereo images. Using this stereo image, the depth effect can be perceived without projection mapping. Use these images and import them to [VaR's VR Video Player](https://play.google.com/store/apps/details?id=com.abg.VRVideoPlayer&hl=en) android app and use it with the VR viewer glasses and phone.

---

## Workflow for Case 2

1. **Prepare R2Gaussian:**
  For this step, do steps 6-7 from Case 1.

2. **Import into Blender:**
  Import the R2Gaussian into Blender using steps 16-17 from Case 1.

3. **Manual Alignment:**
  Manually transform the R2Gaussian in blender to make it align with the 3D model of the object.

4. **Render:**
  Render using the settings mentioned in step 18.

---

## Additional Tools

- **SuperSplat**: Used for visualizing Gaussian splats. [GitHub Repository](https://github.com/RishabhBajaj25/supersplat/tree/main)
- **3DGS Converter**: Converts Gaussian splats to point clouds, facilitating visualization in MeshLab and comparison of COLMAP localization results with Gaussian splat localization. [GitHub Repository](https://github.com/RishabhBajaj25/3dgsconverter)