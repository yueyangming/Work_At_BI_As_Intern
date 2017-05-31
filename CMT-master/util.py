from __future__ import division
import cv2
from numpy import math, hstack
import numpy as np



class FileVideoCapture(object):
    def __init__(self, path):
        self.path = path
        self.frame = 1

    def isOpened(self):
        im = cv2.imread(self.path.format(self.frame))
        return im != None

    def read(self):
        im = cv2.imread(self.path.format(self.frame))
        status = im != None
        if status:
            self.frame += 1
        return status, im


def squeeze_pts(X):
    X = X.squeeze()
    if len(X.shape) == 1:
        X = np.array([X])
    return X


def array_to_int_tuple(X):
    return (int(X[0]), int(X[1]))


def L2norm(X):
    return np.sqrt((X ** 2).sum(axis=1))


current_pos = None
tl = None
br = None


def get_rect(im, title='get_rect'):
    mouse_params = {'tl': None, 'br': None, 'current_pos': None,
                    'released_once': False}

    cv2.namedWindow(title)
    cv2.moveWindow(title, 100, 100)

    def onMouse(event, x, y, flags, param):

        param['current_pos'] = (x, y)

        if param['tl'] is not None and not (flags & cv2.EVENT_FLAG_LBUTTON):
            param['released_once'] = True

        if flags & cv2.EVENT_FLAG_LBUTTON:
            if param['tl'] is None:
                param['tl'] = param['current_pos']
            elif param['released_once']:
                param['br'] = param['current_pos']

    cv2.setMouseCallback(title, onMouse, mouse_params)
    cv2.imshow(title, im)

    while mouse_params['br'] is None:   # While the secnod point is not selected.
        im_draw = np.copy(im)

        if mouse_params['tl'] is not None:   # If the first point is selected.
            cv2.rectangle(im_draw, mouse_params['tl'],
                          mouse_params['current_pos'], (255, 0, 0))

        cv2.imshow(title, im_draw)
        _ = cv2.waitKey(10)

    tl = (min(mouse_params['tl'][0], mouse_params['br'][0]),
          min(mouse_params['tl'][1], mouse_params['br'][1]))
    br = (max(mouse_params['tl'][0], mouse_params['br'][0]),
          max(mouse_params['tl'][1], mouse_params['br'][1]))

    tr = (br[0], tl[1])
    bl = (tl[0], br[1])
    new_tl, new_br, new_tr, new_bl = tl, br, tr, bl

    Rotation_quit_flag = False
    Rotation_Change_flag = False
    Rotation_Angle = 0
    sum_Rotation = 0

    Coor_change_step = 5  # Coordinate changes in every step
    direction_dict = {'j': [-Coor_change_step, 0], 'l':[Coor_change_step, 0],
                      'k': [0, Coor_change_step], 'i': [0, -Coor_change_step]}
    while not Rotation_quit_flag:

        k = cv2.waitKey(20)
        key = chr(k & 255)

        if key == 'q':
            Rotation_quit_flag = True
        if key == 'u':
            Rotation_Angle = 5
            sum_Rotation += 5
            Rotation_Change_flag = True
        if key == 'o':
            Rotation_Angle = -5
            sum_Rotation -= 5
            Rotation_Change_flag = True
        if key in ['j', 'k', 'i', 'l']:
            vector = direction_dict[key]
            tl, br, tr, bl = Move_coor(tl, br, tr, bl, vector)
            new_tl, new_br, new_tr, new_bl = Move_coor(new_tl, new_br, new_tr, new_bl,vector)
            im_draw = np.copy(im)
            Draw_New_Rectangle(im_draw, new_tl, new_br, new_tr, new_bl)
            cv2.imshow(title, im_draw)

        if Rotation_Change_flag:
            # new_tl, new_br, new_tr, new_bl = tl, br, tr, bl
            im_draw = np.copy(im)
            new_tl, new_br, new_tr, new_bl = Update_coor(new_tl, new_br, new_tr, new_bl, Rotation_Angle)
            Draw_New_Rectangle(im_draw, new_tl, new_br, new_tr, new_bl)
            cv2.imshow(title, im_draw)
            Rotation_Change_flag = False

    cv2.destroyWindow(title)
    sum_Rotation = np.deg2rad(sum_Rotation)

    return (tl, br, tr, bl, sum_Rotation)


def Move_coor(tl, br, tr, bl, vector):
    tl = tuple(np.array(tl) + np.array(vector))
    tr = tuple(np.array(tr) + np.array(vector))
    br = tuple(np.array(br) + np.array(vector))
    bl = tuple(np.array(bl) + np.array(vector))
    return tl, br, tr, bl


def Draw_New_Rectangle(im_draw, tl, br, tr, bl):
    Color = (255, 0, 0)
    cv2.line(im_draw, tl, tr, Color)
    cv2.line(im_draw, tr, br, Color)
    cv2.line(im_draw, br, bl, Color)
    cv2.line(im_draw, bl, tl, Color)


