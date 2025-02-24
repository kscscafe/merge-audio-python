import os
import re
from pydub import AudioSegment

# 入力フォルダ
input_folder = "/Users/インプットするファイルが格納されたフォルダを指定"
output_file = "combined_audio_mix.mp3"

# 無音の設定
silence_short = AudioSegment.silent(duration=500)  # 0.5秒
silence_long = AudioSegment.silent(duration=1000)  # 1秒

# 数値を抽出してソートする関数
def extract_number(filename):
    match = re.search(r"HSK4_(\d+)", filename)
    return int(match.group(1)) if match else float('inf')

# フォルダ内のMP3ファイルを取得（HSK4_x のみ対象）
all_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]
hsk_files = sorted([f for f in all_files if re.match(r"HSK4_\d+.mp3", f)], key=extract_number)

# 結合する音声データ
combined_audio = AudioSegment.silent(duration=1000)  # 1秒の無音で開始

# 各 HSK4_x について処理
for file in hsk_files:
    num = extract_number(file)
    
    # HSK4_x（元の音声）
    file_path = os.path.join(input_folder, file)
    audio_x = AudioSegment.from_mp3(file_path)

    # HSK4_x の 0.9倍速バージョン
    audio_x_slow = audio_x._spawn(audio_x.raw_data, overrides={
        "frame_rate": int(audio_x.frame_rate * 0.9)
    }).set_frame_rate(audio_x.frame_rate)

    # 音声の順番通りに結合
    sequence = (
        audio_x + silence_short +  # HSK4_x → 0.5秒無音
        audio_x + silence_short +  # HSK4_x → 0.5秒無音
        audio_x_slow + silence_short +  # HSK4_x 0.9倍速 → 0.5秒無音
        audio_x + silence_long  # HSK4_x → 1秒無音
    )
    
    # 結合
    combined_audio += sequence

# 保存
combined_audio.export(output_file, format="mp3")
print(f"✅ 結合された音声ファイルが {output_file} に保存されました。")
