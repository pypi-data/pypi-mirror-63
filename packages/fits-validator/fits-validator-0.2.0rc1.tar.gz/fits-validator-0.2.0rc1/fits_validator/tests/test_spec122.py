from pathlib import Path
import pytest
from astropy.io import fits
import numpy as np
from fits_validator import spec122_validator, Spec122ValidationException
from fits_validator.exceptions import ValidationException


@pytest.fixture(scope="module")
def valid_spec_122_headers(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    header tests below.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr.fits": Path(file_name),
        "valid_spec_122_dict": valid_spec_122_dict,
        "valid_HDUList": valid_hdu_list,
        "valid header": valid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=["valid_dkist_hdr.fits", "valid_spec_122_dict", "valid_HDUList", "valid header",],
)
def valid_spec_122_header(request, valid_spec_122_headers):
    yield valid_spec_122_headers[request.param]


def test_spec122_valid(valid_spec_122_header):
    """
    Validates a fits header against the SPEC-0122 schema
    Given: A valid SPEC-0122 fits header
    When: Validating headers
    Then: return None and do not raise an exception
    """
    # raises exception on failure
    assert not spec122_validator(valid_spec_122_header)


@pytest.fixture(scope="module")
def invalid_spec_122_headers(tmpdir_factory):
    """
    Create a dict of invalid spec 122 headers to be used in failing
    header tests below.
    """
    invalid_spec_122_dict = {
        "NAXIS": 2,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "WAVELNTH": "NOTSUPPOSEDTOBEASTRING",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
    }

    temp_dir = tmpdir_factory.mktemp("invalid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    invalid_hdu = fits.PrimaryHDU(temp_array)
    # Use the invalid_spec_122_dict from above to overwrite the default header
    for (key, value) in invalid_spec_122_dict.items():
        invalid_hdu.header[key] = value
    invalid_hdu_list = fits.HDUList([invalid_hdu])
    invalid_hdu_list.writeto(str(file_name))

    yield {
        "invalid_dkist_hdr.fits": Path(file_name),
        "invalid_spec_122_dict": invalid_spec_122_dict,
        "invalid_HDUList": invalid_hdu_list,
        "invalid header": invalid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "invalid_dkist_hdr.fits",
        "invalid_spec_122_dict",
        "invalid_HDUList",
        "invalid header",
    ],
)
def invalid_spec_122_header(request, invalid_spec_122_headers):
    yield invalid_spec_122_headers[request.param]


def test_validate_invalid(invalid_spec_122_header):
    """
    Validates an invalid fits header against the SPEC-0122 schema
    Given: A invalid SPEC-0122 fits header
    When: Validating headers
    Then: raise a Spec122ValidationException
    """

    with pytest.raises(Spec122ValidationException):
        spec122_validator(invalid_spec_122_header)


@pytest.fixture(scope="module")
def invalid_file_params(tmpdir_factory):
    """
    Create a dict of invalid file params to be used in failing
    tests below.
    """
    temp_dir = tmpdir_factory.mktemp("invalid_file_params_temp")
    non_existent_file_name = temp_dir.join("tmp_fits_file.fits")
    non_fits_file_name = temp_dir.join("tmp_this_is_not_a_fits_file.dat")
    temp_array = np.ones(1, dtype=np.int16)
    temp_array.tofile(str(non_fits_file_name))
    yield {"file not found": non_existent_file_name, "file_not_fits": non_fits_file_name}


@pytest.fixture(scope="function", params=["file not found", "file_not_fits"])
def invalid_file_param(request, invalid_file_params):
    yield invalid_file_params[request.param]


def test_validate_file_errors(invalid_file_param):
    """
    Validates an invalid file spec
    Given: A invalid file specification: non-existent file or non-fits file
    When: Validating headers
    Then: raise a Spec122ValidationException
    """

    with pytest.raises(ValidationException):
        spec122_validator(invalid_file_param)


