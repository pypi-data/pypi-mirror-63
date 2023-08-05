# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import gzip

import numpy as np

__all__ = ['read_edf', 'read_edf_header',
           'read_edf_from_data', 'read_edf_gz', 'read_header_from_file', 'read_edf_from_file']


def read_edf_from_file(file_path: str):
    data = get_data_from_filepath(file_path)
    return read_edf_from_data(data)


def read_edf_gz(gz_filepath, *, reshape: bool = True):
    _check_file(gz_filepath, '.edf.gz')
    with gzip.open(gz_filepath, 'rb') as f:
        data = f.read()
    return read_edf_from_data(data, reshape=reshape)


def read_edf(edf_filepath, *, reshape: bool = True):
    _check_file(edf_filepath, '.edf')
    with open(edf_filepath, 'rb') as f:
        data = f.read()
    return read_edf_from_data(data, reshape=reshape)


def read_edf_from_data(data, *, reshape: bool = True):
    header_dict = read_header_from_data(data)
    header_end_index = header_dict['headerSize']
    image_size = int(header_dict['Size'])
    raw_image_data = data[header_end_index:header_end_index + image_size]
    data_type = _get_numpy_type(header_dict['DataType'])
    image_shape = (int(header_dict['Dim_2']), int(header_dict['Dim_1']))

    data = np.frombuffer(raw_image_data, data_type)
    if reshape:
        data = np.rot90(np.reshape(data, image_shape))
    return data, header_dict


def read_edf_header(edf_filepath):
    _check_file(edf_filepath, '.edf')
    with open(edf_filepath, 'rb') as f:
        data = f.read()
    return read_header_from_data(data)


def read_edf_header_from_gz(gz_filepath):
    _check_file(gz_filepath, '.edf.gz')
    with gzip.open(gz_filepath, 'rb') as f:
        data = f.read()
    return read_header_from_data(data)


def read_header_from_data(data) -> dict:
    header_end_index = data.find(b'}\n') + 2
    if header_end_index != 1024:
        print('File has unusual size of header bites %i' % header_end_index)
    header = data[1:header_end_index].decode('utf-8')
    header_dict = _get_header_dict(header)
    header_dict.update({'headerSize': header_end_index})
    return header_dict


def read_header_from_file(filepath):
    data = get_data_from_filepath(filepath)
    return read_header_from_data(data)


def get_data_from_filepath(filepath: str):
    _check_file(filepath)
    if filepath.endswith('.edf'):
        with open(filepath, 'rb') as f:
            return f.read()
    elif filepath.endswith('.edf.gz'):
        with gzip.open(filepath, 'rb') as f:
            return f.read()
    else:
        raise ValueError('Unknown file type')


def _get_header_dict(header):
    header_dict = {}
    raw_list = header.replace('\n', '').strip(). \
        replace(' ', ''). \
        replace('{', ''). \
        replace('}', ''). \
        split(';')
    for item in raw_list:
        item = item.split('=')
        if len(item) == 2:
            header_dict.update([item])
    return header_dict


def _check_file(filepath: str, end_filter: str = None) -> None:
    end_filter = end_filter or ''
    if not os.path.isfile(filepath):
        raise FileNotFoundError('File %s doesn\'t exist' % filepath)
    if not filepath.endswith(end_filter):
        raise ValueError('File %s is not an edf.gz file' % filepath)


_EDF_TYPE_DICT = dict(SIGNEDBYTE=np.int8,
                      UNSIGNEDBYTE=np.uint8,
                      SIGNEDSHORT=np.int16,
                      UNSIGNEDSHORT=np.uint16,
                      SIGNEDINTEGER=np.int32,
                      UNSIGNEDINTEGER=np.uint32,
                      SIGNEDLONG=np.int32,
                      UNSIGNEDLONG=np.uint32,
                      SIGNED64=np.int64,
                      UNSIGNED64=np.uint64,
                      FLOATVALUE=np.float32,
                      FLOAT=np.float32,
                      DOUBLEVALUE=np.float64)


def _get_numpy_type(edf_type):
    """
    Returns NumPy type based on edf type.
    """

    try:
        return _EDF_TYPE_DICT[edf_type.upper()]
    except KeyError:
        raise TypeError(f'Unknown edf type: {edf_type}.')
