# merge-audio-python


combine_audio_mix.pyは、次の順番で音声が繰り返されます。\n
	1.	1秒の無音
	2.	HSK4_1 の音声
	3.	0.5秒の無音
	4.	HSK4_1 の音声（2回目）
	5.	0.5秒の無音
	6.	HSK4_1 の 0.9倍速バージョン
	7.	0.5秒の無音
	8.	HSK4_1 の音声（3回目）
	9.	1秒の無音
	10.	HSK4_2 の音声
	11.	0.5秒の無音
	12.	HSK4_2 の音声（2回目）
	13.	0.5秒の無音
	14.	HSK4_2 の 0.9倍速バージョン
	15.	0.5秒の無音
	16.	HSK4_2 の音声（3回目）
	17.	1秒の無音
	18.	HSK4_3 の音声
	19.	…（以降、同様のパターンが続く）



combine_audio_hsk4_j.pyは以下の順番で音声が繰り返される。
  •	HSK4_xxx.mp3 → 2.5秒無音
	•	HSK4_xxx.mp3（もう一度）→ 2秒無音
	•	scroll.mp3 → 2秒無音
	•	HSK4_xxx.mp3（もう一度）→ 2.5秒無音
	•	HSK4_jxxx.mp3（日本語訳）→ 2.5秒無音
	•	HSK4_xxx.mp3（もう一度）→ 2.5秒無音
	•	pon.mp3 → 1秒無音
