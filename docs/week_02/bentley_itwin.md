# Bentley iTwin Capture Modeler

!!! abstract "Key Takeaways"
    - **Photos + Metadata = 3D Reality**: Photogrammetry works by finding matching points in multiple overlapping photos and using GPS metadata to triangulate their position.
    - **Aerotriangulation (AT) is Critical**: This is the "brain" of the process where the software figures out exactly where the camera was for every shot. If the AT fails, the model fails.
    - **Sparse vs. Dense**: You'll see a "sparse" cloud first (points only). The "dense" reconstruction (the actual model) comes afterward.

---

**Bentley iTwin Capture Modeler** (formerly ContextCapture) is a powerful photogrammetry software used to turn 2D drone photos into 3D models and 2D maps.

## 1. Accessing the Software
*   **Lab Computers:** The software is installed on the lab computers. Search for "iTwin Capture Modeler" in the start menu.
*   **Student License:** If you have a student license code, you can download the software from the Bentley Education portal.

## 2. Standard Workflow

The process of creating a model generally follows these steps:

### Step 1: Create a New Project
1.  Open iTwin Capture Modeler.
2.  Click **New Project**.
3.  Name your project (e.g., `Lab_02_Campus_Map`) and choose a save location.

### Step 2: Import Photos
1.  Select the **Photos** tab or block.
2.  Click **Add Photos** -> **Add entire directory** if your drone photos are in one folder.
3.  The software will read the metadata (GPS locations) automatically.

!!! tip "Pro-Tip: The 'Bad Photo' Hunt"
    Before you start the next step, look through your imported photos. If you see a photo that is blurry, pointed at the ground during takeoff, or far away from the study area, **delete it** from the project. "Garbage in = Garbage out" for 3D modeling!

### Step 3: Aerotriangulation (AT)
This step figures out exactly where each camera was in 3D space when it took the picture.
1.  Click **Submit Aerotriangulation**.
2.  Use the default settings for now.
3.  Click **Submit**.
4.  Wait for the process to finish. When complete, you will see a sparse point cloud of your site.

!!! question "Activity: 3D vs. 2D Thinking"
    Look at the sparse point cloud. Can you recognize the buildings or trees yet? 
    - Which areas have the most points? (Hint: These are usually areas with high "texture" like brick or grass). 
    - Are there any "holes" where points are missing? This often happens on shiny surfaces like car roofs or windows.

### Step 4: Reconstruction & Production
Once the AT is done, you can build your outputs.
1.  Click **New Reconstruction**.
2.  Select the area you want to process (usually the whole box).
3.  Click **Submit Production**.
4.  Choose your desired output format:
    *   **Orthophoto/DSM:** Best for 2D maps, measurements, and elevation models (Format: `TIFF`).
    *   **3D Mesh:** Best for realistic visualizations and fly-throughs (Format: `3MX` or `OBJ`).
    *   **Point Cloud:** Best for engineering analysis and volume calculations (Format: `LAS`).
5.  Click **Submit**.

!!! info "Which format do I need?"
    For most labs in this class, you will need the **Orthophoto (TIFF)** to perform measurements in QGIS.

When the production is finished, you can view the results in the integrated viewer or export the files to use in other software like QGIS.
