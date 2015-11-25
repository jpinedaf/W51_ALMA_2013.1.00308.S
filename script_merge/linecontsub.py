threshold_mfs = '2.0mJy'
threshold_freq = '5.0mJy'
import os
if not os.path.exists('test_frequency.image.fits'):
    os.system('rm -rf w51_test_merge_spw3_copy.ms')
    os.system('cp -r w51_test_merge_spw3.ms w51_test_merge_spw3_copy.ms')

    os.system('rm -rf test_frequency.*')
    clean(vis='w51_test_merge_spw3_copy.ms', imagename="test_frequency",
          field="", spw='', mode='channel', outframe='LSRK',
          interpolation='linear', imagermode='mosaic', interactive=False,
          niter=50000, threshold=threshold_freq, imsize=[512,512], cell='0.052arcsec',
          weighting='briggs', phasecenter='J2000 19h23m43.905 +14d30m28.08',
          pbcor=False, usescratch=False, robust=1.0)
    exportfits('test_frequency.image', 'test_frequency.image.fits', dropdeg=True, overwrite=True)
    exportfits('test_frequency.model', 'test_frequency.model.fits', dropdeg=True, overwrite=True)
    for suffix in ('model','flux','psf','residual'):
        os.system('rm -rf test_frequency.{0}'.format(suffix))

    os.system('rm -rf test_mfs.*')
    clean(vis='w51_test_merge_spw3_copy.ms', imagename="test_mfs",
          field="", spw='', mode='mfs', outframe='LSRK',
          interpolation='linear', imagermode='mosaic', interactive=False,
          niter=50000, threshold=threshold_mfs, imsize=[512,512], cell='0.052arcsec',
          weighting='briggs', phasecenter='J2000 19h23m43.905 +14d30m28.08',
          pbcor=False, usescratch=False, robust=1.0)
    exportfits('test_mfs.image', 'test_mfs.image.fits', dropdeg=True, overwrite=True)
    exportfits('test_mfs.model', 'test_mfs.model.fits', dropdeg=True, overwrite=True)
    for suffix in ('model','flux','psf','residual'):
        os.system('rm -rf test_mfs.{0}'.format(suffix))


import numpy as np
import spectral_cube
from astropy import units as u
from astropy.io import fits
from astropy import wcs
# cube = spectral_cube.SpectralCube.read('test_frequency.image.fits').with_spectral_unit(u.Hz)
# cont = cube.min(axis=0)
# contsub = cube-cont
# # temporary hack for issue #251
# contsub._data = contsub._data.value
# contsub = contsub.with_mask(contsub>15*u.mJy)
# ppbeam = np.abs((cube.beam.sr / (cube.wcs.pixel_scale_matrix[0,0]*cube.wcs.pixel_scale_matrix[1,1]*u.deg**2)).decompose())
# hdu = contsub.hdu
# # this scaling may be necessary if setjy is used
# # I found that the cube version was about 70x too low, maybe worse...
# #hdu.data *= ppbeam # because apparently CASA divides by this?
# hdu.writeto('test_contsub_cube.fits', clobber=True)
# header = contsub.header
cubedata = fits.getdata('test_frequency.image.fits')
#cube = spectral_cube.SpectralCube.read('test_frequency.image.fits')
cont = np.percentile(cubedata[1:-1,:,:], 10, axis=0)
contsub = cubedata - cont
contsub[contsub < 0] = 0
#cont = cube.min(axis=0)
#ppbeam = np.abs((cube.beam.sr / (cube.wcs.pixel_scale_matrix[0,0]*cube.wcs.pixel_scale_matrix[1,1]*u.deg**2)).decompose())
header = cubeheader = fits.getheader('test_frequency.image.fits')
#hdu = cont.hdu
#ppbeam = header['BMAJ']*header['BMIN']*2*np.pi/2.35**2/header['CDELT2']**2
hdu = fits.PrimaryHDU(data=contsub, header=header)
# this scaling may be necessary if setjy is used
#hdu.data *= ppbeam # because apparently CASA divides by this?
hdu.writeto('test_contsub_cube.fits', clobber=True)

importfits('test_contsub_cube.fits', 'test_contsub_cube.image',
           overwrite=True, defaultaxes=T,
           defaultaxesvalues=[header['CRVAL1'], header['CRVAL2'],
                              header['CRVAL3'], 'I'])

