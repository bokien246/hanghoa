import easyocr
import cv2

reader = easyocr.Reader(['en']) 


result = reader.readtext('C:\\Users\\kiend\\OneDrive\\Desktop\\hanghoa\\im4.png')
anh = cv2.imread('C:\\Users\\kiend\\OneDrive\\Desktop\\hanghoa\\im4.png')
font = cv2.FONT_HERSHEY_SIMPLEX 


product_database = {
    "Sua": ["milk", "milK", "milx", "mi1k"],
    "bimbim": ["Snack", "snacK", "sn4ck", "sn@ck"],
}

found = False


for detection in result:
    text = detection[1]
    

    for product, representations in product_database.items():
        for representation in representations:
            if representation.lower() in text.lower():
                points = detection[0]
                x1, y1 = points[0]
                x3, y3 = points[2]
                cv2.rectangle(anh, (x1, y1), (x3, y3), (0, 255, 0), 2)
                
                display_text = f"Hang Hoa: {product}"
                text_size = cv2.getTextSize(display_text, font, 1, 2)[0]
                text_width, text_height = text_size[0], text_size[1]
                image_width = anh.shape[1]
                new_x = image_width - text_width - 18  
                cv2.putText(anh, display_text, (new_x, y1 - 10), font, 1, (0, 255, 0), 2, cv2.LINE_AA)
                
                found = True
                break  # Dừng vòng lặp khi đã tìm thấy sản phẩm phù hợp
        if found:
            break  # Thoát khỏi vòng lặp sản phẩm khi đã tìm thấy sản phẩm phù hợp
    if found:
        break  # Thoát khỏi vòng lặp phát hiện khi đã tìm thấy một kết quả phù hợp

# Hiển thị ảnh với kết quả nhận dạng
cv2.imshow('VMUUUUUUU', anh)
cv2.waitKey(0)
cv2.destroyAllWindows()
