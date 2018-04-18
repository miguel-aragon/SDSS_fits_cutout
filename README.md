# SDSS_fits_cutout

Easy download cutout fits images from the SDSS (www.sdss.org) database. This script is based on the DSS_pleiades_mosaic script 
http://irsa.ipac.caltech.edu/docs/howto/DSS_pleiades_mosaic.html

Since quite some time I have been trying to get image cutouts from the SDSS in fits format. The jpg images in the SDSS cutout service are ok for simple tasks but not for anything serious (like training a neural network). Recently, a colleague told me about Montage, a great tool to automate fits cutout, mosaic generation, coverage masks etc. Since Montage doesn’t include a script to retrieve SDSS cutouts in a simple way I wrote the following bash script based on Inseok Song’s pleiades script.

You need to install Montage first and add Montage’s bin folder to your PATH

Download and install Montage:

http://montage.ipac.caltech.edu/

Add Montage’s bin folder to your path, this can be done in your .bashrc file. My Montage installation is in /home/miguel/Packages/Montage:

```bash
export PATH="/home/miguel/Packages/Montage/bin:$PATH"
```


The included python script (make_fits.py) shows how to use the make_lupton_rgb() function in the astropy library to convert the fits files to a regular rgb image roughly following the schema used to produce the SDSS sky images.


