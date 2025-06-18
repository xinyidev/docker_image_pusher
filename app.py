#!/usr/bin/env python3

from flask import Flask, jsonify, request
import ddddocr
import time

app = Flask(__name__)

ocr = ddddocr.DdddOcr(beta=True)  # 切换为第二套ocr模型

def image_recognition(img):
    # Sentences are encoded by calling model.encode()
    start_time = time.time()
    result = ocr.classification(img, png_fix=True)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("image_recognition 执行时间:", elapsed_time, "秒")

    return result


@app.route('/ocr/v1/reader', methods=['POST'])
def ask():
    req = request.get_json(force=True)
    content = req['content']
    # print(f'>>>\n{content}\n>>>')
    result = image_recognition(content)
    return jsonify({
        'code': '200',
        'message': '',
        'data': {
            'message': result
        }
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10020, debug=False)
