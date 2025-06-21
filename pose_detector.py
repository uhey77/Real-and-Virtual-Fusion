import cv2
import mediapipe as mp

class PoseDetector:
    def __init__(self, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        # MediaPipe Pose初期化
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence)
    
    def detect_pose(self, image):
        """画像から姿勢を検出し、ランドマークを返す"""
        # MediaPipeの処理のためBGR→RGB変換
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)
        
        # ポーズが検出されたなら
        if results.pose_landmarks:
            return results.pose_landmarks
        
        return None
    
    def get_landmark_positions(self, landmarks, image_width, image_height):
        """ランドマークの座標を抽出"""
        positions = {}
        
        # MediaPipe Poseランドマークのマッピング
        landmark_indices = {
            "nose": 0,
            "left_eye": 2,
            "right_eye": 5,
            "left_ear": 7,
            "right_ear": 8,
            "left_shoulder": 11,
            "right_shoulder": 12,
            "left_elbow": 13,
            "right_elbow": 14,
            "left_wrist": 15,
            "right_wrist": 16,
            "left_hip": 23,
            "right_hip": 24,
            "left_knee": 25,
            "right_knee": 26,
            "left_ankle": 27,
            "right_ankle": 28
        }
        
        for name, idx in landmark_indices.items():
            landmark = landmarks.landmark[idx]
            positions[name] = {
                "x": int(landmark.x * image_width),
                "y": int(landmark.y * image_height),
                "visibility": landmark.visibility
            }
        
        return positions