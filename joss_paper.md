---
title: 'STON: SofTware for petrOgraphic visualisatioN'
tags:
  - Python
  - Archaeology
  - Image exploration
  - Petrography
authors:
  - name: Romain Thomas
    orcid: 0000-0001-8385-3276
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Evgenia Dammer
    orcid: 0000-0003-0870-9324
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
affiliations:
 - name: RSE team, The University of Sheffield, Regent Court, The University of Sheffield, 211 Portobello St, Sheffield S1 4DP 
   index: 1
 - name: Rathgen Research Laboratory, Staatliche Museen zu Berlin, Stiftung Preussischer Kulturbesitz, Schloßstrasse 1A, 14059 Berlin
   index: 2
date: 20 January 2025
bibliography: joss_paper.bib

---

# Summary

STON (SofTware for petrOgraphic visualisatioN) is a graphical user interface developed with the objective to ease the inspection of images taken from microscopes. It has been developed in the framework of petrography, with images of minerals but it can be used for whatever images. This tool allows you the user to inspect image in detail, modify image parameters (contrast, brightness, sharpness), compare images side by side, combine images, etc. 
Designed to be user friendly, STON is fully customizable. It is developed in Python using the (PySide6)[https://wiki.qt.io/Qt_for_Python] library for the GUI, Pillow [@Murray:2025] and matplotlib [@Hunter:2007] for image display and operation and scikit-image [@vanderwalt:2014] for deeper image processing. 

# Statement of need

Thin-section petrography is a widely used technique in archaeology for analysing the composition of ceramic and stone objects, as well as investigating their production technology and provenance. This method involves studying thin sections mounted on glass slides under a polarised light microscope to examine microscopic features. A critical aspect of archaeological study is comparing and identifying patterns within these features across multiple samples. However, it is typically only possible to view one sample at a time under the microscope. Therefore, this method relies heavily on visual memory and repeated observations, making the process inefficient and time-consuming, particularly when dealing with hundreds of samples.

This tool is designed to address these challenges by enabling users to observe multiple photomicrographs simultaneously in a single, convenient interface. It facilitates detailed comparisons, clustering, and data recording, which is especially important in ceramic paste analysis. By allowing users to view multiple samples side by side, the software supports efficient sample grouping and evaluation of composition characteristics.

While tailored for the specific requirements of petrographic analysis in archaeology, the software has broader applications for other research fields that rely on visual image analysis. By providing an efficient and scalable tool for comparative analysis, it enhances research processes across various disciplines.

# The graphical user interface

![Main window of STON.\label{fig:mainwindow}](figures/screenshot_main_window.png)


STON was designed to simplify researchers' work by providing powerful tools for image analysis and observation. The main window offers access to several visualization tools, including:

- Zoom Window: Enhances image inspection by allowing closer examination and note-taking. It also displays image metadata (currently supported for .tif files only) and provides options to adjust color, sharpness, brightness, and contrast. Additionally, it includes access to the analysis tool (see next section).
- Side-by-Side Comparison Tool: Enables users to compare images directly.
- Image Cluster Tool: Facilitates the creation of image mashups—combining multiple images into a single composite, which is particularly useful for merging images of the same material sample. It also supports generating meta-images, where all selected images are combined into one comprehensive view.


![Image grouping. Left: Mashup image, Right: meta-image.\label{fig:cluster}](figures/cluster.png)

## Main functionalities

STON provides the user with a quick and easy analysis tool that will identify region of interest in the image it is based on the [measure module](https://scikit-image.org/docs/stable/api/skimage.measure.html) of the skimage library. 
  

# Citations

# Acknowledgements

This work was support by....

# References
