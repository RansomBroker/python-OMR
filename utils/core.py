import cv2
import numpy as np
import matplotlib.pyplot as plt
import imutils
import json
import math

def align_images(image, template, maxFeatures=300, keepPercent=0.5, debug=False):
    # convert both the input image and template to grayscale
    imageGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    templateGray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # use ORB to detect keypoints and extract (binary) local
    # invariant features
    orb = cv2.ORB_create(maxFeatures)
    (kpsA, descsA) = orb.detectAndCompute(imageGray, None)
    (kpsB, descsB) = orb.detectAndCompute(templateGray, None)
    # match the features
    method = cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING
    matcher = cv2.DescriptorMatcher_create(method)
    matches = matcher.match(descsA, descsB, None)

    # sort the matches by their distance (the smaller the distance,
    # the "more similar" the features are)
    matches = sorted(matches, key=lambda x:x.distance)
    # keep only the top matches
    keep = int(len(matches) * keepPercent)
    matches = matches[:keep]

    # check to see if we should visualize the matched keypoints
    if debug:
        matchedVis = cv2.drawMatches(image, kpsA, template, kpsB,
            matches, None)
        matchedVis = imutils.resize(matchedVis, width=1000)
        cv2.imshow("Matched Keypoints", matchedVis)
        cv2.waitKey(0)

    # allocate memory for the keypoints (x, y)-coordinates from the
    # top matches -- we'll use these coordinates to compute our
    # homography matrix
    ptsA = np.zeros((len(matches), 2), dtype="float")
    ptsB = np.zeros((len(matches), 2), dtype="float")
    # loop over the top matches
    for (i, m) in enumerate(matches):
        # indicate that the two keypoints in the respective images
        # map to each other
        ptsA[i] = kpsA[m.queryIdx].pt
        ptsB[i] = kpsB[m.trainIdx].pt

    # compute the homography matrix between the two sets of matched
    # points
    (H, mask) = cv2.findHomography(ptsA, ptsB, method=cv2.RANSAC)
    # use the homography matrix to align the images
    (h, w) = template.shape[:2]
    aligned = cv2.warpPerspective(image, H, (w, h))
    # return the aligned image
    return aligned

def detect_filled_rectangles_with_adjusted_filters(image):
    """
    Detect rectangles that are filled with dark color (near black), with adjusted filters:
    - Minimum area (lower threshold)
    - Correct aspect ratio (relaxed range).
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filled_rectangles = []

    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(contour)
            if w * h > 300:
                cropped = gray[y:y+h, x:x+w]
                mean_intensity = np.mean(cropped)
                if mean_intensity < 100:
                    aspect_ratio = float(w) / h
                    if 0.6 < aspect_ratio < 1.5:
                        filled_rectangles.append(approx)

    return filled_rectangles

def detect_circles_in_cropped_image(image):
    """
    Detect circles within the cropped image that are filled with dark color.
    """
    # Convert to grayscale for Hough Circle detection
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(gray_image, (19, 19), 0)
    
    # Use HoughCircles to detect circles
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT, dp=1.2, minDist=5, param1=50, param2=24, minRadius=5, maxRadius=15
    )

    dark_circles = []

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            # Crop the area around the circle
            cropped = gray_image[y-r:y+r, x-r:x+r]
            
            # Calculate the mean intensity in the cropped area
            mean_intensity = np.mean(cropped)
            if mean_intensity < 100:  # Dark intensity check for circles
                dark_circles.append((x, y, r))

    return dark_circles

def find_matching_answer(answerJsonPath, detected_circle, threshold=10):
    answer_selected = ["-" for i in range(60)]
    user_id_list = [0,0,0,0,0,0,0]

    with open(answerJsonPath, 'r') as file:
        answer_position = json.load(file)
    
    # Loop through each answer position
    for answer_idx, answer_list in enumerate(answer_position):
        for idx, (cx, cy) in enumerate(answer_list):
            for (x,y,r) in detected_circle:
                # Calculate distance
                distance = math.sqrt((x - cx)**2 + (y - cy)**2)
                if distance <= threshold:
                    if answer_idx < 9 :
                        user_id_list[idx] = answer_idx 
                    if answer_idx > 9:
                        answer_selected[answer_idx-10] = chr(idx + 65)

    # Formated output
    user_id = "".join(map(str, user_id_list))

    return user_id, answer_selected
                    



