import cv2
import os
import numpy as np
folder = input("Folder: ")
n_folder = len(next(os.walk(folder))[1])
content_folder = os.listdir(folder)
for i in range(0, n_folder):
    current_folder = content_folder[i]
    n_current = len(os.listdir(os.path.join(folder,current_folder)))
    for j in range(1,n_current+1):
        path = os.path.join(folder,current_folder, str(j) + ".jpg")
        if not os.path.exists(path):
            print("No file found at " + str(j))
            break
        else:
            print("Doing: " + path)
        img = cv2.imread(path)
        h, w = img.shape[:2]
        n = j
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".1.jpg"), cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".2.jpg"), cv2.GaussianBlur(img, (7,7), 0))
        
        M = cv2.getRotationMatrix2D((w//2, h//2), 15, 1.0)
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".3.jpg"), cv2.warpAffine(img, M, (w, h)))
    
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".4.jpg"), cv2.flip(img, 1))
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".5.jpg"), cv2.flip(img, 0))
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv[:,:,1] = hsv[:,:,1] * 0.5
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".6.jpg"), cv2.cvtColor(hsv,cv2.COLOR_HSV2BGR))
        
        hsv2 = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv2[:,:,1] = cv2.add(hsv2[:,:,1], 40)
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".7.jpg"), cv2.cvtColor(hsv2,cv2.COLOR_HSV2BGR))
        
        M = cv2.getRotationMatrix2D((w//2, h//2), -15, 1.0)
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".8.jpg"), cv2.warpAffine(img, M, (w, h)))
        
        pts1 = np.float32([[0,0],[w,0],[0,h]])
        pts2 = np.float32([[0,0],[w-40,40],[40,h]])
        M = cv2.getAffineTransform(pts1, pts2)
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".9.jpg"), cv2.warpAffine(img, M, (w,h)))
        
        small = cv2.resize(img, (w//2, h//2))
        big = cv2.resize(small, (w,h))
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".10.jpg"), big)
    
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".11.jpg"), cv2.rotate(img,cv2.ROTATE_90_CLOCKWISE))
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".12.jpg"), cv2.rotate(img, cv2.ROTATE_180))
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".13.jpg"), cv2.bitwise_not(img))
        
        kernel = np.array([[0,-1,0],[-1,5,-1],[0,-1,0]])
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".14.jpg"), cv2.filter2D(img, -1, kernel))
        
        cv2.imwrite(os.path.join(folder,current_folder, str(n) + ".15.jpg"), cv2.convertScaleAbs(img, alpha=1.3,beta=20))
        
        print("done " + str(n) + ".jpg")
        n = n + 1
        

    

    