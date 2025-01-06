import cv2
import numpy as np
import json
from keras_facenet import FaceNet
from scipy.spatial.distance import cosine
import os

# FaceNet 모델 로드
embedder = FaceNet()

# JSON 파일에서 등록된 얼굴 데이터 로드
def load_registered_faces(json_path):
    if not os.path.exists(json_path):
        print(f"등록된 얼굴 데이터를 찾을 수 없습니다: {json_path}")
        return None
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        # JSON이 단일 딕셔너리 형식일 경우
        embedding = data.get('embedding', None)
        if embedding:
            return [normalize_embedding(np.array(embedding).flatten())]
        else:
            print("JSON 데이터에 'embedding' 키가 없습니다.")
            return None
    except json.JSONDecodeError as e:
        print(f"JSON 파일 파싱 중 오류 발생: {e}")
        return None


def normalize_embedding(embedding):
    return embedding / np.linalg.norm(embedding)



# 프레임에서 얼굴 마스킹
def mask_faces_in_frame(image_path, registered_data, similarity_threshold, output_path="masked_image.jpg"):
    image = cv2.imread(image_path)
    if image is None:
        print(f"이미지를 로드할 수 없습니다: {image_path}")
        return

    try:
        faces = embedder.extract(image, threshold=0.95) if registered_data else []
        if not faces:
            print("이미지에서 얼굴을 찾을 수 없거나 JSON 데이터가 없습니다. 원본 이미지를 저장합니다.")
    except Exception as e:
        print(f"얼굴 검출 중 오류가 발생했습니다: {e}. 원본 이미지를 저장합니다.")
        faces = []

    # 얼굴 마스킹 또는 원본 저장
    for face in faces:
         current_embedding = normalize_embedding(np.array(face['embedding']).flatten())  # 검출된 얼굴 임베딩
         for registered_embedding in registered_data:
            similarity = 1 - cosine(registered_embedding, current_embedding)
            if similarity > similarity_threshold:  # 유사도 기준 초과
                (x, y, w, h) = face['box']  # 얼굴 영역 좌표
                face_region = image[y:y + h, x:x + w]
                face_region = cv2.GaussianBlur(face_region, (99, 99), 30)  # 가우시안 블러
                image[y:y + h, x:x + w] = face_region
                break  # 한 번 일치하면 해당 얼굴 마스킹 완료

    # 결과 이미지 저장
    cv2.imwrite(output_path, image)
    print(f"이미지가 저장되었습니다: {output_path}")
