# type: ignore
import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
mp_face_mesh = mp.solutions.face_mesh

camera_no = 0
video_capture = cv2.VideoCapture(camera_no)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)

if __name__ == '__main__':
    with mp_holistic.Holistic(
        static_image_mode=False,
        model_complexity=1,
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

                # 姿勢の描画
                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

                # 顔の描画
                if results.face_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_image, results.face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)

                # 左手の描画
                if results.left_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                # 右手の描画
                if results.right_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                cv2.imshow('Holistic', annotated_image)

                if cv2.waitKey(1) & 0xFF == 27:  # ESCで終了
                    break

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
