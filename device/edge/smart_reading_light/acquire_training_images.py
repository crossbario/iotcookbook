## capture a sequence of images from a webcam

def make_temp_folder():
    from tempfile import mkdtemp
    from os.path import dirname, realpath

    return mkdtemp(prefix=dirname(realpath(__file__)) + '/')


def acquire_img(cap_indx: int = 1, duration: float = 60.0, frequency: float = 0.1, img_dir: str = './') -> None:
    from time import sleep
    from cv2 import VideoCapture, imwrite
    from os.path import join

    cap = VideoCapture(cap_indx)
    n = int(duration/frequency + 0.5)
    k = 1

    print(80 * '#')
    print('img_dir:', img_dir)
    print('create {}-th images'.format(n))
    print(80 * '#')

    for i in range(n):
        _, frame = cap.read()
        img_name = join(img_dir, 'img_{}.png'.format(i))
        imwrite(img_name, frame)
        sleep(frequency)

        if i >= 0.25*k*n:
            print("*done {}".format(i/n))
            k+=1

    # When everything done, release the capture
    # cap.release()
    # cv2.destroyAllWindows()
    return None


if __name__ == "__main__":
    img_dir = make_temp_folder()
    acquire_img(cap_indx=-1, duration=20, frequency=0.5, img_dir=img_dir)
    exit()

