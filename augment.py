import cv2
import os
import numpy as np
import random

folder = input("Folder: ")
seed = int(input("Seed: "))
rng = random.Random(seed)
augment = int(input("Augment: "))
n_folder = len(next(os.walk(folder))[1])
content_folder = os.listdir(folder)

for i in range(0, n_folder):

    current_folder = content_folder[i]
    content = os.listdir(os.path.join(folder,current_folder))
    n_current = len(content)

    for j in range(0,n_current):

        path = os.path.join(folder,current_folder,content[j])

        if not os.path.exists(path):
            print("No file found at " + current_folder)
            break
        else:
            print("Doing: " + path)

        img = cv2.imread(path)
        h, w = img.shape[:2]
        n = content[j]

        random_augments = rng.sample(range(2, 17), augment)

        if 2 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".2.jpg"), cv2.GaussianBlur(img, (7,7), 0))

        if 3 in random_augments:
            M = cv2.getRotationMatrix2D((w//2, h//2), 15, 1.0)
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".3.jpg"), cv2.warpAffine(img, M, (w, h)))

        if 4 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".4.jpg"), cv2.flip(img, 1))
        
        if 5 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".5.jpg"), cv2.flip(img, 0))

        if 6 in random_augments:
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv[:,:,1] = hsv[:,:,1] * 0.5
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".6.jpg"), cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR))

        if 7 in random_augments:
            hsv2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            hsv2[:,:,1] = cv2.add(hsv2[:,:,1], 40)
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".7.jpg"), cv2.cvtColor(hsv2,cv2.COLOR_HSV2BGR))
        
        if 8 in random_augments:
            M = cv2.getRotationMatrix2D((w//2, h//2), -15, 1.0)
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".8.jpg"), cv2.warpAffine(img, M, (w, h)))

        if 9 in random_augments:
            pts1 = np.float32([[0,0],[w,0],[0,h]])
            pts2 = np.float32([[0,0],[w-40,40],[40,h]])
            M = cv2.getAffineTransform(pts1, pts2)
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".9.jpg"), cv2.warpAffine(img, M, (w,h)))

        if 10 in random_augments:
            small = cv2.resize(img, (w//2, h//2))
            big = cv2.resize(small, (w,h))
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".10.jpg"), big)

        if 11 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".11.jpg"), cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE))

        if 12 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".12.jpg"), cv2.rotate(img, cv2.ROTATE_180))

        if 13 in random_augments:    
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".13.jpg"), cv2.bitwise_not(img))

        if 14 in random_augments:
            kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".14.jpg"), cv2.filter2D(img, -1, kernel))

        if 15 in random_augments:
           cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".15.jpg"), cv2.convertScaleAbs(img, alpha=1.3,beta=20))

        if 16 in random_augments:
            cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".16.jpg"), cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))

        print("done " + str(n) + ".jpg")
        

    

    