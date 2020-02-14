import numpy as np
import cv2
import os
import sys
import argparse
from PIL import Image

def resize_and_label_Image(infile, output_dir, size, label):

    if label is not None:
        outfile = str(os.path.splitext(os.path.basename(infile))[0])+"."+str(label)
    else:
        outfile = os.path.splitext(os.path.basename(infile))[0]
    extension = os.path.splitext(infile)[1]
    if extension in ('.jpeg', '.jpg', '.bmp'):
        img = cv2.imread(infile , cv2.IMREAD_COLOR)
        h, w = img.shape[:2]
        c = None if len(img.shape) < 3 else img.shape[2]
        if h == w: 
            img2 = cv2.resize(img, (size[0],size[1]), cv2.INTER_AREA)
        else:
            dif = h if h > w else w
            interpolation = cv2.INTER_AREA if dif > (size[0]+size[1])//2 else cv2.INTER_CUBIC
            x_pos = (dif - w)//2
            y_pos = (dif - h)//2
            if len(img.shape) == 2:
                mask = np.zeros((dif, dif), dtype=img.dtype)
                mask[y_pos:y_pos+h, x_pos:x_pos+w] = img[:h, :w]
            else:
                mask = np.zeros((dif, dif, c), dtype=img.dtype)
                mask[y_pos:y_pos+h, x_pos:x_pos+w, :] = img[:h, :w, :]
            img2 = cv2.resize(mask, (size[0],size[1]), interpolation)
        img2 = Image.fromarray(cv2.cvtColor(img2, cv2.COLOR_RGB2BGR))
        img2.save(os.path.join(output_dir, outfile+extension))


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", help="Directory to look up for images")
    parser.add_argument("-o", help="Output directory")
    parser.add_argument("-l", help="Label number: 1. Gaussian Blur / 2. Motion Blur / 3. Gaussian Noise non monoch / 4. Gaussian Noise monoch / 5. Marble / 6. Twirl")
    parser.add_argument("-s", nargs=2, type=int, help="Output size")
    args = parser.parse_args()

    input_dir = os.path.normpath(args.d) if args.d else os.getcwd()
    output_dir = os.path.normpath(args.o) if args.o else os.path.join(os.getcwd(), 'resized')
    output_size = tuple(args.s) if args.s else (224,224)
    output_label = int(args.l) if args.l else 0

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    for file in os.listdir(input_dir):
        resize_and_label_Image(os.path.join(input_dir, file), output_dir, output_size, output_label)
