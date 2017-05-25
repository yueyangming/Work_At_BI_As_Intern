from __future__ import division
from From_log_To_AOI import read_coor  # coordinates_str
from From_log_To_AOI import read_log  # filename
from From_log_To_AOI import log_to_AOI  # Start_Timestamp, Frame,tl,br,Angle

from From_AOI_To_xml import CreateXml
from From_AOI_To_xml import Generate_DynamicAOI
from From_AOI_To_xml import Generate_Key_frame
from From_AOI_To_xml import Generate_Points_Node
from From_AOI_To_xml import indent

if __name__ == '__main__':

    Start_Timestamp = 1896098000
    filename_list = ['20170525_2_testAOI_001_log.txt', '20170525_2_testAOI_002_log.txt']

    directory = './CMT-master/'
    Timestamp_list = []
    Points_list = []
    Angle_output_list = []
    Visible_output_list = []
    Color_list = []
    Name_list = []

    for filename in filename_list:
        complete_name = directory + filename
        Color = 'Coral'
        Name = filename.split('_log.txt')[0].split('_')[-1]
        Color_list.append(Color)
        Name_list.append(Name)

        Frame, tl, br, active, Angle, Scale = read_log(complete_name)
        Timestamp, Points, Angle_output, Visible_output = log_to_AOI(Start_Timestamp, Frame, tl, br, Angle)

        Timestamp_list.append(Timestamp)
        Points_list.append(Points)
        Angle_output_list.append(Angle_output)
        Visible_output_list.append(Visible_output)

    output_xml_filename = 'Output_' + filename.split('_log.txt')[0].split('_')[0] + '.xml'

    Tree = CreateXml(Points_list, Angle_output_list, Color_list, Name_list, Visible_output_list, Timestamp_list)
    Tree.write(output_xml_filename, "utf-8")


