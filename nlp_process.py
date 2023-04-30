import json
from konlpy.tag import Okt
# Okt(Open Korean Text)는 트위터에서 만든 오픈소스 한국어 처리기인 twitter-korean-text를 이어받아 제작되는 프로젝트이다.
# 명사, 부사, 동사를 추출하고 속도가 준수하여 프로젝트 사용에 유리하다고 판단하여 선정하였다.

# 분류할 분야 목록
fieldName = ['ai', 'android', 'backend', 'frontend', 'bigdataengineer', 'blockchain', 'dataengineer',
          'datascience', 'deeplearning', 'gameclient', 'gameserver', 'machinelearning']

# 사용자의 입력에서 인식한 각각의 문장에 해당하는 분야를 순서대로 List에 담는다.
fields = []

# 분류 할 각각의 분야를 판단할 수 있는 단어들이 담긴 사전을 Load한다.
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

#  문장이 긍정인지 부정인지 판단하여 순서대로 List에 저장하여 return한다.
def define_pos_neg(input_split):
    posEx = ['있', '좋', '느꼈', '느낌', '값진', '경험']
    negEx = ['없', '못', '싫', '않', '도저히', '아니']
    result = []

    # 한 문장에서 "없지 않다"와 같이 부정적 형태소가 짝수 회 입력되면 긍정으로 판단한다.
    for i in input_split:
        direction = 1                          # 부정적인 의미의 형태소가 몇 개 입력되는지에 따른 방향성 저장을 위한 변수. 1이면 긍정, -1이면 부정
        count = 0                              # 긍정과 부정의 count를 계산하여 양수이면 긍정, 0이면 중립, 음수이면 부정
        for p in posEx:                        # 긍정의 값 계산하여 count에 저장
            if i.find(p) != -1:
                count = count + 1
                direction = 1
                break
        for n in negEx:                        # 부정의 값 계산하여 count를 update
            if i.find(n) != -1:
                count = count - 1 * direction
                direction = direction * -1
                break

        if count > 0:                          # 최종적인 count가 양수이면 긍정, 0이면 중립, 음수이면 부정으로 판단하여 결과 List에 
            result.append(1)
        elif count < 0:
            result.append(-1)
        else:
            result.append(0)

    return result

# 문장이 설명하고 있는 분야를 판단한다.
def define_field(input_split):
    okt = Okt()                                # Okt(Open Korean Text) 형태소 분석기 Load
    fields_result = []                         # 각 문장의 분야를 순서대로 저장하기 위한 List

    for i in input_split:
        field_define = [0,0,0,0,0,0,0,0,0,0,0,0]
                                               # 각 문장의 분야 별 점수를 담는 List. 입력된 문장이 여러 분야와 관련된 단어를 포함하는 경우, 가장 많이 관련된 분야로 분류한다. 가장 점수가 높은 분야가 해당 문장의 분야가 된다.
        for k in okt.phrases(i):
            for j in range(0, len(fields)):    # 각 분야 별 사전에서 해당되는 단어가 있는지 판단하여 해당 분야의 점수를 추가한다.
                if fields[j].find(k)!=-1:
                    field_define[j] = field_define[j] + 1
        fields_result.append(fieldName[field_define.index(max(field_define))])
                                               # 가장 점수가 높은 분야를 해당 문장의 분야로 판단하고 결과 List에 추가한다.

    return fields_result

# 한 문장에서 define_pos_neg에서 판단한 각 문장 별 긍정/부정 여부와, define_field에서 판단한 각 문장 별 분야를 종합하여 선호, 중립, 비선호 List에 저장한다.
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

# 각각의 문장이 긍정인지, 부정인지와 분야를 판단 후 순서대로 저장한다.
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

# 문장 각각의 말하고자 하는 분야를 판단하여 저장한다.
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
