# Copyright (c) 2017, The MITRE Corporation. All rights reserved.
# See LICENSE.txt for complete terms.

import sys

from mixbox.binding_utils import *
from . import cybox_common
from . import user_account_object


XML_NS = "http://cybox.mitre.org/objects#WinUserAccountObject-2"


class WindowsPrivilegeType(user_account_object.PrivilegeType):
    """Windows Privilege represents a single privilege that a user may have
    within Windows."""
    xmlns          = XML_NS
    xmlns_prefix   = "WinUserAccountObj"
    xml_type       = "WindowsPrivilegeType"
    xsi_type       = "%s:%s" % (xmlns_prefix, xml_type)

    subclass = None
    superclass = user_account_object.PrivilegeType
    def __init__(self, User_Right=None):
        super(WindowsPrivilegeType, self).__init__()
        self.User_Right = User_Right
    def factory(*args_, **kwargs_):
        if WindowsPrivilegeType.subclass:
            return WindowsPrivilegeType.subclass(*args_, **kwargs_)
        else:
            return WindowsPrivilegeType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_User_Right(self): return self.User_Right
    def set_User_Right(self, User_Right): self.User_Right = User_Right
    def validate_StringObjectPropertyType(self, value):
        # Validate type cybox_common.StringObjectPropertyType, a restriction on None.
        pass
    def hasContent_(self):
        if (
            self.User_Right is not None or
            super(WindowsPrivilegeType, self).hasContent_()
            ):
            return True
        else:
            return False
    def export(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsPrivilegeType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        showIndent(lwrite, level, pretty_print)
        lwrite('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsPrivilegeType')
        if self.hasContent_():
            lwrite('>%s' % (eol_, ))
            self.exportChildren(lwrite, level + 1, namespace_, name_, pretty_print=pretty_print)
            showIndent(lwrite, level, pretty_print)
            lwrite('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            lwrite('/>%s' % (eol_, ))
    def exportAttributes(self, lwrite, level, already_processed, namespace_='WinUserAccountObj:', name_='WindowsPrivilegeType'):
        super(WindowsPrivilegeType, self).exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsPrivilegeType')
        if 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            xsi_type = " xsi:type='%s:%s'" % (self.xmlns_prefix, self.xml_type)
            lwrite(xsi_type)
    def exportChildren(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsPrivilegeType', fromsubclass_=False, pretty_print=True):
        super(WindowsPrivilegeType, self).exportChildren(lwrite, level, 'WinUserAccountObj:', name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.User_Right is not None:
            self.User_Right.export(lwrite, level, 'WinUserAccountObj:', name_='User_Right', pretty_print=pretty_print)
    def build(self, node):
        self.__sourcenode__ = node
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(WindowsPrivilegeType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'User_Right':
            obj_ = cybox_common.StringObjectPropertyType.factory()
            obj_.build(child_)
            self.set_User_Right(obj_)
        super(WindowsPrivilegeType, self).buildChildren(child_, node, nodeName_, True)
# end class WindowsPrivilegeType

class WindowsGroupType(user_account_object.GroupType):
    """Windows Group represents a single windows group."""
    xmlns          = XML_NS
    xmlns_prefix   = "WinUserAccountObj"
    xml_type       = "WindowsGroupType"
    xsi_type       = "%s:%s" % (xmlns_prefix, xml_type)

    subclass = None
    superclass = user_account_object.GroupType
    def __init__(self, Name=None):
        super(WindowsGroupType, self).__init__()
        self.Name = Name
    def factory(*args_, **kwargs_):
        if WindowsGroupType.subclass:
            return WindowsGroupType.subclass(*args_, **kwargs_)
        else:
            return WindowsGroupType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_Name(self): return self.Name
    def set_Name(self, Name): self.Name = Name
    def validate_StringObjectPropertyType(self, value):
        # Validate type cybox_common.StringObjectPropertyType, a restriction on None.
        pass
    def hasContent_(self):
        if (
            self.Name is not None or
            super(WindowsGroupType, self).hasContent_()
            ):
            return True
        else:
            return False
    def export(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsGroupType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        showIndent(lwrite, level, pretty_print)
        lwrite('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsGroupType')
        if self.hasContent_():
            lwrite('>%s' % (eol_, ))
            self.exportChildren(lwrite, level + 1, namespace_, name_, pretty_print=pretty_print)
            showIndent(lwrite, level, pretty_print)
            lwrite('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            lwrite('/>%s' % (eol_, ))
    def exportAttributes(self, lwrite, level, already_processed, namespace_='WinUserAccountObj:', name_='WindowsGroupType'):
        super(WindowsGroupType, self).exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsGroupType')
        if 'xsi:type' not in already_processed:
            already_processed.add('xsi:type')
            xsi_type = " xsi:type='%s:%s'" % (self.xmlns_prefix, self.xml_type)
            lwrite(xsi_type)
    def exportChildren(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsGroupType', fromsubclass_=False, pretty_print=True):
        super(WindowsGroupType, self).exportChildren(lwrite, level, 'WinUserAccountObj:', name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Name is not None:
            self.Name.export(lwrite, level, 'WinUserAccountObj:', name_='Name', pretty_print=pretty_print)
    def build(self, node):
        self.__sourcenode__ = node
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(WindowsGroupType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Name':
            obj_ = cybox_common.StringObjectPropertyType.factory()
            obj_.build(child_)
            self.set_Name(obj_)
        super(WindowsGroupType, self).buildChildren(child_, node, nodeName_, True)
# end class WindowsGroupType

class WindowsUserAccountObjectType(user_account_object.UserAccountObjectType):
    """The WinUserAccountObjectType type is intended to characterize
    Windows user accounts."""

    subclass = None
    superclass = user_account_object.UserAccountObjectType
    def __init__(self, object_reference=None, Custom_Properties=None, xsi_type=None, disabled=None, locked_out=None, Description=None, Domain=None, password_required=None, Full_Name=None, Group_List=None, Home_Directory=None, Last_Login=None, Privilege_List=None, Script_Path=None, Username=None, User_Password_Age=None, Security_ID=None, Security_Type=None):
        super(WindowsUserAccountObjectType, self).__init__(object_reference, Custom_Properties, disabled, locked_out, Description, Domain, password_required, Full_Name, Group_List, Home_Directory, Last_Login, Privilege_List, Script_Path, Username, User_Password_Age, )
        self.Security_ID = Security_ID
        self.Security_Type = Security_Type
    def factory(*args_, **kwargs_):
        if WindowsUserAccountObjectType.subclass:
            return WindowsUserAccountObjectType.subclass(*args_, **kwargs_)
        else:
            return WindowsUserAccountObjectType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_Security_ID(self): return self.Security_ID
    def set_Security_ID(self, Security_ID): self.Security_ID = Security_ID
    def validate_StringObjectPropertyType(self, value):
        # Validate type cybox_common.StringObjectPropertyType, a restriction on None.
        pass
    def get_Security_Type(self): return self.Security_Type
    def set_Security_Type(self, Security_Type): self.Security_Type = Security_Type
    def validate_SIDType(self, value):
        # Validate type cybox_common.SIDType, a restriction on None.
        pass
    def hasContent_(self):
        if (
            self.Security_ID is not None or
            self.Security_Type is not None or
            super(WindowsUserAccountObjectType, self).hasContent_()
            ):
            return True
        else:
            return False
    def export(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsUserAccountObjectType', namespacedef_='', pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        showIndent(lwrite, level, pretty_print)
        lwrite('<%s%s%s' % (namespace_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self.exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsUserAccountObjectType')
        if self.hasContent_():
            lwrite('>%s' % (eol_, ))
            self.exportChildren(lwrite, level + 1, namespace_, name_, pretty_print=pretty_print)
            showIndent(lwrite, level, pretty_print)
            lwrite('</%s%s>%s' % (namespace_, name_, eol_))
        else:
            lwrite('/>%s' % (eol_, ))
    def exportAttributes(self, lwrite, level, already_processed, namespace_='WinUserAccountObj:', name_='WindowsUserAccountObjectType'):
        super(WindowsUserAccountObjectType, self).exportAttributes(lwrite, level, already_processed, namespace_, name_='WindowsUserAccountObjectType')
    def exportChildren(self, lwrite, level, namespace_='WinUserAccountObj:', name_='WindowsUserAccountObjectType', fromsubclass_=False, pretty_print=True):
        super(WindowsUserAccountObjectType, self).exportChildren(lwrite, level, 'WinUserAccountObj:', name_, True, pretty_print=pretty_print)
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Security_ID is not None:
            self.Security_ID.export(lwrite, level, 'WinUserAccountObj:', name_='Security_ID', pretty_print=pretty_print)
        if self.Security_Type is not None:
            self.Security_Type.export(lwrite, level, 'WinUserAccountObj:', name_='Security_Type', pretty_print=pretty_print)
    def build(self, node):
        self.__sourcenode__ = node
        already_processed = set()
        self.buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self.buildChildren(child, node, nodeName_)
    def buildAttributes(self, node, attrs, already_processed):
        super(WindowsUserAccountObjectType, self).buildAttributes(node, attrs, already_processed)
    def buildChildren(self, child_, node, nodeName_, fromsubclass_=False):
        if nodeName_ == 'Security_ID':
            obj_ = cybox_common.StringObjectPropertyType.factory()
            obj_.build(child_)
            self.set_Security_ID(obj_)
        elif nodeName_ == 'Security_Type':
            obj_ = cybox_common.SIDType.factory()
            obj_.build(child_)
            self.set_Security_Type(obj_)
        super(WindowsUserAccountObjectType, self).buildChildren(child_, node, nodeName_, True)
# end class WindowsUserAccountObjectType

GDSClassesMapping = {
    'Build_Utility': cybox_common.BuildUtilityType,
    'Errors': cybox_common.ErrorsType,
    'Time': cybox_common.TimeType,
    'Group_List': user_account_object.GroupListType,
    'Certificate_Issuer': cybox_common.StringObjectPropertyType,
    'User_Password_Age': cybox_common.DurationObjectPropertyType,
    'Metadata': cybox_common.MetadataType,
    'Hash': cybox_common.HashType,
    'Information_Source_Type': cybox_common.ControlledVocabularyStringType,
    'Home_Directory': cybox_common.StringObjectPropertyType,
    'Block_Hash_Value': cybox_common.HashValueType,
    'Fuzzy_Hash_Structure': cybox_common.FuzzyHashStructureType,
    'SubDatum': cybox_common.MetadataType,
    'Segment_Hash': cybox_common.HashValueType,
    'Digital_Signature': cybox_common.DigitalSignatureInfoType,
    'Code_Snippets': cybox_common.CodeSnippetsType,
    'Value': cybox_common.StringObjectPropertyType,
    'Length': cybox_common.IntegerObjectPropertyType,
    'User_Account': user_account_object.UserAccountObjectType,
    'Encoding': cybox_common.ControlledVocabularyStringType,
    'Internationalization_Settings': cybox_common.InternationalizationSettingsType,
    'Tool_Configuration': cybox_common.ToolConfigurationType,
    'English_Translation': cybox_common.StringObjectPropertyType,
    'Functions': cybox_common.FunctionsType,
    'String_Value': cybox_common.StringObjectPropertyType,
    'Build_Utility_Platform_Specification': cybox_common.PlatformSpecificationType,
    'Compiler_Informal_Description': cybox_common.CompilerInformalDescriptionType,
    'System': cybox_common.ObjectPropertiesType,
    'Platform': cybox_common.PlatformSpecificationType,
    'Usage_Context_Assumptions': cybox_common.UsageContextAssumptionsType,
    'Type': cybox_common.ControlledVocabularyStringType,
    'Compilers': cybox_common.CompilersType,
    'Username': cybox_common.StringObjectPropertyType,
    'Tool_Type': cybox_common.ControlledVocabularyStringType,
    'String': cybox_common.ExtractedStringType,
    'Tool': cybox_common.ToolInformationType,
    'Build_Information': cybox_common.BuildInformationType,
    'Tool_Hashes': cybox_common.HashListType,
    'Compiler_Platform_Specification': cybox_common.PlatformSpecificationType,
    'Error_Instances': cybox_common.ErrorInstancesType,
    'Data_Segment': cybox_common.StringObjectPropertyType,
    'Certificate_Subject': cybox_common.StringObjectPropertyType,
    'Language': cybox_common.StringObjectPropertyType,
    'Property': cybox_common.PropertyType,
    'Strings': cybox_common.ExtractedStringsType,
    'Domain': cybox_common.StringObjectPropertyType,
    'File_System_Offset': cybox_common.IntegerObjectPropertyType,
    'Security_Type': cybox_common.SIDType,
    'Reference_Description': cybox_common.StructuredTextType,
    'User_Account_Info': cybox_common.ObjectPropertiesType,
    'Configuration_Settings': cybox_common.ConfigurationSettingsType,
    'Simple_Hash_Value': cybox_common.SimpleHashValueType,
    'Byte_String_Value': cybox_common.HexBinaryObjectPropertyType,
    'Group': user_account_object.GroupType,
    'Instance': cybox_common.ObjectPropertiesType,
    'Privilege': user_account_object.PrivilegeType,
    'Import': cybox_common.StringObjectPropertyType,
    'Identifier': cybox_common.PlatformIdentifierType,
    'Tool_Specific_Data': cybox_common.ToolSpecificDataType,
    'Execution_Environment': cybox_common.ExecutionEnvironmentType,
    'Dependencies': cybox_common.DependenciesType,
    'Offset': cybox_common.IntegerObjectPropertyType,
    'Date': cybox_common.DateRangeType,
    'Hashes': cybox_common.HashListType,
    'Segments': cybox_common.HashSegmentsType,
    'Segment_Count': cybox_common.IntegerObjectPropertyType,
    'Usage_Context_Assumption': cybox_common.StructuredTextType,
    'Block_Hash': cybox_common.FuzzyHashBlockType,
    'Dependency': cybox_common.DependencyType,
    'Full_Name': cybox_common.StringObjectPropertyType,
    'Error': cybox_common.ErrorType,
    'Trigger_Point': cybox_common.HexBinaryObjectPropertyType,
    'Environment_Variable': cybox_common.EnvironmentVariableType,
    'Byte_Run': cybox_common.ByteRunType,
    'Libraries': cybox_common.LibrariesType,
    'Contributors': cybox_common.PersonnelType,
    'Image_Offset': cybox_common.IntegerObjectPropertyType,
    'Imports': cybox_common.ImportsType,
    'Library': cybox_common.LibraryType,
    'References': cybox_common.ToolReferencesType,
    'Script_Path': cybox_common.StringObjectPropertyType,
    'Internal_Strings': cybox_common.InternalStringsType,
    'Custom_Properties': cybox_common.CustomPropertiesType,
    'Configuration_Setting': cybox_common.ConfigurationSettingType,
    'User_Right': cybox_common.StringObjectPropertyType,
    'Security_ID': cybox_common.StringObjectPropertyType,
    'Privilege_List': user_account_object.PrivilegeListType,
    'Function': cybox_common.StringObjectPropertyType,
    'Description': cybox_common.StringObjectPropertyType,
    'Code_Snippet': cybox_common.ObjectPropertiesType,
    'Build_Configuration': cybox_common.BuildConfigurationType,
    'Last_Login': cybox_common.DateTimeObjectPropertyType,
    'Address': cybox_common.HexBinaryObjectPropertyType,
    'Search_Within': cybox_common.IntegerObjectPropertyType,
    'Segment': cybox_common.HashSegmentType,
    'Compiler': cybox_common.CompilerType,
    'Name': cybox_common.StringObjectPropertyType,
    'Signature_Description': cybox_common.StringObjectPropertyType,
    'Block_Size': cybox_common.IntegerObjectPropertyType,
    'Search_Distance': cybox_common.IntegerObjectPropertyType,
    'Fuzzy_Hash_Value': cybox_common.FuzzyHashValueType,
    'Dependency_Description': cybox_common.StructuredTextType,
    'Contributor': cybox_common.ContributorType,
    'Tools': cybox_common.ToolsInformationType,
    'Data_Size': cybox_common.DataSizeType,
}

USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""

def usage():
    print(USAGE_TEXT)
    sys.exit(1)

def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass

def parse(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_User_Account'
        rootClass = WindowsUserAccountObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
#    sys.stdout.write('<?xml version="1.0" ?>\n')
#    rootObj.export(sys.stdout.write, 0, name_=rootTag,
#        namespacedef_='',
#        pretty_print=True)
    return rootObj

def parseEtree(inFileName):
    doc = parsexml_(inFileName)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_User_Account'
        rootClass = WindowsUserAccountObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
    rootElement = rootObj.to_etree(None, name_=rootTag)
    content = etree_.tostring(rootElement, pretty_print=True,
        xml_declaration=True, encoding="utf-8")
    sys.stdout.write(content)
    sys.stdout.write('\n')
    return rootObj, rootElement

def parseString(inString):
    from mixbox.vendor.six import StringIO
    doc = parsexml_(StringIO(inString))
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'Windows_User_Account'
        rootClass = WindowsUserAccountObjectType
    rootObj = rootClass.factory()
    rootObj.build(rootNode)
    # Enable Python to collect the space used by the DOM.
    doc = None
#    sys.stdout.write('<?xml version="1.0" ?>\n')
#    rootObj.export(sys.stdout.write, 0, name_="Windows_User_Account",
#        namespacedef_='')
    return rootObj

def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


# Register abstract types
setattr(user_account_object, "WindowsGroupType", WindowsGroupType)
setattr(user_account_object, "WindowsPrivilegeType", WindowsPrivilegeType)


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

__all__ = [
    "WindowsUserAccountObjectType",
    "WindowsGroupType",
    "WindowsPrivilegeType"
    ]
