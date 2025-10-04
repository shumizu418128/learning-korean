import json

import hgtk

# 例: 삼겹살（サムギョプサル）
# 例: 딸기（タルギ、いちご） 濃音あり
# 例: 꽁치（コンチ、サンマ） 濃音あり
# 例: 쌍둥이（サンドゥンイ、双子） 濃音あり
# 例: 회사（フェサ、会社） 合成母音あり
# 例: 과일（クァイル、果物） 合成母音あり

input_text = input("Enter the text: ").strip()

# 母音
vowel_read_dict = {
    "ㅏ": "a",
    "ㅑ": "ya",
    "ㅓ": "eo (o)",
    "ㅕ": "yeo (yo)",
    "ㅗ": "o",
    "ㅛ": "yo",
    "ㅜ": "u",
    "ㅠ": "yu",
    "ㅡ": "eu (u)",
    "ㅣ": "i",
}

# 子音
consonant_read_dict = {
    "ㄱ": "k/g",
    "ㄴ": "n",
    "ㄷ": "t/d",
    "ㄹ": "l",
    "ㅁ": "m",
    "ㅂ": "p/b",
    "ㅅ": "s",
    "ㅇ": "",
    "ㅈ": "ch/j",
    "ㅊ": "ch",  # 激音
    "ㅋ": "k",  # 激音
    "ㅌ": "t",  # 激音
    "ㅍ": "p",  # 激音
    "ㅎ": "h",
}

# 子音の濃音
strong_consonant_read_dict = {
    "ㄲ": ["kk", "ㄱ"],
    "ㄸ": ["tt", "ㄷ"],
    "ㅃ": ["pp", "ㅂ"],
    "ㅆ": ["ss", "ㅅ"],
    "ㅉ": ["cch", "ㅈ"],
}

# パッチム
patchum_read_dict = {
    "ㄱ": "k",
    "ㅋ": "k",
    "ㄲ": "k",
    "ㄴ": "n",
    "ㅁ": "m",
    "ㅇ": "ng",
    "ㅂ": "p",
    "ㅍ": "p",
    "ㄹ": "l",
    "ㄷ": "ッ",
    "ㅅ": "ッ",
    "ㅈ": "ッ",
    "ㅊ": "ッ",
    "ㅌ": "ッ",
    "ㅎ": "ッ",
    "ㅆ": "ッ",
}

# 合成母音を分解
diphthong_read_dict = {
    "ㅘ": ["ㅗ", "ㅏ"],
    "ㅙ": ["ㅗ", "ㅐ"],
    "ㅚ": ["ㅗ", "ㅣ"],
    "ㅝ": ["ㅜ", "ㅓ"],
    "ㅞ": ["ㅜ", "ㅔ"],
    "ㅟ": ["ㅜ", "ㅣ"],
    "ㅢ": ["ㅡ", "ㅣ"],
    "ㅐ": ["ㅏ", "ㅣ"],
    "ㅒ": ["ㅑ", "ㅣ"],
    "ㅔ": ["ㅓ", "ㅣ"],
    "ㅖ": ["ㅕ", "ㅣ"],
}

all_result = []

for char in input_text:
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
    strong_consonant = strong_consonant_read_dict.get(consonant)
    if strong_consonant:
        consonant_info = {
            "symbol": consonant,
            "note": "濃音",
            "reading": strong_consonant[0],
            "base": {
                "symbol": strong_consonant[1],
                "reading": consonant_read_dict[strong_consonant[1]],
            }
        }
    else:
        consonant_info = {
            "symbol": consonant,
            "note": "",
            "reading": consonant_read_dict[consonant],
        }
    result["components"]["子音"] = consonant_info

    # 母音の分析（ネスト構造）
    vowel_info = {
        "symbol": vowel,
        "note": "合成母音" if diphthong_read_dict.get(vowel) else "",
    }
    # 合成母音の場合は2つの母音を分析
    diphthong = diphthong_read_dict.get(vowel)
    if diphthong:
        vowel_info["components"] = [
            {"symbol": diphthong[0], "reading": vowel_read_dict[diphthong[0]]},
            {"symbol": diphthong[1], "reading": vowel_read_dict[diphthong[1]]},
        ]
        vowel_info["combined_reading"] = (
            f"{vowel_read_dict[diphthong[0]]} + {vowel_read_dict[diphthong[1]]}"
        )
    else:
        vowel_info["reading"] = vowel_read_dict[vowel]
    result["components"]["母音"] = vowel_info

    # パッチムの分析（ネスト構造）
    if patchum:
        patchum_info = {
            "symbol": patchum,
            "note": "",
            "reading": patchum_read_dict.get(patchum, ""),
        }
        result["components"]["パッチム"] = patchum_info

    all_result.append(result)

with open("result.json", "w", encoding="utf-8") as f:
    json.dump(all_result, f, ensure_ascii=False, indent=4)
