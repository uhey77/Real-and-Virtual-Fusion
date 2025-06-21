# config.py
# 設定パラメータの集約

# 姿勢検出の設定
POSE_DETECTION_CONFIG = {
    "min_detection_confidence": 0.5,
    "min_tracking_confidence": 0.5
}

# スムージングの設定
SMOOTHING_CONFIG = {
    "max_history": 15,
    "default_smoothing_factor": 0.8,
    "min_smoothing_factor": 0.0,
    "max_smoothing_factor": 0.95,
    "smoothing_step": 0.05
}

# UI設定
UI_CONFIG = {
    "window_name": "ポーズアニメーション",
    "thumbnail_width": 160,
    "thumbnail_height": 120
}

# カメラ設定
CAMERA_CONFIG = {
    "device_id": 0,
    "width": 640,
    "height": 480
}
