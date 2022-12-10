# Imported libraries needed
import numpy as np
import cv2
import matplotlib.pyplot as plt
from phantominator import shepp_logan


def show(img):  # Displays the images
    plt.imshow(img, cmap='gray')
    plt.show()  # Shows the actual phantom with coordinates


def cutImage(img, cutType, imageAmountSlice, counter):
    # Variables that are inside the equation to help determine what type of slice
    (a0, b1) = img.shape
    fullysliced = 1 / imageAmountSlice
    sliceamounta = a0 / imageAmountSlice
    sliceamountb = b1 / imageAmountSlice
    amusliced = counter / imageAmountSlice
    countersliced = (counter + 1) / imageAmountSlice

    if cutType == "horizontal":
        stored = []  # Array that stores the slice values
        if counter == 0:
            for i in range(int(a0 * fullysliced)):
                for j in range(b1):
                    stored.append(img[i, j])
        else:
            for i in range(int(a0 * amusliced),
                           int(a0 * countersliced)):
                for j in range(b1):
                    stored.append(img[i, j])
        if len(stored) > int(b1 * int(sliceamounta)):
            finalImage = np.reshape(stored, (int(sliceamounta) + 1, b1))
            return finalImage
        else:
            finalImage = np.reshape(stored, (int(sliceamounta), b1))
            return finalImage
#################################################Ending cutting horizontal##############################################
    elif cutType == "vertical":
        stored = []  # Array that stores the slice values
        if counter == 0:
            for i in range(a0):
                for j in range(int(b1 * fullysliced)):
                    stored.append(img[i, j])
        else:
            for i in range(a0):
                for j in range(int(b1 * amusliced),
                               int(b1 * countersliced)):
                    stored.append(img[i, j])
        if len(stored) > int(a0 * int(sliceamountb)):
            finalImage = np.reshape(stored, (a0, int(sliceamountb + 1)))
            return finalImage
        else:
            finalImage = np.reshape(stored, (a0, int(sliceamountb)))
            return finalImage
#################################################Ending cutting vertical################################################
    elif cutType == "diagonal":
        if imageAmountSlice == 1:
            return img
        finalImage = np.zeros((a0, b1))
        for i in range(a0):
            for j in range(b1):
                if counter == 0:
                    if (i + j) <= (a0 * 2 * fullysliced):
                        finalImage[i, j] = img[i, j]
                else:
                    if (a0 * 2 * countersliced) >= (i + j) >= (
                            a0 * 2 * amusliced):
                        finalImage[i, j] = img[i, j]
        return finalImage


#################################################Ending cutting diagonal################################################
# Creating the phantom and editing it
print("Give a x coordinate: ")  # Put a x point of where tumor wants to be
x = int(input())
print("Give a y coordinate: ")  # Put a y point of where tumor wants to be
y = int(input())
print("Input the slice type: ")  # Pick horizontal, vertical, or diagonal
type = str(input())
print("Enter number of cuts: ")  # Inputting the number of cuts
imageAmountSlice = int(input())  # Should not be bigger than 256 by 256
phantom = np.array(shepp_logan(256))  # Image cutting 256 by 256
phantom = np.multiply(phantom, 256)  # Needed to work with numpy

# These are to make the phantom like a colon
cv2.circle(phantom, center=(125, 100), radius=10, color=(0, 0, 0), thickness=20)  # Black Circle
cv2.circle(phantom, center=(120, 145), radius=10, color=(0, 0, 0), thickness=50)  # Colon Black Circle
cv2.circle(phantom, center=(85, 193), radius=3, color=(27, 27, 27), thickness=20)  # Grey Circle
cv2.circle(phantom, center=(110, 215), radius=2, color=(27, 27, 27), thickness=20)  # Grey Circle
cv2.circle(phantom, center=(145, 205), radius=0, color=(27, 27, 27), thickness=20)  # Grey Circle
cv2.circle(phantom, center=(130, 220), radius=0, color=(27, 27, 27), thickness=20)  # Grey Circle

if 100 < x < 150 and 100 < y < 150:  # Picking an x and y to go inside the colon
    cv2.circle(phantom, center=(x, y), radius=1, color=(255, 255, 0), thickness=20)  # Tumor White Circle
    cv2.putText(phantom, "*", (x - 6, y + 10), cv2.FONT_HERSHEY_DUPLEX, .75, 30)  # Polyp Star
else:
    print("THE TUMOR IS NOT INSIDE THE COLON!")

cv2.imwrite("phantom.png", phantom)
plt.title('Virtual Colonoscopy')
show(phantom)  # Gives the title
########################################################################################################################
D1 = 100
D2 = 100
# Here we are cutting the image and putting it back together
(c0, d1) = phantom.shape
if 1 <= imageAmountSlice < c0:
    if type == "vertical":
        counter = 0  # Starting with 0 (slices)
        title = "VerticalCut#1"  # Gives the first cut image name
        split = cutImage(phantom, type, imageAmountSlice, counter)
        cv2.imwrite(title + ".png", split)  # Creates to initialize image
        finalImage = np.array(split)  # Putting back the image
        counter = counter + 1  # Increase when slice happened
        for i in range(1, imageAmountSlice):
            title = "VerticalCut#"
            title = title + str(i + 1)  # Switch images by increasing number
            split = cutImage(phantom, type, imageAmountSlice, counter)
            cv2.imwrite(title + ".png", split)
            finalImage = np.append(finalImage, split, axis=1)
            counter = counter + 1
        plt.title('Result Image')
        show(finalImage)  # Give the final image of vertical cut
#################################################Ending vertical########################################################
    elif type == "horizontal":
        counter = 0
        title = "HorizontalCut#1"
        split = cutImage(phantom, type, imageAmountSlice, counter)
        cv2.imwrite(title + ".png", split)
        finalImage = np.array(split)  # Putting back the image
        counter = counter + 1
        for i in range(1, imageAmountSlice):
            title = "HorizontalCut#"
            title = title + str(i + 1)
            split = cutImage(phantom, type, imageAmountSlice, counter)
            cv2.imwrite(title + ".png", split)
            finalImage = np.append(finalImage, split, axis=0)
            counter = counter + 1
        plt.title('Result Image')
        show(finalImage)  # Give the final image of horizontal cut
#################################################Ending horizontal######################################################
    elif type == "diagonal":
        counter = 0
        title = "DiagonalCut#1"
        split = cutImage(phantom, type, imageAmountSlice, counter)
        (e0, f1) = split.shape
        cv2.imwrite(title + ".png", split)
        finalImage = np.zeros((c0, d1))  # Putting back the image
        for i in range(e0):
            for j in range(f1):
                if split[i, j] != 0:
                    finalImage[i, j] = split[i, j]
        counter = counter + 1
        for i in range(1, imageAmountSlice):
            title = "DiagonalCut#"
            title += str(i + 1)
            split = cutImage(phantom, type, imageAmountSlice, counter)
            cv2.imwrite(title + ".png", split)
            for j in range(e0):  # Run through the loops
                for k in range(f1):  # Run through the loop
                    if split[j, k] != 0:  # If portion found add it to the split array
                        finalImage[j, k] = split[j, k]
            counter = counter + 1
        plt.title('Result Image')
        show(finalImage)  # Give the final image of diagonal cut
#################################################Ending diagonal########################################################
    else:
        print("INVALID SLICE TYPE!")
else:
    print("ERROR! TOO MANY CUTS OR TOO FEW CUTS!")
