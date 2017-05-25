# *-* coding=utf-8

# input_filename = './CMT-master/111_log.txt'

def read_coor(coordinates_str):
    ## Input Coordinats_str, output: two coordinates, tl and br, (top left and bottom right)

    # 'Cooridinates :(569, 533)*(682, 534)*(682, 683)*(568, 682)'
    coordinates_temp = coordinates_str.split(':')[1]  # (569, 533)*(682, 534)*(682, 683)*(568, 682)
    tl_temp = coordinates_temp.split('*')[0]
    tl_temp = tl_temp.replace('(', '[')
    tl_temp = tl_temp.replace(')', ']')
    tl = eval(tl_temp)

    br_temp = coordinates_temp.split('*')[2]
    br_temp = br_temp.replace('(', '[')
    br_temp = br_temp.replace(')', ']')
    br = eval(br_temp)

    return tl, br

def read_log(input_filename):
    ## Read log file. input filename with path, output:
    ## Frame, tl, br,active, Angle, Scale
    ## All output are lists.

    f = open(input_filename, 'r')
    list = []
    Frame = []
    tl = []
    br = []
    active = []
    Angle = []
    Scale = []

    for line in f.readlines():

        temp_line = line.strip('\n')
        if 'nan' in temp_line:  #If object not detected in Current Frame
            continue
        list.append(temp_line)
        split_temp = temp_line.split('#')
        Frame.append(int(split_temp[0].split(':')[1]))
        tl_temp, br_temp = read_coor(split_temp[1])
        tl.append(tl_temp)
        br.append(br_temp)

        active.append(int(split_temp[2].split(':')[1]))
        Angle.append(float(split_temp[3].split(':')[1]))
        Scale.append(float(split_temp[4].split(':')[1]))

    return Frame, tl, br, active, Angle, Scale

def log_to_AOI(Start_Timestamp, Frame,tl,br,Angle):
    ## Input Start_Timestamp, Frame, tl,br,Angle,
    ## Output : Points, Angle, Visible, Timestamp
    ## All are list

    Timestamp = []
    Points = []
    Angle_output = []
    Visible_output = []

    for index in range(len(Frame)):
        # From Frame to Timestamps
        timestamp_temp = Start_Timestamp + round((Frame[index] - 1) * (1/24 * 1000)) * 1000
        Timestamp.append(int(timestamp_temp))
        # As opencv start from frame 1 while python start from frame 0
        temp = [tl[index], br[index]]
        Points.append(temp)
        Angle_output.append(Angle[index])
        Visible_output.append(True)
        if index != len(Frame) - 1:  # Not the last Frame
            if Frame[index+1] != Frame[index] + 1:   # Next Frame object dispear
                timestamp_temp = Start_Timestamp + round((Frame[index] - 1) * (1 / 24 * 1000)) * 1000
                Timestamp.append(int(timestamp_temp))
                temp = [tl[index], br[index]]
                Points.append(temp)
                Angle_output.append(Angle[index])
                Visible_output.append(False)
    # The last frame

    # One frame after the last, Current Frame in XML file
    index = -1
    timestamp_temp = Start_Timestamp + round((Frame[index] - 1) * (1 / 24 * 1000)) * 1000
    Timestamp.append(int(timestamp_temp))
    temp = [tl[index], br[index]]
    Points.append(temp)
    Angle_temp = (Angle[index] + 360) % 360

    Angle_output.append(Angle_temp)
    Visible_output.append(False)

    return Timestamp, Points, Angle_output, Visible_output
