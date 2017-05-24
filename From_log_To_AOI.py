# *-* coding=utf-8

filename = './CMT-master/111_log.txt'


def read_coor(coordinates_str):

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

def read_log(filename):

    f = open(filename, 'r')
    list = []
    Frame = []
    tl = []
    br = []
    active = []
    Angle = []
    Scale = []

    for line in f.readlines():

        temp_line = line.strip('\n')
        if 'nan' in temp_line:
            continue
        list.append(temp_line)
        split_temp = temp_line.split('#')
        Frame.append(split_temp[0].split(':')[1])
        tl_temp, br_temp = read_coor(split_temp[1])
        tl.append(tl_temp)
        br.append(br_temp)

        active.append(int(split_temp[2].split(':')[1]))
        Angle.append(float(split_temp[3].split(':')[1]))
        Scale.append(float(split_temp[4].split(':')[1]))

    return Frame, tl, br, active, Angle, Scale



# def log_to_AOI(Frame,tl,br,Angle):
