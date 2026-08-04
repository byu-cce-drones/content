<h2>QGIS for Civil Engineering: Measuring Area and Distance from Drone Imagery</h2>

<p>QGIS is a free, open-source GIS platform that's become a go-to tool for civil engineering students working with drone-captured orthomosaics. Because an orthomosaic is georeferenced, every pixel corresponds to a real-world coordinate — so QGIS can turn that aerial image into actual measurements: distances for pipeline runs or drainage paths, and areas for earthwork pads, stockpiles, or impervious surfaces. Pair it with a DEM/DSM and you can even estimate cut/fill volumes, making it useful for site surveys, grading checks, and as-built verification.</p>

<p>The basic workflow is simple: import the orthomosaic as a raster layer file (GeoTIFF), confirm it's in a projected CRS with real-world units (not degrees), then use the <strong>Measure Line</strong> and <strong>Measure Area</strong> tools to click directly on the image for instant readouts. For more precise or reusable work, features can be digitized into a vector layer and exported for reporting or CAD. Because it's free, cross-platform, and easy to pick up for basic tasks while still scaling up to more advanced terrain and drainage analysis, QGIS is a practical entry point for students before they hit professional GIS work.</p>

<h3>How to Download QGIS (Mac &amp; PC)</h3>
<ol>
  <li>Go to the official QGIS download page (you will be prompted to donate to the creators, but it is by no means required): <strong>qgis.org/download</strong></li>
  <li>Select your operating system (<strong>Windows</strong> or <strong>macOS</strong>) from the download options</li>
  <li>Choose a version — the <strong>Long Term Release (LTR)</strong> is recommended for stability; the Latest Release includes newer features but may be less stable</li>
  <li>Download the installer file (<strong>.msi</strong> for Windows, <strong>.dmg</strong> for Mac)</li>
  <li>Run the installer:
    <ul>
      <li><strong>Windows:</strong> Open the downloaded .msi file and follow the setup wizard (accept the license, keep default install options, click Install)</li>
      <li><strong>Mac:</strong> Open the downloaded .dmg file and drag the QGIS icon into your Applications folder</li>
    </ul>
  </li>
  <li>Launch QGIS from your Start Menu (Windows) or Applications folder (Mac)
    <ul>
      <li><strong>Mac only:</strong> If the first launch is blocked by security settings, control-click the QGIS icon and select <strong>Open</strong>, then confirm in the dialog that appears</li>
    </ul>
  </li>
</ol>