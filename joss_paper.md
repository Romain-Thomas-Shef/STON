---
title: 'STON: SofTware for petrOgraphic visualisatioN'
tags:
  - Python
  - Archeology
  - Image exploration
authors:
  - name: Romain Thomas
    orcid: 0000-0001-8385-3276
    equal-contrib: true
    affiliation: "1" # (Multiple affiliations must be quoted)
  - name: Evgenia Dammer
    equal-contrib: true # (This is how you can denote equal contributions between multiple authors)
    affiliation: 2
affiliations:
 - name: RSE team, The University of Sheffield, Regent Court, The University of Sheffield, 211 Portobello St, Sheffield S1 4DP 
   index: 1
 - name:
   index: 2
date: 20 January 2025
bibliography: joss_paper.bib

---

# Summary

STON (SofTware for petrOgraphic visualisatioN) is a graphical user interface developed with the objective to ease the inspection of images taken from microscopes. It has been developed in the framework of petrography, with images of minerals but it can be used for whatever images. This tool allows you the user to inspect image in detail, modify image parameters (contrast, brightness, sharpness), compare images side by side, combine images, etc. 
Designed to be user friendly, STON is fully customizable. It is developed in Python using the (PySide6)[https://wiki.qt.io/Qt_for_Python] library for the GUI, Pillow [@Murray:2025] and matplotlib [@Hunter:2007] for image display and operation and scikit analysis [@Pegregosa:2011] for deeper image processing. 

# Statement of need

--> Evgenia you should write the Statement of need :)  

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
