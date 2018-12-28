import cv2
import argparse
import numpy as np
import os
import imghdr


def get_arguments():
    ap = argparse.ArgumentParser()

    try:
        ap.add_argument('-i', '--input', required=True,
                        help='Loading path for input image')
    except:
        return 6
    try:
        ap.add_argument('-o', '--output', required=True,
                        help='Loading path for output image')
        args = vars(ap.parse_args())
    except:
        return 5

    if not args['input'] or not args['output']:
        ap.error("Critical error: input or output path is absent!")
    return args


def main():
    while True:
        args = get_arguments()

        if args == 5:
            print("Critical error 5: Parameter input error ")
            return 5
        if args == 6:
            print("Critical error 6: Parameter output error ")
        else:
            img = str(args['input'])

            # Is there a file in the specified path
        if os.path.isfile(img) == False:
            # print("Critical error 10: File does not exist!")
            return 10

                # The input file is not an image
        if imghdr.what(img) == None:
            print("Critical error 11: File is not in correct format. Only .jpeg files can be used.")
            return 11

        try:
            image = cv2.imread(img)
        except BaseException:
            print("Critical error 13: Could not read image")
            return 13

        try:
            white_lower = np.asarray([230, 230, 230])
            white_upper = np.asarray([255, 255, 255])

            mask = cv2.inRange(image, white_lower, white_upper)
            mask = cv2.bitwise_not(mask)

            # find contours in the mask and initialize the current
            im, cnt, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        except:
            print("Critical error 14: File processing error")
            return 14

        # only proceed if at least one contour was found
        if len(cnt) > 0:
            try:
                largest_contour = max(cnt, key=lambda x: cv2.contourArea(x))
                bounding_rect = cv2.boundingRect(largest_contour)
                cropped_image = image[bounding_rect[1]: bounding_rect[1] + bounding_rect[3],
                                bounding_rect[0]:bounding_rect[0] + bounding_rect[2]]
            except:
                print("Critical error 14: File processing error")
                return 14
            try:
                cv2.imwrite(str(args['output']), cropped_image)
            except:
                # print("Critical error 15: Error save file")
                return 15

        return 0
        #else: print("Critical error 1: No image was detected")


if __name__ == '__main__':
    main()