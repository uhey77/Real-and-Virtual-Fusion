# type: ignore
import cv2
import mediapipe as mp
import os
import numpy as np
import time

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

# 描画用の変数
canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # 描画用キャンバス
drawing_color = (0, 0, 255)  # 赤色で描画
drawing_thickness = 2
is_drawing = False
drawing_mode = False  # 描画モードのフラグ
last_point = None
drawings = []  # 保存された描画のリスト
current_drawing = []  # 現在の描画パス

# アニメキャラクター関連の変数
character_image = None
has_character = False
character_parts = {}  # 体のパーツごとの画像を格納する辞書


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


# アニメキャラクター画像を読み込む関数
def load_character_image(character_name):
    """指定したキャラクター画像を読み込む関数"""
    # characters フォルダがない場合は作成
    if not os.path.exists("characters"):
        os.makedirs("characters")
        print("charactersフォルダを作成しました。キャラクター画像を入れてください。")
        return None, False

    # キャラクター画像のパスを指定
    char_path = f"characters/{character_name.lower()}.png"  # 透過PNGを想定

    if os.path.exists(char_path):
        img = cv2.imread(char_path, cv2.IMREAD_UNCHANGED)  # アルファチャンネルも読み込む

        # アルファチャンネルがある場合
        if img.shape[2] == 4:
            # アルファチャンネルを分離
            alpha = img[:, :, 3]
            # BGRチャンネルのみの画像を作成
            rgb = img[:, :, :3]
            # アルファチャンネルをマスクとして使用
            mask = alpha / 255.0
            mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
            return rgb, mask, True
        else:
            return img, None, True
    else:
        print(f"キャラクター画像 {char_path} が見つかりません。")
        return None, None, False


# キャラクターパーツを読み込む関数
def load_character_parts():
    """キャラクターの体のパーツごとの画像を読み込む関数"""
    parts = {}
    parts_folder = "character_parts"

    # フォルダがない場合は作成
    if not os.path.exists(parts_folder):
        os.makedirs(parts_folder)
        print(f"{parts_folder}フォルダを作成しました。キャラクターのパーツ画像を入れてください。")
        print("例: head.png, body.png, right_arm.png, left_arm.png, right_leg.png, left_leg.png")
        return {}

    # 各パーツの画像を読み込む
    part_names = ["head", "body", "right_arm", "left_arm", "right_leg", "left_leg"]

    for part in part_names:
        part_path = f"{parts_folder}/{character_name}{part}.png"
        if os.path.exists(part_path):
            img = cv2.imread(part_path, cv2.IMREAD_UNCHANGED)  # アルファチャンネルも読み込む

            # アルファチャンネルがある場合
            if img.shape[2] == 4:
                # アルファチャンネルを分離
                alpha = img[:, :, 3]
                # BGRチャンネルのみの画像を作成
                rgb = img[:, :, :3]
                # アルファチャンネルをマスクとして使用
                mask = alpha / 255.0
                mask = np.repeat(mask[:, :, np.newaxis], 3, axis=2)
                parts[part] = {"image": rgb, "mask": mask}
            else:
                parts[part] = {"image": img, "mask": None}

            print(f"{part} 画像を読み込みました。")

    if not parts:
        print("パーツ画像が見つかりませんでした。")

    return parts


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


# マウスコールバック関数（描画モード用）
def draw_on_canvas(event, x, y, flags, param):
    global is_drawing, last_point, canvas, current_drawing

    if drawing_mode:
        if event == cv2.EVENT_LBUTTONDOWN:
            # 描画開始
            is_drawing = True
            last_point = (x, y)
            current_drawing = [(x, y)]  # 新しい描画パスを開始

        elif event == cv2.EVENT_MOUSEMOVE and is_drawing:
            # 描画中
            if last_point is not None:
                cv2.line(canvas, last_point, (x, y), drawing_color, drawing_thickness)
                last_point = (x, y)
                current_drawing.append((x, y))  # 現在の描画パスに点を追加

        elif event == cv2.EVENT_LBUTTONUP:
            # 描画終了
            is_drawing = False
            if len(current_drawing) > 1:
                drawings.append(current_drawing.copy())  # 完成した描画パスを保存
                current_drawing = []


