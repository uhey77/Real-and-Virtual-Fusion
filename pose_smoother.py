# pose_smoother.py
# ポーズのスムージング処理
import copy

class PoseSmoother:
    def __init__(self, max_history=15, smoothing_factor=0.8):
        # スムージング用の過去ポーズ記録
        self.pose_history = []
        self.max_history = max_history
        self.smoothing_factor = smoothing_factor
    
    def reset_history(self):
        """履歴をリセット"""
        self.pose_history = []
    
    def increase_smoothing(self, step=0.05):
        """スムージング係数を上げる"""
        self.smoothing_factor = min(0.95, self.smoothing_factor + step)
    
    def decrease_smoothing(self, step=0.05):
        """スムージング係数を下げる"""
        self.smoothing_factor = max(0.0, self.smoothing_factor - step)
    
    def apply_smoothing(self, landmarks):
        """加重移動平均スムージングを適用"""
        # ランドマークのディープコピーを作成
        smoothed_landmarks = copy.deepcopy(landmarks)
        
        # 現在のランドマークを一時的なリストに変換
        current_pose = []
        for landmark in landmarks.landmark:
            current_pose.append({
                'x': landmark.x,
                'y': landmark.y,
                'z': landmark.z,
                'visibility': landmark.visibility
            })
        
        # 履歴に追加
        self.pose_history.append(current_pose)
        
        # 履歴が長すぎる場合は古いものを削除
        if len(self.pose_history) > self.max_history:
            self.pose_history.pop(0)
        
        # 履歴が不足している場合は現在のポーズを返す
        if len(self.pose_history) < 3:
            return landmarks
        
        # 各ランドマークに対して加重平均を計算
        for i in range(len(landmarks.landmark)):
            sumX = 0
            sumY = 0
            sumZ = 0
            total_weight = 0
            
            # 過去のフレームに対して加重平均を計算
            for j, frame in enumerate(self.pose_history):
                # 三角重み付け（最新のデータほど重み大）
                weight = (j + 1) / len(self.pose_history)
                
                sumX += frame[i]['x'] * weight
                sumY += frame[i]['y'] * weight
                sumZ += frame[i]['z'] * weight
                total_weight += weight
            
            # 重み付け平均を計算
            avgX = sumX / total_weight
            avgY = sumY / total_weight
            avgZ = sumZ / total_weight
            
            # スムージングを適用
            smoothed_landmarks.landmark[i].x = landmarks.landmark[i].x * (1 - self.smoothing_factor) + avgX * self.smoothing_factor
            smoothed_landmarks.landmark[i].y = landmarks.landmark[i].y * (1 - self.smoothing_factor) + avgY * self.smoothing_factor
            smoothed_landmarks.landmark[i].z = landmarks.landmark[i].z * (1 - self.smoothing_factor) + avgZ * self.smoothing_factor
        
        return smoothed_landmarks
