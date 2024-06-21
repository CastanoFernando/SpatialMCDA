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
import os
from osgeo import gdal, ogr, osr

path1 = "C:/Users/casta/Downloads/radios_eph/radios_eph.shp"
path2 = "C:/Users/casta/Downloads/GeogToWGS84GeoKey5.tif"

# ======================================================= #
# Main code
# ------------------------------------------------------- #

def get_file_extension(file_name: str) -> str:
    """Get the extension of the file. Returns the file extension. Useful for determining if the input layer is a raster or a vector.

    Args:
        file_name (str): path_dir/name of the file.

    Returns:
        str: extension of the file.
    """

    # Split the path and the extension
    name, ext = os.path.splitext(file_name)
    # Return extension without the "." (dot)
    return ext[1:]
# End def

def get_vector_data(file_name: str) -> list:
    """_summary_

    Args:
        file_name (str): _description_
        SubLayer (str | int, optional): _description_. Defaults to None.

    Returns:
        list: _description_
    """

    # Dictionary to populate
    info_dict = {}
    # Get the datasource
    datasource = ogr.Open(file_name)

    # Number of sublayers and where store the info of each sublayer
    info_dict["sublayers_count"] = datasource.GetLayerCount()
    info_dict["sublayers"] = {}

    # Loop through "sub"layers (thinking the shp as a "layer" and not as a ds)
    for layer_idx in range(info_dict["sublayers_count"]):
        
        #info_dict["sublayers"].append({})
        
        layer = datasource.GetLayer(layer_idx)
        name = layer.GetName()
        info_dict["sublayers"][name] = {}
        # Return the name of the spatial reference system
        SpatialRef = layer.GetSpatialRef().GetName()
        info_dict["sublayers"][name]["SpatialRef"] = SpatialRef
        # Return the extent of the layer (measure by crs)
        info_dict["sublayers"][name]["extent"] = layer.GetExtent()
        # Return number of features (objects/vectors)
        FeaturesCount = layer.GetFeatureCount()
        info_dict["sublayers"][name]["FeaturesCount"] = FeaturesCount
        # Return number of fields (variables)
        layer_info = layer.GetLayerDefn()
        FieldsCount = layer_info.GetFieldCount()
        info_dict["sublayers"][name]["FieldsCount"] = FieldsCount
        # Loop through the fields in the layer and get his names
        name_list = []
        for i in range(FieldsCount):
            name_list.append(layer_info.GetFieldDefn(i).GetName())
        # End for
        info_dict["sublayers"][name]["Fields"] = name_list
    # End for

    name_list = []
    for x, val in info_dict["sublayers"].items():
        name_list.extend(val["Fields"])
        pass
    # End for
    # Return the list of fields' names
    return info_dict, name_list
# End def


def get_vector_proj(file_name: str) -> str:
    """_summary_

    Args:
        file_name (str): _description_

    Returns:
        str: _description_
    """
    # Get spatial reference information
    dataset = ogr.Open(file_name)    
    layer = dataset.GetLayer()
    spatialRef = layer.GetSpatialRef()
    # Return the name of the spatial reference system
    return spatialRef.GetName()
# End def


def get_raster_proj(file_name: str):
    """_summary_

    Args:
        file_name (str): _description_

    Returns:
        _type_: _description_
    """
    # Get spatial reference information
    dataset = gdal.Open(file_name)
    # Return the name of the spatial reference system
    return dataset.GetSpatialRef().GetName()
# End defs

def get_raster_macrogeom(file_name: str) -> tuple:
    """_summary_

    Args:
        file_name (str): _description_

    Returns:
        tuple: _description_
    """
    # Get spatial reference information
    dataset = gdal.Open(file_name)
    geom = dataset.GetGeoTransform()
    # Set data needed
    x_min = geom[0]
    px_size = geom[1]
    y_max = geom[3]
    return x_min, y_max, px_size
# End def

def get_vector_macrogeom(file_name: str) ->tuple:
    """_summary_

    Args:
        file_name (str): _description_

    Returns:
        tuple: _description_
    """
    # Get spatial reference information
    dataset = ogr.Open(file_name)    
    layer = dataset.GetLayer()
    geom = layer.GetExtent()
    # Set data needed
    x_min = geom[0]
    x_max = geom[1]
    y_min = geom[2]
    y_max = geom[3]
    return x_min, y_min, x_max, y_max
# End def

def reproject():
    pass
# End def