# 骨格の関節点を取得する関数
def get_joint_position(results, joint_type):
    if results.pose_landmarks:
        if joint_type == "right_wrist":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_WRIST]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_wrist":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_WRIST]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "right_elbow":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ELBOW]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_elbow":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ELBOW]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "right_shoulder":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_SHOULDER]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_shoulder":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_SHOULDER]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "right_hip":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_HIP]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_hip":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_HIP]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "right_knee":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_KNEE]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_knee":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_KNEE]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "right_ankle":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.RIGHT_ANKLE]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "left_ankle":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_ANKLE]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
        elif joint_type == "nose":
            landmark = results.pose_landmarks.landmark[mp_holistic.PoseLandmark.NOSE]
            return (int(landmark.x * frame_width), int(landmark.y * frame_height))
    return None


# キャラクターを描画する関数
def draw_character(image, results):
    global character_parts

    # パーツがない場合は処理しない
    if not character_parts:
        return image

    # 合成用の空の画像
    character_layer = np.zeros_like(image)

    # 頭部の位置を取得
    head_pos = get_joint_position(results, "nose")
    if head_pos and "head" in character_parts:
        head = character_parts["head"]
        h, w = head["image"].shape[:2]
        
        # 頭部の画像を配置する座標を計算
        x1 = max(0, head_pos[0] - w // 2)
        y1 = max(0, head_pos[1] - h // 2)
        x2 = min(image.shape[1], x1 + w)
        y2 = min(image.shape[0], y1 + h)
        
        # 画像サイズが画面からはみ出る場合は調整
        w_actual = x2 - x1
        h_actual = y2 - y1
        
        if w_actual > 0 and h_actual > 0:
            # マスクがある場合はマスクを使用して合成
            if head["mask"] is not None:
                roi = character_layer[y1:y2, x1:x2]
                mask_roi = head["mask"][:h_actual, :w_actual]
                img_roi = head["image"][:h_actual, :w_actual]
                character_layer[y1:y2, x1:x2] = roi * (1 - mask_roi) + img_roi * mask_roi
            else:
                character_layer[y1:y2, x1:x2] = head["image"][:h_actual, :w_actual]

    # 体の位置を取得（左右の肩の中間）
    left_shoulder = get_joint_position(results, "left_shoulder")
    right_shoulder = get_joint_position(results, "right_shoulder")

    if left_shoulder and right_shoulder and "body" in character_parts:
        body_x = (left_shoulder[0] + right_shoulder[0]) // 2
        body_y = (left_shoulder[1] + right_shoulder[1]) // 2

        body = character_parts["body"]
        h, w = body["image"].shape[:2]

        # 体の画像を配置する座標を計算
        x1 = max(0, body_x - w // 2)
        y1 = max(0, body_y - h // 4)  # 体の上部を肩の位置に合わせる
        x2 = min(image.shape[1], x1 + w)
        y2 = min(image.shape[0], y1 + h)

        # 画像サイズが画面からはみ出る場合は調整
        w_actual = x2 - x1
        h_actual = y2 - y1

        if w_actual > 0 and h_actual > 0:
            # マスクがある場合はマスクを使用して合成
            if body["mask"] is not None:
                roi = character_layer[y1:y2, x1:x2]
                mask_roi = body["mask"][:h_actual, :w_actual]
                img_roi = body["image"][:h_actual, :w_actual]
                character_layer[y1:y2, x1:x2] = roi * (1 - mask_roi) + img_roi * mask_roi
            else:
                character_layer[y1:y2, x1:x2] = body["image"][:h_actual, :w_actual]

    # 右腕の位置と角度を計算
    right_shoulder = get_joint_position(results, "right_shoulder")
    right_elbow = get_joint_position(results, "right_elbow")
    right_wrist = get_joint_position(results, "right_wrist")

    if right_shoulder and right_elbow and right_wrist and "right_arm" in character_parts:
        # 腕のパーツを取得
        right_arm = character_parts["right_arm"]

        # 肩から肘、肘から手首への角度を計算
        shoulder_to_elbow_angle = np.degrees(np.arctan2(right_elbow[1] - right_shoulder[1],
                                                        right_elbow[0] - right_shoulder[0]))

        # 腕の画像を回転
        h, w = right_arm["image"].shape[:2]
        center = (w // 2, h // 4)  # 腕の上部（肩側）を回転の中心に

        # 回転行列を作成
        M = cv2.getRotationMatrix2D(center, shoulder_to_elbow_angle, 1.0)

        # 画像を回転
        rotated_arm = cv2.warpAffine(right_arm["image"], M, (w, h))
        if right_arm["mask"] is not None:
            rotated_mask = cv2.warpAffine(right_arm["mask"], M, (w, h))
        else:
            rotated_mask = None

        # 腕を肩の位置に配置
        x1 = max(0, right_shoulder[0] - center[0])
        y1 = max(0, right_shoulder[1] - center[1])
        x2 = min(image.shape[1], x1 + w)
        y2 = min(image.shape[0], y1 + h)

        # 画像サイズが画面からはみ出る場合は調整
        w_actual = x2 - x1
        h_actual = y2 - y1

        if w_actual > 0 and h_actual > 0:
            # マスクがある場合はマスクを使用して合成
            if rotated_mask is not None:
                roi = character_layer[y1:y2, x1:x2]
                mask_roi = rotated_mask[:h_actual, :w_actual]
                img_roi = rotated_arm[:h_actual, :w_actual]
                character_layer[y1:y2, x1:x2] = roi * (1 - mask_roi) + img_roi * mask_roi
            else:
                character_layer[y1:y2, x1:x2] = rotated_arm[:h_actual, :w_actual]

    # 左腕の位置と角度を計算
    left_shoulder = get_joint_position(results, "left_shoulder")
    left_elbow = get_joint_position(results, "left_elbow")
    left_wrist = get_joint_position(results, "left_wrist")

    if left_shoulder and left_elbow and left_wrist and "left_arm" in character_parts:
        # 腕のパーツを取得
        left_arm = character_parts["left_arm"]

        # 肩から肘、肘から手首への角度を計算
        shoulder_to_elbow_angle = np.degrees(np.arctan2(left_elbow[1] - left_shoulder[1], left_elbow[0] - left_shoulder[0]))

        # 腕の画像を回転
        h, w = left_arm["image"].shape[:2]
        center = (w // 2, h // 4)  # 腕の上部（肩側）を回転の中心に

        # 回転行列を作成
        M = cv2.getRotationMatrix2D(center, shoulder_to_elbow_angle, 1.0)

        # 画像を回転
        rotated_arm = cv2.warpAffine(left_arm["image"], M, (w, h))
        if left_arm["mask"] is not None:
            rotated_mask = cv2.warpAffine(left_arm["mask"], M, (w, h))
        else:
            rotated_mask = None

        # 腕を肩の位置に配置
        x1 = max(0, left_shoulder[0] - center[0])
        y1 = max(0, left_shoulder[1] - center[1])
        x2 = min(image.shape[1], x1 + w)
        y2 = min(image.shape[0], y1 + h)

        # 画像サイズが画面からはみ出る場合は調整
        w_actual = x2 - x1
        h_actual = y2 - y1
        if w_actual > 0 and h_actual > 0:
            # マスクがある場合はマスクを使用して合成
            if rotated_mask is not None:
                roi = character_layer[y1:y2, x1:x2]
                mask_roi = rotated_mask[:h_actual, :w_actual]
                img_roi = rotated_arm[:h_actual, :w_actual]
                character_layer[y1:y2, x1:x2] = roi * (1 - mask_roi) + img_roi * mask_roi
            else:
                character_layer[y1:y2, x1:x2] = rotated_arm[:h_actual, :w_actual]
    
    # 同様に右脚と左脚も配置（省略）
    
    # キャラクターレイヤーを元の画像に合成
    # キャラクターレイヤーの非ゼロの部分を抽出
    character_mask = np.any(character_layer > 0, axis=2)
    character_mask = np.repeat(character_mask[:, :, np.newaxis], 3, axis=2)
    
    # 元の画像にキャラクターを合成
    result_image = np.where(character_mask, character_layer, image)
    
    return result_image

# 描画をアニメーションさせる関数
def animate_drawings(image, results):
    # 最初の描画が存在する場合のみ処理
    if len(drawings) > 0:
        # 右手首の位置を取得
        right_wrist_pos = get_joint_position(results, "right_wrist")
        
        if right_wrist_pos:
            # 最初の描画を取得
            drawing = drawings[0]
            
            # 描画の中心を計算
            x_coords = [p[0] for p in drawing]
            y_coords = [p[1] for p in drawing]
            center_x = sum(x_coords) / len(x_coords)
            center_y = sum(y_coords) / len(y_coords)
            
            # 描画を右手首に移動（オフセットを使用）
            offset_x = right_wrist_pos[0] - center_x
            offset_y = right_wrist_pos[1] - center_y
            
            # 描画パスをアニメーション
            for i in range(1, len(drawing)):
                pt1 = (int(drawing[i-1][0] + offset_x), int(drawing[i-1][1] + offset_y))
                pt2 = (int(drawing[i][0] + offset_x), int(drawing[i][1] + offset_y))
                cv2.line(image, pt1, pt2, drawing_color, drawing_thickness)
    
    return image

def print_instructions():
    print("\n--- 操作方法 ---")
    print("ESC: 終了")
    print("c: 背景の国を変更")
    print("d: 描画モード切替")
    print("r: 描画をリセット")
    print("s: 描画を保存して骨格に関連付け")
    print("a: 全ての描画を表示/非表示")
    print("l: キャラクターを読み込む")
    print("p: キャラクターパーツを読み込む")
    print("---------------\n")

if __name__ == '__main__':
    # 使用する国を指定
    country = input("背景にする国名を入力してください (例: japan): ")
    background = set_country_background(country)
    
    # ウィンドウ名を設定
    window_name = 'Character Animation with Holistic'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, draw_on_canvas)
    
    print_instructions()
    
    # アニメーションフラグ
    animate_mode = False
    show_all_drawings = False
    character_mode = False
    
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

                # MediaPipeで骨格検出
                results = holistic.process(image)

                image.flags.writeable = True
                annotated_image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # 背景と人物を合成
                composed_image = compose_background(annotated_image, background, results)
                
                # 描画モードの場合、キャンバスを表示
                if drawing_mode:
                    # キャンバスと画像を合成
                    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) > 0
                    mask = np.stack([mask] * 3, axis=2)
                    composed_image = np.where(mask, canvas, composed_image)
                
                # アニメーションモードの場合、描画を骨格に合わせて動かす
                if animate_mode:
                    composed_image = animate_drawings(composed_image, results)
                
                # 全ての描画を表示
                if show_all_drawings and not drawing_mode:
                    # キャンバスと画像を合成
                    mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) > 0
                    mask = np.stack([mask] * 3, axis=2)
                    composed_image = np.where(mask, canvas, composed_image)
                
                # キャラクターモードの場合、キャラクターを表示
                if character_mode:
                    composed_image = draw_character(composed_image, results)

                # 姿勢の描画（デバッグ用）
                if results.pose_landmarks and not character_mode:
                    mp_drawing.draw_landmarks(
                        composed_image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)

                # モード情報を表示
                mode_text = "描画モード: オン" if drawing_mode else "描画モード: オフ"
                anim_text = "アニメーション: オン" if animate_mode else "アニメーション: オフ"
                char_text = "キャラクターモード: オン" if character_mode else "キャラクターモード: オフ"
                
                cv2.putText(composed_image, mode_text, (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(composed_image, anim_text, (10, 90),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(composed_image, char_text, (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # フレームレートと国名を表示
                cv2.putText(composed_image, f"Country: {country}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # 説明テキスト
                if drawing_mode:
                    cv2.putText(composed_image, "マウスで描画してください", (10, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                cv2.imshow(window_name, composed_image)

                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESCで終了
                    break
                elif key == ord('c'):  # 'c'キーで国を変更
                    country = input("新しい背景にする国名を入力してください: ")
                    background = set_country_background(country)
                elif key == ord('d'):  # 'd'キーで描画モード切替
                    drawing_mode = not drawing_mode
                    animate_mode = False  # 描画モードになったらアニメーションは無効
                    print(f"描画モード: {'オン' if drawing_mode else 'オフ'}")
                elif key == ord('r'):  # 'r'キーで描画リセット
                    canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
                    drawings = []
                    current_drawing = []
                    print("描画をリセットしました。")
                elif key == ord('s'):  # 's'キーで描画を保存して骨格に関連付け
                    if len(drawings) > 0:
                        animate_mode = True
                        drawing_mode = False
                        print("描画を保存し、骨格アニメーションを開始しました。")
                    else:
                        print("描画が保存されていません。まず何か描いてください。")
                elif key == ord('a'):  # 'a'キーで全描画表示/非表示
                    show_all_drawings = not show_all_drawings
                    print(f"全ての描画: {'表示' if show_all_drawings else '非表示'}")
                elif key == ord('l'):  # 'l'キーでキャラクター読み込み
                    character_name = input("読み込むキャラクター名を入力してください: ")
                    character_image, character_mask, has_character = load_character_image(character_name)
                    if has_character:
                        character_mode = True
                        print(f"キャラクター {character_name} を読み込みました。")
                    else:
                        print("キャラクターを読み込めませんでした。")
                elif key == ord('p'):  # 'p'キーでキャラクターパーツ読み込み
                    character_parts = load_character_parts()
                    if character_parts:
                        character_mode = True
                        print("キャラクターパーツを読み込みました。")
                    else:
                        print("キャラクターパーツを読み込めませんでした。")
                elif key == ord('h'):  # 'h'キーでヘルプ表示
                    print_instructions()

        finally:
            video_capture.release()
            cv2.destroyAllWindows()
