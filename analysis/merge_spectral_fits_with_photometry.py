"""
Generally meant to be run from merge_outflow_core_tables.py
"""
import numpy as np
import paths
from astropy.table import Table, Column
from astropy import table
from astropy import units as u
import masscalc

spectral_line_fit_tbl = Table.read(paths.tpath('spectral_lines_and_fits.csv'))

cores_merge = Table.read(paths.tpath('core_continuum_and_line.ipac'), format='ascii.ipac')

molcld_exclude_names = ['13COv=0', 'C18O', 'H2CO', 'COv=0']
molcld_exclude = np.array([any(nm in row['Species'] for nm in molcld_exclude_names)
                           for row in spectral_line_fit_tbl])

brightest_noncld_lines = []
brightest_noncld_qns = []
brightest_noncld_fluxes = []
brightest_fitted_brightness = [] 

for row in cores_merge:
    src = row['SourceID']

    amplitudes = spectral_line_fit_tbl['{0}FittedAmplitude'.format(src)]
    noncld_amplitudes = amplitudes * ~molcld_exclude

    brightest_ind = np.argmax(amplitudes)
    brightest_noncloud_ind = np.argmax(noncld_amplitudes)
    if noncld_amplitudes.max() > 0:
        brightest_noncld_lines.append(spectral_line_fit_tbl['Species'][brightest_noncloud_ind])
        brightest_noncld_qns.append(spectral_line_fit_tbl['Resolved QNs'][brightest_noncloud_ind])
        brightest_noncld_fluxes.append(amplitudes[brightest_noncloud_ind])
        brightest_fitted_brightness.append(amplitudes[brightest_noncloud_ind]*spectral_line_fit_tbl['{0}JtoK'.format(src)][brightest_noncloud_ind])
    else:
        brightest_noncld_lines.append('-')
        brightest_noncld_qns.append('-')
        brightest_noncld_fluxes.append(np.nan)
        brightest_fitted_brightness.append(np.nan)


cores_merge.add_column(Column(brightest_noncld_lines, 'BrightestFittedLine'))
cores_merge.add_column(Column(brightest_noncld_qns, 'BrightestFittedQNs'))
cores_merge.add_column(Column(brightest_noncld_fluxes, 'BrightestFittedApMeanFlux', unit=u.Jy))
cores_merge.add_column(Column(brightest_fitted_brightness, 'BrightestFittedApMeanBrightness', unit=u.K))

cores_merge.write(paths.tpath('core_continuum_and_line.ipac'), format='ascii.ipac', overwrite=True)
