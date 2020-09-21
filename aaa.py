# import the necessary packages
import argparse
import cv2 as cv
import numpy as np
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
refPt = []

lista_puntos =[]

cropping = False
def click_and_crop(event, x, y, flags, param):
    # grab references to the global variables
    global refPt, cropping
    # if the left mouse button was clicked, record the starting
    # (x, y) coordinates and indicate that cropping is being
    # performed
    if event == cv.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        lista_puntos.append((x, y))
        print (lista_puntos)
        cropping = True
    # check to see if the left mouse button was released
    elif event == cv.EVENT_LBUTTONUP:
        # record the ending (x, y) coordinates and indicate that
        # the cropping operation is finished
        refPt.append((x, y))
        cropping = False
        # draw a rectangle around the region of interest
        cv.rectangle(image, refPt[0], refPt[1], (0, 255, 0), 2)
        cv.imshow("image", image)


class PixelMapper(object):
    """
    Create an object for converting pixels to geographic coordinates,
    using four points with known locations which form a quadrilteral in both planes
    Parameters
    ----------
    pixel_array : (4,2) shape numpy array
        The (x,y) pixel coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    lonlat_array : (4,2) shape numpy array
        The (lon, lat) coordinates corresponding to the top left, top right, bottom right, bottom left
        pixels of the known region
    """
    def __init__(self, pixel_array, lonlat_array):
        assert pixel_array.shape==(4,2), "Need (4,2) input array"
        assert lonlat_array.shape==(4,2), "Need (4,2) input array"
        self.M = cv.getPerspectiveTransform(np.float32(pixel_array),np.float32(lonlat_array))
        self.invM = cv.getPerspectiveTransform(np.float32(lonlat_array),np.float32(pixel_array))
        
    def pixel_to_lonlat(self, pixel):
        """
        Convert a set of pixel coordinates to lon-lat coordinates
        Parameters
        ----------
        pixel : (N,2) numpy array or (x,y) tuple
            The (x,y) pixel coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (lon, lat) coordinates
        """
        if type(pixel) != np.ndarray:
            pixel = np.array(pixel).reshape(1,2)
        assert pixel.shape[1]==2, "Need (N,2) input array" 
        pixel = np.concatenate([pixel, np.ones((pixel.shape[0],1))], axis=1)
        lonlat = np.dot(self.M,pixel.T)
        
        return (lonlat[:2,:]/lonlat[2,:]).T
    
    def lonlat_to_pixel(self, lonlat):
        """
        Convert a set of lon-lat coordinates to pixel coordinates
        Parameters
        ----------
        lonlat : (N,2) numpy array or (x,y) tuple
            The (lon,lat) coordinates to be converted
        Returns
        -------
        (N,2) numpy array
            The corresponding (x, y) pixel coordinates
        """
        if type(lonlat) != np.ndarray:
            lonlat = np.array(lonlat).reshape(1,2)
        assert lonlat.shape[1]==2, "Need (N,2) input array" 
        lonlat = np.concatenate([lonlat, np.ones((lonlat.shape[0],1))], axis=1)
        pixel = np.dot(self.invM,lonlat.T)
        
        return (pixel[:2,:]/pixel[2,:]).T




# construct the argument parser and parse the arguments
#ap = argparse.ArgumentParser()
#ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())
# load the image, clone it, and setup the mouse callback function
image = cv.imread("1.jpeg")
clone = image.copy()
cv.namedWindow("image")
cv.setMouseCallback("image", click_and_crop)
# keep looping until the 'q' key is pressed
while True:
    # display the image and wait for a keypress
    cv.imshow("image", image)
    key = cv.waitKey(1) & 0xFF

    # if the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
    	var1= np.array([
    		[-20.288346,-70.117299],
    		[-20.288236,-70.117131],
    		[-20.288354,-70.117042],
    		[-20.288495,-70.117119]
    	])
    	var2= np.array([
    		[341,279],
    		[604,206],
    		[910,231],
    		[967,399]
    	])
    	pm = PixelMapper(var2,var1)

    	lonlat_0 = pm.pixel_to_lonlat([350,400])


    	cv.circle(image, (350,400), 8, (0,255,255), thickness=3, lineType=3, shift=0)

    	cantidad_lineas = 5
    	delta=0.00005
    	p1=[]
    	p2=[]
    	p_tupla=[]

    	for i in range(cantidad_lineas):
    		p1.append(pm.lonlat_to_pixel([-20.288346 + (delta*i),-70.117299 - delta]))
    		p2.append(pm.lonlat_to_pixel([-20.288346 + (delta*i),-70.117299 + delta]))

    	print(p1)
#    	print(p2)
#    	print(p1[i][0][0])

#    	for i in p1:
#    		print(int(p1[i][0][0]))
#    		p_tupla = p_tupla.append(zip(int(p1[i][0][0]),int(p2[i][0][1])))

#    	print(p_tupla)



#    	cv.line(image,p_tupla,p_tupla, (250,0,0), thickness=3)


    # if the 'c' key is pressed, break from the loop
    elif key == ord("c"):
        break

# close all open windows
cv.destroyAllWindows()