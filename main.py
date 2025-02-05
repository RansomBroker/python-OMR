from utils import *
import cv2

def scan_answer(template_image, image_path, answer_json):
    """
    Full processing pipeline:
    - Detect rectangles.
    - Increase image brightness.
    - Crop image based on bounding sboxes.
    - Detect circles in the cropped image.
    """
    img = load_image(image_path)
    template = load_image(template_image)

    # Detect filled rectangles
    filled_rectangles = detect_filled_rectangles_with_adjusted_filters(img)
    template_rectangles = detect_filled_rectangles_with_adjusted_filters(template)

    if len(filled_rectangles) == 0:
        return {"error": "No filled rectangles detected.", "code": 1, "answer_selected": None, "user_id_detected": None}

    # Draw rectangles on the image
    img_with_rectangles = draw_filled_rectangles(img, filled_rectangles)
    template_with_rectangles = draw_filled_rectangles(template, template_rectangles)

    # Detect brightness of both images
    img_brightness_level = detect_brightness_level(img_with_rectangles)
    template_brightness_level = detect_brightness_level(template_with_rectangles)

    print(f"Image Brightness Level: {img_brightness_level}")
    print(f"Template Brightness Level: {template_brightness_level}")

    if img_brightness_level < 150:
        return {"error": "Image brightness is too low.", "code": 2, "answer_selected": None, "user_id_detected": None}

    # Crop the image with detected bounding boxes
    cropped_image_with_margin = crop_with_margin(img_with_rectangles, filled_rectangles)
    template_cropped_image_with_margin = crop_with_margin(template_with_rectangles, template_rectangles)

    # Display images
    #display_image(adjusted_img)  # Show image with adjusted brightness
    #display_image(cropped_image_with_margin)  # Show cropped image with detected circles
    #display_image(template_with_rectangles)  # Show template image with rectangles
    #display_image(template_cropped_image_with_margin)  # Show cropped template image

    # Align Image
    aligned_image = align_images(cropped_image_with_margin, template_cropped_image_with_margin, debug=False)

    # Detect dark circles on the aligned image
    lower_image_brightness = increase_image_brightness(aligned_image, 0.5)
    print(detect_brightness_level(lower_image_brightness))
    dark_circles_in_aligned_image = detect_circles_in_cropped_image(lower_image_brightness)

    # If dark circles are detected, draw them on the aligned image in red
    for (x, y, r) in dark_circles_in_aligned_image:
        cv2.circle(aligned_image, (x, y), r, (0, 0, 255), 4)  # Red circles

    # Display aligned image with dark circles
    # display_image(aligned_image)  

    # Matched Answer
    (user_id, answer_selected) = find_matching_answer(answer_json, dark_circles_in_aligned_image)

    print(user_id, answer_selected)
    return {"error": None, "code": 0, "answer_selected": answer_selected, "user_id": user_id}

# Run the full processing pipeline on the image with brightness adjustment
# image_path = 'images\lembar valid2.jpg'  # Adjust the path as necessary
# scan_answer("images\lembar jawaban.jpg", image_path, answer_json="answer_position.json")