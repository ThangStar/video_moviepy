from inference_sdk import InferenceHTTPClient, InferenceConfiguration
import cv2
import os
import numpy as np
from PIL import ImageFont, ImageDraw, Image

def put_text_with_custom_font(img, text, position, font_path, font_size=32, color=(0, 255, 0)):
    # Chuyển ảnh OpenCV sang định dạng PIL
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # Tạo đối tượng draw
    draw = ImageDraw.Draw(pil_img)
    
    # Load font
    font = ImageFont.truetype(font_path, font_size)
    
    # Vẽ text
    draw.text(position, text, font=font, fill=color)
    
    # Chuyển lại sang định dạng OpenCV
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def draw_and_save_detection(image_path, predictions, output_dir="temp/images/detection"):
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(output_dir, exist_ok=True)
    
    # Đọc ảnh gốc
    image = cv2.imread(image_path)
    
    # Font path
    font_path = "temp/fonts/ChakraPetch-Medium.ttf"
    
    # Vẽ khung cho mỗi khuôn mặt được phát hiện
    for pred in predictions['predictions']:
        # Lấy tọa độ khung
        x = int(pred['x'] - pred['width']/2)
        y = int(pred['y'] - pred['height']/2)
        w = int(pred['width'])
        h = int(pred['height'])
        
        # Vẽ khung màu xanh lá
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Thêm nhãn với độ tin cậy
        label = f"Tuổi: {pred['class_id']} ({pred['confidence']*100:.1f}%)"
        
        # Sử dụng font tùy chỉnh
        image = put_text_with_custom_font(
            image, 
            label, 
            (x, max(y - 35, 0)),  # Điều chỉnh vị trí text cao hơn một chút
            font_path,
            font_size=32
        )
    
    # Tạo tên file output
    filename = os.path.basename(image_path)
    output_path = os.path.join(output_dir, f"detected_{filename}")
    
    # Lưu ảnh
    cv2.imwrite(output_path, image)
    return output_path
def face_detection(image_path):
    custom_configuration = InferenceConfiguration(confidence_threshold=0.3)

    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="BNQHlg5L0Mdac8Vdw0K1"
    )

    # Cấu hình và thực hiện dự đoán
    CLIENT.configure(custom_configuration)
    predictions = CLIENT.infer(image_path, model_id="agedetect/1")
    return predictions
    # print(predictions)
    # # Vẽ và lưu kết quả
    # output_path = draw_and_save_detection(image_path, predictions)
    # print(f"Đã lưu ảnh kết quả tại: {output_path}")