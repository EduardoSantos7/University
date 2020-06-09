import cv2
import numpy as np


def sift_detector(new_image, image_template):
    # Function that compares input image to template
    # It then returns the number of SIFT matches between them
    new_image = new_image.astype('uint8')
    image1 = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)
    image2 = image_template

    # Create SIFT detector object
    #sift = cv2.SIFT()
    sift = cv2.xfeatures2d.SIFT_create()
    # Obtain the keypoints and descriptors using SIFT
    keypoints_1, descriptors_1 = sift.detectAndCompute(image1, None)
    keypoints_2, descriptors_2 = sift.detectAndCompute(image2, None)

    # Define parameters for our Flann Matcher
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=3)
    search_params = dict(checks=100)

    # Create the Flann Matcher object
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    # Obtain matches using K-Nearest Neighbor Method
    # the result 'matchs' is the number of similar matches found in both images
    matches = flann.knnMatch(descriptors_1, descriptors_2, k=2)

    # Store good matches using Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good_matches.append((m,n))
   # return len(good_matches)

    return good_matches, keypoints_1, keypoints_2


# Load our image template, this is our reference image
image_template = cv2.imread('phone.jpg')
# image_template = cv2.resize(image_template, (800, 800))

image = cv2.imread('phone.jpg')
image = cv2.resize(image, (800, 800))

# Get height and width of webcam image
height, width = image.shape[:2]

# Define ROI Box Dimensions
top_left_x = int(width / 3)
top_left_y = int((height / 2) + (height / 4))
bottom_right_x = int((width / 3) * 2)
bottom_right_y = int((height / 2) - (height / 4))

# Draw rectangular window for our region of interest
cv2.rectangle(image, (top_left_x, top_left_y),
                (bottom_right_x, bottom_right_y), 255, 3)

# Crop window of observation we defined above
cropped = image[bottom_right_y:top_left_y, top_left_x:bottom_right_x]

# Flip image orientation horizontally
image = cv2.flip(image, 1)

# Get number of SIFT matches
matches, k1, k2 = sift_detector(cropped, image_template)

image = cv2.drawMatches(cropped, k1, image_template, k2, [m for m, n in matches], image)

# Display status string showing the current no. of matches
cv2.putText(image, str(matches), (450, 450),
            cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 1)

# Our threshold to indicate object deteciton
# We use 10 since the SIFT detector returns little false positves
threshold = 10

# If matches exceed our threshold then object has been detected
if len(matches) > threshold:
    cv2.rectangle(image, (top_left_x, top_left_y),
                    (bottom_right_x, bottom_right_y), (0, 255, 0), 3)
    cv2.putText(image, 'Object Found', (50, 50),
                cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
cv2.imshow('Object Detector using SIFT', image)
cv2.waitKey(0)
