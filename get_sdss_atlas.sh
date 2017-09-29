#!/bin/bash
#
# Cutout fits images from SDSS
#
# Adapted from Inseok Song, 2007
#   http://irsa.ipac.caltech.edu/docs/howto/DSS_pleiades_mosaic.html
#
# Arguments:
#   $1 ra
#   $2 dec
#   $3 size
#   $4 base_name
#
# Usage: sh get_sdss_atlas.sh 199.54198 -1.2436732 0.05 gal_000
#
# Miguel Aragon-Calvo 2017
#
#
echo ra   $1
echo dec  $2
echo size $3
echo file $4

#--- Working directory
mkdir $4;
cd $4;

mHdr -p 0.4 "\"$1 $2\"" $3 $4.hdr

for bands in u g r i z; do echo Processing ${bands};
			   mkdir $bands;
			   cd $bands;
			   mkdir raw projected;
			   cd raw;
			   mArchiveList sdss ${bands} "\"$1 $2\"" $3 $3 remote.tbl;
			   mArchiveExec remote.tbl;
			   cd .. ;
			   mImgtbl raw rimages.tbl ;
			   mProjExec -p raw rimages.tbl ../$4.hdr projected stats.tbl ;
			   mImgtbl projected pimages.tbl ;
			   mAdd -p projected pimages.tbl ../$4.hdr ${bands}.fits ;
			   cd .. ;
done


cd .. ;

#mJPEG -blue $4/g/g.fits -1s "99.999%" gaussian-log -green $4/r/r.fits -1s "99.999%" gaussian-log -red $4/i/i.fits -1s "99.999%" gaussian-log -out $4.jpg
