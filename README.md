# Virtual-Colonoscopy
Final Project


Due: Sat 12/10/22 11:59 PM
__________________________________________________________________________________________________________________
We implemented a virtual CT (specifically part of the colon) to detect abnormalities, such as benign tumor (polyps) and/or cancerous tumor; the algorithms were developed using python. Furthermore, the algorithm would essentially imitate the performance of a CT scanner in various orientations. We created a system that collects numerous projections along different orientations upon image slicing. It would consist of our code slicing the phantom image diagonally, horizontally, and vertically.

### Instructions on how to run the code:
1) Press the run button.
2) Enter a x value for the tumor to be placed (100 < x < 150) any number not between the tumor will not be inside the colon.
3) Enter a y value for the tumor to be placed (100 < y < 150) any number not between the tumor will not be inside the colon.
4) Enter a slice type, "vertical", "horizontal", or "diagonal" anything else will be an invalid slice type.
5) Enter the number of slices, a integer value 1-255 anything else will be too few cuts or too many cuts.
