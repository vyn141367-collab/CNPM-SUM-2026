import os
import time
from flask import Blueprint, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from infrastructure.repositories.submission_repository import SubmissionRepository

bp = Blueprint('submissions', __name__, url_prefix='/api/submissions')

# Đường dẫn thư mục lưu ảnh nộp
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@bp.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    """API trả về file ảnh công khai cho Judge và Admin xem"""
    return send_from_directory(UPLOAD_FOLDER, filename)

@bp.route('', methods=['POST'])
def submit_film():
    # Xử lý trường hợp nhận tệp ảnh tải lên (multipart/form-data)
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Tệp ảnh không hợp lệ"}), 400
            
        filename = secure_filename(file.filename)
        unique_filename = f"{int(time.time())}_{filename}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        file.save(file_path)
        
        # Đường dẫn URL tới ảnh vừa lưu
        image_url = f"http://127.0.0.1:9999/api/submissions/uploads/{unique_filename}"
        data = request.form.to_dict()
        data['image_url'] = image_url
    else:
        # Xử lý nếu gửi JSON truyền đường dẫn URL cũ
        data = request.json or {}

    # Kiểm tra trường bắt buộc
    required_fields = ['image_url', 'film_stock', 'camera', 'film_format']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Thiếu thông tin bắt buộc: {field}"}), 400
            
    repo = SubmissionRepository()
    try:
        new_sub = repo.create_submission(data)
        return jsonify({
            "message": "Nộp bài thành công!", 
            "submission_id": new_sub.id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('', methods=['GET'])
def get_all_submissions():
    repo = SubmissionRepository()
    subs = repo.get_all()
    
    result = []
    for s in subs:
        result.append({
            "id": s.id,
            "title": s.title,
            "image_url": s.image_url,
            "film_stock": s.film_stock,
            "camera": s.camera,
            "lens": s.lens,
            "iso": s.iso,
            "film_format": s.film_format,
            "developing_lab": s.developing_lab,
            "scanning_specs": s.scanning_specs
        })
        
    return jsonify({"data": result}), 200

@bp.route('/<sub_id>', methods=['PUT'])
def update_submission(sub_id):
    """API Cập nhật thông tin bài nộp"""
    data = request.json
    repo = SubmissionRepository()
    try:
        repo.update_submission(sub_id, data)
        return jsonify({"message": "Cập nhật thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/<sub_id>', methods=['DELETE'])
def delete_submission(sub_id):
    """API Xóa bài nộp"""
    repo = SubmissionRepository()
    try:
        repo.delete_submission(sub_id)
        return jsonify({"message": "Xóa thành công!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500