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
from typing import Annotated, overload, Union
from annotated_types import Ge
from osgeo import gdal, ogr, osr
from core.utils import *
from core.messages import *
from core.SMCDALayer import SMCDALayer


# ======================================================= #
# SMCDACriteria class
# ------------------------------------------------------- #

class SMCDACriteria:
    """
        ### Objetivo
        Organizar la información del criterio. Esta clase no
        está creada para que el público la use, más bien para
        tener un orden interno y encapsular métodos para analizar
        el comportamiento de la información.
    """

    # Start method
    def __init__(self, alias: str, importance: Union[Annotated[int, Ge(1)], None] = None) -> None:
        """
        ## Descripción
        Crea una instancia de la clase, la cual permite la 
        organización del modelo.

        ## Parámetros:
            * `alias` (str): Nombre con el que el programa se va a referir al criterio.
            * `importance` (int [Greater equal than 1] | None, optional): 
            Importancia del criterio (para más información leer 
            el README).
        """
        # =========================== #
        # Checks
        
        ### Types
        # name
        if((alias is None) | (type(alias) is str)): pass
        else: raise RuntimeError(STR_ERROR('name'))
        # importance
        if((importance is None) | (type(importance) is int)): pass
        else: raise RuntimeError(PINT_ERROR('importance'))
        
        ### Valid parameters
        # name
        if(alias.replace('_', '').isalnum()): pass
        else: raise RuntimeError(ALIAS_ERROR)
        # importance
        if(importance is None): pass
        elif(type(importance) is int and importance >= 1): pass
        else: raise RuntimeError(PINT_ERROR('importance'))

        # =========================== #
        # Add Attributes

        self.alias = alias
        self.importance = importance
        self.layers = {}
    # End def
    
    # Start method
    def update_alias(self, alias: str) -> None:
        """
        ## Descripción
        Modifica el alias del criterio.

        ## Parámetros:
            * `alias` (str): Nuevo nombre con el que el programa se va a referir al criterio.
        """

        # =========================== #
        # Checks

        ### Type
        if((alias is None) | (type(alias) is str)): pass
        else: raise RuntimeError(STR_ERROR('criteria_alias'))
        ### Valid parameters
        if(alias.replace('_', '').isalnum()): pass
        else: raise RuntimeError(ALIAS_ERROR)

        # =========================== #
        # Update Attribute
        self.alias = alias
        return
    # End def

    # Start method
    def update_importance(self, importance: Union[Annotated[int, Ge(1)], None]) -> None:
        """
        ## Descripción
        Modifica la importancia del criterio.

        ## Parámetros:
            * `importance` (int [Greater equal than 1] | None, optional): 
            Importancia del criterio (para más información leer 
            el README).
        """

        # =========================== #
        # Checks

        ### Types
        if((importance is None) | (type(importance) is int)): pass
        else: raise RuntimeError(PINT_ERROR('importance'))
        
        ### Valid parameters
        if(importance >= 1): pass
        else: raise RuntimeError(PINT_ERROR('importance'))

        self.importance = importance
        return
    # End def

    # Start method
    @overload
    def add_layer(self, alias: str, layer: SMCDALayer, weight: float = None) -> None:
        """
        ## Descripción
        Agrega una capa al criterio.

        ## Parámetros:
            * `alias` (str): Nombre con el que el programa se va a referir a la capa.
            * `layer` (SMCDALayer): Objeto que organiza toda la información necesaria para poder realizar el ejercicio.
            * `weight` (float, optional): Peso de la capa en el criterio. A diferencia del criterio, en este nivel no es difícil asignar pesos a las capas, ya que las características que representan son más homogéneas. No es obligatorio asignarlo en el momento de la creación, se puede incorporar y/o modificar luego de forma individual (con el método update_layer) o de forma conjunta (con el método asign_weights2layers). Si es obligatorio asignarle pesos a todas las capas antes de ejecutar su computo. No se exige que los pesos sumen `1`, esto se forzará al tipificar el resultado del criterio.
        """
        ...
    @overload
    def add_layer(self, alias: str, path: str, FieldName: str = None, positive: bool = True, na: int = 0, weight: float = None) -> None:
        """
        ## Descripción
        Agrega una capa al criterio.

        ## Parámetros:
            * `alias` (str): Nombre con el que el programa se va a referir a la capa.
            * `path` (str): Objeto que organiza toda la información necesaria para poder realizar el ejercicio.
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
            * `weight` (float, optional): Peso de la capa en el criterio. A diferencia del criterio, en este nivel no es difícil asignar pesos a las capas, ya que las características que representan son más homogéneas. No es obligatorio asignarlo en el momento de la creación, se puede incorporar y/o modificar luego de forma individual (con el método update_layer) o de forma conjunta (con el método asign_weights2layers). Si es obligatorio asignarle pesos a todas las capas antes de ejecutar su computo. No se exige que los pesos sumen `1`, esto se forzará al tipificar el resultado del criterio.
        """
        ...
    def add_layer(self, alias: str = None, layer: SMCDALayer = None, path: str = None, FieldName: str = None, positive: bool = True, na: int = 0, weight: float = None) -> None:

        # Create key in layers dict
        self.layers[alias] = {}
        if(layer is not None):
            # Check if it is a SMCDALayer object
            # Add the SMCDALayer object
            if(type(layer) == SMCDALayer): self.layers[alias]["object"] = layer
            else: raise RuntimeError(LAYER_ERROR)
            
        else:
            # Create and add the SMCDALayer object
            self.layers[alias]["object"] =  SMCDALayer(path, FieldName, positive, na)
        # End if
        
        # Add the weight
        self.layers[alias]["weight"] = weight
        return
    # End def
    
    # Start method
    def delete_layer(self, alias: str) -> None:
        """
        ## Descripción
        Elimina una capa en el criterio.

        ## Parámetros:
            * `alias` (str): Nombre de la capa que se quiere eliminar.
        """
        del self.layers[alias]
        return
    # End def
    
    # Start method
    def update_layer(self, current_alias: str, new_alias: str = None, path: str = None, FieldName: str = None, positive: bool = True, neutral: int = 0, weight: float = None) -> None:
        """
        ## Descripción
        Elimina una capa en el criterio.

        ## Parámetros:
            * `current_alias` (str): Nombre actual de la capa que se quiere modificar.
            * `new_alias` (str, optional): Nuevo nombre que se le quiere dar a la capa.
            * `path` (str, optional): En este parámetro se debe indicar la
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
            * `weight` (float, optional): Peso de la capa en el criterio. A diferencia del criterio, en este nivel no es difícil asignar pesos a las capas, ya que las características que representan son más homogéneas. No es obligatorio asignarlo en el momento de la creación, se puede incorporar y/o modificar luego de forma individual (con el método update_layer) o de forma conjunta (con el método asign_weights2layers). Si es obligatorio asignarle pesos a todas las capas antes de ejecutar su computo. No se exige que los pesos sumen `1`, esto se forzará al tipificar el resultado del criterio.
        """

        layer = self.layers[current_alias]["object"]
        if(path is not None): layer.update_path(path)
        if(FieldName is not None): layer.update_field(FieldName)
        if(positive is not None): layer.update_positive(positive)
        if(neutral is not None): layer.update_neutral(neutral)
        if(new_alias is not None): 
            del self.layers[current_alias]
            self.layers[new_alias]["object"] = layer
            if(weight is not None): self.layers[new_alias]["weight"] = weight
        else:
            self.layers[current_alias]["object"] = layer
            if(weight is not None): self.layers[current_alias]["weight"] = weight
        # End if
        return
    # End def
    
    # Start method
    def asign_weights2layers(self, weight: Union[float, int, list] = None, layer: Union[str, list] = None, using_importance: bool = False) -> None:

        # Check if it has the same length as self.layers

        # Check if "importance" is a list that contains only
        # positive integers.

        # If importance is none, ask the relative importance
        # of the j elements in {2, 3, ..., n} against the
        # first element

        # Check the number of variables, if equals 1, don't
        # ask.
        return
    # End def

    # =============================== #
    # Next upgrades: methods
    # ------------------------------- #    
    def __str__(self):
        text  = "\n# ==================================== #"
        text += "\n# Spatial MCDA model"
        text += "\n#"
        text += f"\n# Criteria: {self.name}"
        text += "\n#"
        text += f"\n# Variables:"
        for x in self.layers:
            text += f"\n# {x.alias} ()"
        return text
    # End def
# End class

def check_importance(criteria: SMCDACriteria) -> Union[float, str]:
    # Check if criteria has importance
    if(criteria.importance is None):
        return "<NA>"
    else:
        return str(criteria.importance)
# End def
