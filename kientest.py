import easyocr
import cv2


reader = easyocr.Reader(['en']) 


result = reader.readtext('C:\\Users\\kiend\\OneDrive\\Desktop\\Nhan dien bien\\hanghoa\\im5.jpg')


product_database = {
    "sữa": ["milk", "milK", "milx", "mi1k"],
    "bread": ["bread", "breaD", "bre4d", "br3ad"],
    "bimbim": ["Snack", "snacK", "sn4ck", "sn@ck"],
}


for detection in result:
    text = detection[1]
    
  
    for product, representations in product_database.items():
        for representation in representations:
            if representation.lower() in text.lower():
                print(f"Phát hiện sản phẩm: {product}")
                print(f"Văn bản: {text}")
                print(f"Vị trí: {detection[0]}")
                break  
        else:
            continue  
        break  
    else:
        continue  
    break  
