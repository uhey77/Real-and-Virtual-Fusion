# ui_manager.py
# UI表示と入力処理
import cv2
import numpy as np
from datetime import datetime

class UIManager:
    def __init__(self, window_name="Pose Animation"):
        self.window_name = window_name
        self.prev_frame_time = 0
        self.current_frame_time = 0
        
        # キーマッピング
        self.key_commands = {
            ord('s'): {"action": "smooth_up"},
            ord('d'): {"action": "smooth_down"},
            ord('r'): {"action": "reset_history"},
            ord('c'): {"action": "change_color"}
        }
    
    def initialize(self):
        """UIの初期化"""
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        return True
    
    def create_canvas(self, width, height):
        """描画用キャンバスの作成"""
        return np.zeros((height, width, 3), dtype=np.uint8)
    
    def update(self, canvas, video_frame, pose_detected):
        """UIの更新処理"""
        # フレームレート計算
        self.current_frame_time = datetime.now().timestamp()
        fps = 1 / (self.current_frame_time - self.prev_frame_time) if self.prev_frame_time > 0 else 0
        self.prev_frame_time = self.current_frame_time
        
        # FPS表示
        cv2.putText(
            canvas, 
            f"FPS: {int(fps)}", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (255, 255, 255), 
            2
        )
        
        # ポーズ検出状態の表示
        if pose_detected:
            cv2.putText(
                canvas,
                "ポーズ検出中",
                (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )
        else:
            height, width, _ = canvas.shape
            cv2.putText(
                canvas,
                "ポーズが検出されていません",
                (width // 4, height // 2),
                cv2.FONT_HERSHEY_SIMPLEX,
                1.5,
                (0, 0, 255),
                2
            )
        
        # デバッグ用のサムネイル表示
        self.add_thumbnail(canvas, video_frame)
        
        # 操作方法の表示
        self.add_control_help(canvas)
    
    def add_thumbnail(self, canvas, frame, width=160, height=120):
        """サムネイルの表示"""
        h, w, _ = canvas.shape
        thumbnail = cv2.resize(frame, (width, height))
        canvas[10:10+height, w-10-width:w-10] = thumbnail
    
    def add_control_help(self, canvas):
        """操作方法のヘルプ表示"""
        h, w, _ = canvas.shape
        controls = [
            "操作方法:",
            "S: スムージング強度アップ",
            "D: スムージング強度ダウン",
            "R: 履歴リセット",
            "C: キャラクター色変更",
            "ESC: 終了"
        ]
        
        y_pos = h - 150
        for text in controls:
            cv2.putText(
                canvas,
                text,
                (10, y_pos),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (200, 200, 200),
                1,
                cv2.LINE_AA
            )
            y_pos += 25
    
    def display(self, canvas):
        """キャンバスの表示"""
        cv2.imshow(self.window_name, canvas)
    
    def handle_key(self, key):
        """キー入力の処理"""
        if key in self.key_commands:
            return self.key_commands[key]
        return None
