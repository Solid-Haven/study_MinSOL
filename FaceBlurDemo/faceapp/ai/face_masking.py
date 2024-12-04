import os
import json
import cv2

def process_video(video_path, user_id):
    """
    하드코딩된 얼굴 데이터로 영상을 처리하는 테스트용 함수.
    """
    # JSON에서 하드코딩된 얼굴 데이터를 로드 (가정)
    dummy_embedding = [0.1, 0.2, 0.3, 0.4, 0.5]  # 간단한 하드코딩 데이터
    print(f"사용자 {user_id}의 얼굴 데이터: {dummy_embedding}")

    # 영상 읽기
    if not os.path.exists(video_path):
        print(f"오류: {video_path} 파일이 존재하지 않습니다.")
        return None

    cap = cv2.VideoCapture(video_path)
    processed_dir = os.path.join('media', 'processed_videos')
    os.makedirs(processed_dir, exist_ok=True)

    # 처리된 파일 경로
    processed_path = os.path.join(processed_dir, f"user_{user_id}_processed.mp4")
    print(f"Processed video path: {processed_path}")

    # 영상 저장 설정
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 여기서 얼굴을 모자이크 처리하는 로직을 간단히 구현
        height, width, _ = frame.shape
        cv2.rectangle(frame, (50, 50), (width - 50, height - 50), (0, 255, 0), 5)
        cv2.putText(frame, 'Mock Mosaic', (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # 결과를 저장
        if out is None:
            out = cv2.VideoWriter(processed_path, fourcc, 30.0, (width, height))
        out.write(frame)

    cap.release()
    if out:
        out.release()
    
    # 파일 확인
    if not os.path.exists(processed_path):
        print(f"Error: Processed file not found at {processed_path}")
        return None

    print(f"사용자 {user_id}의 영상이 처리되어 {processed_path}에 저장되었습니다.")
    return processed_path
