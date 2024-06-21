# ======================================================= #
"""
@ProjectName: SpatialMCDA
@Author: FernandoCastano
@Email: castano.fernando.martin@gmail.com
@Version: 0.1.0
"""
# ------------------------------------------------------- #

from core.SMCDAModel import SMCDAModel
from core.SMCDACriteria import SMCDACriteria
from core.SMCDALayer import SMCDALayer

model1 = SMCDAModel("modeloprueba", "C:/test", 22185)
print(model1)
model1.add_criteria("socioeconomic")
print(model1)

qwe = SMCDACriteria("qwe")
path1 = "C:/Users/casta/Downloads/radios_eph/radios_eph.shp"
qwe.add_layer("layer1", SMCDALayer(path1))
qwe.add_layer(SMCDALayer(path1))
print(asd)
qwe.layers["object"] = SMCDALayer(path1)
