import os
import re
from pydub import AudioSegment

# 入力フォルダ
input_folder = "/Users/インプットするファイルが格納されたフォルダを指定"
output_file = os.path.join(input_folder, "combined_audio.mp3")  # フルパスで保存

# 無音の設定（元に戻す）
silence_1s = AudioSegment.silent(duration=1000)  # 1秒
silence_2s = AudioSegment.silent(duration=2000)  # 2秒
silence_2_5s = AudioSegment.silent(duration=2500)  # 2.5秒

# フォルダの存在確認
if not os.path.exists(input_folder):
    print(f"❌ エラー: 指定したフォルダ '{input_folder}' が存在しません。")
    exit(1)

# 数値を抽出してソートする関数
def extract_number(filename):
    match = re.search(r"HSK4_(\d+)", filename)
    return int(match.group(1)) if match else float('inf')

# フォルダ内のMP3ファイルを取得
all_files = [f for f in os.listdir(input_folder) if f.endswith(".mp3")]

# HSK4_xxx.mp3 のみを取得（HSK4_jxxx.mp3 を除外）
hsk_files = sorted(
    [f for f in all_files if re.match(r"HSK4_\d+\.mp3$", f) and not f.startswith("HSK4_j")],
    key=extract_number
)

# scroll.mp3 と pon.mp3 の確認
scroll_file = os.path.join(input_folder, "scroll.mp3")
pon_file = os.path.join(input_folder, "pon.mp3")

scroll_audio = AudioSegment.from_mp3(scroll_file) if os.path.exists(scroll_file) else AudioSegment.silent(duration=0)
pon_audio = AudioSegment.from_mp3(pon_file) if os.path.exists(pon_file) else AudioSegment.silent(duration=0)

# 結合する音声データ
combined_audio = AudioSegment.silent(duration=1000)  # 1秒の無音で開始

# 各 HSK4_xxx について対応する日本語訳 HSK4_jxxx を探す
for file in hsk_files:
    num = extract_number(file)
    hsk_j = f"HSK4_j{num:03}.mp3"  # ゼロ埋めして3桁にする

    # HSK4_xxx（元の音声）
    file_path = os.path.join(input_folder, file)
    try:
        audio_x = AudioSegment.from_mp3(file_path)
    except Exception:
        print(f"⚠️ エラー: {file_path} を読み込めませんでした。スキップします。")
        continue

    # HSK4_jxxx（日本語訳）の存在を確認
    file_j = os.path.join(input_folder, hsk_j)
    if os.path.exists(file_j):
        audio_j = AudioSegment.from_mp3(file_j)
        print(f"✅ 日本語訳ファイル '{hsk_j}' を結合します。")
    else:
        audio_j = AudioSegment.silent(duration=0)
        print(f"⚠️ 日本語訳ファイル '{hsk_j}' が見つかりません。無音でスキップします。")

    # 音声の順番通りに結合（元の設定に戻す）
    sequence = (
        audio_x + silence_2_5s +  # HSK4_xxx → 2.5秒無音
        audio_x + silence_2s +  # HSK4_xxx（もう一度） → 2秒無音
        scroll_audio + silence_2s +  # scroll.mp3 → 2秒無音
        audio_x + silence_2_5s +  # HSK4_xxx（もう一度） → 2.5秒無音
        audio_j + silence_2_5s +  # HSK4_jxxx（日本語訳） → 2.5秒無音
        audio_x + silence_2_5s +  # HSK4_xxx（もう一度） → 2.5秒無音
        pon_audio + silence_1s  # pon.mp3 → 1秒無音
    )

    # 結合
    combined_audio += sequence

# 最終的な結合音声を保存
combined_audio.export(output_file, format="mp3")
print(f"✅ 結合された音声ファイルが {output_file} に保存されました。")
