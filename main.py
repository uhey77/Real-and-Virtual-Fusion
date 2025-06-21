import cv2
from pose_detector import PoseDetector
from character_renderer import CharacterRenderer
from pose_smoother import PoseSmoother
from ui_manager import UIManager

class PoseAnimationApp:
    def __init__(self):
        # コンポーネントの初期化
        self.pose_detector = PoseDetector()
        self.pose_smoother = PoseSmoother(max_history=15, smoothing_factor=0.8)
        self.character_renderer = CharacterRenderer()
        self.ui_manager = UIManager(window_name="Pose Animation")
        
        # カメラの初期化
        self.cap = cv2.VideoCapture(0)
        
        # アプリケーション状態
        self.running = False
    
    def initialize(self):
        """アプリケーションの初期化"""
        if not self.cap.isOpened():
            print("カメラを開けませんでした。")
            return False
        
        self.ui_manager.initialize()
        self.running = True
        return True
    
    def process_frame(self):
        """1フレームの処理"""
        # カメラからフレームを取得
        success, frame = self.cap.read()
        if not success:
            print("カメラからのフレーム取得に失敗しました。")
            return None
        
        # 画像の反転（自分を見るように）
        frame = cv2.flip(frame, 1)
        
        # ポーズ検出
        landmarks = self.pose_detector.detect_pose(frame)
        
        # スムージング適用
        if landmarks:
            smoothed_landmarks = self.pose_smoother.apply_smoothing(landmarks)
        else:
            smoothed_landmarks = None
        
        # 描画用キャンバスを作成
        height, width, _ = frame.shape
        canvas = self.ui_manager.create_canvas(width, height)
        
        # UI更新（FPS、ステータス表示など）
        self.ui_manager.update(canvas, frame, smoothed_landmarks is not None)
        
        # キャラクター描画
        if smoothed_landmarks:
            self.character_renderer.draw_character(canvas, smoothed_landmarks, width, height)
        
        return canvas
    
    def handle_key_events(self):
        """キー入力の処理"""
        key = cv2.waitKey(1) & 0xFF
        
        # ESCキーが押されたら終了
        if key == 27:
            self.running = False
            return
        
        # キー入力をUIマネージャに渡す
        command = self.ui_manager.handle_key(key)
        
        # UIマネージャからのコマンドを処理
        if command:
            if command["action"] == "smooth_up":
                self.pose_smoother.increase_smoothing()
                print(f"スムージング係数: {self.pose_smoother.smoothing_factor:.2f}")
            elif command["action"] == "smooth_down":
                self.pose_smoother.decrease_smoothing()
                print(f"スムージング係数: {self.pose_smoother.smoothing_factor:.2f}")
            elif command["action"] == "reset_history":
                self.pose_smoother.reset_history()
                print("履歴リセット")
            elif command["action"] == "change_color":
                self.character_renderer.next_color_scheme()
                print("キャラクターの色を変更しました")
    
    def run(self):
        """メインループ"""
        if not self.initialize():
            return
        
        while self.running and self.cap.isOpened():
            # フレーム処理
            canvas = self.process_frame()
            if canvas is None:
                break
            
            # 表示
            self.ui_manager.display(canvas)
            
            # キー入力処理
            self.handle_key_events()
        
        # リソース解放
        self.cleanup()
    
    def cleanup(self):
        """リソースの解放"""
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    app = PoseAnimationApp()
    app.run()