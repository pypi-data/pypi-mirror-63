# SpectroscPy 0.1.0
# SpectroscPy is a script package developed by and containing contributions from

    # Karen Oda Hjorth Dundas
    # Magnus Ringholm
    # Yann Cornation
    # Benedicte Ofstad

# The package is released under a LGPL licence.
# For questions, please contact on karen.o.dundas@uit.no

# Integration tests for SpectroscPy

import os
import numpy as np
import pytest
from spectroscpy import SpectroscPy_run

def test_SpectroscPy_run():

    data_dir = '{0}/'.format(os.path.dirname(__file__))

    ###############################################
    # Testing various combinations of spectra
    ###############################################

    # IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/m'
    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[1.70424946e-05, 7.11347711e-06, 1.16235812e-06, 2.59612870e-05, 9.52361364e-09, \
                        7.56689106e-05], [], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.']
    names = [data_dir,'hf_H2O2.rsp_tensor', 'H2O2.mol']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # With Raman, 'Raman: CPG 45+4, a.u.'
    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[1.70424946e-05, 7.11347711e-06, 1.16235812e-06, 2.59612870e-05, 9.52361364e-09, \
                        7.56689106e-05], [[0.07930255, 0.45635755, 0.0458494 , 0.01015121, 0.07769959, \
                        0.03215856], [0.08495927, 0.49572019, 0.04674917, 0.0103366 , 0.08624967, \
                        0.03293001]], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR', 'Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.', 'Raman: CPG 45+4, a.u.']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # Also with hyper Raman
    ref_intensities = [[1.70424946e-05, 7.11347711e-06, 1.16235812e-06, 2.59612870e-05, 9.52361364e-09, \
                        7.56689106e-05], [[0.07930255, 0.45635755, 0.0458494 , 0.01015121, 0.07769959, \
                        0.03215856], [0.08495927, 0.49572019, 0.04674917, 0.0103366 , 0.08624967, \
                        0.03293001]], [[9.85551833e-101, 3.35681974e-101, 1.06694277e-101,  5.46408614e-101, 1.24271719e-102, 4.79330164e-100], [3.82565832e-106, \
                        1.37469213e-106, 1.76919208e-108, 5.47227480e-108, 8.67017002e-110, \
                        7.20503289e-111]], [[8.00059356e-102, 5.40734225e-102, 2.43932466e-102, \
                        8.79663799e-102, 1.88164067e-103, 5.79703442e-101], [3.04266736e-107, \
                        2.43369330e-107, 3.50106218e-109, 8.84144861e-109, 9.51538090e-111, \
                        8.58568255e-112]]]

    spectroscopy_type = ['IR', 'Raman', 'Hyper Raman']    
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #############################################
    # Testing other frequency units
    #############################################

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/cm'
    ref_wn = [4148.47683024, 4141.04282853, 1781.48022177, 1589.13503803, 1486.97905661, 182.99945651]
    ref_intensities = [[1.70424946e-05, 7.11347711e-06, 1.16235812e-06, 2.59612870e-05, \
                        9.52361364e-09, 7.56689106e-05], [], [], []]
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/cm', 'IR: SSDG, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: 1/s'
    ref_wn = [1.24368207e+14, 1.24145341e+14, 5.34074335e+13, 4.76410699e+13, 4.45785106e+13, \
              5.48618569e+12]
    spectroscopy_specification = ['Vib modes: 1/s', 'IR: SSDG, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # Only IR with SSDG a.u., outproj, single snapshot, 'Vib modes: Eh'
    ref_wn = [0.01890185, 0.01886798, 0.00811702, 0.00724063, 0.00677518, 0.00083381]
    spectroscopy_specification = ['Vib modes: Eh', 'IR: SSDG, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    ##########################################
    # Testing IR without outprojection
    ##########################################
    ref_wn = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, 1.48698110e+05, \
              1.83061036e+04, 4.66792909e+02, 2.28608186e+02, 3.76592066e+00, 1.78308846e+00, \
              2.00676340e-16, 6.82319818e-14]
    ref_intensities = [[1.70425815e-05, 7.11360916e-06, 1.16243696e-06, 2.59611627e-05, 9.52928458e-09, \
                        7.56686604e-05, 4.15214594e-06, 1.41336245e-09, 1.03022827e-14, 6.28763989e-14, \
                        6.88801500e-14, 2.09588423e-05], [], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #########################################
    # Testing various IR units
    #########################################

    # IR 'IR: SSDG, C**2/kg'
    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[4.80247329e-13, 2.00453540e-13, 3.27545582e-14, 7.31573576e-13, 2.68369749e-16, \
                        2.13230475e-12], [], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['IR']
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, C**2/kg']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # IR 'IR: SSDG, D2A2/amu'
    ref_intensities = [[7.16729788e-01, 2.99160484e-01, 4.88834942e-02, 1.09181362e+00, 4.00519861e-04, \
                        3.18229012e+00], [], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: SSDG, D2A2/amu']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # IR 'IR: MDAC, m**2/(s*mol)'
    ref_intensities = [[2.47758955e+13, 1.03413714e+13, 1.68980328e+12, 3.77417830e+13, 1.38451595e+10, \
                        1.10005317e+14], [], [], []]

    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, m**2/(s*mol)']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # IR 'IR: MDAC, L/(cm*s*mol)'
    ref_intensities = [[2.47758955e+14, 1.03413714e+14, 1.68980328e+13, 3.77417830e+14, 1.38451595e+11, \
                        1.10005317e+15], [], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: MDAC, L/(cm*s*mol)']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # IR 'IR: NIMAC, m/mol'
    ref_intensities = [[3.02861786e+04, 1.26413440e+04, 2.06562397e+03, 4.61357442e+04, 1.69243922e+01, \
                        1.34471049e+05], [], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, m/mol']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # IR 'IR: NIMAC, km/mol'
    ref_intensities = [[3.02861786e+01, 1.26413440e+01, 2.06562397e+00, 4.61357442e+01, 1.69243922e-02, \
                        1.34471049e+02], [], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'IR: NIMAC, km/mol']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    ##########################################
    # Testing Raman without outprojection
    ##########################################
    # 'Raman: CPG 45+4, a.u.'
    ref_wn = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, 1.48698110e+05, \
              1.83061036e+04, 4.66792909e+02, 2.28608186e+02, 3.76592066e+00, 1.78308846e+00, \
              2.00676340e-16, 6.82319818e-14]
    ref_intensities = [[], [[7.93028424e-02, 4.56357234e-01, 4.58507534e-02, 1.01512626e-02, \
                        7.76989345e-02, 3.21671155e-02, 1.60659179e-02, 5.49605023e-03, 6.02922285e-10, \
                        1.06834364e-09, 3.10284231e-10, 2.09492567e-02], [8.49595795e-02, \
                        4.95719846e-01, 4.67506291e-02, 1.03366556e-02, 8.62489799e-02, 3.29389362e-02, \
                        1.68834189e-02, 5.83206659e-03, 6.39431311e-10, 1.13117595e-09, 3.26647263e-10, \
                        2.18399868e-02]], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+4, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    ###########################################
    # Testing Raman with different temperature
    ###########################################
    # 'Raman: CPG 45+4, a.u.'
    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[], [[0.07930255, 0.45635755, 0.0458494 , 0.01015121, 0.07769959, 0.03215856], \
                       [0.08495927, 0.49572019, 0.04674917, 0.0103366 , 0.08624967, 0.03293001]], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+4, a.u.']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 500)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #########################################
    # Testing various Raman units
    #########################################

    # 'Raman: CPG 45+7, a.u.'
    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[], [[0.13877932, 0.56428613, 0.07978227, 0.01776461, 0.10018108, 0.05627554], \
                       [0.14867857, 0.61365418, 0.08134747, 0.01808905, 0.11121732, 0.05762325]], [], []]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Raman']
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: CPG 45+7, a.u.']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # 'Raman: PCPG 45+4, Å^4/amu'
    ref_intensities = [[], [[11.33579065, 65.23338327,  6.55387684,  1.45104975, 11.10665772, \
                        4.59686046], [12.14438241, 70.86002056,  6.68249426,  1.47755042, 12.32883741, \
                        4.70713297]], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: PCPG 45+4, Å^4/amu']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # 'Raman: PCPG 45+7, Å^4/amu'
    ref_intensities = [[], [[19.83761352, 80.66108141, 11.40436285,  2.53933706, 14.32024325, \
                        8.04422734], [21.25264742, 87.71792697, 11.6280985 ,  2.58571323, 15.89780238, \
                        8.236874  ]], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: PCPG 45+7, Å^4/amu']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # 'Raman: SCS 45+4, SI arb units'
    ref_intensities = [[], [[1.85414028e-29, 1.06126499e-28, 8.48762513e-31, 1.33348242e-31, \
                        8.35971680e-31, 3.78651284e-34], [6.73119760e-27, 3.94114608e-26, \
                        1.42095339e-26, 3.65739856e-27, 3.32639854e-26, 7.75759390e-26]], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: SCS 45+4, SI arb units']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    # 'Raman: SCS 45+7, SI arb units'
    ref_intensities = [[], [[3.24474221e-29, 1.31225421e-28, 1.47692670e-30, 2.33359423e-31, \
                        1.07785061e-30, 6.62616810e-34], [1.17795837e-26, 4.87876183e-26, \
                        2.47257765e-26, 6.40044748e-27, 4.28932792e-26, 1.35747862e-25]], [], []]
    spectroscopy_specification = ['Vib modes: 1/m', 'Raman: SCS 45+7, SI arb units']

    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #############################################
    # Testing Hyper Raman without outprojection
    #############################################

    ref_wn = [4.14848132e+05, 4.14105192e+05, 1.78147036e+05, 1.58912905e+05, 1.48698110e+05, \
              1.83061036e+04, 4.66792909e+02, 2.28608186e+02, 3.76592066e+00, 1.78308846e+00, \
              2.00676340e-16, 6.82319818e-14]
    ref_intensities = [[], [], [[9.85549499e-101, 3.35679874e-101, 1.06696937e-101, 5.46410276e-101, \
                        1.24273163e-102, 4.79110170e-100, 1.29596830e-097, 6.99273981e-098, \
                        2.84695831e-101, 3.37310007e-100,             np.inf,             np.inf], \
                       [3.82566612e-106, 1.37469568e-106, 1.76919292e-108, 5.47220679e-108, \
                        8.67032099e-110, 7.21145931e-111, 8.56086890e-115, 2.69279948e-116, \
                        8.05707043e-127, 4.78087853e-127,             np.inf,             np.inf]], \
                      [[8.00057305e-102, 5.40731618e-102, 2.43935820e-102, 8.79665600e-102, \
                        1.88154206e-103, 5.79384626e-101, 3.39043475e-098, 1.79744049e-098, \
                        8.29443860e-102, 6.86173729e-101,             np.inf,             np.inf], \
                       [3.04267284e-107, 2.43370332e-107, 3.50101973e-109, 8.84133056e-109, \
                        9.51567543e-111, 8.59242628e-112, 2.23372492e-115, 6.71451880e-117, \
                        2.31448961e-127, 9.28443974e-128,             np.inf,             np.inf]]]
    run_specification = ['Single snapshot',  'No FraME', 'No outproj']
    spectroscopy_type = ['Hyper Raman']
    spectroscopy_specification = ['Vib modes: 1/m']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #################################################
    # Testing Hyper Raman with different temperature
    #################################################

    ref_wn = [414847.68302357, 414104.28285256, 178148.02217701, 158913.50380254, 148697.90566093, \
              18299.94565116]
    ref_intensities = [[], [], [[9.85558277e-101, 3.35684217e-101, 1.07311924e-101, 5.51854262e-101, \
                        1.25922078e-102, 6.86920935e-100], [3.82568333e-106, 1.37470132e-106, \
                        1.77943383e-108, 5.52681289e-108, 8.78531200e-110, 1.03254256e-110]], \
                      [[8.00064588e-102, 5.40737837e-102, 2.45344577e-102, 8.88430754e-102, \
                        1.90662932e-103, 8.30764390e-101], [3.04268726e-107, 2.43370956e-107, \
                        3.52132963e-109, 8.92956475e-109, 9.64174748e-111, 1.23040141e-111]]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Hyper Raman']
    spectroscopy_specification = ['Vib modes: 1/m']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 500)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])

    #################################################
    # Testing Hyper Raman acetonitrile and PBE0
    #################################################

    ref_wn = [317856.39743121, 317853.74787773, 311438.99096985, 243343.46125899, 160281.82059371, \
              160280.65824062, 155928.11021045, 115925.32030771, 115924.61054995,  98390.40505199, \
               57141.73061079,  57138.76702502]
    ref_intensities = [[], [], [[9.52351878e-106, 9.27476233e-106, 8.05600747e-106, 7.46579764e-108, \
                        4.17705217e-108, 4.06008034e-108, 3.48145016e-108, 3.79615088e-108, \
                        3.55349173e-108, 2.26338978e-109, 5.17814619e-109, 5.44371383e-109]], \
                      [[1.45733666e-106, 1.54882648e-106, 1.23182079e-106, 1.94220561e-108, \
                        7.82483387e-109, 8.26566336e-109, 9.20161572e-109, 7.00582253e-109, \
                        7.81882342e-109, 2.79478667e-110, 5.39999839e-110, 4.40554970e-110]]]
    run_specification = ['Single snapshot',  'No FraME', 'Outproj']
    spectroscopy_type = ['Hyper Raman']
    spectroscopy_specification = ['Vib modes: 1/m']
    names = [data_dir,'ir_raman_hyper_raman_opt_pcseg-2_PBE0_acetonitrile.rsp_tensor', 'opt_pcseg-2_PBE0_acetonitrile.mol']
    wn, intensities = SpectroscPy_run(run_specification, spectroscopy_type, spectroscopy_specification, \
                                      [], names, 'Keep all', 0, 298)

    assert np.allclose(ref_wn, wn)
    assert len(ref_intensities) == len(intensities)
    for i in range(len(intensities)):
        assert np.allclose(ref_intensities[i], intensities[i])
