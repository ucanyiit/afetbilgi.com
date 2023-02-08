import json
import pandas as pd

from utils.functions import turkish_title


def index_or_none(l, i):
    if len(l) > i:
        return l[i]
    else:
        return None

def main():
    city_translation = json.loads(open("./utils/il_translate.json").read())

    sheet_id = "131Wi8A__gpRobBT3ikt5VD3rSZIPZxxtbqZTOUHUmB8"
    sheet_name = "Ge%C3%A7ici%20Bar%C4%B1nma%20Alanlar%C4%B1"
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

    json_name = "../datasets/barinma.json"
    df = pd.read_csv(url, encoding="utf-8")

    parsed = []
    options = []

    city_name = None

    for _, row in df.iterrows():
        tmp_sehir = turkish_title(row['Şehir'].strip())
        
        if tmp_sehir != city_name:
            if city_name is None:
                city_name = tmp_sehir
            else:
                options.append({
                    "name_tr": city_name,
                    "name_en": city_translation[city_name]['en'],
                    "name_ku": city_translation[city_name]['ku'],
                    "name_ar": city_translation[city_name]['ar'],
                    "value": {
                        "type": "data",
                        "data": {
                            "city": city_name,
                            "dataType": "city-accommodation",
                            "items": parsed
                        }
                    }
                })
                city_name = row[0]

                parsed = []

        get_data = lambda x: x if not pd.isna(x) else None

        parsed.append({
            "city": city_name,
            "name": get_data(row['Lokasyon']),
            "is_validated": get_data(row['Doğrulanma Durumu']) == "Doğrulandı",
            "url": get_data(row['Link']),
            "address": get_data(row['Konum linki']),
            "validation_date": get_data(row['Doğrulanma Tarihi']),
        })
        
    else:
        options.append({
            "name": city_name,
            "value": {
                "type": "data",
                "data": {
                    "city": city_name,
                    "dataType": "city-accommodation",
                    "items": parsed
                }
            }
        })

    data = {
        "type": "question",
        "text_tr": "Hangi şehirde kalacak yer arıyorsunuz?",
        "text_en": "In which city are you looking for temporary accommodation?",
        "text_ku": "Hûn li Kîjan Bajarî Cihên Lêhihewinê yên Demkî Digerin?",
        "text_ar": "في أي مدينة تبحث عن مساكن مؤقة",
        "autocompleteHint": "Şehir",
        "options": options
    }

    with open(json_name, "w+", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
