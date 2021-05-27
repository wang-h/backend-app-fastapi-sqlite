import pandas as pd
import jieba
import json
from itertools import chain
import logging
logging.basicConfig(level=logging.INFO)


def load_additional_dicts():
    logging.info("# 1. 载入药品信息...")
    drug_dict = load_drug_dict("./data/国家药品编码本位码信息（国产药品）.xlsx",
                               "./data/国家药品编码本位码信息（进口药品）.xlsx")
    logging.info("# 共载入【%d】个药品信息..." % len(drug_dict))

    logging.info("# 2. 载入疾病信息...")
    disease_dict = load_disease_dict("./data/疾病名称.xls")
    logging.info("# 共载入【%d】个疾病信息..." % len(disease_dict))

    logging.info("# 3. 载入症状信息...")
    symptom_dict = load_symptom_dict("./data/症状疾病科室.xlsx")
    logging.info("# 共载入【%d】个症状信息..." % len(symptom_dict))

    logging.info("# 4. 载入检查信息...")
    test_dict = load_test_dict("./data/医院检查项目.xlsx")
    logging.info("# 共载入【%d】个检查信息..." % len(test_dict))

    for term in chain(drug_dict.keys(), symptom_dict.keys(), disease_dict.keys(), test_dict.keys()):
        try:
            jieba.add_word(term)
        except:
            pass
    return drug_dict, symptom_dict, disease_dict, test_dict


def tokenize(text):

    return [word for word in jieba.cut(
        text, use_paddle=True) if word not in [' ', '\u3000', '\n']]

# respiratory_symptoms_data = pd.read_excel(path, sheet_name=1)
# breast_symptoms_data = pd.read_excel(path, sheet_name=2)
# ss = data.head()
# print(ss)


def load_test_dict(path):

    test_data = pd.read_excel(path, sheet_name=0,
                              header=None)
    tests = []
    for key in test_data.to_dict(
            orient='list')[0]:

        if "(" in key:

            parts = key.split("(")
            tests.append(parts[0])
            for item in parts[1].rstrip(")").split("/"):
                tests.append(item+parts[0])
                tests.append(item)
        else:
            tests.append(key)
            # for item in test_data.to_dict(
            #     orient='list')[0])
            # print(tests)
    return {k: "检查" for k in set(tests)}


def load_drug_dict(path1, path2):
    drug_data = pd.read_excel(path1,
                              sheet_name=0,
                              skiprows=2,
                              header=0)
    imported_drug_data = pd.read_excel(path2,
                                       sheet_name=0,
                                       skiprows=2,
                                       header=0)
    drugs = {v: "药品" for (k, v) in chain(drug_data["产品名称"].to_dict(
    ).items(), imported_drug_data["产品名称"].to_dict().items())}
    return drugs


def load_symptom_dict(path):
    symptoms = []
    respiratory_symptom_data = pd.read_excel(path,
                                             sheet_name=1,
                                             skiprows=1,
                                             header=None)
    symptoms.extend(respiratory_symptom_data.to_dict(
        orient='list')[0])

    breast_symptom_data = pd.read_excel(path,
                                        sheet_name=2,
                                        skiprows=2,
                                        header=None)

    symptoms.extend(breast_symptom_data.to_dict(
        orient='list')[0])

    general_symptom_data = pd.read_excel(path,
                                         sheet_name=3,
                                         skiprows=2,
                                         header=None)
    len_cols = len(general_symptom_data.columns)
    for i in range(1, len_cols):
        for key in general_symptom_data[i]:
            symptoms.append(key)
    symptoms = set(symptoms)
    return {v: "症状" for k, v in enumerate(set(symptoms))}


def load_disease_dict(path):
    diseases = []
    disease_data = pd.read_excel(path,
                                 sheet_name=1,
                                 skiprows=1,
                                 header=None)

    diseases.extend(disease_data.to_dict(
        orient='list')[1])

    disease2_data = pd.read_excel(path,
                                  sheet_name=2,
                                  skiprows=1,
                                  header=None)

    for key in disease2_data.to_dict(
            orient='list')[2]:
        if "，" in key:
            main_key = key.split("，")[0]
            diseases.append(main_key)
        else:
            diseases.append(key)
    disease3_data = pd.read_excel(path,
                                  sheet_name=3,
                                  skiprows=1,
                                  header=None)
    diseases.extend(disease3_data.to_dict(
        orient='list')[0])

    diseases = set(diseases)
    return {v: "疾病" for k, v in enumerate(set(diseases))}


def reload_data_from_json():
    with open('case_table.txt', 'r', encoding='utf8') as json_file:
        case_table = json.load(json_file)
    return case_table


def search_symptom(sent, symptom_dict):
    return list(set([word for word in sent if word in symptom_dict]))


def search_drug(sent, drug_dict):
    return list(set([word for word in sent if word in drug_dict]))


def search_disease(sent, disease_dict):
    return list(set([word for word in sent if word in disease_dict]))


def search_test(sent, test_dict):
    return list(set([word for word in sent if word in test_dict]))


def sample_test(patient_id, case_table, drug_dict, symptom_dict, disease_dict, test_dict):
    for patient_id, case in case_table.items():
        print("# 患者ID：", patient_id)
        for attr in case.keys():
            print("## 属性", attr)
            print()
            print("**原始**", case[attr])
            print()
            case[attr] = tokenize(case[attr])
            print("**分词后**：", case[attr])
            print()
            print("**症状**：", search_symptom(case[attr], symptom_dict))
            print()
            print("**药品**：", search_drug(case[attr], drug_dict))
            print()
            print("**疾病**：", search_disease(case[attr], disease_dict))
            print()
            print("**检查**：", search_test(case[attr], test_dict))
            print()


if __name__ == "__main__":
    # 2. 从json中读取病例数据
    case_table = reload_data_from_json()
    drug_dict, symptom_dict, disease_dict, test_dict = load_additional_dicts()
    sample_test("52948", case_table, drug_dict,
                symptom_dict, disease_dict, test_dict)
