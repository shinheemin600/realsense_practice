import pyrealsense2 as rs
import numpy as np
import cv2

# 파이프라인 생성
pipeline = rs.pipeline()

# 구성 설정
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# 정렬 객체 생성 (depth를 color 프레임에 정렬)
align_to = rs.stream.color
align = rs.align(align_to)

# 스트리밍 시작
pipeline.start(config)

try:
    while True:
        # 프레임 수신
        frames = pipeline.wait_for_frames()
        aligned_frames = align.process(frames)

        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not depth_frame or not color_frame:
            continue

        # numpy 배열로 변환
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Depth 시각화를 위한 컬러맵 변환
        depth_colormap = cv2.applyColorMap(
            cv2.convertScaleAbs(depth_image, alpha=0.03),
            cv2.COLORMAP_JET
        )

        # RGB + Depth 나란히 표시
        images = np.hstack((color_image, depth_colormap))

        # 디스플레이
        cv2.imshow('RealSense RGB + Depth', images)

        # 'q' 키 누르면 종료
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # 종료 처리
    pipeline.stop()
    cv2.destroyAllWindows()

