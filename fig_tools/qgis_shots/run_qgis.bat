@echo off
call C:\OSGeo4W\bin\o4w_env.bat
path %OSGEO4W_ROOT%\apps\qgis\bin;%PATH%
set QGIS_PREFIX_PATH=%OSGEO4W_ROOT:\=/%/apps/qgis
set GDAL_FILENAME_IS_UTF8=YES
set VSI_CACHE=TRUE
set VSI_CACHE_SIZE=1000000
set QT_PLUGIN_PATH=%OSGEO4W_ROOT%\apps\qgis\qtplugins;%OSGEO4W_ROOT%\apps\qt5\plugins
"%OSGEO4W_ROOT%\bin\qgis-bin.exe" --nologo --noversioncheck --profiles-path G:\GIT_Repo\byu-cce-drones-content\.claude\local\scratch\qgis\profiles --profile capture --code %~dp0capture.py
