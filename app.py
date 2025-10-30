#!/usr/bin/env python3

import os
import fitz
import base64
from paddleocr import PaddleOCR, draw_ocr
from flask import Flask, jsonify, request
import time
import datetime
from PIL import Image

app = Flask(__name__)

ocr = PaddleOCR(use_angle_cls=True, rec_model_dir="ch_PP-OCRv4_rec_server_infer", lang="ch")  # need to run only once to download and load model into memory

def base64_to_image(base64_string, output_image_path):
    """
    将Base64编码的字符串转换为图片并保存到指定的路径。

    参数:
    base64_string (str): Base64编码的字符串。
    output_image_path (str): 输出图片文件的路径。
    """
    # 将Base64编码的字符串转换为二进制数据
    image_data = base64.b64decode(base64_string)

    # 将二进制数据写入文件
    with open(output_image_path, "wb") as image_file:
        image_file.write(image_data)

    original_image = Image.open(output_image_path)
    new_size = (original_image.size[0] * 4, original_image.size[1] * 4)

    # 使用resize方法放大图片，并使用LANCZOS滤波器提高质量
    resized_image = original_image.resize(new_size, Image.Resampling.LANCZOS)

    # 保存放大后的图片
    resized_image.save(output_image_path)


def image2Text(base64_string):
    # Sentences are encoded by calling model.encode()
    img_path = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+".png"
    base64_to_image(base64_string,img_path)

    start_time = time.time()
    result = ocr.ocr(img_path, cls=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("image2Text 执行时间:", elapsed_time, "秒")

    if len(result) > 0:
        os.remove(img_path)

    return result


@app.route('/ocr/v1/imageToText', methods=['POST'])
def ask():
    req = request.get_json(force=True)
    content = req['content']
    print(f'>>>\n{content}\n>>>')
    result = image2Text(content)
    val = ''
    if len(result) > 0:
        result = result[0]
        val = [line[1][0] for line in result]
    return jsonify({
        'code': '200',
        'message': '',
        'data': {
            'message': val[0]
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10020, debug=False)
