About MESMA
===========

MESMA is both a QGIS plugin and stand-alone python package that implements the MESMA (Multiple Endmember Spectral
Mixture Analysis) unmixing algorithm in the field of Remote Sensing.

It is based on VIPER Tools: a software package written for ENVI/IDL and released in 2007.
Several updates have been released since and now it has been ported to PyQGIS in the period 2017 - 2020.
The original VIPER Tools is now split over two python/QGIS tools: **Spectral Library Tool** and **MESMA**.

**Spectral Library Tool** provides the following:
 - Creating spectral libraries interactively (selecting spectra from an image or using regions of interest) and managing
   the metadata (developed by HU Berlin)
 - Optimizing spectral libraries with Iterative Endmember Selection, Ear-Masa-Cob or CRES
 - Website: https://spectral-libraries.readthedocs.io
 - Repository: https://bitbucket.org/kul-reseco/spectral-libraries

**MESMA** provides the following:
 - Running SMA and MESMA (with multi-level fusion, stable zone unmixing, ...)
 - Post-processing of the MESMA results (visualisation tool, shade normalisation, ...)
 - Website: https://mesma.readthedocs.io
 - Repository: https://bitbucket.org/kul-reseco/mesma

The software has now been developed in the open source environment to encourage further development of the tool.

Referencing the MESMA tool
==========================

When using the MESMA tool, please use the following citation:

Crabbé, A. H., Somers, B., Roberts, D. A., Halligan, K., Dennison, P., Dudley, K. (2019).
MESMA QGIS Plugin (Version x) [Software]. Available from https://bitbucket.org/kul-reseco/mesma.

Acknowledgements
================

The software and user guide are based on VIPER Tools 2.0 (UC Santa Barbara, VIPER Lab):
Roberts, D. A., Halligan, K., Dennison, P., Dudley, K., Somers, B., Crabbe, A., 2018, Viper Tools User Manual,
Version 2, 91 pp.

MESMA is also using two python packages developed by Benjamin Jakimow and Andreas Rabe:
 - QGISPluginSupport (Benjamin Jakimow, HU Berlin): https://bitbucket.org/jakimowb/qgispluginsupport
 - hub-datacube (Andreas Rabe, HU Berlin): https://bitbucket.org/hu-geomatics/hub-datacube

This revision is funded primarily through BELSPO (the Belgian Science Policy Office) in the framework
of the STEREO III Programme – Project LUMOS - SR/01/321.

Logo's were created for free at https://logomakr.com.

Software Licence
================

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General
Public License as published by the Free Software Foundation; either version 3 of the License, or any later version.

What is new in the Spectral Library Tool 1.0?
=============================================

Differences between Viper Tools 2.0 and The Spectral Library Tool 1.0:
 - The migration to PyQGIS is not just a translation from IDL to Python, but also a serious re-write of the code and a
   revision of the GUI to match the look and feel of other QGIS tools.
 - Library Creation has been revised thoroughly, with integration of GIS: inside QGIS, a spectral library is now
   represented as a vector layer and each spectrum as a feature. This makes it easier to select spectra from a map,
   use polygons for selection and manage features and their metadata via the attribute table.
 - Library Creation now also has extra features to import and save spectral libraries (from raster or vector sources,
   from ASD, CSV, ARTMO, ECOSIS, ENVI en SPECCHIO).
 - The output of the Library Optimization tools has been optimized, breaking backwards compatibility with the IDL tools.
 - The EMC tool also allows for square arrays that have been run in non-reset mode.