os.system('rm -rf w51_test_merge_spw3_copy_linecubesub.ms')
split('w51_test_merge_spw3_copy.ms', 'w51_test_merge_spw3_copy_linecubesub.ms', datacolumn='data')

# os.system('rm -rf test_frequency_linecubesub_dirty.*')
# # try using clean to populate the model column
# clean(vis='w51_test_merge_spw3_copy_linecubesub.ms', imagename="test_frequency_linecubesub_dirty",
#       field="", spw='', mode='channel', outframe='LSRK',
#       interpolation='linear', imagermode='mosaic', interactive=False,
#       modelimage='test_contsub_cube.image',
#       niter=0, threshold='50.0mJy',
#       pbcor=False, usescratch=True)
# exportfits('test_frequency_linecubesub_dirty.image', 'test_frequency_linecubesub_dirty.image.fits', dropdeg=True, overwrite=True)
# exportfits('test_frequency_linecubesub_dirty.model', 'test_frequency_linecubesub_dirty.model.fits', dropdeg=True, overwrite=True)
# for suffix in ('image','model','flux','psf','residual'):
#     os.system('rm -rf test_frequency_linecubesub_dirty.{0}'.format(suffix))

im.open('w51_test_merge_spw3_copy_linecubesub.ms')
from astropy import coordinates
c = coordinates.SkyCoord(header['CRVAL1'], header['CRVAL2'], unit=('deg','deg'), frame='fk5')
im.defineimage(nx=cubedata.shape[1],
               cellx='{0}arcsec'.format(header['CDELT2']*3600),
               mode='channel',
               nchan=cubedata.shape[0],
               phasecenter='J2000 {0} {1}'.format(c.ra.to_string(),
                                                  c.dec.to_string())),
os.system('rm -rf model_contsubcube')
im.makemodelfromsd(sdimage='test_contsub_cube.image', modelimage='model_contsubcube')
# apparently images can't be applied across frequency, but models can
#im.ft(model='test_continuum_min.image')
im.ft(model='model_contsubcube')
im.close()
# setjy does some strange scaling
#setjy(vis='w51_test_merge_spw3_copy_linecubesub.ms', model='model_test', usescratch=True,
#      field='', standard='manual')
#
# ft claims there is no frequency overlap between the image and the data
#ft(vis='w51_test_merge_spw3_copy_linecubesub.ms', model='test_continuum_min.image', usescratch=True, nterms=1)

uvsub('w51_test_merge_spw3_copy_linecubesub.ms')

os.system('rm -rf test_mfs_linecubesub.*')
clean(vis='w51_test_merge_spw3_copy_linecubesub.ms', imagename="test_mfs_linecubesub",
      field="", spw='', mode='mfs', outframe='LSRK',
      interpolation='linear', imagermode='mosaic', interactive=False,
      niter=50000, threshold=threshold_mfs, imsize=[512,512], cell='0.052arcsec',
      weighting='briggs', phasecenter='J2000 19h23m43.905 +14d30m28.08',
      pbcor=False, usescratch=False, robust=1.0)
exportfits('test_mfs_linecubesub.image', 'test_mfs_linecubesub.image.fits', dropdeg=True, overwrite=True)
exportfits('test_mfs_linecubesub.model', 'test_mfs_linecubesub.model.fits', dropdeg=True, overwrite=True)
for suffix in ('image','model','flux','psf','residual'):
    os.system('rm -rf test_mfs_linecubesub.{0}'.format(suffix))


os.system('rm -rf test_frequency_linecubesub.*')
clean(vis='w51_test_merge_spw3_copy_linecubesub.ms', imagename="test_frequency_linecubesub",
      field="", spw='', mode='channel', outframe='LSRK',
      interpolation='linear', imagermode='mosaic', interactive=False,
      niter=50000, threshold=threshold_freq, imsize=[512,512], cell='0.052arcsec',
      weighting='briggs', phasecenter='J2000 19h23m43.905 +14d30m28.08',
      pbcor=False, usescratch=False, robust=1.0)
exportfits('test_frequency_linecubesub.image', 'test_frequency_linecubesub.image.fits', dropdeg=True, overwrite=True)
exportfits('test_frequency_linecubesub.model', 'test_frequency_linecubesub.model.fits', dropdeg=True, overwrite=True)
for suffix in ('image','model','flux','psf','residual'):
    os.system('rm -rf test_frequency_linecubesub.{0}'.format(suffix))


