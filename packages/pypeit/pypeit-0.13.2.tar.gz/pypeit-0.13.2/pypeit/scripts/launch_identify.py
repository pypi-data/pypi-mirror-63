#!/usr/bin/env python
#
# See top-level LICENSE file for Copyright information
#
# -*- coding: utf-8 -*-
"""
Launch the identify GUI tool.
"""


def parser(options=None):
    import argparse

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Launch PypeIt identify tool, display extracted'
                                                 'MasterArc, and load linelist.'
                                                 'Run above the Masters/ folder',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('file', type=str, default=None, help='PypeIt MasterArc file')
    parser.add_argument("--lamps", default=None, help="Comma separated list of calibration lamps (no spaces)",
                        action="store_true")
    parser.add_argument("--wmin", default=3000.0, help="Minimum wavelength range",
                        action="store_true")
    parser.add_argument("--wmax", default=10000.0, help="Maximum wavelength range",
                        action="store_true")
    parser.add_argument("--slit", default=0, help="Slit number to wavelength calibrate",
                        action="store_true")
    parser.add_argument("--det", default=1, help="Detector index",
                        action="store_true")

    return parser.parse_args() if options is None else parser.parse_args(options)


def main(args):

    import os
    import sys
    import astropy.io.fits as fits
    from pypeit.masterframe import MasterFrame
    from pypeit.spectrographs.util import load_spectrograph
    from pypeit.core import parse
    from pypeit.core.gui import identify as gui_identify
    from pypeit.core.wavecal import waveio, templates
    from pypeit.wavecalib import WaveCalib
    from pypeit import edgetrace
    from pypeit.images import pypeitimage

    # Load the MasterArc file
    if os.path.exists(args.file):
        arcfil = args.file
    else:
        try:
            arcfil = "Masters/{0:s}".format(args.file)
        except FileNotFoundError:
            print("Could not find MasterArc file.")
            sys.exit()
    msarc = pypeitimage.PypeItImage.from_file(arcfil)

    mdir = msarc.head0['MSTRDIR']
    mkey = msarc.head0['MSTRKEY']

    # Load the spectrograph
    specname = msarc.head0['PYP_SPEC']
    spec = load_spectrograph(specname)
    par = spec.default_pypeit_par()['calibrations']['wavelengths']

    # Get the lamp list
    if args.lamps is None:
        lamplist = par['lamps']
        if lamplist is None:
            print("ERROR :: Cannot determine the lamps")
            sys.exit()
    else:
        lamplist = args.lamps.split(",")
    par['lamps'] = lamplist

    # Load the tslits_dict
    trc_file = os.path.join(mdir, MasterFrame.construct_file_name('Edges', mkey, file_format='fits.gz'))
    tslits_dict = edgetrace.EdgeTraceSet.from_file(trc_file).convert_to_tslits_dict()

    # Check if a solution exists
    solnname = os.path.join(mdir, MasterFrame.construct_file_name('WaveCalib', mkey, file_format='json'))
    wv_calib = waveio.load_wavelength_calibration(solnname) if os.path.exists(solnname) else None

    # Load the MasterFrame (if it exists and is desired)?
    wavecal = WaveCalib(msarc, tslits_dict, spec, par)
    arccen, arc_maskslit = wavecal.extract_arcs()

    binspec, binspat = parse.parse_binning(spec.get_meta_value(msarc.head0['F1'], 'binning'))

    # Launch the identify window
    arcfitter = gui_identify.initialise(arccen, slit=int(args.slit), par=par, wv_calib_all=wv_calib)
    final_fit = arcfitter.get_results()

    # Ask the user if they wish to store the result in PypeIt calibrations
    ans = ''
    while ans != 'y' and ans != 'n':
        ans = input("Would you like to store this wavelength solution in the archive? (y/n):")
    if ans == 'y' and final_fit['rms'] < 0.1:
        gratname = fits.getheader(msarc.head0['F1'])[spec.meta['dispname']['card']].replace("/", "_")
        dispangl = "UNKNOWN"
        templates.pypeit_identify_record(final_fit, binspec, specname, gratname, dispangl, outdir=mdir)
        print("Your wavelength solution has been stored")
        print("Please consider sending your solution to the PypeIt team!")
