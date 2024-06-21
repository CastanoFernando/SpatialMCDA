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

from typing import Annotated, overload
from annotated_types import Ge

import os
from pyproj import CRS
from osgeo import gdal, ogr, osr
from core.SMCDACriteria import SMCDACriteria, check_importance
from core.SMCDALayer import SMCDALayer
from core.utils import *
from core.messages import *


# ======================================================= #
# SMCDAModel class
# ------------------------------------------------------- #

class SMCDAModel:
    """
    ### Objetivo
    Organizar tanto la información como las capas a utilizar.
    La idea es tener un control de que los atributos se 
    encuentran bien especificados y estos se puedan modificar
    de una forma amigable sin caer en fallos de especificación.

    ### Aspectos técnicos
    Por ahora solo admite las extensiones .shp y .tif (añadiré
    otras si se requieren en el proyecto). Utiliza los paquetes
    gdal y ogr para manipular a las capas (permite extender a
    otras extensiones).
    """
    
    # Start method
    def __init__(
            self, 
            alias: str = None, 
            output_dir: str = None, 
            epsg: str = None
            ) -> None:
        """
        ## Descripción
        Crea una instancia de la clase `SMCDAModel`. La utilidad de 
        esta clase es la de organizar la información del modelo y 
        los elementos que se deben utilizar. Por ahora solo soporta
        capas con extensiones `.shp` y `.tif`.

        ## Parámetros:
            * `alias` (str, optional): Nombre con el que el 
            programa se va a referir al modelo. No es necesario 
            declararlo al momento de crear el modelo, pero 
            se necesitará agregar luego. Defaults to None.
            * `output_dir` (str, optional): Directorio en 
            el que se van a guardar los resultados de la 
            ejecución. No es necesario declararlo al momento 
            de crear el modelo, pero se necesitará agregar 
            luego. Defaults to None.
            * `epsg` (int, optional): Sistema de coordenadas 
            de referencia que se utilizará para trabajar con 
            los insumos y el sistema de coordenadas que tendrá 
            el archivo de salida. No es necesario declararlo, 
            el programa utilizará el sistema de coordenadas 
            de una de las capas, aunque se recomienda informarlo. 
            Recomiendo revisar la página web `https://epsg.io/?q=` 
            para analizar cual se ajusta mejor a la región 
            de análisis. Defaults to None.

        ## Ejemplo
            >>> SMCDAModel("modelo1", "C:/Downloads", 22185)
        """

        # =========================== #
        # Checks

        ### Types
        # alias
        if((alias is None) | (type(alias) is str)): pass
        else: raise RuntimeError(STR_ERROR('alias'))
        # output_dir
        if((output_dir is None) | (type(output_dir) is str)): pass
        else: raise RuntimeError(STR_ERROR('output_dir'))
        # crs
        if((epsg is None) | (type(epsg) is int)): pass
        else: raise RuntimeError(INT_ERROR('epsg'))

        ### Valid parameters
        # alias
        if(alias.replace('_', '').isalnum()): pass
        else: raise RuntimeError(ALIAS_ERROR)
        # output_dir
        if(os.path.exists(output_dir)): pass
        else: raise RuntimeError(DIR_ERROR)
        # crs
        CRS(epsg)
        
        # =========================== #
        # Add attributes
        
        self.alias = alias
        self.output_dir = output_dir
        self.epsg = epsg
        self.criterias = {}
        self.feasible_region = {}

        return
    # End def

    # Start method
    def update_alias(self, alias: str) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `alias` de una instancia.

        ## Parámetros:
            * `alias` (str): En este parámetro se debe indicar 
            el nombre con el que se identificará el modelo.
        """

        ### Type
        if((alias is None) | (type(alias) is str)): pass
        else: raise RuntimeError(STR_ERROR('alias'))
        ### Valid parameters
        if(alias.replace('_', '').isalnum()): pass
        else: raise RuntimeError(ALIAS_ERROR)

        self.alias = alias
        return
    # End def

    # Start method
    def update_output_dir(self, output_dir: str) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `output_dir` de una instancia.

        ## Parámetros:
            * `output_dir` (str): En este parámetro se debe indicar 
            el directorio donde se guardarán las capas intermedias y finales.
        """
        # =========================== #
        # Checks

        ### Type
        if((output_dir is None) | (type(output_dir) is str)): pass
        else: STR_ERROR('output_dir')
        ### Valid parameters
        if(os.path.exists(output_dir)): pass
        else: raise RuntimeError(DIR_ERROR)

        # =========================== #
        # Update Attribute
        self.output_dir = output_dir
        return
    # End def

    # Start method
    def update_crs(self, epsg: int) -> None:
        """
        ## Descripción
        Permite modificar el parámetro `epsg` de una instancia.

        ## Parámetros:
            * `epsg` (int): En este parámetro se debe indicar 
            el código de la referencia espacial.
        """

        ### Type
        if((epsg is None) | (type(epsg) is int)): pass
        else: raise RuntimeError(INT_ERROR('epsg'))
        ### Valid parameters
        CRS(epsg)
        
        # =========================== #
        # Update Attribute
        self.epsg = epsg
        return
    # End def

    # Start method
    def add_criteria(self, criteria_alias: str, importance: Annotated[int, Ge(1)] = None) -> None:
        """
        ## Descripción
        Agregar un nuevo criterio al modelo.

        ## Parámetros:
            * `criteria_alias` (str): Nombre con el que se 
            va a identificar al criterio.
            * `importance` (int [Greater equal than 1], optional): 
            Importancia del criterio (para más información leer 
            el README). No es necesario establecerlo ahora, 
            pero si se requerirá asignar un valor antes de 
            ejecutar el cómputo del modelo. Defaults to `None`.
        """
        # =========================== #
        # Checks
        
        ### Types
        # alias
        if((criteria_alias is None) | (type(criteria_alias) is str)): pass
        else: raise RuntimeError(STR_ERROR('criteria_alias'))
        # importance
        if((importance is None) | (type(importance) is int)): pass
        else: raise RuntimeError(PINT_ERROR('importance'))

        ### Valid parameters
        # alias
        if(criteria_alias.replace('_', '').isalnum()): pass
        else: raise RuntimeError(ALIAS_ERROR)
        # importance
        if(importance is None): pass
        elif(type(importance) is int and importance >= 1): pass
        else: raise RuntimeError(PINT_ERROR('importance'))

        ### If exists the alias
        names = list(self.criterias.keys())
        if(criteria_alias in names): raise RuntimeError(ALIAS2_ERROR)

        # =========================== #
        # Add criteria
        self.criterias[criteria_alias] = SMCDACriteria(criteria_alias, importance)
        
        return
    # End def

    # =============================== #
    # Next upgrades: methods
    # ------------------------------- #

    # Start method
    def delete_criteria(self, criteria_alias: str) -> None:
        """
        ## Descripción
        Elimina un criterio del modelo.

        ## Parámetros:
            * `criteria_alias` (str): Nombre del criterio 
            que se quiere eliminar.
        """
        ### If exists the alias, delete it
        names = list(self.criterias.keys())
        if(criteria_alias in names): del self.criterias[criteria_alias]
        else: raise RuntimeError("The criteria with that name does not exist")

        return
    # End def

    # Start method
    def update_criteria(self, current_criteria_alias: str, new_criteria_alias: str = None, importance: Annotated[int, Ge(1)] = None) -> None:
        """
        ## Descripción
        Modificar el alias del criterio y/o la importancia del criterio.

        ## Parámetros:
            * `current_criteria_alias` (str): Alias actual del criterio 
            que se quiere modificar.
            * `new_criteria_alias` (str): Nuevo alias del criterio. 
            * `importance` (str): Importancia del criterio. 
        """
        # =========================== #
        # Update Attributes
        
        # Store the criteria in an object
        criteria = self.criterias[current_criteria_alias]
        # Check if pass a new alias
        if(new_criteria_alias is not None): criteria.update_alias(new_criteria_alias)
        # Check if pass a new importance
        if(importance is not None): criteria.update_importance(importance)

        return
    # End def

    # Start method
    @overload
    def add_layer2criteria(self, ):
        """
        ## Descripción

        ## Parámetros:
            * `current_criteria_alias` (str): Alias actual del criterio 
            que se quiere modificar.
            * `new_criteria_alias` (str): Nuevo alias del criterio. 
            * `importance` (str): Importancia del criterio. 
        """
        return
    # End def

    def add_layer2feasibleregion(self, ):
        return
    # End def

    def delete_layer(self):
        return
    # End def

    def update_layer(self):
        return
    # End def

    def print_criteria():
        return
    # End def

    def print_layer():
        return
    # End def

    def asign_importance(self, criteria: str = None, to_layers: bool = False):
        return
    # End def

    def run_analysis():
        """            
        * `pixel_size` (float, optional): El resultado 
        de la ejecución es una capa ráster con píxeles
        cuadrados. Es recomendable especificar el tamaño 
        del píxel, ya que permitirá controla el trade-off
        entre detalle y tiempo de cómputo, también es 
        recomendable tener clara la unidad de medida del 
        sistema de coordenadas, por las dudas se agrega un
        tope superior de max(X / 10^6, Y/ 10^6). Defaults 
        to min(X / 5000, Y / 5000)
        """
        return
    # End def

    # Start method
    def __str__(self):
        text  = "\n# ==================================== #"
        text += "\n# Spatial MCDA model"
        text += f"\n# alias: {self.alias}"
        text += f"\n# output_dir: {self.output_dir}"
        text += f"\n# EPSG: {self.epsg}"
        text += "\n#"
        text += "\n# Criterias:"
        if(not self.criterias):
            text += "\n#    EMPTY"
        else:
            for c in self.criterias:
                text += f"\n#    {c.name}    [{check_importance(c)}]"
        # End if
        text += "\n#"
        text += "\n# Note: Criteria importance in squared brackets."
        text += "\n# ------------------------------------ #\n"
        return text
    # End def
# End class