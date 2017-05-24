# *-* coding=utf-8

from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

filename = 'Output_test.xml'

def CreateXml( Points, Angle, Color, Name, Visible, Timestamps):
    AOI_Tree = ElementTree()
    Root = Element("ArrayOfDynamicAOI")  # Root Element
    AOI_Tree._setroot(Root)
    DynamicAOI_Node = Element("DynamicAOI")
    # DynamicAOI_Node = Generate_DynamicAOI()
    KeyFrames_num = 1
    DynamicAOI_Node = Generate_DynamicAOI(DynamicAOI_Node, Points, Angle, KeyFrames_num,
                                          Color, Name, Visible, Timestamps)
    Root.append(DynamicAOI_Node)

    indent(Root)

    return AOI_Tree

def Generate_DynamicAOI(DynamicAOI_Node, Points, Angle, KeyFrames_num,
                        Color, Name, Visible, TimeStamps, Type = 'Rectangle'):
    # Points[0], Angle[0], Visible[0] is initial frame

    DynamicAOI_Node.tag = 'DynamicAOI'
    SubElement(DynamicAOI_Node, 'Enabled').text = 'true'
    SubElement(DynamicAOI_Node, 'Scope').text = 'Local'
    SubElement(DynamicAOI_Node, 'Style').text = 'HalfTransparent'
    SubElement(DynamicAOI_Node, 'Transparency').text = '50'
    SubElement(DynamicAOI_Node, 'Type').text = Type

    point_1 = Points[0][0]  # Final frame
    point_2 = Points[0][1]
    Points_Node = Generate_Points_Node(point_1, point_2)
    Points_Node.tag = 'Points'
    DynamicAOI_Node.append(Points_Node)

    SubElement(DynamicAOI_Node, 'Angle').text = str(Angle[0])
    SubElement(DynamicAOI_Node, 'Name').text = str(Name)
    SubElement(DynamicAOI_Node, 'Visible').text = 'true' if Visible[0] else 'false'
    SubElement(DynamicAOI_Node, 'Color').text = 'NamedColor:' + Color
    CurrentTimeStamp = TimeStamps[0]
    SubElement(DynamicAOI_Node, 'CurrentTimeStamp').text = str(CurrentTimeStamp)

    KeyFrames_Node = Element('KeyFrames')
    for i in range(KeyFrames_num):
        KeyFrame_Node = Element('KeyFrame')
        KeyFrames_Node.append(Generate_Key_frame(KeyFrame_Node, Points[i+1][0],
                                                 Points[i+1][1], Angle[i+1], Visible[i+1], TimeStamps[i+1]))
    DynamicAOI_Node.append(KeyFrames_Node)
    return DynamicAOI_Node

def Generate_Key_frame(Key_Frame_Node, point_1, point_2, Angle, Visible, Timestamp):

    # Key_Frame_Node = Element('KeyFrame')
    Key_Frame_Node.tag = 'KeyFrame'
    Points_Node = Generate_Points_Node(point_1, point_2)

    SubElement(Key_Frame_Node, 'Angle').text = str(Angle)
    SubElement(Key_Frame_Node, 'Visible').text = 'true' if Visible else 'false'
    SubElement(Key_Frame_Node, 'Timestamp').text = str(Timestamp)
    Key_Frame_Node.append(Points_Node)

    return Key_Frame_Node

def Generate_Points_Node(point_1, point_2):

    Point_1 = Element('Point')
    SubElement(Point_1, 'X').text = str(point_1[0])
    SubElement(Point_1, 'Y').text = str(point_1[1])

    Point_2 = Element('Point')
    SubElement(Point_2, 'X').text = str(point_2[0])
    SubElement(Point_2, 'Y').text = str(point_2[1])

    Points_Node = Element('Points')
    Points_Node.append(Point_1)
    Points_Node.append(Point_2)

    return Points_Node

def indent(elem, level=0):
    i = "\n" + level * "    "
    # print(elem)
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "    "
        for e in elem:
            # print(e)
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem

if __name__ == '__main__':

    temp = [[27, 586], [155, 897]]
    Points = []
    Points.append(temp)
    Points.append(temp)
    Angle = [0, 0]
    Color = 'Coral'
    Name = 'AOI 001'
    Visible = [False, True]
    Timestamps = [0, 63012000]

    book = CreateXml(Points, Angle, Color, Name, Visible, Timestamps)
    book.write(filename, "utf-8")