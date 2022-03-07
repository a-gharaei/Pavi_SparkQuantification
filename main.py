#Author: Paviththiren Sivasothilingam
#Programm: Spark Quantification


from nptdms import TdmsFile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2




###################################################################################################################
# FORCES
###################################################################################################################

#READ-OUT
#########

#Read out from TdmsFile and save it in a pandas-dataframe
tdms_file = TdmsFile('Data/Force/Force.tdms')
dx = pd.DataFrame()
Data = pd.DataFrame()

for group in tdms_file.groups():
    df = group.as_dataframe()
    dx = pd.DataFrame(df)

#RENAMING DATA SET
# Overall name of data frame: Data
# Forces acting in their respective direction: F_x, F_y, F_z
F_x = dx["cDAQ1Mod2/ai0"][:]
F_y = dx["cDAQ1Mod2/ai0"][:]
F_z = dx["cDAQ1Mod2/ai2"][:]

Data["F_x"] = F_x
Data["F_y"] = F_y
Data["F_z"] = F_z

#CONVERSION FROM VOLTAGE TO FORCE
#Sensitivity of the setup: 500 N/V
Data = Data * 500


########################################################################################################################
# IMAGE ANALYSIS                                                                                                       #
########################################################################################################################

#READ-OUT
#########
img = cv2.imread('/home/pavi/PycharmProjects/Spark_Experiment/Data/Camera/Sample_Bitmaps/20220225-173020-image-0000449.BMP')


#CONVERSION TO GREY-SCALE
#########################
gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
rows,columns = gray_scale.shape
(minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray_scale)



#EDGE DETECTION (tried, but not useful)
###############
"""
img_blur = cv2.GaussianBlur(gray_scale,(3,3),0)
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx = 1, dy= 0, ksize=5)
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx = 0, dy= 1, ksize=5)
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx = 1, dy= 1, ksize=5)


#cv2.imshow('a',sobelx)
#cv2.imshow('b',sobely)
#cv2.imshow('c',sobelxy)

edges = cv2.Canny(image=gray_scale, threshold1= 100, threshold2=200)
cv2.imshow("test",edges)
"""

#SPARK AREA + AVERAGE SPARK BRIGHTNESS + BRIGHTEST SPARKS
#########################################################
low_threshold = 40
high_threshold = 140
spark_area = 0
total_pixels = rows * columns
average_spark_brightness = 0
max_spark_brightness = 0
for x in range(rows):
    for y in range(columns):
        if x in range(106,417):
            if y in range(1096,1751):
                if gray_scale[x][y] < high_threshold and gray_scale[x][y] > low_threshold:
                    spark_area += 1
                    average_spark_brightness += gray_scale[x][y]
            else:
                if gray_scale[x][y] > low_threshold:
                    spark_area += 1
                    average_spark_brightness += gray_scale[x][y]
        else:
            if gray_scale[x][y] > low_threshold:
                spark_area += 1
                average_spark_brightness += gray_scale[x][y]

        if gray_scale[x][y] > 0.9 * maxVal:
            max_spark_brightness += 1



average_spark_brightness /= spark_area
ratio_max_spark_brightness = max_spark_brightness / spark_area

#SPARK AREA: BASE CODE
"""
for x in range(rows):
    for y in range(columns):
        if gray_scale[x][y] > low_threshold:
            spark_area += 1
            spark_loc_x.append(x)
            spark_loc_y.append(y)

for x in range(106,417):
    for y in range(1096,1751):
        if gray_scale[x][y] < high_threshold and gray_scale[x][y] > low_threshold:
            spark_area = spark_area - 1
            spark_loc_x.remove(x)
            spark_loc_y.remove(y)
"""

#AVERAGE SPARK BRIGHTNESS
#########################

"""
average_spark_brightness = 0
for x in range(len(spark_loc_x)):
    for y in range(len(spark_loc_y)):
        average_spark_brightness += gray_scale[spark_loc_x[x]][spark_loc_y[y]]

average_spark_brightness /= spark_area
"""



########################################################################################################################
# OUTPUT                                                                                                               #
########################################################################################################################

#SPARK DISPLAY
##############
print("Spark Area: " + str(spark_area))
print("Total Pixels: " + str(total_pixels))
print("Ratio: " + str(round(spark_area/total_pixels,5)))
print("Average Spark Brightness: " + str(average_spark_brightness))
print("Brightest Sparks :" + str(max_spark_brightness))
print("Ratio Brightest Sparks: " + str(ratio_max_spark_brightness))
counted_sparks_image = gray_scale.copy()
for x in range(rows):
    for y in range(columns):
        if counted_sparks_image[x][y] < low_threshold:
            counted_sparks_image[x][y] = 0

for x in range(106,417):
    for y in range(1096,1751):
        if counted_sparks_image[x][y] < high_threshold:
            counted_sparks_image[x][y] = 0

#cv2.imwrite('/home/pavi/PycharmProjects/Spark_Experiment/Data/Camera/Gray_Scale3.BMP',gray_scale)
cv2.imshow("Spark Area", counted_sparks_image)
cv2.imshow("Gray Scale", gray_scale)

cv2.waitKey(0)

#PLOTTING
#########/

#Moving Average Filter: Uncomment  to see general trends in the data
"""
#Data["x"] = Data["x"].rolling(100).mean()
#Data["y"] = Data["y"].rolling(100).mean()
#Data["z"] = Data["z"].rolling(100).mean()
"""

"""
x = np.arange(len(dx))
plt.plot(x,Data["F_x"],'r', x,Data["F_y"], 'b',x,Data["F_z"],'g')
plt.show()
"""

#print(Data)
#print(dx.tail())


