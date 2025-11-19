import numpy as np
import csv
import os

def convert_raw_rgb_to_csv(raw_file_path, csv_file_path, width, height, channels=3):
    """
    순수 바이너리 "Raw" RGB 파일을 CSV로 변환합니다.
    (기본값: 8비트, 3채널 RGB)
    
    :param raw_file_path: 입력 .raw 파일 경로
    :param csv_file_path: 출력 .csv 파일 경로
    :param width: 이미지 너비 (픽셀)
    :param height: 이미지 높이 (픽셀)
    :param channels: 채널 수 (RGB는 3)
    """
    try:
        # 표준 RGB는 채널당 8비트(unsigned 8-bit integer)입니다.
        dtype = np.uint8
        
        # 바이너리 파일 읽기
        print(f"Reading {raw_file_path}...")
        data = np.fromfile(raw_file_path, dtype=dtype)
        
        # 파일 크기 검증
        expected_size = width * height * channels
        if data.size != expected_size:
            print(f"Error: 파일 크기가 일치하지 않습니다.")
            print(f"예상된 값 개수: {expected_size} (W:{width} * H:{height} * C:{channels})")
            print(f"파일에 포함된 실제 값 개수: {data.size}")
            print("너비(width), 높이(height) 또는 채널(channels) 값을 확인하세요.")
            return
            
        # 1D 배열을 3D (height, width, channels) 배열로 변환
        pixels = data.reshape((height, width, channels))
        
        print(f"Writing data to {csv_file_path}...")
        with open(csv_file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            # 헤더(Header) 작성
            writer.writerow(['x', 'y', 'R', 'G', 'B'])
            
            # 각 픽셀을 순회하며 좌표와 RGB 값 작성
            for y in range(height):
                for x in range(width):
                    # R, G, B 값 추출
                    r, g, b = pixels[y, x]
                    writer.writerow([x, y, r, g, b])
                    
        print(f"성공: {raw_file_path} -> {csv_file_path}")

    except FileNotFoundError:
        print(f"Error: 입력 파일을 찾을 수 없습니다. {raw_file_path}")
    except Exception as e:
        print(f"에러가 발생했습니다: {e}")


# --- 사용 방법 ---
if __name__ == "__main__":
    
    # !!! 중요 !!!
    # 여기에 실제 Raw RGB 데이터의 너비와 높이를 입력하세요.
    # 예시로 640x480을 사용합니다.
    IMAGE_WIDTH = 1440
    IMAGE_HEIGHT = 960
    
    # 데모를 위한 더미(dummy) Raw RGB 파일 생성
    # 실제 파일을 사용할 때는 이 부분은 필요 없습니다.
    DUMMY_RGB_FILE = '111111_Color.raw'
    OUTPUT_CSV_FILE = 'converted_rgb_output.csv'
    
    print("데모를 위한 더미 RGB 파일을 생성합니다...")
    # (높이, 너비, 채널) 형태의 랜덤 8비트 데이터 생성
    try:
        dummy_rgb_data = np.random.randint(0, 256, (IMAGE_HEIGHT, IMAGE_WIDTH, 3), dtype=np.uint8)
        dummy_rgb_data.tofile(DUMMY_RGB_FILE)
        print(f"'{DUMMY_RGB_FILE}' 파일 생성 완료.")
    except Exception as e:
        print(f"더미 파일 생성 중 에러: {e}")
        exit()

    # --- 변환기 실행 ---
    # 실제 파일을 변환하려면:
    # 1. 'IMAGE_WIDTH'와 'IMAGE_HEIGHT'를 실제 값으로 변경하세요.
    # 2. 'raw_file_path'를 실제 업로드한 파일 이름으로 변경하세요. (예: "my_rgb_data.raw")
    
    print("\n--- RGB 변환 시작 ---")
    convert_raw_rgb_to_csv(
        raw_file_path=DUMMY_RGB_FILE,  # <-- 실제 파일 이름으로 변경
        csv_file_path=OUTPUT_CSV_FILE,
        width=IMAGE_WIDTH,
        height=IMAGE_HEIGHT
    )
