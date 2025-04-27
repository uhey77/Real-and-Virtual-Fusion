import xml.etree.ElementTree as ET
import random

def create_pose_animator_svg():
    # SVG要素の作成
    svg = ET.Element('svg')
    svg.set('xmlns', 'http://www.w3.org/2000/svg')
    svg.set('viewBox', '0 0 600 800')
    svg.set('width', '600')
    svg.set('height', '800')
    
    # 背景
    background = ET.SubElement(svg, 'rect')
    background.set('width', '100%')
    background.set('height', '100%')
    background.set('fill', '#f0f0f0')
    
    # スケルトン構造（関節点とその接続を定義）
    skeleton = ET.SubElement(svg, 'g')
    skeleton.set('id', 'skeleton')
    skeleton.set('stroke', '#888888')
    skeleton.set('stroke-width', '2')
    skeleton.set('fill', 'none')
    
    # 胴体のライン
    spine = ET.SubElement(skeleton, 'line')
    spine.set('id', 'spine')
    spine.set('x1', '300')
    spine.set('y1', '200')
    spine.set('x2', '300')
    spine.set('y2', '400')
    
    left_shoulder_line = ET.SubElement(skeleton, 'line')
    left_shoulder_line.set('id', 'leftShoulderLine')
    left_shoulder_line.set('x1', '300')
    left_shoulder_line.set('y1', '220')
    left_shoulder_line.set('x2', '230')
    left_shoulder_line.set('y2', '220')
    
    right_shoulder_line = ET.SubElement(skeleton, 'line')
    right_shoulder_line.set('id', 'rightShoulderLine')
    right_shoulder_line.set('x1', '300')
    right_shoulder_line.set('y1', '220')
    right_shoulder_line.set('x2', '370')
    right_shoulder_line.set('y2', '220')
    
    left_hip_line = ET.SubElement(skeleton, 'line')
    left_hip_line.set('id', 'leftHipLine')
    left_hip_line.set('x1', '300')
    left_hip_line.set('y1', '400')
    left_hip_line.set('x2', '270')
    left_hip_line.set('y2', '400')
    
    right_hip_line = ET.SubElement(skeleton, 'line')
    right_hip_line.set('id', 'rightHipLine')
    right_hip_line.set('x1', '300')
    right_hip_line.set('y1', '400')
    right_hip_line.set('x2', '330')
    right_hip_line.set('y2', '400')
    
    # 左腕のライン
    left_upper_arm_line = ET.SubElement(skeleton, 'line')
    left_upper_arm_line.set('id', 'leftUpperArmLine')
    left_upper_arm_line.set('x1', '230')
    left_upper_arm_line.set('y1', '220')
    left_upper_arm_line.set('x2', '180')
    left_upper_arm_line.set('y2', '300')
    
    left_lower_arm_line = ET.SubElement(skeleton, 'line')
    left_lower_arm_line.set('id', 'leftLowerArmLine')
    left_lower_arm_line.set('x1', '180')
    left_lower_arm_line.set('y1', '300')
    left_lower_arm_line.set('x2', '160')
    left_lower_arm_line.set('y2', '380')
    
    # 右腕のライン
    right_upper_arm_line = ET.SubElement(skeleton, 'line')
    right_upper_arm_line.set('id', 'rightUpperArmLine')
    right_upper_arm_line.set('x1', '370')
    right_upper_arm_line.set('y1', '220')
    right_upper_arm_line.set('x2', '420')
    right_upper_arm_line.set('y2', '300')
    
    right_lower_arm_line = ET.SubElement(skeleton, 'line')
    right_lower_arm_line.set('id', 'rightLowerArmLine')
    right_lower_arm_line.set('x1', '420')
    right_lower_arm_line.set('y1', '300')
    right_lower_arm_line.set('x2', '440')
    right_lower_arm_line.set('y2', '380')
    
    # 左脚のライン
    left_upper_leg_line = ET.SubElement(skeleton, 'line')
    left_upper_leg_line.set('id', 'leftUpperLegLine')
    left_upper_leg_line.set('x1', '270')
    left_upper_leg_line.set('y1', '400')
    left_upper_leg_line.set('x2', '250')
    left_upper_leg_line.set('y2', '550')
    
    left_lower_leg_line = ET.SubElement(skeleton, 'line')
    left_lower_leg_line.set('id', 'leftLowerLegLine')
    left_lower_leg_line.set('x1', '250')
    left_lower_leg_line.set('y1', '550')
    left_lower_leg_line.set('x2', '240')
    left_lower_leg_line.set('y2', '680')
    
    # 右脚のライン
    right_upper_leg_line = ET.SubElement(skeleton, 'line')
    right_upper_leg_line.set('id', 'rightUpperLegLine')
    right_upper_leg_line.set('x1', '330')
    right_upper_leg_line.set('y1', '400')
    right_upper_leg_line.set('x2', '350')
    right_upper_leg_line.set('y2', '550')
    
    right_lower_leg_line = ET.SubElement(skeleton, 'line')
    right_lower_leg_line.set('id', 'rightLowerLegLine')
    right_lower_leg_line.set('x1', '350')
    right_lower_leg_line.set('y1', '550')
    right_lower_leg_line.set('x2', '360')
    right_lower_leg_line.set('y2', '680')
    
    # キャラクターの体
    character = ET.SubElement(svg, 'g')
    character.set('id', 'character')
    
    # 胴体
    body = ET.SubElement(character, 'path')
    body.set('id', 'body')
    body.set('d', 'M270,220 C270,200 330,200 330,220 L330,400 C330,420 270,420 270,400 Z')
    body.set('fill', '#ffaaaa')
    body.set('stroke', '#000000')
    body.set('stroke-width', '2')
    
    # 頭
    head = ET.SubElement(character, 'circle')
    head.set('id', 'head')
    head.set('cx', '300')
    head.set('cy', '150')
    head.set('r', '60')
    head.set('fill', '#ffffcc')
    head.set('stroke', '#000000')
    head.set('stroke-width', '2')
    
    face = ET.SubElement(character, 'ellipse')
    face.set('id', 'face')
    face.set('cx', '300')
    face.set('cy', '150')
    face.set('rx', '40')
    face.set('ry', '45')
    face.set('fill', '#ffffee')
    
    # 目
    left_eye_shape = ET.SubElement(character, 'ellipse')
    left_eye_shape.set('id', 'leftEyeShape')
    left_eye_shape.set('cx', '285')
    left_eye_shape.set('cy', '140')
    left_eye_shape.set('rx', '8')
    left_eye_shape.set('ry', '12')
    left_eye_shape.set('fill', 'white')
    left_eye_shape.set('stroke', '#000000')
    left_eye_shape.set('stroke-width', '1')
    
    left_pupil = ET.SubElement(character, 'circle')
    left_pupil.set('id', 'leftPupil')
    left_pupil.set('cx', '285')
    left_pupil.set('cy', '140')
    left_pupil.set('r', '4')
    left_pupil.set('fill', '#000000')
    
    right_eye_shape = ET.SubElement(character, 'ellipse')
    right_eye_shape.set('id', 'rightEyeShape')
    right_eye_shape.set('cx', '315')
    right_eye_shape.set('cy', '140')
    right_eye_shape.set('rx', '8')
    right_eye_shape.set('ry', '12')
    right_eye_shape.set('fill', 'white')
    right_eye_shape.set('stroke', '#000000')
    right_eye_shape.set('stroke-width', '1')
    
    right_pupil = ET.SubElement(character, 'circle')
    right_pupil.set('id', 'rightPupil')
    right_pupil.set('cx', '315')
    right_pupil.set('cy', '140')
    right_pupil.set('r', '4')
    right_pupil.set('fill', '#000000')
    
    # 口
    mouth = ET.SubElement(character, 'path')
    mouth.set('id', 'mouth')
    mouth.set('d', 'M285,170 C295,180 305,180 315,170')
    mouth.set('fill', 'none')
    mouth.set('stroke', '#000000')
    mouth.set('stroke-width', '2')
    
    # 左腕
    left_arm = ET.SubElement(character, 'path')
    left_arm.set('id', 'leftArm')
    left_arm.set('d', 'M270,220 L180,300 L160,380')
    left_arm.set('stroke', '#000000')
    left_arm.set('stroke-width', '2')
    left_arm.set('fill', '#ffffcc')
    
    # 右腕
    right_arm = ET.SubElement(character, 'path')
    right_arm.set('id', 'rightArm')
    right_arm.set('d', 'M330,220 L420,300 L440,380')
    right_arm.set('stroke', '#000000')
    right_arm.set('stroke-width', '2')
    right_arm.set('fill', '#ffffcc')
    
    # 左脚
    left_leg = ET.SubElement(character, 'path')
    left_leg.set('id', 'leftLeg')
    left_leg.set('d', 'M270,400 L250,550 L240,680')
    left_leg.set('stroke', '#000000')
    left_leg.set('stroke-width', '2')
    left_leg.set('fill', '#aaaaff')
    
    # 右脚
    right_leg = ET.SubElement(character, 'path')
    right_leg.set('id', 'rightLeg')
    right_leg.set('d', 'M330,400 L350,550 L360,680')
    right_leg.set('stroke', '#000000')
    right_leg.set('stroke-width', '2')
    right_leg.set('fill', '#aaaaff')
    
    # 関節点（実際にPose Animatorで利用される）
    joints = ET.SubElement(svg, 'g')
    joints.set('id', 'joints')
    joints.set('fill', 'red')
    joints.set('stroke', 'none')
    
    # 頭部の関節点
    nose = ET.SubElement(joints, 'circle')
    nose.set('id', 'nose')
    nose.set('cx', '300')
    nose.set('cy', '130')
    nose.set('r', '3')
    
    left_eye = ET.SubElement(joints, 'circle')
    left_eye.set('id', 'leftEye')
    left_eye.set('cx', '285')
    left_eye.set('cy', '140')
    left_eye.set('r', '3')
    
    right_eye = ET.SubElement(joints, 'circle')
    right_eye.set('id', 'rightEye')
    right_eye.set('cx', '315')
    right_eye.set('cy', '140')
    right_eye.set('r', '3')
    
    left_ear = ET.SubElement(joints, 'circle')
    left_ear.set('id', 'leftEar')
    left_ear.set('cx', '270')
    left_ear.set('cy', '150')
    left_ear.set('r', '3')
    
    right_ear = ET.SubElement(joints, 'circle')
    right_ear.set('id', 'rightEar')
    right_ear.set('cx', '330')
    right_ear.set('cy', '150')
    right_ear.set('r', '3')
    
    # 上半身の関節点
    left_shoulder = ET.SubElement(joints, 'circle')
    left_shoulder.set('id', 'leftShoulder')
    left_shoulder.set('cx', '230')
    left_shoulder.set('cy', '220')
    left_shoulder.set('r', '5')
    
    right_shoulder = ET.SubElement(joints, 'circle')
    right_shoulder.set('id', 'rightShoulder')
    right_shoulder.set('cx', '370')
    right_shoulder.set('cy', '220')
    right_shoulder.set('r', '5')
    
    left_elbow = ET.SubElement(joints, 'circle')
    left_elbow.set('id', 'leftElbow')
    left_elbow.set('cx', '180')
    left_elbow.set('cy', '300')
    left_elbow.set('r', '5')
    
    right_elbow = ET.SubElement(joints, 'circle')
    right_elbow.set('id', 'rightElbow')
    right_elbow.set('cx', '420')
    right_elbow.set('cy', '300')
    right_elbow.set('r', '5')
    
    left_wrist = ET.SubElement(joints, 'circle')
    left_wrist.set('id', 'leftWrist')
    left_wrist.set('cx', '160')
    left_wrist.set('cy', '380')
    left_wrist.set('r', '5')
    
    right_wrist = ET.SubElement(joints, 'circle')
    right_wrist.set('id', 'rightWrist')
    right_wrist.set('cx', '440')
    right_wrist.set('cy', '380')
    right_wrist.set('r', '5')
    
    # 下半身の関節点
    left_hip = ET.SubElement(joints, 'circle')
    left_hip.set('id', 'leftHip')
    left_hip.set('cx', '270')
    left_hip.set('cy', '400')
    left_hip.set('r', '5')
    
    right_hip = ET.SubElement(joints, 'circle')
    right_hip.set('id', 'rightHip')
    right_hip.set('cx', '330')
    right_hip.set('cy', '400')
    right_hip.set('r', '5')
    
    left_knee = ET.SubElement(joints, 'circle')
    left_knee.set('id', 'leftKnee')
    left_knee.set('cx', '250')
    left_knee.set('cy', '550')
    left_knee.set('r', '5')
    
    right_knee = ET.SubElement(joints, 'circle')
    right_knee.set('id', 'rightKnee')
    right_knee.set('cx', '350')
    right_knee.set('cy', '550')
    right_knee.set('r', '5')
    
    left_ankle = ET.SubElement(joints, 'circle')
    left_ankle.set('id', 'leftAnkle')
    left_ankle.set('cx', '240')
    left_ankle.set('cy', '680')
    left_ankle.set('r', '5')
    
    right_ankle = ET.SubElement(joints, 'circle')
    right_ankle.set('id', 'rightAnkle')
    right_ankle.set('cx', '360')
    right_ankle.set('cy', '680')
    right_ankle.set('r', '5')
    
    # XML宣言とDOCTYPE宣言を追加
    tree = ET.ElementTree(svg)
    
    # SVGファイルに保存するため文字列に変換
    xml_str = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n'
    xml_str += ET.tostring(svg, encoding='unicode')
    
    return xml_str

