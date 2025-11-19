from PIL import Image
import numpy as np
import os

# --- 1. 설정 (SETTINGS) ---
# 입력 파일 (이미지 파일)
input_img_file = '111111_Depth.png'

# 출력할 파일 이름들
output_raw_file = '111111_Depth_merged.raw'
output_csv_file = '111111_Depth_merged.csv'

# --- 2. 실행 로직 (MAIN SCRIPT) ---

print(f"--- Process Start ---")

# 1) 이미지 파일 존재 여부 확인
if not os.path.exists(input_img_file):
    print(f"ERROR: Input file '{input_img_file}' not found.")
    exit()

# 2) 이미지 로드 (Pillow 사용)
print(f"1. Loading image: {input_img_file}...")
try:
    with Image.open(input_img_file) as img:
        # 이미지 정보 추출
        width, height = img.size
        mode = img.mode
        print(f"   - Dimensions: {width} x {height}")
        print(f"   - Mode: {mode}")

        # 3) 이미지를 NumPy 배열로 변환 (핵심 단계)
        # 이미지가 16bit Depth라면 자동으로 uint16으로, 8bit라면 uint8로 변환됩니다.
        img_array = np.array(img)
        print(f"   - Converted to NumPy Array. Shape: {img_array.shape}, Dtype: {img_array.dtype}")

except Exception as e:
    print(f"ERROR loading image: {e}")
    exit()

# 4) RAW 파일 생성 (Binary 저장)
print(f"2. Saving RAW file: {output_raw_file}...")
try:
    # tofile()은 헤더 없이 순수 데이터만 바이너리로 저장합니다.
    img_array.tofile(output_raw_file)
    print("   - RAW save complete.")
except Exception as e:
    print(f"ERROR saving RAW: {e}")

# 5) CSV 파일 생성 (NumPy의 빠른 저장 기능 활용)
print(f"3. Saving CSV file: {output_csv_file}...")

try:
    # 만약 이미지가 컬러(RGB, 3차원)라면 2차원으로 펼쳐야 CSV 저장이 쉽습니다.
    if img_array.ndim == 3:
        print("   - Warning: Color image detected. Saving as flattened 2D array for CSV.")
        # (높이, 너비*3) 형태로 변경하여 저장
        save_array = img_array.reshape(img_array.shape[0], -1)
    else:
        # 흑백/Depth(2차원) 이미지는 그대로 저장
        save_array = img_array

    # 두 번째 코드의 효율적인 방식(savetxt) 사용
    # fmt='%d'는 정수형, '%.2f'는 실수형
    np.savetxt(output_csv_file, save_array, delimiter=',', fmt='%d')
    print("   - CSV save complete.")

except Exception as e:
    print(f"ERROR saving CSV: {e}")

print(f"\n--- All Done! ---")
print(f"Check created files: {output_raw_file}, {output_csv_file}")
