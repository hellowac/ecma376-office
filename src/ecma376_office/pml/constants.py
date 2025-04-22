"""
PML 包所需的常量值
"""

from enum import StrEnum

from ecma376_office.constants import RELATIONSHIP_TYPE_BASE


class CONTENT_TYPE(StrEnum):
    """
    各个部件的内容类型
    """

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#133-部件概览

    # 13.3.1 评论作者部件
    CommentAuthors = 'application/vnd.openxmlformats-officedocument.drawingml.viewProps+xml'

    # 13.3.2 评论部件
    Comments = 'application/vnd.openxmlformats-officedocument.presentationml.comments+xml'

    # 13.3.3 讲义母板部件
    HandoutMaster = 'application/vnd.openxmlformats-officedocument.presentationml.handoutMaster+xml'

    # 13.3.4 笔记母版部件
    NotesMaster = 'application/vnd.openxmlformats-officedocument.presentationml.notesMaster+xml'

    # 13.3.5 笔记幻灯片部件
    NotesSlide = 'application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml'

    # 13.3.6 演示部件
    Presentation = 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'
    Presentation1 = 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'
    Presentation2 = 'application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml'

    # 13.3.7 演示属性部件
    PresentationProperties = 'application/vnd.openxmlformats-officedocument.presentationml.presProps+xml'

    # 13.3.8 幻灯片部件
    Slide = 'application/vnd.openxmlformats-officedocument.presentationml.slide+xml'

    # 13.3.9 幻灯片布局部件
    SlideLayout = 'application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml'

    # 13.3.10 幻灯片母版部件
    SlideMaster = 'application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml'

    # 13.3.11 幻灯片同步数据部件
    SlideSynchronizationData = 'application/vnd.openxmlformats-officedocument.presentationml.slideUpdateInfo+xml'

    # 13.3.12 用户已定义标签部件
    UserDefinedTags = 'application/vnd.openxmlformats-officedocument.presentationml.tags+xml'

    # 13.3.13 视图属性部件
    ViewProperties = 'application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml'
    # -------------------------------------------------------------------------------------------


class NAMESPACE(StrEnum):
    """OPC XML 命名空间的常量值"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#133-部件概览

    # 13.3.1 评论作者部件
    CommentAuthors = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.2 评论部件
    Comments = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.3 讲义母板部件
    HandoutMaster = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.4 笔记母版部件
    NotesMaster = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.5 笔记幻灯片部件
    NotesSlide = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.6 演示部件
    Presentation = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.7 演示属性部件
    PresentationProperties = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.8 幻灯片部件
    Slide = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.9 幻灯片布局部件
    SlideLayout = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.10 幻灯片母版部件
    SlideMaster = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.11 幻灯片同步数据部件
    SlideSynchronizationData = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.12 用户已定义标签部件
    UserDefinedTags = 'http://purl.oclc.org/ooxml/presentationml/main'

    # 13.3.13 视图属性部件
    ViewProperties = 'http://purl.oclc.org/ooxml/presentationml/main'
    # -------------------------------------------------------------------------------------------


class RELATIONSHIP_TYPE(str, RELATIONSHIP_TYPE_BASE):
    """OPC 关系类型"""

    # -------------------------------------------------------------------------------------------
    # https://hellowac.github.io/ecma-376-zh-cn/ecma-part1/chapter-13/#133-部件概览

    # 13.3.1 评论作者部件
    # CommentAuthors = "http://purl.oclc.org/ooxml/officeDocument/relationships/comments"
    CommentAuthors = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/commentAuthors'

    # 13.3.2 评论部件
    # Comments = "http://purl.oclc.org/ooxml/officeDocument/relationships/comments"
    Comments = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/comments'

    # 13.3.3 讲义母板部件
    # HandoutMaster = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/hnadoutMaster"
    # )
    HandoutMaster = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/handoutMaster'

    # 13.3.4 笔记母版部件
    # NotesMaster = "http://purl.oclc.org/ooxml/officeDocument/relationships/notesMaster"
    NotesMaster = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster'

    # 13.3.5 笔记幻灯片部件
    # NotesSlide = "http://purl.oclc.org/ooxml/officeDocument/relationships/notesSlide"
    NotesSlide = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide'

    # 13.3.6 演示部件
    # Presentation = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/officeDocument"
    # )
    Presentation = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument'

    # 13.3.7 演示属性部件
    # PresentationProperties = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/presProps"
    # )
    PresentationProperties = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps'

    # 13.3.8 幻灯片部件
    # Slide = "http://purl.oclc.org/ooxml/officeDocument/relationships/slide"
    Slide = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide'

    # 13.3.9 幻灯片布局部件
    # SlideLayout = "http://purl.oclc.org/ooxml/officeDocument/relationships/slideLayout"
    SlideLayout = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout'

    # 13.3.10 幻灯片母版部件
    # SlideMaster = "http://purl.oclc.org/ooxml/officeDocument/relationships/slideMaster"
    SlideMaster = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster'

    # 13.3.11 幻灯片同步数据部件
    # SlideSynchronizationData = (
    #     "http://purl.oclc.org/ooxml/officeDocument/relationships/slideUpdateInfo"
    # )
    SlideSynchronizationData = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideUpdateInfo'

    # 13.3.12 用户已定义标签部件
    # UserDefinedTags = "http://purl.oclc.org/ooxml/officeDocument/relationships/tags"
    UserDefinedTags = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/tags'

    # 13.3.13 视图属性部件
    # ViewProperties = "http://purl.oclc.org/ooxml/officeDocument/relationships/viewProps"
    ViewProperties = 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps'

    # 13.4 HTML 发布位置
    HTMLPublishLocation = 'http://purl.oclc.org/ooxml/officeDocument/relationships/htmlPubSaveAs'

    # 13.5 幻灯片同步服务器位置
    SlideSynchronizationServerLocation = 'http://purl.oclc.org/ooxml/officeDocument/relationships/slideUpdateUrl'
    # -------------------------------------------------------------------------------------------
