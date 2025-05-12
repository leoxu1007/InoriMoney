# decide category based on ご利用先
def smart_decide_pay_category_and_program(merchant):
    # TODO 此处应该训练模型进行快速分类 商家 -> 消费条目 消费项目
    if "業務スーパー" in merchant or "ｷﾞﾖｳﾑｽ-ﾊﾟ" in merchant:
        return "日常餐食", "基本生活"
    if "フレンテ笹塚" in merchant:
        return "日常餐食", "基本生活"
    elif "セリア" in merchant or "ＤＡＩＳＯ" in merchant:
        return "家庭用品", "基本生活"
    elif "セブン" in merchant and "イレブン" in merchant:
        return "日常餐食", "基本生活"
    elif "ドン・キホーテ" in merchant or "ﾄﾞﾝｷﾎｰﾃ" in merchant:
        return "日常餐食", "基本生活"
    elif "成田空港" in merchant:
        return "日常餐食", "旅行"
    elif "株式会社オークハウス" in merchant:
        return "房租", "基本生活"
    elif "東京ガス" in merchant:
        return "水电气", "基本生活"
    elif "ＥＮＥＯＳ　Ｐｏｗｅｒ〔電気〕" in merchant:
        return "水电气", "基本生活"
    elif "ﾎﾟｳﾞｫｺﾞﾘﾖｳﾘｮｳｷﾝ" in merchant:
        return "电话费", "基本生活"
    elif "ドコモご利用料金" in merchant:
        return "电话费", "基本生活"
    elif "楽天モバイル通信料" in merchant:
        return "网费", "基本生活"
    elif "ZHONGGUOTIELUWANGLUO" in merchant or "ＪＲ東日本" in merchant:
        return "长途客车・火车", "旅行"
    elif "ALP" in merchant or "ALIPAY" in merchant:
        return "NA", "旅行"
    elif "JETSTAR" in merchant:
        return "飞机", "旅行"
    elif "ｱｺﾞﾀﾞ" in merchant:
        return "外泊", "旅行"
    elif "マツモトキヨシ" in merchant or "サンドラッグ" in merchant:
        return "药品费", "健康"
    elif "マクドナルド" in merchant:
        return "外食", "基本生活"
    elif "利用国" in merchant:
        return "NA", "旅行"
    elif "ｸﾗﾌﾞﾖｱｿﾋﾞ" in merchant:
        return "订阅服务", "兴趣爱好"
    elif "ジーユー" in merchant:
        return "服饰", "基本生活"
    elif "ＡＭＡＺＯＮ" in merchant:
        return "NA", "兴趣爱好"
    elif "スターバックス" in merchant:
        return "外食", "兴趣爱好"
    elif "松屋" in merchant:
        return "外食", "NA"
    elif "ユー・エス・ジェイ" in merchant:
        return "文化活动", "兴趣爱好"
    else:
        return "NA", "NA"


    # elif "test" in merchant:
    #     return "NA", "NA"