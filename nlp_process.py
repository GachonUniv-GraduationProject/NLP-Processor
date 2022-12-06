import json
from konlpy.tag import Okt

fieldName = ['ai', 'android', 'backend', 'frontend', 'bigdataengineer', 'blockchain', 'dataengineer',
          'datascience', 'deeplearning', 'gameclient', 'gameserver', 'machinelearning']
fields = []


def load_jsons():
    with open('fieldData/ai.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/android.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/backend.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/frontend.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/bigdataengineer.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/blockchain.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/dataengineer.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/datascience.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/deeplearning.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/gameclient.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/gameserver.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))
    with open('fieldData/machinlearning.json', 'r', encoding="UTF-8") as f:
        fields.append(json.dumps(json.load(f), ensure_ascii = False))


def define_pos_neg(input_split):
    posEx = ['있', '좋', '느꼈', '느낌', '값진', '경험']
    negEx = ['없', '못', '싫', '않', '도저히', '아니']
    result = []

    for i in input_split:
        direction = 1
        count = 0
        for p in posEx:
            if i.find(p) != -1:
                count = count + 1
                direction = 1
                break
        for n in negEx:
            if i.find(n) != -1:
                count = count - 1 * direction
                direction = direction * -1
                break

        if count > 0:
            result.append(1)
        elif count < 0:
            result.append(-1)
        else:
            result.append(0)

    return result

def define_field(input_split):
    okt = Okt()
    fields_result = []

    for i in input_split:
        field_define = [0,0,0,0,0,0,0,0,0,0,0,0]
        for k in okt.phrases(i):
            for j in range(0, len(fields)):
                if fields[j].find(k)!=-1:
                    field_define[j] = field_define[j] + 1
        fields_result.append(fieldName[field_define.index(max(field_define))])

    return fields_result


def ho_bulho(input_split):
    ho_list = []
    joonglip_list = []
    bulho_list = []

    for i in range(0, len(input_split)):
        if define_pos_neg(input_split)[i] == 1:
            ho_list.append(define_field(input_split)[i])
        elif define_pos_neg(input_split)[i] == 0:
            joonglip_list.append(define_field(input_split)[i])
        else:
            bulho_list.append(define_field(input_split)[i])

    return ho_list, joonglip_list, bulho_list


def classify_pos_neg_sentences(sentences):
    if sentences[len(sentences) - 1] == '.':
        sentences = sentences[:-1]
    sentence_split_list = sentences.split(".")
    classify = define_pos_neg(sentence_split_list)
    field = define_field(sentence_split_list)
    result = {
        "classify": []
    }
    for i in range(len(classify)):
        res_each = {
            "field": field[i],
            "value": classify[i]
        }
        result["classify"].append(res_each)

    return result


def classify_fields(sentences):
    if sentences[len(sentences) - 1] == '.':
        sentences = sentences[:-1]
    sentence_split_list = sentences.split(".")
    fields_result = define_field(sentence_split_list)
    result = {
        "classify": []
    }

    for i in range(len(fields_result)):
        res_each = {
            "field": fields_result[i],
            "sentence": sentence_split_list[i]
        }
        result["classify"].append(res_each)

    return result
