import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import make_lupton_rgb
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename
import scipy.misc


file_name = 'gal_000'
PATH = 'gal_000/'

g = fits.open(PATH+'g/g.fits')[0].data
r = fits.open(PATH+'r/r.fits')[0].data*0.8
i = fits.open(PATH+'i/i.fits')[0].data*0.7

rgb = make_lupton_rgb(i, r, g, Q=10, stretch=0.3, minimum=0.0)

scipy.misc.imsave(file_name+'.png', rgb)


#plt.imshow(rgb_default, origin='lower')

#plt.imshow(rgb, origin='lower')
