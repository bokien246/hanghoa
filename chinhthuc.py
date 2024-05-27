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


def process_image(image_path, reader, product_database):
    anh = cv2.imread(image_path)
    if anh is None:
        print(f"Không thể đọc hình ảnh: {image_path}")
        return

    resized_image, scaling_factor = resize_image(anh, 800, 800)
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
    cv2.imshow('Kết quả nhận dạng', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
reader = easyocr.Reader(['en'])

product_database = {
    "Sua": ["milk", "milK", "milx", "mi1k"],
    "bimbim": ["Snack", "snacK", "sn4ck", "sn@ck"],
    "Banhmi": ["Staff", "stafF", "st@ff", "st4ff"],
    "xucxich": ["VISSAN", "VISSAn", "VISS@N", "VISS4N"],
    "KhoBo": ["BEEF JERKY", "BEEF JERKy", "BEEF @JERKY", "BEEF JERK4Y"]
}

image_directory = 'C:\\Users\\kiend\\OneDrive\\Desktop\\hanghoa\\anh'

while True:
    image_files = [f for f in os.listdir(image_directory) if f.endswith(('.jpg', '.png'))]
    if not image_files:
        print("Không có tệp hình ảnh nào trong thư mục.")
        break

    print("Các tệp hình ảnh có sẵn:")
    for image_file in image_files:
        print(image_file)

    image_name = input("Nhập tên tệp ảnh để xử lý (hoặc 'exit' để thoát): ")
    if image_name.lower() == 'exit':
        break
    if image_name in image_files:
        image_path = os.path.join(image_directory, image_name)
        process_image(image_path, reader, product_database)
        print("Đã xử lý xong ảnh. Bạn có thể nhập tên tệp ảnh khác hoặc nhập 'exit' để thoát.")
    else:
        print("Tệp không tồn tại. Vui lòng thử lại.")
