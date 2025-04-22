# opc 相关的部件注册

from ecma376_office.opc.constants import CONTENT_TYPE as OCT
from ecma376_office.opc.parts import CorePropertiesPart, ImagePart
from ecma376_office.part import PART_TYPE_MAP

# 注册OPC的不同类型的部件的构造对象

PART_TYPE_MAP.update({
    OCT.CORE_PROPERTIES: CorePropertiesPart,
    OCT.JPEG: ImagePart,
    OCT.JPG: ImagePart,
    OCT.PNG: ImagePart,
    OCT.GIF: ImagePart,
    OCT.JPEG: ImagePart,
    OCT.JPEG: ImagePart,
})
