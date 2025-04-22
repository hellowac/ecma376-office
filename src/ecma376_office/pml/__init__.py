# PML 相关的部件注册

from ecma376_office.part import PART_TYPE_MAP
from ecma376_office.pml.constants import CONTENT_TYPE as CT
from ecma376_office.pml.parts import (
    CommentAuthorsPart,
    CommentsPart,
    HandoutMasterPart,
    NotesMasterPart,
    NotesSlidePart,
    PresentaionPart,
    PresentationPropertiesPart,
    SlideLayoutPart,
    SlideMasterPart,
    SlidePart,
    SlideSynchronizationDataPart,
    UserDefinedTagsPart,
    ViewProperitesPart,
)

PART_TYPE_MAP.update({
    CT.Presentation: PresentaionPart,
    CT.Presentation1: PresentaionPart,
    CT.Presentation2: PresentaionPart,
    CT.CommentAuthors: CommentAuthorsPart,
    CT.Comments: CommentsPart,
    CT.HandoutMaster: HandoutMasterPart,
    CT.NotesMaster: NotesMasterPart,
    CT.NotesSlide: NotesSlidePart,
    CT.PresentationProperties: PresentationPropertiesPart,
    CT.Slide: SlidePart,
    CT.SlideLayout: SlideLayoutPart,
    CT.SlideMaster: SlideMasterPart,
    CT.SlideSynchronizationData: SlideSynchronizationDataPart,
    CT.UserDefinedTags: UserDefinedTagsPart,
    CT.ViewProperties: ViewProperitesPart,
})
