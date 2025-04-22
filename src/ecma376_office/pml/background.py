from __future__ import annotations

from typing import Optional

from ecma376_office.oxml.dml.main import CT_StyleMatrixReference
from ecma376_office.oxml.pml.core import CT_Background, CT_BackgroundProperties


class BackGround:
    """幻灯片背景"""

    def __init__(self, oxml: CT_Background) -> None:
        self.oxml = oxml

    @property
    def style_matrix_reference(self) -> Optional[CT_StyleMatrixReference]:
        """填充样式"""

        bg = self.oxml.background_pr

        if isinstance(bg, CT_StyleMatrixReference):
            return bg

        return None

    @property
    def properties(self):
        """效果特性"""

        bg = self.oxml.background_pr

        # 样式矩阵参考
        if isinstance(bg, CT_BackgroundProperties):
            return bg

        return None
