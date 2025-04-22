# ---------
from typing import BinaryIO

from ecma376_office.opc.package import PPTxPackage, WordPackage
from ecma376_office.pml.presentation import Presentation
from ecma376_office.wml.wordprocessing import WordProcessing


def open_pptx(filename: str | BinaryIO):
    """打开pptx文件"""

    pptx_package = PPTxPackage.open(filename)

    return Presentation(pptx_package, pptx_package.presentation_part)


def open_docx(filename: str | BinaryIO):
    """打开docx文件"""

    docx_package = WordPackage.open(filename)

    return WordProcessing(docx_package, docx_package.docx_main_part)


def open_xlsx(filename: str):
    """打开xlsx文件"""
