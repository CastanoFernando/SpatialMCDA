# ======================================================= #
"""
@ProjectName: SpatialMCDA
@Author: FernandoCastano
@Email: castano.fernando.martin@gmail.com
@Version: 0.1.0
"""
# ------------------------------------------------------- #

# ======================================================= #
# Packages and utils
# ------------------------------------------------------- #
# from typing import Optional, Tuple, Union, overload
from typing import Annotated, Union
from annotated_types import Gt
from core.utils import *
from core.messages import *

# ======================================================= #
# Layer class
# ------------------------------------------------------- #

class SMCDALayer:
    """
    ### Objetivo
    Organizar los insumos con la información georreferenciada. 
    Por ahora solo admite las extensiones .shp y .tif (añadiré
    otras si se requieren en el proyecto). La idea es tener 
    un control de que los atributos se encuentran bien 
    especificados y tener una los datos básicos para consultar 
    al añadirlos en el objeto del modelo.
    """

    def __init__(self, path: str, FieldName: str = None, positive: bool = True, na: int = 0, **kwargs) -> None:
        """
        ## Descripción
        Clase atómica del programa/paquete. Permite organizar 
        y controlar toda la información relevante a la capa.

        ## Parámetros:
            * `path` (str): En este parámetro se debe indicar la
            ruta completa al archivo ".shp" o ".tif (incluido 
            el nombre del archivo). Ejemplo: "C:/Descargas/prueba.tif". 
            * `FieldName` (str, optional): Este parámetro se utilizará únicamente en el caso de que la capa sea un archivo ".shp". Los elementos dentro de una capa vectorial tienen lo que se denominan "campos", los cuales reflejan características de estos objetos (es decir, variables). Esta función permite utilizar uno de estos campos. En caso de que no se utilice ningún campo, se utilizará el mismo valor para todos los objetos de la capa. Defaults to None.
            * `positive` (bool, optional): Indicar si la escala
            de la capa representa una característica positiva 
            (a mayor valor, mejor la alternativa) o una característica
            negativa. Defaults to `True`.
            * `na` (int, optional): Indica el valor que se 
            imputará en las zonas sin datos de la capa. El dato
            se utilizará después de tipificar la escala, pero
            previamente a transformar la escala en caso de 
            que la capa represente una característica indeseable. 
            Los únicos valores posibles son el `0` y el `1`.
            Usualmente se emplea el `0`. Defaults to `0`.
        """
        
        # =========================== #
        # Checks
        
        ### Types
        # path
        if(type(path) != str): raise RuntimeError(STR_ERROR('path'))
        # FieldName
        if((FieldName is None) | (type(FieldName) is str)): pass
        else: raise RuntimeError(STR_ERROR('LayerName'))
        # positive
        if(type(positive) != bool): raise RuntimeError(BOOL_ERROR('positive'))
        # na
        if(type(na) != int): raise RuntimeError(NEUTRAL_ERROR)


        # Compatible files extensions for now: .tif, .shp
        self.extension = get_file_extension(path)
        # Add attributes if it has a compatible extension
        if self.extension == 'tif':
            #
            self.driver = 'GTiff'
            # Raster data
            self.ProjectionName = get_raster_proj(path)
            self.geomdata = get_raster_macrogeom(path)
        elif self.extension == 'shp':
            #
            self.driver = 'ESRI Shapefile'
            self.ProjectionName = get_vector_proj(path)
            self.geomdata = get_vector_macrogeom(path)
            self.sublayersinfo, self.fields = get_vector_data(path)
            # FieldName
            if FieldName is None: 
                self.field = False
            elif(FieldName in self.fields): self.field
            else: raise RuntimeError(FIELD_ERROR)
            # End if
        else:
            raise RuntimeError(EXTENSION_ERROR)
        # End if

        # na has to be 0 or 1
        if(na not in [0, 1]): raise RuntimeError(NEUTRAL_ERROR)
        
        # =========================== #
        # Attributes

        self.path = path
        self.file_name = os.path.basename(path)
        self.positive = positive
        self.na = na
        self.buffer = { "compute": False, "dist": 0}
        self.proximity = {"compute": False, "dist": 0}

        
        # =========================== #
        # Next upgrades: more attributes?
        '''
        Allowed kwargs options: for now, none.
        '''
        allowed_args = []

        #
        for element in kwargs.keys():
            if element in allowed_args:
                pass
            else:
                KWARGS_WARNING(element)
            # End if
        # End for
    # End def

    # Start method
    def update_path(self, path: str) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `path` de una instancia.

        ## Parámetros:
            * `path` (str): En este parámetro se debe indicar la
            ruta completa al archivo ".shp" o ".tif (incluido 
            el nombre del archivo). Ejemplo: "C:/Descargas/prueba.tif". 
        """
        
        ### Types
        # path
        if(type(path) != str): raise RuntimeError(STR_ERROR('path'))

        # Compatible files extensions for now: .tif, .shp
        extension = get_file_extension(path)
        # Add attributes if it has a compatible extension
        if extension == 'tif':
            #
            self.driver = 'GTiff'
            # Raster data
            self.ProjectionName = get_raster_proj(path)
            self.geomdata = get_raster_macrogeom(path)
        elif extension == 'shp':
            #
            self.driver = 'ESRI Shapefile'
            self.ProjectionName = get_vector_proj(path)
            self.geomdata = get_vector_macrogeom(path)
        else:
            raise RuntimeError(EXTENSION_ERROR)
        # End if

        self.path = path
        self.file_name = os.path.basename(path)
        self.extension = get_file_extension(path)

        return
    # End def

    # Start method
    def update_positive(self, positive: bool) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `positive` de una instancia.

        ## Parámetros:
            * `positive` (bool, optional): Indicar si la escala
            de la capa representa una característica positiva 
            (a mayor valor, mejor la alternativa) o una característica
            negativa. Defaults to `True`.
        """
        # positive
        if(type(positive) != bool): raise RuntimeError(BOOL_ERROR('positive'))

        self.positive = positive
        return
    # End def

    # Start method
    def update_na(self, na: int) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `na` de una instancia.

        ## Parámetros:
            * `na` (int, optional): Indica el valor que se 
            imputará en las zonas sin datos de la capa. El dato
            se utilizará después de tipificar la escala, pero
            previamente a transformar la escala en caso de 
            que la capa represente una característica indeseable. 
            Los únicos valores posibles son el `0` y el `1`.
            Usualmente se emplea el `0`. Defaults to `0`.
        """

        # na
        if(type(na) != int): raise RuntimeError(NEUTRAL_ERROR)
        # na has to be 0 or 1
        if(na not in [0, 1]): raise RuntimeError(NEUTRAL_ERROR)

        self.na = na
        return
    # End def

    # Start method
    def update_field(self, FieldName: Union[str, None]) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `na` de una instancia.

        ## Parámetros:
            * `FieldName` (str, optional): Este parámetro se 
            utilizará únicamente en el caso de que la capa 
            sea un archivo ".shp". Los elementos dentro de 
            una capa vectorial tienen lo que se denominan "campos", 
            los cuales reflejan características de estos objetos 
            (es decir, variables). Esta función permite utilizar 
            uno de estos campos. En caso de que no se utilice 
            ningún campo, se asignará el mismo valor para todos 
            los objetos de la capa. Si se asignó un campo de 
            forma errónea, y no quiere asignar ninguno, deberá
            ingresar `None` en el parámetro.
        """

        path = self.path
        extension = self.extension
        # Check if extension is .shp

        # Types
        if((type(FieldName).__name__ in ["str", "NoneType"])): pass
        else: raise RuntimeError(STR_ERROR('LayerName'))
        # check if is in list
        if(FieldName is None): self.field
        elif(FieldName in self.fields): self.field
        else: raise RuntimeError(FIELD_ERROR)
        
        return
    # End def
    
    # Start method
    def calc_buffer(self, compute: bool = False, dist: Annotated[float, Gt(0)] = 1):
        """
        ## Descripción
        Declara que se debe computar un buffer sobre la capa. Esto solo se puede realizar para capas vectoriales. Una mejora sería extenderlo para capas ráster (el proyecto no lo requiere). También conocido como zona de influencia. Se crea un nuevo objeto con el conjunto de puntos que se encuentran a una distancia menor a `dist`.

        ## Parámetros:
            * `compute` (bool):  Si se requiere aplicar el buffer a la capa. En caso de querer cancelar el requerimiento de aplicar el buffer, fijar este parámetro en False. Defaults to False.
            * `dist` (float, Greater than 0): Distancia en la que se considera que se encuentra en el radio de influencia del objeto (en la unidad de medida del sistema de coordenadas de la capa). Defaults to 1.
        """


        # Upgrade: Check with the extent of the layers (crs unit
        #  of the model or the layer)

        self.buffer["compute"] = compute
        self.buffer["dist"] = dist
        return
    # End def
    
    # Start method
    def calc_proximity(self, compute: bool = True, dist: Annotated[float, Gt(0)] = 1):
        """
        ## Descripción
        Declara que se debe computar un buffer que tenga en cuenta la distancia con el punto más cercano del objeto. Es decir que al márgen extensivo de si pertenece a la zona de influencia (leer la descripción del método calc_buffer), sino que también incorpora un márgen intensivo en el que la influencia del objeto disminuye a medida que se aleja de este.

        ## Parámetros:
            * `compute` (bool):  Si se requiere aplicar el la proximidad a la capa. En caso de querer cancelar el requerimiento de aplicar la proximidad, fijar este parámetro en False. Defaults to False.
            * `dist` (float, Greater than 0): Distancia en la que se considera que se encuentra en el radio de influencia del objeto (en la unidad de medida del sistema de coordenadas de la capa). Defaults to 1.
        """

        # Upgrade: Check with the extent of the layers (crs unit
        #  of the model or the layer)

        self.buffer["compute"] = compute
        self.buffer["dist"] = dist
        return
    # End def
# End class