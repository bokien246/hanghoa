import easyocr
import cv2
import os
def resize_image(image, max_width, max_height):
    height, width = image.shape[:2]
    scaling_factor = min(max_width / width, max_height / height)
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)
    resized_image = cv2.resize(image, (new_width, new_height))
    return resized_image, scaling_factor
def process_image(image_path, reader, product_database, output_directory):
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Could not read image: {image_path}")
        return
    resized_image, scaling_factor = resize_image(original_image, 800, 800)
    result = reader.readtext(resized_image)
    font = cv2.FONT_HERSHEY_SIMPLEX
    found = False
    for detection in result:
        text = detection[1]
        for product, representations in product_database.items():
            for representation in representations:
                if representation.lower() in text.lower():
                    points = detection[0]
                    x1, y1 = int(points[0][0]), int(points[0][1])
                    x3, y3 = int(points[2][0]), int(points[2][1])
                    cv2.rectangle(resized_image, (x1, y1), (x3, y3), (0, 255, 0), 2)
                    display_text = f"Hang Hoa: {product}"
                    text_size = cv2.getTextSize(display_text, font, 1, 2)[0]
                    text_width, text_height = text_size[0], text_size[1]
                    image_width = resized_image.shape[1]
                    new_x = image_width - text_width - 18
                    cv2.putText(resized_image, display_text, (new_x, y1 - 10), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    found = True
                    break
            if found:
                break
        if found:
            break
    output_path = os.path.join(output_directory, os.path.basename(image_path))
    cv2.imwrite(output_path, resized_image)
reader = easyocr.Reader(['en'])
product_database = {
    "Sua": ["milk", "milK", "milx", "mi1k"],
    "bimbim": ["Snack", "snacK", "sn4ck", "sn@ck"],
    "Banhmi":["Staff", "stafF", "st@ff", "st4ff"],
    "xucxich":["VISSAN", "VISSAn", "VISS@N", "VISS4N"],
    "KhoBo" : ["BEEF JERKY", "BEEF JERKy", "BEEF @JERKY", "BEEF JERK4Y"]
}

input_directory = 'C:\\Users\\kiend\\OneDrive\\Desktop\\hanghoa\\anh'

output_directory = os.path.join(input_directory, 'luutru')
os.makedirs(output_directory, exist_ok=True)


for filename in os.listdir(input_directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(input_directory, filename)
        process_image(image_path, reader, product_database, output_directory)
        print(f"Processed: {filename}")

print("Ket Qua:")
