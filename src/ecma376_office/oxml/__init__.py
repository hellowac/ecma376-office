# 注册 命名空间中的 类映射
import logging

logger = logging.getLogger(__name__)

# opc  # opc包封装必要xml定义
# dml  # 文档基础xml定义，绘制，颜色，等等
from ecma376_office.oxml.dml import dml_diagram_namespace as dml_diagram_namespace
from ecma376_office.oxml.dml import dml_main_namespace as dml_main_namespace
from ecma376_office.oxml.opc import content_type_namespace as content_type_namespace
from ecma376_office.oxml.opc import core_properties_namespace as core_properties_namespace
from ecma376_office.oxml.opc import relationship_namespace as relationship_namespace

# pml  # *.pptx 文件
from ecma376_office.oxml.pml import pml_core_namespace  # noqa: F401

# shared  # opc包共享的xml定义
from ecma376_office.oxml.shared import (
    shared_additional_character_namespace as shared_additional_character_namespace,
)
from ecma376_office.oxml.shared import (
    shared_bibliography_namespace as shared_bibliography_namespace,
)
from ecma376_office.oxml.shared import (
    shared_common_st_namespace as shared_common_st_namespace,
)
from ecma376_office.oxml.shared import (
    shared_cust_data_pr_namespace as shared_cust_data_pr_namespace,
)
from ecma376_office.oxml.shared import (
    shared_custom_schema_pr_namespace as shared_custom_schema_pr_namespace,
)
from ecma376_office.oxml.shared import (
    shared_doc_custom_pr_namespace as shared_doc_custom_pr_namespace,
)
from ecma376_office.oxml.shared import (
    shared_doc_pr_extended_namespace as shared_doc_pr_extended_namespace,
)
from ecma376_office.oxml.shared import (
    shared_doc_pr_variant_namespace as shared_doc_pr_variant_namespace,
)
from ecma376_office.oxml.shared import (
    shared_math_namespace as shared_math_namespace,
)

# ecma-376 第一版的vml模块的xml定义
from ecma376_office.oxml.vml import vml_drawing_namespace, vml_main_namespace  # noqa: F401

# wml  # *.word 文件, 暂不支持
from ecma376_office.oxml.wml import wml_main_namespace  # noqa: F401

# sml  # *.xlsx 文件, 暂不支持

logger.info('oxml 初始化xml对象模型成功!!!')
