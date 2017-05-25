from From_log_To_AOI import read_coor  # coordinates_str
from From_log_To_AOI import read_log  # filename
from From_log_To_AOI import log_to_AOI  # Start_Timestamp, Frame,tl,br,Angle

from From_AOI_To_xml import CreateXml
from From_AOI_To_xml import Generate_DynamicAOI
from From_AOI_To_xml import Generate_Key_frame
from From_AOI_To_xml import Generate_Points_Node
from From_AOI_To_xml import indent

if __name__ == '__main__':

    log_filename = './CMT-master/111_log.txt'
    Start_Timestamp = 0
    Color = 'Coral'
    Name = 'AOI 001'


    Frame, tl, br, active, Angle, Scale = read_log(log_filename)

    Timestamp, Points, Angle_output, Visible_output = log_to_AOI(Start_Timestamp, Frame, tl, br, Angle)

    output_xml_filename = 'Output_' + log_filename.split('/')[-1].split('.')[0].split('_')[0] + '.xml'


    Tree = CreateXml(Points, Angle_output, Color, Name, Visible_output, Timestamp)
    Tree.write(output_xml_filename, "utf-8")