def customize_character(head_color='#ffffcc', body_color='#ffaaaa', arm_color='#ffffcc', leg_color='#aaaaff'):
    """キャラクターの色をカスタマイズして新しいSVGを作成"""
    svg_str = create_pose_animator_svg()
    
    # 色を置換
    svg_str = svg_str.replace('fill="#ffffcc" stroke="#000000" stroke-width="2"', f'fill="{head_color}" stroke="#000000" stroke-width="2"')
    svg_str = svg_str.replace('fill="#ffaaaa" stroke="#000000" stroke-width="2"', f'fill="{body_color}" stroke="#000000" stroke-width="2"')
    svg_str = svg_str.replace('fill="#ffffcc"', f'fill="{arm_color}"')
    svg_str = svg_str.replace('fill="#aaaaff"', f'fill="{leg_color}"')
    
    return svg_str

def generate_random_character():
    """ランダムな色のキャラクターを作成"""
    # ランダムな色を生成
    def random_color():
        return f'#{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}'
    
    head_color = random_color()
    body_color = random_color()
    arm_color = random_color()
    leg_color = random_color()
    
    return customize_character(head_color, body_color, arm_color, leg_color)

def save_svg(svg_str, filename):
    """SVG文字列をファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_str)
    print(f"SVGファイルを保存しました: {filename}")

# メイン実行部分
if __name__ == "__main__":
    # 基本キャラクターの作成と保存
    basic_svg = create_pose_animator_svg()
    save_svg(basic_svg, "character-basic.svg")
    
    # カスタマイズしたキャラクターの作成と保存
    custom_svg = customize_character(head_color='#FFD700', body_color='#FF6347', arm_color='#FFD700', leg_color='#4169E1')
    save_svg(custom_svg, "character-custom.svg")
    
    # ランダムキャラクターの作成と保存
    random_svg = generate_random_character()
    save_svg(random_svg, "character-random.svg")
    
    print("3種類のキャラクターSVGファイルを作成しました。")