@pytest.fixture(scope="module")
def max_headers(tmpdir_factory):
    headers = {
        "SIMPLE": True,
        "BITPIX": 16,
        "NAXIS": 3,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "BUNIT": "adu",
        "DATE": "2017-05-30T17:28:21.996",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "DATE-BGN": "2017-05-30T00:46:13.618",
        "DATE-END": "2017-05-30T00:46:13.718",
        "ORIGIN": "National Solar Observatory",
        "TELESCOP": "Daniel K. Inouye Solar Telescope",
        "OBSERVAT": "Haleakala High Altitude Observatory Site",
        "NETWORK": "DKIST",
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "OBSERVER": "8QN27LDFC7EQHKK4B3WDIN4FY7VG16",
        "OBJECT": "EAML29SS4SGV959A4GR5GNDAG1FANM",
        "CHECKSUM": "33989WFLS3IVX0LLYTQW3U1PT8AKFG",
        "DATASUM": "9WNO5RGILE66C2VLRJ45RQEBFL1IHU",
        "WCSAXES": 2,
        "WCSNAME": "Helioprojective",
        "CRPIX1": 2048.0,
        "CRPIX2": 2048.0,
        "CRDATE1": "2035-03-31T09:38:56.668",
        "CRDATE2": "2035-03-31T09:38:56.668",
        "CRVAL1": -304.9906422447552,
        "CRVAL2": -658.9384652992346,
        "CDELT1": 0.07,
        "CDELT2": 0.07,
        "CUNIT1": "arcsec",
        "CUNIT2": "arcsec",
        "CTYPE1": "HPLN-TAN",
        "CTYPE2": "HPLT-TAN",
        "PC1_1": 0.9231997511186788,
        "PC1_2": -0.3843204646312885,
        "PC2_1": 0.3843204646312885,
        "PC2_2": 0.9231997511186788,
        "LONPOLE": 180.0,
        "TAZIMUTH": 618993.1279034158,
        "TELEVATN": 819.9173809486648,
        "TELTRACK": "Standard Differential Rotation Tracking",
        "TELSCAN": "Raster",
        "TTBLANGL": 295548.0744481586,
        "TTBLTRCK": "fixed coude table angle",
        "DKIST001": "Manual",
        "DKIST002": "Full",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "DKIST005": "9CVKTL2JWMH1LHU6G3O2UPE2SO9SUW",
        "DKIST006": "OG4Y0R39WGGB3N0R7VIDQG7VQYD79N",
        "DKIST007": False,
        "DKIST008": 999562,
        "DKIST009": 5750,
        "DKIST010": 295882,
        "ID___001": "73QYTMXIMDLCNZUEBELYY6TZ8QGYKV",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___004": "MY50PNI7QUGSKLW5D8XB9N4SDKFDZ4",
        "ID___005": "59ULPBE5GG9S93M9IG63FCWMV63WAD",
        "ID___006": "7VWWG70RLGVD9AC1J9X6Y937EJIQNV",
        "ID___007": "U8M3EWALJLU5F5B96WB4QL3SN0Z1C8",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___009": "XV64I6WTJEJ93202Z5ZJ15MDBBBPRE",
        "ID___010": "KKWSIWJD2NKL11J03X51ZZR0C6FSHG",
        "ID___011": "OB6PYAI9XC3PTXLLY4I1LV26RTDEGS",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "ID___014": "UX4QYSNNFC1O99JD3TVPAGUU4XR0JB",
        "CAM__001": "ODJIY4RO6SG7T6YVHT4QVNJPVYGQW7",
        "CAM__002": "JRA5H1LSKENNLLWUZNHW9X93Z9J6G0",
        "CAM__003": 206077,
        "CAM__004": 553109.1055738949,
        "CAM__005": 931934.0145101176,
        "CAM__006": 336899.9459380526,
        "CAM__007": 450499,
        "CAM__008": 105605,
        "CAM__009": 278167,
        "CAM__010": 45681,
        "CAM__011": 882899,
        "CAM__012": 849283,
        "CAM__013": 191847,
        "CAM__014": 859469,
        "CAM__015": 208276,
        "CAM__016": 71858,
        "CAM__017": 540083,
        "CAM__018": 462616,
        "CAM__019": 763903,
        "CAM__020": 626497,
        "PAC__001": "I0ZJXRV29HDPUM2NB1P8YWXC2U6ZPN",
        "PAC__002": "LCEN78S9ZFFD54FT7W4IQRZ53DVOHO",
        "PAC__003": "08DT3NZOX1XC4U6KT462GIMJ1KH9R1",
        "PAC__004": "Clear",
        "PAC__005": "186BGJFTFDVEOECZ80ENVCKM5RZL4U",
        "PAC__006": "NIRRetarder",
        "PAC__007": "some string",
        "PAC__008": 332880.8796027036,
        "PAC__009": 39391.69758352268,
        "PAC__010": "Undefined",
        "PAC__011": 228814.6368968824,
        "WS___001": "CYWKXJOAROTHYHNBZOD8Z7VGJITI23",
        "WS___002": 516056.5759472652,
        "WS___003": 188143,
        "WS___004": 943419.0784243871,
        "WS___005": 282679.0410177523,
        "WS___006": 348537.5489154414,
        "WS___007": 870761.4045310392,
    }

    temp_dir = tmpdir_factory.mktemp("max_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_header dict from above to overwrite the default header
    for (key, value) in headers.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield Path(str(file_name))


def test_validate_maxheaders(max_headers):
    """
    Validates a spec122 compliant header with a large number of keywords
    Given: A spec122 compliant fits file with many header keywords
    When: Validating headers
    Then: return None and do not raise an exception
    """
    assert not spec122_validator(max_headers)
