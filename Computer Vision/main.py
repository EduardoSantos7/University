import cv2

toyota_car = cv2.imread("toyota_car.jpg", 0)
toyota_car_2 = cv2.imread("toyota_car_3.jpeg", 0)

# Detectors
orb = cv2.ORB_create(nfeatures=7000)
sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()

# Keypoints
orb_toyota_key_points, orb_toyota_descriptor = orb.detectAndCompute(toyota_car, None)
orb_toyota_key_points_2, orb_toyota_descriptor_2 = orb.detectAndCompute(toyota_car_2, None)
sift_toyota_key_points, sift_toyota_descriptor = sift.detectAndCompute(toyota_car, None)
sift_toyota_key_points_2, sift_toyota_descriptor_2 = sift.detectAndCompute(toyota_car_2, None)
surf_toyota_key_points, surf_toyota_descriptor = surf.detectAndCompute(toyota_car, None)
surf_toyota_key_points_2, surf_toyota_descriptor_2 = surf.detectAndCompute(toyota_car_2, None)

# Brute Force Matching
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
orb_matches = bf.match(orb_toyota_descriptor, orb_toyota_descriptor_2)
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
sift_matches = bf.match(sift_toyota_descriptor, sift_toyota_descriptor_2)
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)
surf_matches = bf.match(surf_toyota_descriptor, surf_toyota_descriptor_2)

# Sort
orb_matches = sorted(orb_matches, key=lambda x: x .distance)
sift_matches = sorted(sift_matches, key=lambda x: x .distance)
surf_matches = sorted(surf_matches, key=lambda x: x .distance)

print(len(orb_matches), len(orb_toyota_descriptor), len(orb_matches)/ len(orb_toyota_descriptor))
print(len(sift_matches), len(sift_toyota_descriptor), len(sift_matches)/ len(sift_toyota_descriptor))
print(len(surf_matches), len(surf_toyota_descriptor),
      len(surf_matches) / len(surf_toyota_descriptor))

orb_matching_result = cv2.drawMatches(
    toyota_car, orb_toyota_key_points, toyota_car_2,
    orb_toyota_key_points_2, orb_matches[:200], None)

sift_matching_result = cv2.drawMatches(
    toyota_car, sift_toyota_key_points, toyota_car_2,
    sift_toyota_key_points_2, sift_matches[:200], None)

surf_matching_result = cv2.drawMatches(
    toyota_car, surf_toyota_key_points, toyota_car_2,
    surf_toyota_key_points_2, surf_matches[:200], None)

# Create window with freedom of dimensions
cv2.namedWindow("output", cv2.WINDOW_NORMAL)
orb_img = cv2.resize(orb_matching_result, (1000, 600))
sift_img = cv2.resize(sift_matching_result, (1000, 600))
surf_img = cv2.resize(surf_matching_result, (1000, 600))
cv2.imshow("Toyota1", orb_img)
cv2.waitKey(0)
cv2.imshow("Toyota2", sift_img)
cv2.waitKey(0)
cv2.imshow("Toyota3", surf_img)
cv2.waitKey(0)
