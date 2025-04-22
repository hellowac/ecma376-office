"""
对应xsd: shared-bibliography.xsd


<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema"
  xmlns="http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
  xmlns:s="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
  targetNamespace="http://schemas.openxmlformats.org/officeDocument/2006/bibliography"
  elementFormDefault="qualified">
  <xsd:import namespace="http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes"
    schemaLocation="shared-commonSimpleTypes.xsd"/>
  ...
</xsd:schema>
"""

from __future__ import annotations

import logging
from typing import Optional, TypeVar

from ecma376_office.oxml import utils
from ecma376_office.oxml.base import OxmlBaseElement, ST_BaseEnumType, lookup
from ecma376_office.oxml.exceptions import OxmlElementValidateError
from ecma376_office.oxml.shared.common_simple_types import CT_String as s_CT_String
from ecma376_office.oxml.shared.common_simple_types import ST_String as s_ST_String

namespace_b = 'http://schemas.openxmlformats.org/officeDocument/2006/bibliography'
namespace_s = 'http://schemas.openxmlformats.org/officeDocument/2006/sharedTypes'

logger = logging.getLogger(__name__)

ns_map = {
    'b': namespace_b,  # 当前命名空间
    's': namespace_s,
}


def qn(tag: str):
    """将 dc:creator 这种的标签,转换为 {http://purl.org/dc/elements/1.1/}creator 这样的形式"""

    global ns_map

    if ':' not in tag:
        return tag

    ns_prefix, ns = tag.split(':')

    return f'{{{ns_map[ns_prefix]}}}{ns}'


SubBaseElement = TypeVar('SubBaseElement', bound=OxmlBaseElement)


class ST_SourceType(ST_BaseEnumType):
    """
    aaa
    """

    ArticleInAPeriodical = 'ArticleInAPeriodical'
    Book = 'Book'
    BookSection = 'BookSection'
    JournalArticle = 'JournalArticle'
    ConferenceProceedings = 'ConferenceProceedings'
    Report = 'Report'
    SoundRecording = 'SoundRecording'
    Performance = 'Performance'
    Art = 'Art'
    DocumentFromInternetSite = 'DocumentFromInternetSite'
    InternetSite = 'InternetSite'
    Film = 'Film'
    Interview = 'Interview'
    Patent = 'Patent'
    ElectronicSource = 'ElectronicSource'
    Case = 'Case'
    Misc = 'Misc'


class CT_NameListType(OxmlBaseElement):
    """
    aaa
    """

    def person(self) -> list[CT_PersonType]:
        """
        aaa
        """

        return getattr(self, qn('b:Person'))


class CT_PersonType(OxmlBaseElement):
    """
    aaa
    """

    def last(self) -> list[s_CT_String]:
        """
        aaa
        """

        return getattr(self, qn('s:Last'))

    def first(self) -> list[s_CT_String]:
        """
        aaa
        """

        return getattr(self, qn('s:First'))

    def middle(self) -> list[s_CT_String]:
        """
        aaa
        """

        return getattr(self, qn('s:Middle'))


class CT_NameType(OxmlBaseElement):
    """
    aaa
    """

    def name_list(self) -> CT_NameListType:
        """
        aaa
        """

        return getattr(self, qn('b:NameList'))


class CT_NameOrCorporateType(OxmlBaseElement):
    """
    aaa
    """

    def name_lst(self) -> Optional[CT_NameListType | s_CT_String]:
        """
        aaa
        """

        name_list = getattr(self, qn('b:NameList'))

        if name_list is not None:
            return name_list

        corporate: s_CT_String = getattr(self, qn('s:Corporate'))

        if corporate is not None:
            return corporate

        msg = '应至少存在一个元素'
        raise OxmlElementValidateError(msg)


class CT_AuthorType(OxmlBaseElement):
    """
    aaa
    """

    def author_type(self) -> list[CT_NameType | CT_NameOrCorporateType]:
        """
        aaa
        """

        tags = (
            qn('b:Artist'),  # CT_NameType
            qn('b:Author'),  # CT_NameOrCorporateType
            qn('b:BookAuthor'),  # CT_NameType
            qn('b:Compiler'),  # CT_NameType
            qn('b:Composer'),  # CT_NameType
            qn('b:Conductor'),  # CT_NameType
            qn('b:Counsel'),  # CT_NameType
            qn('b:Director'),  # CT_NameType
            qn('b:Editor'),  # CT_NameType
            qn('b:Interviewee'),  # CT_NameType
            qn('b:Interviewer'),  # CT_NameType
            qn('b:Inventor'),  # CT_NameType
            qn('b:Performer'),  # CT_NameOrCorporateType
            qn('b:ProducerName'),  # CT_NameType
            qn('b:Translator'),  # CT_NameType
            qn('b:Writer'),  # CT_NameType
        )

        return self.iterchildren(*tags, reversed=False)  # type: ignore



