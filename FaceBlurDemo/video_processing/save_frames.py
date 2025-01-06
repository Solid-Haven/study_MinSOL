import cv2
import os

def save_frames(video_path, frames_dir, fps_dir):
    # 비디오 파일 이름 추출
    video_name = video_path.split('/')[-1].split('.')[0]  # 파일명 추출 (확장자 제거)

    # 프레임 저장 폴더 생성
    video_frames_dir = f"{frames_dir}/{video_name}"  # 프레임 저장 디렉토리
    fps_file_output_path = f"{fps_dir}/{video_name}.txt"  # FPS 저장 경로

    # 디렉토리 생성
    if not os.path.exists(video_frames_dir):
        os.makedirs(video_frames_dir)
    if not os.path.exists(fps_dir):
        os.makedirs(fps_dir)

    # 비디오 파일 읽기
    cap = cv2.VideoCapture(video_path)

    # FPS 정보 추출 및 저장
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"원본 영상 FPS: {fps}")
    with open(fps_file_output_path, 'w') as f:
        f.write(str(fps))

    frame_count = 0

    # 비디오의 각 프레임 저장
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_file_path = f"{video_frames_dir}/frame_{frame_count:04d}.png"  # 4자리 숫자로 정렬
        cv2.imwrite(frame_file_path, frame)
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()

    print(f"총 {frame_count}개의 프레임이 {video_frames_dir}에 저장되었습니다.")
    print(f"FPS 정보는 {fps_file_output_path}에 저장되었습니다.")

# 실행 예시
if __name__ == "__main__":
    video_path = 'before/video/2024-12-07-11_15.mp4'  # 처리할 비디오 경로
    frames_dir = 'before/frame'  # 프레임 저장 기본 경로
    fps_dir = 'after/ftp'  # FPS 정보 저장 기본 경로

    save_frames(video_path, frames_dir, fps_dir)
