import os
from collections import OrderedDict
from astropy.io import fits
import numpy as np

def save_fits_from_array(array,
                         folder: str,
                         file_name: str,
                         header,
                         overwrite: bool = False,
                         dtyp: str = 'int32',
                         do_not_scale_image_data: bool = False,
                         ignore_blank: bool = False,
                         uint: bool = False,
                         scale_back: bool or None = None):
    """
    Save fits file from array to selected location.
    Parameters
    ----------
    array - list like image data, example: [[2, 3, 4], [1, 1, 1], [2, 3, 1]]
    folder - folder, where fits will be saved, example: '/home/fits/'
    file_name - file name without '.fits', example: 'file_no_2233'
    header - fits header in dict format, example: {"FITS_STD": "beta_1", "TEL": "iris"}
    overwrite - overwrite existing file, default=False
    dtyp - array type [str], example: 'int16', 'int32'
    do_not_scale_image_data - astropy PrimaryHDU  parameter
    ignore_blank - astropy PrimaryHDU  parameter
    uint - astropy PrimaryHDU  parameter
    scale_back - astropy PrimaryHDU  parameter
    """
    if os.path.splitext(file_name)[1] == "":
        file_name = f"{file_name}.fits"
    file_name = os.path.join(folder, file_name)

    hdr = fits.Header()

    if isinstance(header, dict):
        for n in header.keys():
            try:
                hdr[n] = header[n][0]
                hdr.comments[n] = header[n][1]
            except (LookupError, TypeError):
                hdr[n] = header[n]
    elif isinstance(header, fits.Header):
        hdr = header
    else:
        hdr["OCASTD"] = "No fits header provided"

    if dtyp=='int32':
        narray = np.array(array, dtype=np.int32)
    elif dtyp=='int16':
        narray = np.array(array, dtype=np.int16)
    elif dtyp=='sideint16':
        s_array = np.array(array) - 32768
        narray = np.array(s_array, dtype=np.int16)
    elif dtyp=='none':
        narray = array
    else:
        narray = array

    hdu = fits.PrimaryHDU(data=narray,
                          header=hdr,
                          do_not_scale_image_data=do_not_scale_image_data,
                          ignore_blank=ignore_blank,
                          uint=uint,
                          scale_back=scale_back)
    hdul = fits.HDUList([hdu])
    hdul.writeto(file_name, overwrite=overwrite)
    if dtyp=='sideint16':
        hdul2 = fits.open(file_name)
        hdul2[0].header['BZERO'] = 32768
        hdul2.writeto(file_name, overwrite=True)

# Lets Follow the FitS standard version 4, as defined in
# https://fits.gsfc.nasa.gov/fits_standard.html
# https://fits.gsfc.nasa.gov/standard40/fits_standard40aa-le.pdf
# https://heasarc.gsfc.nasa.gov/docs/fcg/common_dict.html may be also useful

def fits_header(oca_std="BETA2",
                obs="OCA",
                obs_lat='',
                parsed_obs_lat='',
                obs_lon='',
                parsed_obs_lon='',
                obs_elev='',
                origin='CAMK PAN',
                tel_id='',
                utc_now='',
                jd='',
                req_ra='',
                req_dec='',
                epoch='',
                tel_ra='',
                tel_dec='',
                tel_alt='',
                tel_az='',
                airmass='',
                obs_mode='',
                focus='',
                rotator_pos='',
                observer='',
                obs_type='',
                object='',
                filter='',
                req_exp='',
                cam_exp='',
                det_size='',
                ccd_sec='',
                ccd_name='',
                ccd_temp='',
                ccd_binx='',
                ccd_biny='',
                read_mod='',
                gain='',
                r_noise=''
                ):

    _header = OrderedDict({
        "OCASTD": (oca_std, "OCA FITS HDU standard version"),
        "OBSERVAT": (obs, "Cerro Armazones Observatory"),
        "OBS-LAT": (parsed_obs_lat, f"[deg] Observatory longitude {obs_lat}"),
        "OBS-LONG": (parsed_obs_lon, f"[deg] Observatory latitude {obs_lon}"),
        "OBS-ELEV": (obs_elev, f"[m] Observatory elevation"),
        "ORIGIN": (origin, "Institution created this FITS file"),
        "TEL": (tel_id, ''),
        "DATE-OBS": (utc_now, "DateTime of observation start"),
        "JD": (jd, "Julian date of observation start"),
        "RA": (req_ra, "Requested object RA"),
        "DEC": (req_dec, "Requested object DEC"),
        "EQUINOX": (epoch, "Requested RA DEC epoch"),
        "TEL_RA": (tel_ra, "Telescope RA"),
        "TEL_DEC": (tel_dec, "Telescope DEC"),
        "TEL_ALT": (tel_alt, "[deg] Telescope mount ALT"),
        "TEL_AZ": (tel_az, "[deg] Telescope mount AZ"),
        "AIRMASS": (airmass, ''),
        "OBSMODE": (obs_mode, "TRACKING, GUIDING, JITTER or ELSE"),
        "FOCUS": (focus, "Focus position"),
        "ROTATOR": (rotator_pos, "[deg] Rotator position"),
        "OBSERVER": (observer, ''),
        "OBSTYPE": (obs_type, ''),
        "OBJECT": (object, ''),
        "FILTER": (filter, ''),
        "EXPREQ": (req_exp, "[s] Requested exposure time"),
        "EXPTIME": (cam_exp, "[s] Executed exposure time"),
        "DETSIZE": (det_size, ''),
        "CCDSEC": (ccd_sec, ''),
        "CCD_NAME": (ccd_name, ''),
        "CCD_TEMP": (ccd_temp, ''),
        "CCD_BINX": (ccd_binx, ''),
        "CCD_BINY": (ccd_biny, ''),
        "READ_MOD": (read_mod, ''),
        "GAIN": (gain, ''),
        "RNOISE": (r_noise, ''),
    })

    return _header

def fits_stat(array, size: int or None = None, min: bool = True, max: bool = True,
              mean: bool = True, median: bool = True, std: bool = True):
    """
    Main fits statistics
    :param array: list like image data, example: [[2, 3, 4], [1, 1, 1], [2, 3, 1]]
    :param size: size of sample taken random (if size=None will calculate whole array)
    :param min: array minimum, should calculate this stat, default Yes
    :param max: array maximum, should calculate this stat, default Yes
    :param mean: array mean, should calculate this stat, default Yes
    :param median: array median, should calculate this stat, default Yes
    :param std: array standard deviation, should calculate this stat, default Yes
    :return: Dict[str, float]
    """

    result = {}
    narray = np.array(array)
    if size is not None:
        narray = array_random_subset_2d(narray, size=size)

    if min:
        result['min'] = np.amin(narray)

    if max:
        result['max'] = np.amax(narray)

    if mean:
        result['mean'] = np.mean(narray)

    if median:
        result['median'] = np.median(narray)

    if std:
        result['std'] = np.std(narray)

    return result

def array_random_subset_2d(array, size: int, replace: bool = False):
    """
    Func randomly selecting points from array
    :param array: 2d numpy array
    :param size: size of subset
    :param replace: with or without replacement
    :return: array random subset
    """
    nrows, ncols = array.shape
    row_indices = np.random.choice(nrows, size=size, replace=replace)
    col_indices = np.random.choice(ncols, size=size, replace=replace)
    return array[row_indices, col_indices]