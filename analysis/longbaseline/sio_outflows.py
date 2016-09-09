from spectral_cube import SpectralCube
from astropy import units as u

northcube = SpectralCube.read('/Volumes/passport/alma/w51/longbaseline/W51northcax.SPW0_ALL_medsub_cutout.fits')
northvcube = northcube.with_spectral_unit(u.km/u.s, rest_value=217.10498*u.GHz,
                                          velocity_convention='radio')

northslab = northvcube.spectral_slab(-20*u.km/u.s, 180*u.km/u.s)
northmed = northslab.median(axis=0)
northmslab = northslab-northmed

northsioblue = northmslab.spectral_slab(-32*u.km/u.s, 55*u.km/u.s).moment0()
northsioblue.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_m32to55kms_north.fits', overwrite=True)

northsiored = northmslab.spectral_slab(74*u.km/u.s, 118*u.km/u.s).moment0()
northsiored.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_74to118kms_north.fits', overwrite=True)




e2cube = SpectralCube.read('/Volumes/passport/alma/w51/longbaseline/W51e2cax.SPW0_ALL_medsub_cutout.fits')
e2vcube = e2cube.with_spectral_unit(u.km/u.s, rest_value=217.10498*u.GHz,
                                    velocity_convention='radio')

e2slab = e2vcube.spectral_slab(-20*u.km/u.s, 180*u.km/u.s)
e2slab.allow_huge_operations = True
e2med = e2slab.median(axis=0)
e2mslab = e2slab-e2med

e2sioblue = e2mslab.spectral_slab(-32*u.km/u.s, 55*u.km/u.s).moment0()
e2sioblue.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_m32to55kms_e2.fits', overwrite=True)

e2siored = e2mslab.spectral_slab(74*u.km/u.s, 118*u.km/u.s).moment0()
e2siored.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_74to118kms_e2.fits', overwrite=True)




e8cube = SpectralCube.read('/Volumes/passport/alma/w51/longbaseline/W51e8cax.SPW0_ALL_medsub_cutout.fits')
e8vcube = e8cube.with_spectral_unit(u.km/u.s, rest_value=217.10498*u.GHz,
                                    velocity_convention='radio')

e8slab = e8vcube.spectral_slab(-20*u.km/u.s, 180*u.km/u.s)
e8slab.allow_huge_operations = True
e8med = e8slab.median(axis=0)
e8mslab = e8slab-e8med

e8sioblue = e8mslab.spectral_slab(-32*u.km/u.s, 55*u.km/u.s).moment0()
e8sioblue.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_m32to55kms_e8.fits', overwrite=True)

e8siored = e8mslab.spectral_slab(74*u.km/u.s, 118*u.km/u.s).moment0()
e8siored.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_74to118kms_e8.fits', overwrite=True)






d2cube = SpectralCube.read('/Volumes/passport/alma/w51/longbaseline/W51northwestcax.SPW0_ALL_medsub_cutout.fits')
d2vcube = d2cube.with_spectral_unit(u.km/u.s, rest_value=217.10498*u.GHz,
                                    velocity_convention='radio')

d2slab = d2vcube.spectral_slab(-20*u.km/u.s, 180*u.km/u.s)
d2slab.allow_huge_operations = True
d2med = d2slab.median(axis=0)
d2mslab = d2slab-d2med

d2sioblue = d2mslab.spectral_slab(-32*u.km/u.s, 55*u.km/u.s).moment0()
d2sioblue.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_m32to55kms_d2.fits', overwrite=True)

d2siored = d2mslab.spectral_slab(74*u.km/u.s, 118*u.km/u.s).moment0()
d2siored.write('/Users/adam/work/w51/alma/FITS/longbaseline/SiO_74to118kms_d2.fits', overwrite=True)
