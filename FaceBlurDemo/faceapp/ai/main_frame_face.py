import os
from .face_recog import mask_faces_in_frame, load_registered_faces

def process_all_frames(frames_dir, json_dir, output_dir, similarity_threshold=0.5):
    # JSON 파일 로드
    for json_file in os.listdir(json_dir):
        if not json_file.endswith(".json"):
            continue
        json_path = os.path.join(json_dir, json_file)
        registered_data = load_registered_faces(json_path)
        if registered_data is None:
            continue
        
        # 처리할 이미지 경로 설정
        for frame_file in os.listdir(frames_dir):
            if not frame_file.endswith((".jpg", ".png")):
                continue
            image_path = os.path.join(frames_dir, frame_file)
            frame_name = os.path.splitext(frame_file)[0]  # 파일명 추출
            
            # 결과 이미지 경로 설정
            output_path = os.path.join(output_dir, f"masked_{frame_name}.jpg")
            
            # 얼굴 마스킹 수행
            mask_faces_in_frame(image_path, registered_data, similarity_threshold, output_path)

def main():
    # 경로 설정
    frames_dir = "before/frame/2024-12-07-11_15"  # 처리할 프레임들이 저장된 디렉토리
    json_dir = "face/json"  # 등록된 얼굴 데이터(JSON)가 저장된 디렉토리
    output_dir = "after/frame/2024-12-07-11_15"  # 결과 이미지가 저장될 디렉토리

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 모든 프레임 처리
    process_all_frames(frames_dir, json_dir, output_dir)

if __name__ == "__main__":
    main()
