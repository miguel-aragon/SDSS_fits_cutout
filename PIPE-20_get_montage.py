#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np

from astropy.io import fits

import subprocess

import glob

# In[2]:


import importlib
import sys
sys.path.insert(0, '/home/maragon/.local/python_utils/')
import idl as idl

from Imaging.image_grids import show_image_row
from Astro.astro_io import mrdfits

import Surveys.sdss_cutout as sdss_cutout
import Surveys.desi_cutout as desi_cutout
importlib.reload(sdss_cutout)
importlib.reload(desi_cutout)


#-----------------------------------------------------
#
#-----------------------------------------------------   
def extract_url(_file):
    f = open(_file, 'r')
    data = f.read()
    f.close()

    urls  = []
    names = []
    for it in data.split(' '):  
        if it.find('http') == 0:
            names.append(it.split('/')[-1])
            urls.append(it.replace('http://data.sdss3', 'https://data.sdss'))
    return names, urls


#-------------------------------------------
#
#
def fix_mProjExec(_file):

    f = open(_file, 'r')
    data = f.read()
    f.close()
    print(">>> -------------------------")
    print(data)
    print("<<< -------------------------")
    url = data.split('"')[-2].replace('&amp;', '&')

    subprocess.call(['wget', '-O', _file+'.fix', url])


sdss  = mrdfits('SDSS_template_final.fits')
scale = np.load('SDSS_template_final_scale.npy')


PATH0 = '/home/maragon/DataCenter/DATA_ALL/SDSS/SDSS_montage/TESTING/Images/'

filters = ['u','g','i','r','z']

VERBOSE = False

for i in range(68, sdss['ra'].shape[0]):
    
    ra_i  = str(sdss['ra'][i])
    dec_i = str(sdss['dec'][i])
    rad_i = str(sdss['petroRad_r'][i]*scale[i]/60/60)

    FILE = str(i).zfill(5)
    
    PATH1 = PATH0 + FILE

    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print(FILE)
    
    subprocess.call(['mkdir', PATH1])
    
    subprocess.call(['mHdr' ,'-p' ,'0.396','"'+ra_i+' '+dec_i+'"', rad_i,  PATH1+'/'+FILE+'.hdr'])

    #fix_mProjExec(PATH1+'/'+FILE+'.hdr')    
    
    for fil_i in filters:
        if VERBOSE == True: print(">>> processing filter ", fil_i)
        PATH2 = PATH1 + '/'+fil_i
        subprocess.call(['mkdir', PATH2])
        subprocess.call(['mkdir', PATH2+'/raw'])
        subprocess.call(['mkdir', PATH2+'/projected'])
    
    
        subprocess.call(['mArchiveList', 'sdss', fil_i, '"'+ra_i+' '+dec_i+'"',rad_i,rad_i, PATH2+'/raw/remote.tbl'])
        names, urls = extract_url(PATH2+'/raw/remote.tbl')

        for name_i, url_i in zip(names, urls):
            #--- Manually download files
            if VERBOSE == True: print(">>>    downloading frame ", name_i)
            subprocess.call(['wget', '-O', PATH2+'/raw/'+name_i, url_i])
            subprocess.call(['bzip2', '-d', PATH2+'/raw/'+name_i])
            
        if VERBOSE == True: print(">>> Adding frames ", fil_i)
        print(">>> mImgtbl: ", PATH2+'/rimages.tbl')
        subprocess.call(['mImgtbl', PATH2+'/raw/' ,PATH2+'/rimages.tbl'])
        print('mImgtbl ' + PATH2+'/raw/ ' + PATH2+'/rimages.tbl')

        print(">>> mProjExec: ",  PATH1+'/'+FILE+'.hdr')
        subprocess.call(['mProjExec','-p',PATH2+'/raw/',PATH2+'/rimages.tbl',PATH1+'/'+FILE+'.hdr',PATH2+'/projected',PATH2+'/stats.tbl'])
        print('mProjExec -p ' + PATH2+'/raw/',PATH2+'/rimages.tbl ' + PATH1+'/'+FILE+'.hdr ' + PATH2+'/projected',PATH2+'/stats.tbl')

        #fix_mProjExec(PATH1+'/'+FILE+'.hdr')

        fils2 = [it.split('/')[-1] for it in glob.glob(PATH2+'/raw/*.fits')] 
        for fil2_i in fils2:
            subprocess.call(['mProject', PATH2+'/raw/'+fil2_i, PATH2+'/projected/'+fil2_i, PATH1+'/'+FILE+'.hdr'])

        print(">>> mImgtbl")
        subprocess.call(['mImgtbl',  PATH2+'/projected', PATH2+'/pimages.tbl'])
        
        print(">>> mAdd")
        subprocess.call(['mAdd', '-p', PATH2+'/projected', PATH2+'/pimages.tbl', PATH1+'/'+FILE+'.hdr', PATH1+'/'+fil_i+'.fits'])
        
        if VERBOSE == True: print(">>> cleaning up ")
        print(">>> " + 'rm -rf '+ PATH2)
        subprocess.call(['rm', '-rf', PATH2])
        print(">>> " + 'rm -rf '+ PATH1+'/'+fil_i+'_area.fits')
        subprocess.call(['rm', '-rf', PATH1+'/'+fil_i+'_area.fits'])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




