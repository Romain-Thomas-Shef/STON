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
Designed to be user friendly, STON is fully customizable. It is developed in Python using the (PySide6)[https://wiki.qt.io/Qt_for_Python] library for the GUI, Pillow [@Murray:2025] and matplotlib [@Hunter:2007] for image display and operation and scikit analysis [@Pedregosa:2011] for deeper image processing. 

# Statement of need

Thin-section petrography is a widely used technique in archaeology for analysing the composition of ceramic and stone objects, as well as investigating their production technology and provenance. This method involves studying thin sections mounted on glass slides under a polarised light microscope to examine microscopic features. A critical aspect of archaeological study is comparing and identifying patterns within these features across multiple samples. However, it is typically only possible to view one sample at a time under the microscope. Therefore, this method relies heavily on visual memory and repeated observations, making the process inefficient and time-consuming, particularly when dealing with hundreds of samples.

This tool is designed to address these challenges by enabling users to observe multiple photomicrographs simultaneously in a single, convenient interface. It facilitates detailed comparisons, clustering, and data recording, which is especially important in ceramic paste analysis. By allowing users to view multiple samples side by side, the software supports efficient sample grouping and evaluation of composition characteristics.

While tailored for the specific requirements of petrographic analysis in archaeology, the software has broader applications for other research fields that rely on visual image analysis. By providing an efficient and scalable tool for comparative analysis, it enhances research processes across various disciplines.



# The graphical user interface

## GUI: Main window

## Secondary windows


# Citations

Citations to entries in paper.bib should be in
[rMarkdown](http://rmarkdown.rstudio.com/authoring_bibliographies_and_citations.html)
format.

If you want to cite a software repository URL (e.g. something on GitHub without a preferred
citation) then you can do it with the example BibTeX entry below for @fidgit.

For a quick reference, the following citation commands can be used:
- `@author:2001`  ->  "Author et al. (2001)"
- `[@author:2001]` -> "(Author et al., 2001)"
- `[@author1:2001; @author2:2001]` -> "(Author1 et al., 2001; Author2 et al., 2002)"

# Figures

# Acknowledgements

This work was support by....

# References
