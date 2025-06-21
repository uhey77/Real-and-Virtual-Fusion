import xml.etree.ElementTree as ET
import random

def create_improved_svg():
    """改良版のPose Animator SVGを作成"""
    svg_content = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 800" width="600" height="800">
  <!-- 背景 -->
  <rect width="100%" height="100%" fill="#f0f0f0" />
  
  <!-- キャラクターの体 -->
  <g id="character">
    <!-- 胴体 -->
    <path id="bodyPath" d="M270,220 C270,200 330,200 330,220 L330,400 C330,420 270,420 270,400 Z" fill="#ffaaaa" stroke="#000000" stroke-width="2" />
    
    <!-- 頭 -->
    <circle id="headCircle" cx="300" cy="150" r="60" fill="#ffffcc" stroke="#000000" stroke-width="2" />
    <ellipse id="face" cx="300" cy="150" rx="40" ry="45" fill="#ffffee" />
    
    <!-- 目 -->
    <ellipse id="leftEyeShape" cx="285" cy="140" rx="8" ry="12" fill="white" stroke="#000000" stroke-width="1" />
    <circle id="leftPupil" cx="285" cy="140" r="4" fill="#000000" />
    
    <ellipse id="rightEyeShape" cx="315" cy="140" rx="8" ry="12" fill="white" stroke="#000000" stroke-width="1" />
    <circle id="rightPupil" cx="315" cy="140" r="4" fill="#000000" />
    
    <!-- 口 -->
    <path id="mouthPath" d="M285,170 C295,180 305,180 315,170" fill="none" stroke="#000000" stroke-width="2" />
    
    <!-- 左腕 -->
    <path id="leftArmPath" d="M270,220 L180,300 L160,380" stroke="#000000" stroke-width="2" fill="#ffffcc" />
    
    <!-- 右腕 -->
    <path id="rightArmPath" d="M330,220 L420,300 L440,380" stroke="#000000" stroke-width="2" fill="#ffffcc" />
    
    <!-- 左脚 -->
    <path id="leftLegPath" d="M270,400 L250,550 L240,680" stroke="#000000" stroke-width="2" fill="#aaaaff" />
    
    <!-- 右脚 -->
    <path id="rightLegPath" d="M330,400 L350,550 L360,680" stroke="#000000" stroke-width="2" fill="#aaaaff" />
  </g>
  
  <!-- 関節点（実際にPose Animatorで利用される）-->
  <g id="joints" fill="red" stroke="none">
    <circle id="nose" cx="300" cy="130" r="5" />
    <circle id="leftEye" cx="285" cy="140" r="5" />
    <circle id="rightEye" cx="315" cy="140" r="5" />
    <circle id="leftEar" cx="270" cy="150" r="5" />
    <circle id="rightEar" cx="330" cy="150" r="5" />
    
    <circle id="leftShoulder" cx="230" cy="220" r="5" />
    <circle id="rightShoulder" cx="370" cy="220" r="5" />
    <circle id="leftElbow" cx="180" cy="300" r="5" />
    <circle id="rightElbow" cx="420" cy="300" r="5" />
    <circle id="leftWrist" cx="160" cy="380" r="5" />
    <circle id="rightWrist" cx="440" cy="380" r="5" />
    
    <circle id="leftHip" cx="270" cy="400" r="5" />
    <circle id="rightHip" cx="330" cy="400" r="5" />
    <circle id="leftKnee" cx="250" cy="550" r="5" />
    <circle id="rightKnee" cx="350" cy="550" r="5" />
    <circle id="leftAnkle" cx="240" cy="680" r="5" />
    <circle id="rightAnkle" cx="360" cy="680" r="5" />
  </g>
</svg>
"""
    return svg_content

def save_svg(svg_str, filename):
    """SVG文字列をファイルに保存"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_str)
    print(f"SVGファイルを保存しました: {filename}")

# 実行
improved_svg = create_improved_svg()
save_svg(improved_svg, "character-simplified.svg")
print("シンプル化したキャラクターSVGを作成しました。")
