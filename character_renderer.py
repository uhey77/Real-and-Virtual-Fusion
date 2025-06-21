import cv2
import numpy as np
import math

class CharacterRenderer:
    def __init__(self):
        # カラースキームの初期化
        self.color_schemes = [
            {  # デフォルト
                'head': (204, 255, 255),  # BGR: #FFFFCC
                'body': (170, 170, 255),  # BGR: #FFAAAA
                'arms': (255, 221, 221),  # BGR: #DDDDFF
                'legs': (255, 170, 170)   # BGR: #AAAAFF
            },
            {  # カラフル
                'head': (0, 215, 255),    # BGR: #FFD700 (金)
                'body': (71, 99, 255),    # BGR: #FF6347 (トマト)
                'arms': (225, 105, 65),   # BGR: #4169E1 (青)
                'legs': (50, 205, 50)     # BGR: #32CD32 (緑)
            },
            {  # モノクロ
                'head': (224, 224, 224),  # BGR: #E0E0E0
                'body': (160, 160, 160),  # BGR: #A0A0A0
                'arms': (128, 128, 128),  # BGR: #808080
                'legs': (96, 96, 96)      # BGR: #606060
            },
            {  # ピンク系
                'head': (193, 182, 255),  # BGR: #FFB6C1
                'body': (180, 105, 255),  # BGR: #FF69B4
                'arms': (214, 112, 218),  # BGR: #DA70D6
                'legs': (211, 85, 186)    # BGR: #BA55D3
            }
        ]
        
        self.current_scheme = 0
        self.colors = self.color_schemes[self.current_scheme]
    
    def next_color_scheme(self):
        """次のカラースキームに切り替え"""
        self.current_scheme = (self.current_scheme + 1) % len(self.color_schemes)
        self.colors = self.color_schemes[self.current_scheme]
    
    def draw_character(self, canvas, landmarks, width, height):
        """キャラクターを描画"""
        # インデックスマッピング
        nose = landmarks.landmark[0]
        left_eye = landmarks.landmark[2]
        right_eye = landmarks.landmark[5]
        left_shoulder = landmarks.landmark[11]
        right_shoulder = landmarks.landmark[12]
        left_elbow = landmarks.landmark[13]
        right_elbow = landmarks.landmark[14]
        left_wrist = landmarks.landmark[15]
        right_wrist = landmarks.landmark[16]
        left_hip = landmarks.landmark[23]
        right_hip = landmarks.landmark[24]
        left_knee = landmarks.landmark[25]
        right_knee = landmarks.landmark[26]
        left_ankle = landmarks.landmark[27]
        right_ankle = landmarks.landmark[28]
        
        # 座標変換関数
        def transform_x(x):
            return int(x * width)
        
        def transform_y(y):
            return int(y * height)
        
        # 頭を描画
        head_size = max(
            int(math.sqrt(
                (transform_x(left_eye.x) - transform_x(right_eye.x))**2 +
                (transform_y(left_eye.y) - transform_y(right_eye.y))**2
            ) * 5),
            30
        )
        cv2.circle(
            canvas, 
            (transform_x(nose.x), transform_y(nose.y)), 
            head_size, 
            self.colors['head'], 
            -1
        )
        cv2.circle(
            canvas, 
            (transform_x(nose.x), transform_y(nose.y)), 
            head_size, 
            (0, 0, 0), 
            2
        )
        
        # 体を描画
        body_points = np.array([
            [transform_x(left_shoulder.x), transform_y(left_shoulder.y)],
            [transform_x(right_shoulder.x), transform_y(right_shoulder.y)],
            [transform_x(right_hip.x), transform_y(right_hip.y)],
            [transform_x(left_hip.x), transform_y(left_hip.y)]
        ], np.int32)
        cv2.fillPoly(canvas, [body_points], self.colors['body'])
        cv2.polylines(canvas, [body_points], True, (0, 0, 0), 2)
        
        # 左腕を描画（ベジェ曲線近似）
        self._draw_limb(
            canvas,
            [(transform_x(left_shoulder.x), transform_y(left_shoulder.y)),
             (transform_x(left_elbow.x), transform_y(left_elbow.y)),
             (transform_x(left_wrist.x), transform_y(left_wrist.y))],
            self.colors['arms'],
            thickness=15
        )
        
        # 右腕を描画
        self._draw_limb(
            canvas,
            [(transform_x(right_shoulder.x), transform_y(right_shoulder.y)),
             (transform_x(right_elbow.x), transform_y(right_elbow.y)),
             (transform_x(right_wrist.x), transform_y(right_wrist.y))],
            self.colors['arms'],
            thickness=15
        )
        
        # 左脚を描画
        self._draw_limb(
            canvas,
            [(transform_x(left_hip.x), transform_y(left_hip.y)),
             (transform_x(left_knee.x), transform_y(left_knee.y)),
             (transform_x(left_ankle.x), transform_y(left_ankle.y))],
            self.colors['legs'],
            thickness=20
        )
        
        # 右脚を描画
        self._draw_limb(
            canvas,
            [(transform_x(right_hip.x), transform_y(right_hip.y)),
             (transform_x(right_knee.x), transform_y(right_knee.y)),
             (transform_x(right_ankle.x), transform_y(right_ankle.y))],
            self.colors['legs'],
            thickness=20
        )
        
        # 目を描画
        cv2.circle(canvas, (transform_x(left_eye.x), transform_y(left_eye.y)), head_size//6, (0, 0, 0), -1)
        cv2.circle(canvas, (transform_x(right_eye.x), transform_y(right_eye.y)), head_size//6, (0, 0, 0), -1)
        
        # 鼻を描画
        cv2.circle(canvas, (transform_x(nose.x), transform_y(nose.y)), head_size//8, (0, 0, 255), -1)
        
        # 笑顔を描画
        smile_center = (transform_x(nose.x), transform_y(nose.y) + head_size//3)
        axes = (head_size//2, head_size//4)
        cv2.ellipse(canvas, smile_center, axes, 0, 0, 180, (0, 0, 0), 2)
    
    def _draw_limb(self, canvas, points, color, thickness=10):
        """関節を線で描画（ベジェ曲線の簡易近似）"""
        # 単純な線描画
        for i in range(len(points) - 1):
            cv2.line(canvas, points[i], points[i+1], color, thickness, cv2.LINE_AA)
        
        # 関節点に円を描画してなめらかに見せる
        for point in points[1:-1]:
            cv2.circle(canvas, point, thickness//2, color, -1)