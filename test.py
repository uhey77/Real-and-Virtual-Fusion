# type: ignore
import cv2
import mediapipe as mp
import os
import numpy as np

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh

# カメラ設定
camera_no = 0
video_capture = cv2.VideoCapture(camera_no)

# カメラのサイズを取得
ret, test_frame = video_capture.read()
if ret:
    frame_height, frame_width = test_frame.shape[:2]
else:
    frame_width, frame_height = 640, 480


# 背景画像の設定
def set_country_background(country_name):
    """指定した国の背景画像を読み込む関数"""
    # backgrounds フォルダがない場合は作成
    if not os.path.exists("backgrounds"):
        os.makedirs("backgrounds")
        print("backgroundsフォルダを作成しました。背景画像を入れてください。")

    # 背景画像のパスを指定
    bg_path = f"backgrounds/{country_name.lower()}.jpg"

    if os.path.exists(bg_path):
        bg_image = cv2.imread(bg_path)
        # カメラのサイズに合わせてリサイズ
        bg_image = cv2.resize(bg_image, (frame_width, frame_height))
        return bg_image
    else:
        print(f"背景画像 {bg_path} が見つかりません。")
        # 見つからない場合はデフォルト背景を生成（例：青空色）
        default_bg = np.ones((frame_height, frame_width, 3), dtype=np.uint8) * np.array([255, 204, 153], dtype=np.uint8)
        cv2.putText(default_bg, f"{country_name}", (int(frame_width/4), int(frame_height/2)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2)
        return default_bg


# 背景画像と人物を合成する関数
def compose_background(frame, background, results):
    """人物を抽出して背景と合成する関数"""
    # フレームと背景のサイズを同じにする
    frame = cv2.resize(frame, (background.shape[1], background.shape[0]))

    # セグメンテーションマスクがある場合はそれを使用
    if results.segmentation_mask is not None:
        # マスクをフレームのサイズにリサイズ
        segmentation_mask = cv2.resize(
            results.segmentation_mask, (background.shape[1], background.shape[0]))

        # マスクを3チャンネルに拡張
        condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.1

        # 背景と人物を合成
        output_image = np.where(condition, frame, background)
        return output_image
    else:
        # セグメンテーションがない場合はフレームをそのまま返す
        print("セグメンテーションマスクが取得できませんでした。")
        return frame


if __name__ == '__main__':
    # 使用する国を指定
    country = input("背景にする国名を入力してください (例: japan): ")
    background = set_country_background(country)

    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
        enable_segmentation=True,  # セグメンテーション有効化
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as holistic:
        try:
            while video_capture.isOpened():
                ret, frame = video_capture.read()
                if not ret:
                    print("カメラの取得できず")
                    break

                frame = cv2.flip(frame, 1)
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                results = holistic.process(image)

                image.flags.writeable = True
                annotated_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 背景と人物を合成
                composed_image = compose_background(annotated_image, background, results)

                # 姿勢の描画
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        composed_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

                # 顔の描画
                if results.face_landmarks:
                    mp_drawing.draw_landmarks(
                        composed_image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

                # 左手の描画
                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        composed_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                # 右手の描画
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        composed_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                # フレームレートと国名を表示
                cv2.putText(composed_image, f"Country: {country}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                cv2.imshow('Country Background Holistic', composed_image)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESCで終了
                    break
                elif key == ord('c'):  # 'c'キーで国を変更
                    country = input("新しい背景にする国名を入力してください: ")
                    background = set_country_background(country)

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
