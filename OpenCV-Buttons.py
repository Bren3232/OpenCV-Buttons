
# Create buttons with OpenCV and Numpy only. Control variables while running a video loop.


# import time
import cv2
import numpy as np
import imutils as im


cap = cv2.VideoCapture("mixkit-going-down-highway.mp4")

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920 // 2)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080 // 2)

rot = 0
canny = 0
pause = 0


def b1p():
    global rot
    rot += 5

def b2p():
    global rot
    rot -= 5

def b3p():   # toggle canny
    global canny
    if canny == 0:
        canny = 1
    else:
        canny = 0

def b4p():  # toggle pause
    global pause
    if pause == 0:
        pause = 1
    else:
        pause = 0

def b_all_release():
    pass


def cv_buttons(frame, window, loc, txt, txt_size, padding, col, txt_col, on_press=None, on_release=None):
    '''
    all inputted lists must be of same length. Button1 is index 0, Button2 is index 1 and so on

    Params
    ------
    * frame: image to contain the buttons
    * window: a string to name the window, needed for cv2.setMouseCallBack
    * loc: a list of pixel location for each button. Will be the top left corner. Format in x, y
    * txt: a list of strings for the button text. Needs to match length of loc
    * txt_size: a list of text size params. 1 is standard size, can be float. Needs to match length of loc
    * padding: a list of button padding. Adds this padding around the text of the button to the edge of it.
    * col: a list of the background colors for each button
    * txt_col: a list of text color for each button
    * on_press: a list of predefined function to be called when button is pressed
    * on_release: same as on_press, but for button release

    Returns:
    -------
    does not return
    '''


    cv2.namedWindow(window)

    txt_img_list = []

    for idx, btn in enumerate(loc):

        # Text
        txt_s = cv2.getTextSize(txt[idx], cv2.FONT_HERSHEY_COMPLEX_SMALL, txt_size[idx], 3)  # [0][0] is width
        txt_img = np.zeros(shape=[txt_s[0][1] + padding[idx] * 2, txt_s[0][0] + padding[idx] * 2, 3], dtype=np.uint8)
        txt_img[:, :] = col[idx]     # the BG color
        cv2.putText(txt_img, txt[idx], (padding[idx], txt_s[0][1] + padding[idx]), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                    txt_size[idx], txt_col[idx])

        # frame
        frame[btn[1]:btn[1] + txt_img.shape[0], btn[0]:btn[0] + txt_img.shape[1]] = txt_img

        txt_img_list.append(txt_img)


    def events(event, x, y, flags, param):

        for idx, btn in enumerate(loc):

            if x < btn[0] + txt_img_list[idx].shape[1] and x > btn[0] and y < btn[1] + txt_img_list[idx].shape[0] and y > btn[1]:
                if event == cv2.EVENT_LBUTTONDOWN and on_press != None:
                    on_press[idx]()

                if event == cv2.EVENT_LBUTTONUP and on_release != None:
                    on_release[idx]()

                if event == cv2.EVENT_LBUTTONDBLCLK and on_press != None:  # use this so that every click registers as a click, don't need for release
                    on_press[idx]()

    cv2.setMouseCallback(window, events)


once = 0

while True:

    if pause == 0:
        paus = "Pause"
        ret, img = cap.read()
        if ret == True:
            img_paused = img.copy()  # to avoid continuously applying operations to same image when paused
    else:
        paus = "Unpause"
        img = img_paused


    if ret == True:

        img = im.resize(img, 640)

        # img operations
        img = im.rotate(img, rot)   # for video have to do operations in loop, just change global vars in btn funcs

        if canny == 1:
            img = im.auto_canny(img)                        # converts to gray img
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)      # needed for show in 1 window


        txt = [f"+ Rotate {rot}", f"- Rotate {rot}", "Toggle Canny", paus]  # everytime because has changing vars

        if once == 0:
            paus = "Pause"

            # For showing in 1 window
            loc = [[20, img.shape[0] + 25], [350, img.shape[0] + 25], [40, img.shape[0] + 110], [400, img.shape[0] + 110]]

            # For showing in 2 windows
            # loc = [[20, 25], [350, 25], [40, 110], [400, 110]]

            # txt = ["+ Rotate", "- Rotate", "Toggle Canny", paus]
            txt_size = [1, 1.4, 1, 1]
            padding = [15, 15, 15, 15]
            col = [[90, 90, 90], [100, 30, 30], [100, 110, 30], [0, 0, 140]]
            txt_col = [[250, 250, 250], [250, 250, 250], [250, 250, 250], [250, 250, 250]]
            press = [b1p, b2p, b3p, b4p]
            release = [b_all_release, b_all_release, b_all_release, b_all_release]

            controls = np.zeros((img.shape[0] // 2, img.shape[1], img.shape[2]), dtype=np.uint8) + 15

            once = 1

        # For showing in 2 windows (avoids minor obscurity)
        # controls = np.zeros((img.shape[0] // 2, img.shape[1], img.shape[2]), dtype=np.uint8) + 15

        # For showing in 1 window
        window_frame = np.vstack((img, controls))

        cv_buttons(frame=window_frame, window="this window", loc=loc, txt=txt, txt_size=txt_size, padding=padding,
                   col=col, txt_col=txt_col, on_press=press, on_release=release)

        # For showing in 2 windows
        # cv_buttons(frame=controls, window="this window", loc=loc, txt=txt, txt_size=txt_size, padding=padding,
        #            col=col, txt_col=txt_col, on_press=press, on_release=release)


        # Show in 1 window
        cv2.imshow("this window", window_frame)    # loc is based on window, not the frame

        # Show in 2 windows
        # cv2.imshow("img", img)
        # cv2.imshow("this window", controls)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
cv2.destroyAllWindows()