class CT_SourceType(OxmlBaseElement):
    """
    aaa
    """

    def source_type(self) -> list[s_CT_String]:
        """
        aaa
        """

        tags = (
            qn('s:AbbreviatedCaseNumbe'),
            qn('s:AlbumTitl'),
            qn('s:Autho'),
            qn('s:BookTitl'),
            qn('s:Broadcaster'),
            qn('s:BroadcastTitl'),
            qn('s:CaseNumbe'),
            qn('s:ChapterNumbe'),
            qn('s:City'),
            qn('s:Comments'),
            qn('s:ConferenceNam'),
            qn('s:CountryRegio'),
            qn('s:Court'),
            qn('s:Day'),
            qn('s:DayAccesse'),
            qn('s:Department'),
            qn('s:Distributor'),
            qn('s:Edition'),
            qn('s:Guid'),
            qn('s:Institution'),
            qn('s:InternetSiteTitl'),
            qn('s:Issue'),
            qn('s:JournalNam'),
            qn('s:LC'),
            qn('s:Medium'),
            qn('s:Month'),
            qn('s:MonthAccesse'),
            qn('s:NumberVolume'),
            qn('s:Pages'),
            qn('s:PatentNumbe'),
            qn('s:PeriodicalTitl'),
            qn('s:ProductionCompan'),
            qn('s:PublicationTitl'),
            qn('s:Publisher'),
            qn('s:RecordingNumbe'),
            qn('s:RefOrde'),
            qn('s:Reporter'),
            qn('s:SourceTyp'),
            qn('s:ShortTitl'),
            qn('s:StandardNumbe'),
            qn('s:StateProvinc'),
            qn('s:Station'),
            qn('s:Tag'),
            qn('s:Theater'),
            qn('s:ThesisTyp'),
            qn('s:Title'),
            qn('s:Type'),
            qn('s:URL'),
            qn('s:Version'),
            qn('s:Volume'),
            qn('s:Year'),
            qn('s:YearAccesse'),
        )

        return self.iterchildren(*tags, reversed=False)  # type: ignore


class CT_Sources(OxmlBaseElement):
    """
    aaa
    """

    def source(self) -> list[CT_SourceType]:
        """
        aaa
        """

        return getattr(self, qn('b:Source'))

    def selected_style(self) -> Optional[s_ST_String]:
        """
        aaa
        """

        val = self.attrib.get('SelectedStyle')

        if val is None:
            return None

        return s_ST_String(utils.AnyStrToStr(val))  # type: ignore

    def style_name(self) -> Optional[s_ST_String]:
        """
        aaa
        """

        val = self.attrib.get('StyleName')

        if val is None:
            return None

        return s_ST_String(utils.AnyStrToStr(val))  # type: ignore

    def uri(self) -> Optional[s_ST_String]:
        """
        aaa
        """

        val = self.attrib.get('URI')

        if val is None:
            return None

        return s_ST_String(utils.AnyStrToStr(val))  # type: ignore


shared_bibliography_namespace = lookup.get_namespace(namespace_b)
shared_bibliography_namespace[None] = OxmlBaseElement
shared_bibliography_namespace['Source'] = CT_SourceType
shared_bibliography_namespace['Sources'] = CT_Sources
shared_bibliography_namespace['Person'] = CT_PersonType
shared_bibliography_namespace['NameList'] = CT_NameType
shared_bibliography_namespace['Artist'] = CT_NameListType
shared_bibliography_namespace['Author'] = CT_NameOrCorporateType
shared_bibliography_namespace['Compiler'] = CT_NameType
shared_bibliography_namespace['Composer'] = CT_NameType
shared_bibliography_namespace['Conductor'] = CT_NameType
shared_bibliography_namespace['Counsel'] = CT_NameType
shared_bibliography_namespace['Director'] = CT_NameType
shared_bibliography_namespace['Editor'] = CT_NameType
shared_bibliography_namespace['Interviewee'] = CT_NameType
shared_bibliography_namespace['Interviewer'] = CT_NameType
shared_bibliography_namespace['Inventor'] = CT_NameType
shared_bibliography_namespace['Performer'] = CT_NameOrCorporateType
shared_bibliography_namespace['ProducerName'] = CT_NameType
shared_bibliography_namespace['Translator'] = CT_NameType
shared_bibliography_namespace['Writer'] = CT_NameType
