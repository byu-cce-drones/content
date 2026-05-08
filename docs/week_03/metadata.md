# Metadata for Aerial Measurements

!!! abstract "Key Takeaways"
    - **Metadata** is "data about data"—the context that makes an image useful.
    - For drones, the most critical metadata is **Location** (GPS), **Time**, and **Orientation**.
    - **EXIF** is the standard format used to store this information inside image files.
    - Accurate metadata is essential for photogrammetry and 3D modeling.

---

## 1. What is Metadata?

In the simplest terms, **metadata** is "data about data." 

Think of a **can of soup** in your pantry. 
*   The **data** is the soup inside the can (the actual content you want).
*   The **metadata** is the label on the outside: the ingredients, nutritional facts, expiration date, and manufacturer. 

Without the label (metadata), you wouldn't know if the soup is tomato or chicken noodle, or if it expired three years ago. The soup exists, but it's hard to use safely or effectively.

---

## 2. Why Metadata Matters for Drones

When we fly drones to take measurements or photos, the images themselves are our **data**. However, a photo of a construction site or a cornfield isn't very useful on its own if we don't know the context.

For aerial measurements, the most critical metadata includes:

1.  **Location (Geospatial Data):** 
    *   **Latitude and Longitude:** Exactly where on Earth was the drone when it took the picture?
    *   **Altitude:** How high above the ground was it? (This affects the scale of the image—how big things look).
2.  **Time (Temporal Data):** 
    *   **Timestamp:** When was the image captured? This is crucial for tracking changes over time (e.g., "How much did the construction site progress between Monday and Friday?").
3.  **Orientation:**
    *   **Heading (Yaw):** Which direction was the drone facing?
    *   **Gimbal Pitch:** Was the camera looking straight down (nadir) or at an angle (oblique)?

---

## 3. EXIF Data

Most digital cameras, including those on drones, automatically save this metadata inside the image file itself. This format is called **EXIF** (Exchangeable Image File Format).

If you take a photo with a drone and open the file properties on your computer, you can often see this hidden information. It tells software (like photogrammetry tools) exactly how to stitch the photos together to create a 3D model or a map.

!!! info "Digital Detective: Finding EXIF Data"
    You can check the metadata of any photo on your own computer:
    - **Windows:** Right-click an image > **Properties** > **Details** tab.
    - **Mac:** Right-click an image > **Get Info** > **More Info** section.
    - **Mobile:** Open the photo in your gallery and look for an "i" icon or "Details" menu.
    
    *Try this with a photo you've taken recently! Can you find the GPS coordinates or the camera settings (ISO, Shutter Speed)?*

---

## 4. Summary & Privacy

*   **Data** = The image or measurement itself.
*   **Metadata** = The "who, what, when, where, and how" of that data.

!!! warning "A Note on Privacy"
    Because metadata often includes exact GPS coordinates, many social media platforms (like Instagram or Facebook) automatically strip metadata from your photos when you upload them to protect your privacy. However, for engineering and surveying, we **must** keep this data intact for our tools to work!

Always ensure your drone's settings are correct (especially the clock and GPS connection) so your metadata is accurate. **Bad metadata can make good data useless!**