def Update_coor(tl, br, tr, bl, Angle):

    center_x = (tl[0] + br[0]) / 2
    center_y = (tl[1] + br[1]) / 2
    Angle = (Angle / 360) * 2 * np.pi

    tl = new_coor(tl, Angle, center_x, center_y)
    br = new_coor(br, Angle, center_x, center_y)
    tr = new_coor(tr, Angle, center_x, center_y)
    bl = new_coor(bl, Angle, center_x, center_y)

    return tl, br, tr, bl


def new_coor(target, Angle, center_x, center_y):

    temp_x = (target[0] - center_x) * np.cos(Angle) - (target[1] - center_y) * np.sin(Angle) \
             + center_x

    temp_y = (target[0] - center_x) * np.sin(Angle) + (target[1] - center_y) * np.cos(Angle) \
             + center_y

    temp_x = int(temp_x)
    temp_y = int(temp_y)

    results = (temp_x, temp_y)

    return results


def my_cross(vector, x2, y2):

    return vector[0] * y2 - x2 * vector[1]


def between_vectors(vector_1, vector_2, coor,start_1,start_2):
    temp = my_cross(vector_1, coor[0] - start_1[0], coor[1] - start_1[1]) * \
        my_cross(vector_2, coor[0] - start_2[0], coor[1] - start_2[1]) < 0
    return temp


def in_rect(keypoints, tl, br, tr, bl):
    if type(keypoints) is list:
        keypoints = keypoints_cv_to_np(keypoints)
    vector_h_1 = [tr[0] - tl[0], tr[1] - tl[1]]
    vector_h_2 = [br[0] - bl[0], br[1] - bl[1]]
    vector_v_1 = [tl[0] - bl[0], tl[1] - bl[1]]
    vector_v_2 = [tr[0] - br[0], tr[1] - br[1]]

    results = []
    for each in keypoints:
        temp_h = between_vectors(vector_h_1, vector_h_2, each, tr, br)
        temp_v = between_vectors(vector_v_1, vector_v_2, each, tl, tr)
        results.append(temp_h & temp_v)

    result = np.array(results)
    return result


def keypoints_cv_to_np(keypoints_cv):
    keypoints = np.array([k.pt for k in keypoints_cv])
    return keypoints


def find_nearest_keypoints(keypoints, pos, number=1):
    if type(pos) is tuple:
        pos = np.array(pos)
    if type(keypoints) is list:
        keypoints = keypoints_cv_to_np(keypoints)

    pos_to_keypoints = np.sqrt(np.power(keypoints - pos, 2).sum(axis=1))
    ind = np.argsort(pos_to_keypoints)
    return ind[:number]


def draw_keypoints(keypoints, im, color=(255, 0, 0)):
    for k in keypoints:
        radius = 3  # int(k.size / 2)
        center = (int(k[0]), int(k[1]))

        # Draw circle
        cv2.circle(im, center, radius, color)


def track(im_prev, im_gray, keypoints, THR_FB=20):
    if type(keypoints) is list:
        keypoints = keypoints_cv_to_np(keypoints)
    num_keypoints = keypoints.shape[0]

    # Status of tracked keypoint - True means successfully tracked
    status = [False] * num_keypoints

    # If at least one keypoint is active
    if num_keypoints > 0:
        # Prepare data for opencv:
        # Add singleton dimension
        # Use only first and second column
        # Make sure dtype is float32
        pts = keypoints[:, None, :2].astype(np.float32)
        # Calculate forward optical flow for prev_location
        nextPts, status, _ = cv2.calcOpticalFlowPyrLK(im_prev, im_gray, pts, None)

        # Calculate backward optical flow for prev_location
        pts_back, _, _ = cv2.calcOpticalFlowPyrLK(im_gray, im_prev, nextPts, None)

        # Remove singleton dimension
        pts_back = squeeze_pts(pts_back)
        pts = squeeze_pts(pts)
        nextPts = squeeze_pts(nextPts)
        status = status.squeeze()

        # Calculate forward-backward error
        fb_err = np.sqrt(np.power(pts_back - pts, 2).sum(axis=1))

        # Set status depending on fb_err and lk error
        large_fb = fb_err > THR_FB
        status = ~large_fb & status.astype(np.bool)

        nextPts = nextPts[status, :]
        keypoints_tracked = keypoints[status, :]
        keypoints_tracked[:, :2] = nextPts

    else:
        keypoints_tracked = np.array([])
    return keypoints_tracked, status


def rotate(pt, rad):
    if (rad == 0):
        return pt

    pt_rot = np.empty(pt.shape)

    s, c = [f(rad) for f in (math.sin, math.cos)]

    pt_rot[:, 0] = c * pt[:, 0] - s * pt[:, 1]
    pt_rot[:, 1] = s * pt[:, 0] + c * pt[:, 1]

    return pt_rot


def br(bbs):
    result = hstack((bbs[:, [0]] + bbs[:, [2]] - 1, bbs[:, [1]] + bbs[:, [3]] - 1))

    return result


def bb2pts(bbs):
    pts = hstack((bbs[:, :2], br(bbs)))

    return pts
