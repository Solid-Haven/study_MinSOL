import numpy as np
import json
import time
import os
from django.conf import settings

def register_face(user_id):
    
    # 하드코딩된 얼굴 데이터 (예: 128차원 임베딩)
    dummy_embedding = np.random.rand(128).tolist()

    # 딜레이 추가 (AI 모델이 동작하는 것처럼)
    print("얼굴 등록 중...")
    time.sleep(2)

    # JSON 데이터 생성
    face_data = {
        "user_id": user_id,
        "embedding": dummy_embedding
    }

    # JSON 파일 저장
    output_dir = os.path.join(settings.MEDIA_ROOT, 'landmarks')
    os.makedirs(output_dir, exist_ok=True)
    json_file_path = os.path.join(output_dir, f"user_{user_id}_face_embedding.json")
    with open(json_file_path, 'w') as json_file:
        json.dump(face_data, json_file)

    print(f"사용자 {user_id}의 얼굴 데이터가 {json_file_path}에 저장되었습니다.")
