In this work we study sound as a possible chronic stressor of an Antarctic Specially Protected Area (ASPA). Recorings where made in Fildes Peninsula, part of King George/South Shetland Island, at two specific points. 1) Ardley site, located inside Ardley Island (which is the ASPA)
and 2) Frei site, located near a conglomerate of research stations within a distance of approximately 2km from the ASPA. 

The main goal of this work was to quantify the presence of a power generator noise inside the ASPA, with the source coming from Frei site. For that we implemented a continuous sound monitoring protocol, recording 5 minutes of every hour for 24hs during all days of 2022-2023 Antarctic Summer Campaign.
These recordings where made with Audiomoth devices at a sample rate of 48kHz and Mid-High gain. 

To quantify the noise we developed an automatic detection algorithm and cross-validate it with perceptual and meterological data. At first we characterize the source by its fundamental frequency (see **generator_characterization.py**, recordings can be found [here](https://doi.org/10.5281/zenodo.14803434)). We use
this information to evaluate the presence of this frequency component in the recordings made at [Ardley](https://doi.org/10.5281/zenodo.14780840) and [Frei](https://doi.org/10.5281/zenodo.14801757) site (see **detection_around_75Hz.py**). 

![](https://github.com/m-anzibarfialho/Power-generator-detector/blob/main/Figure_2%20(1).jpg)
