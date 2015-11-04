clearcal(vis='w51_test_small.ms')
os.system('rm -rf test_channel_dirty.*')
flagmanager(vis='w51_test_small.ms', versionname='flagdata_1', mode='restore')
clean(vis='w51_test_small.ms', imagename="test_channel_dirty", field="", spw='',
      mode='channel', outframe='LSRK', interpolation='linear', imagermode='mosaic',
      interactive=False, niter=0, threshold='250.0mJy', imsize=[512,512],
      cell='0.06arcsec', phasecenter='J2000 19h23m43.905 +14d30m28.08',
      start=53, nchan=1,
      weighting='briggs', usescratch=True, pbcor=False, robust=-2.0)
exportfits('test_channel_dirty.image', 'test_channel_dirty.image.fits', dropdeg=True, overwrite=True)
os.system('rm -rf test_channel.*')
clean(vis='w51_test_small.ms', imagename="test_channel", field="", spw='',
      mode='channel', outframe='LSRK', interpolation='linear', imagermode='mosaic',
      interactive=False, niter=1000, threshold='250.0mJy', imsize=[512,512],
      cell='0.06arcsec', phasecenter='J2000 19h23m43.905 +14d30m28.08',
      start=53, nchan=1,
      weighting='briggs', usescratch=True, pbcor=False, robust=-2.0)
exportfits('test_channel.image', 'test_channel.image.fits', dropdeg=True, overwrite=True)

gaincal(vis='w51_test_small.ms', caltable="phase.cal", field="", solint="30s",
        calmode="p", refant="", gaintype="G", uvrange='0~400')
#plotcal(caltable="phase.cal", xaxis="time", yaxis="phase", subplot=331,
#        iteration="antenna", plotrange=[0,0,-30,30], markersize=5,
#        fontsize=10.0,)

flagmanager(vis='w51_test_small.ms', mode='save', versionname='backup')
applycal(vis="w51_test_small.ms", field="", gaintable=["phase.cal"],
         interp="linear")
flagmanager(vis='w51_test_small.ms', mode='restore', versionname='backup')
os.system('rm -rf w51_test_small_selfcal.ms')
os.system('rm -rf w51_test_small_selfcal.ms.flagversions')
split(vis="w51_test_small.ms", outputvis="w51_test_small_selfcal.ms",
      datacolumn="corrected")

os.system('rm -rf test_selfcal_channel.*')
clean(vis='w51_test_small_selfcal.ms', imagename="test_selfcal_channel",
      multiscale=[0,3,6,12], field="", spw='', mode='channel', outframe='LSRK',
      interpolation='linear', imagermode='mosaic', interactive=False,
      niter=1000, threshold='250.0mJy', imsize=[512,512], cell='0.06arcsec',
      phasecenter='J2000 19h23m43.905 +14d30m28.08', weighting='briggs',
      start=53, nchan=1,
      usescratch=True, pbcor=False, robust=-2.0)
exportfits('test_selfcal_channel.image', 'test_selfcal_channel.image.fits', dropdeg=True, overwrite=True)

os.system("rm -rf phase_2.cal")
gaincal(vis="w51_test_small_selfcal.ms", caltable="phase_2.cal", field="",
        solint="30s", calmode="p", refant="", gaintype="G", uvrange='0~400')
#plotcal(caltable="phase_2.cal", xaxis="time", yaxis="phase", subplot=331,
#        iteration="antenna", plotrange=[0,0,-30,30], markersize=5,
#        fontsize=10.0,)


flagmanager(vis='w51_test_small_selfcal.ms', mode='save', versionname='backup')
applycal(vis="w51_test_small_selfcal.ms", field="", gaintable=["phase_2.cal"],
         interp="linear")
flagmanager(vis='w51_test_small_selfcal.ms', mode='restore', versionname='backup')
os.system('rm -rf w51_test_small_selfcal_2.ms')
os.system('rm -rf w51_test_small_selfcal_2.ms.flagversions')
split(vis="w51_test_small_selfcal.ms", outputvis="w51_test_small_selfcal_2.ms",
      datacolumn="corrected")

os.system('rm -rf test_selfcal_2_channel.*')
clean(vis='w51_test_small_selfcal_2.ms', imagename="test_selfcal_2_channel",
      multiscale=[0,3,6,12], field="", spw='', mode='channel', outframe='LSRK',
      interpolation='linear', imagermode='mosaic', interactive=False,
      niter=1000, threshold='250.0mJy', imsize=[512,512], cell='0.06arcsec',
      phasecenter='J2000 19h23m43.905 +14d30m28.08', weighting='briggs',
      start=53, nchan=1,
      usescratch=True, pbcor=False, robust=-2.0)
exportfits('test_selfcal_2_channel.image', 'test_selfcal_2_channel.image.fits', dropdeg=True, overwrite=True)

os.system("rm -rf phase_3.cal")
gaincal(vis="w51_test_small_selfcal_2.ms", caltable="phase_3.cal", field="",
        solint="30s", calmode="p", refant="", gaintype="G", uvrange='0~400')
#plotcal(caltable="phase_3.cal", xaxis="time", yaxis="phase", subplot=331,
#        iteration="antenna", plotrange=[0,0,-30,30], markersize=5,
#        fontsize=10.0,)

