import json

import hgtk

import config

# 例: 삼겹살（サムギョプサル）
# 例: 딸기（タルギ、いちご） 濃音あり
# 例: 꽁치（コンチ、サンマ） 濃音あり
# 例: 쌍둥이（サンドゥンイ、双子） 濃音あり
# 例: 회사（フェサ、会社） 合成母音あり
# 例: 과일（クァイル、果物） 合成母音あり
# 例: 외식（ウェシク、外食） 合成母音あり・例外あり

input_text = input("Enter the text: ").strip().replace(" ", "")


all_result = []

for i, char in enumerate(input_text):
    decomposed = hgtk.letter.decompose(char)
    decomposed_list = list(decomposed)

    # ネスト構造の結果を作成
    result = {
        "character": char,
        "components": {"子音": {}, "母音": {}, "パッチム": {}},
    }
    # 子音、母音、パッチム
    consonant, vowel, patchum = decomposed_list

    # 子音の分析（ネスト構造）
    # 子音の濃音の場合は、詳細情報を追加
    strong_consonant = config.strong_consonant_read_dict.get(consonant)
    if strong_consonant:
        consonant_info = {
            "symbol": consonant,
            "note": "濃音",
            "reading": strong_consonant[0],
            "base": {
                "symbol": strong_consonant[1],
                "reading": config.consonant_read_dict[strong_consonant[1]],
            },
        }
    elif consonant == "ㅇ" and i > 0:
        # 直前のパッチムを取得
        before_decomposed = hgtk.letter.decompose(input_text[i - 1])
        before_decomposed_list = list(before_decomposed)
        _, _, before_patchum = before_decomposed_list

        # 直前のパッチムの読みを取得
        reading = config.consonant_read_dict.get(before_patchum)
        if reading is None:
            reading = config.strong_consonant_read_dict.get(before_patchum)

        consonant_info = {
            "symbol": consonant,
            "reading": "",
            "before_patchum": {
                "symbol": before_patchum,
                "reading": reading,
            },
        }
    else:
        consonant_info = {
            "symbol": consonant,
            "reading": config.consonant_read_dict[consonant],
        }
    result["components"]["子音"] = consonant_info

    # 母音の分析（ネスト構造）
    vowel_info = {
        "symbol": vowel,
    }
    # 合成母音の場合は2つの母音を分析
    diphthong = config.diphthong_read_dict.get(vowel)
    if diphthong:
        vowel_info["components"] = [
            {
                "symbol": diphthong["symbol"][0],
                "reading": config.vowel_read_dict[diphthong["symbol"][0]],
            },
            {
                "symbol": diphthong["symbol"][1],
                "reading": config.vowel_read_dict[diphthong["symbol"][1]],
            },
        ]
        vowel_info["combined_reading"] = diphthong["reading"]
        vowel_info["note"] = "合成母音"
        if "note" in diphthong:
            vowel_info["note"] += f" ※{diphthong.get('note', '')}"
    else:
        vowel_info["reading"] = config.vowel_read_dict[vowel]
    result["components"]["母音"] = vowel_info

    # パッチムの分析（ネスト構造）
    if patchum:
        patchum_info = {
            "symbol": patchum,
            "reading": config.patchum_read_dict.get(patchum, ""),
        }
        result["components"]["パッチム"] = patchum_info

    all_result.append(result)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(all_result, f, ensure_ascii=False, indent=4)
