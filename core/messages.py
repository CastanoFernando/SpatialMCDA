# ======================================================= #
'''
@ProjectName: SpatialMCDA
@Author: FernandoCastano
@Email: castano.fernando.martin@gmail.com
@Version: 0.1.0
'''
# ------------------------------------------------------- #

# ======================================================= #
# Packages
# ------------------------------------------------------- #

import warnings

# ======================================================= #
# Main code
# ------------------------------------------------------- #

EXTENSION_ERROR = 'The file extension is not supported by the package. Please use ESRI shapefile (.shp extension) for vectors and GTiff (.tif extension) for rasters.'

ALIAS_ERROR = 'The alias has non alphanumeric characters, please provide an alias with only alphanumeric chars.'

DIR_ERROR = "The output_dir doesn't exist, please provide an existing address"

NEUTRAL_ERROR = "The na parameter has to be 0 or 1. See the help function for more details"

FIELD_ERROR = "The field doens't match with an existing field in the layer."

IDX_WARNING = 'The program will only use layerName if both, layerName and layerIndex was passed.'

ALIAS2_ERROR = "The alias already exists in the model"

LAYER_ERROR = "The object in layer parameter is not a SMCDALayer"

def KWARGS_WARNING(element: str) -> str:
    return warnings.warn(f'{element} not allowed, will be omited')
# End def

def STR_ERROR(arg: str) -> str: 
    return f'object in {arg} argument is not a string element.'
# End def

def INT_ERROR(arg: str) -> str:
    return f'object in {arg} argument is not a integer element.'
# End def

def FLOAT_ERROR(arg: str) -> str:
    return f'object in {arg} argument is not a float element.'
# End def


def LIST_ERROR(arg: str) -> str:
    return f'object in {arg} argument is not a list object.'
# End def

def PINT_ERROR(arg: str) -> str:
    return f'{arg} is not a positive integer'
# End def

def BOOL_ERROR(arg: str) -> str:
    return f'{arg} is not boolean'
# End def