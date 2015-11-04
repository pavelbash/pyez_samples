__author__ = 'mdevyatov'
from lxml import etree

def parse_file(file_to_parse):
    """Parse the file with multiple junos outputs in xml format

    Args:
        file_to_parse (file): an open file to parse
    Returns:
        A list of lxml trees with <rpc-reply> root elements
    """

    list_of_xml_trees = []
    parser = etree.XMLPullParser(events=['end'], recover=True)
    for line in file_to_parse:
        parser.feed(line)
        for action, element in parser.read_events():
            if (action == 'end') and (element.tag == 'rpc-reply'):
                list_of_xml_trees.append(parser.close())
                parser = etree.XMLPullParser(events=('start', 'end'), recover=True)
    return list_of_xml_trees

def fpc_ram_utilization(xml_tree):
    """Returns dictionary of FPC and Heap utilization from XML output

    Args:
        xml_tree (lxml.etree._Element): Output of "show chassis fpc | display xml" Junos rpc reply
    Returns:
        A dict mapping FPC# to heap utilization level if this information present in the input tree
         {'0': '12',
          '1': '27',
          '2': '24'}
    """

    fpc_ram_utilization = {}
    for element in  xml_tree.findall('.//resource-monitor-summary-information-summary'):
        fpc_num = "unknown"
        for sub_element in element:
            if sub_element.tag == 'fpc-slot':
                if not sub_element.attrib:
                    fpc_num = sub_element.text
            if sub_element.tag == 'used-heap-mem-percent':
                fpc_ram_utilization[fpc_num] = sub_element.text

    return fpc_ram_utilization


