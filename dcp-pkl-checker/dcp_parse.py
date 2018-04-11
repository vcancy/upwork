# Clairmeta - (C) YMAGIS S.A.
# See LICENSE for more information

import os
from utils.xml import parse_xml
from settings import DCP_SETTINGS
from logger import get_log


def discover_schema(node):
    """ Assign file Schema using detected namespace """
    xmlns = node.get('__xmlns__', None)

    if xmlns:
        node['Schema'] = 'Unknown'
        if xmlns.startswith('smpte_stereo'):
            node['Schema'] = 'SMPTE Stereoscopic'
        elif xmlns.startswith('smpte'):
            node['Schema'] = 'SMPTE'
        elif xmlns.startswith('interop'):
            node['Schema'] = 'Interop'
        elif xmlns.startswith('atmos'):
            node['Schema'] = 'Atmos'


def generic_parse(
    path,
    root_name,
    force_list=(),
    namespaces=DCP_SETTINGS['xmlns']
):
    """ Parse an XML and returns a Python Dictionary """
    try:
        res_dict = parse_xml(
            path,
            namespaces=namespaces,
            force_list=force_list)

        if res_dict and root_name in res_dict:
            node = res_dict[root_name]
            discover_schema(node)

            return {
                'FileName': os.path.basename(path),
                'FilePath': path,
                'Info': {
                    root_name: node
                }
            }
    except Exception as e:
        get_log().info("Error parsing XML {} : {}".format(path, str(e)))


def assetmap_parse(path):
    """ Parse DCP ASSETMAP """
    am = generic_parse(path, "AssetMap", ("Asset",))

    if am:
        # Two ways of identifying a PKL inside the assetmap :
        # <PackingList></PackingList> (Interop)
        # <PackingList>true</PackingList> (SMPTE)
        # Hide these specificities and return PackingList: True in both cases
        for asset in am['Info']['AssetMap']["AssetList"]["Asset"]:
            if 'PackingList' in asset:
                asset['PackingList'] = True

    return am


def volindex_parse(path):
    """ Parse DCP VOLINDEX """
    return generic_parse(path, "VolumeIndex")


def pkl_parse(path):
    """ Parse DCP PKL """
    return generic_parse(path, "PackingList", ("Asset",))

