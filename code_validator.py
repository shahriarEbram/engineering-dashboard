import re
import streamlit as st

equipment_name = {
    'D': 'قالب ریخته گری',
    'C': 'قالب ماهیچه',
    'F': 'فیکسچر',
    'G': 'گیج',
    'M': 'ماشین آلات',
    'T': 'ابزار براده برداری',
    'V': 'متفرقه',
    'Q': 'متفرقه خارج از شرکت',
    'R': 'کارخانه آلیاژ سازی',
    'N': 'CNC',
    'S': 'SQA',
    'A': 'نقشه'
}

equipment_name_subset = {

    'D': {
        '10': 'LPDC',
        '11': 'DC (Gravity)',
        '12': 'TILT',
        '13': 'HPDC'
    },
    'C': {
        '10': 'واترجکت',
        '11': 'اویل جکت',
        '12': 'پورت دود',
        '13': 'پورت هوا',
        '14': 'پورت دود و هوا',
        '15': 'میل بادامک',
        '16': 'شمع',
        '17': 'TOP CORE',
        '18': 'کانال وسط',
        '19': 'میل بادامک و کانال',
        '20': 'رایزر کور'
    },
    'F': {
        '10': 'شیفت عرضی',
        '11': 'شیفت طولی',
        '12': 'كنترل اندازه محفظه',
        '13': 'حكاكي شماره زني',
        '14': 'برش اره',
        '15': 'سیت و گاید',
        '16': 'حكاكي لیزر',
        '51': 'ماشینکاری op10',
        '52': 'ماشینکاری op20',
        '53': 'ماشینکاری op50',
        '54': 'ماشینکاری OP30',
        '55': 'ماشینکاری OP40',
        '71': 'کلمپ های هیدرولیک چکشی',
        '72': 'کلمپ های هیدرولیک گردشی',
        '73': 'فیکسچر ماشینکاری کیوب',
        '74': 'فیکسچر درپوش',
        '75': 'فیکسچر محفظه',
        '76': 'فیکسچر منیفولد',
        '77': 'فیکسچر جانبی',
        '78': 'فیکسچر شمع',
        '79': 'فیکسچر استکانی',
        '80': 'فیکسچر ماشینکاری لانگبورینگ',
        '81': 'فیکسچرهای ماشین هکرت',
    },
    'G': {
        '10': ' موقعيت كپه',
        '11': 'منيفولد دود',
        '12': 'منيفولد هوا',
        '13': ' لنگي و سيت و گايد',
        '14': 'میز صافی سطح',
        '15': 'مولتی کنترلی استکانی'

    },
    'M': {
        '10': '0',
        '11': 'ریخته گری DC',
        '12': 'ریخته گری TILT',
        '13': 'واترجکت',
        '14': 'اویل جکت',
        '15': 'پورت دود',
        '16': 'پورت هوا',
        '17': 'پورت دود و هوا',
        '18': 'میل بادامک',
        '19': 'شمع',
        '20': 'کانال وسط',
        '21': 'ماشین کاری',
        '22': 'مخصوص',
        '23': 'تست راکروم',
        '24': 'سواخ آب',
        '25': 'لوپرژر',
        '26': 'کوره ذوب',
        '27': 'کاراسلی',
        '28': 'شات بلاست',
        '29': 'دکورینگ',
        '30': 'کوره عملیات حرارتی',
        '31': 'کوره بازیافت',
        '32': 'دستگاه هم زن',
        '33': 'دستگاه سرند',
        '34': 'tx3000',
        '35': 'دستگاه تست کاسه نمد',
        '36': 'کفتراش',
        '37': 'دستگاه کیوب',
        '38': 'ماشین ماهیچه افقی',
        '39': 'ماشین ماهیچه عمودی',
        '40': 'فاتا',
        '41': 'کوره پخت',
        '42': 'میز ویبره',
        '43': 'دستگاه سیت و گاید سمت دود',
        '44': 'دستگاه سیت و گاید سمت هوا',
        '45': 'نوار نقاله کوره بازیافت',
        '46': 'همزن مذاب(MTS)',
        '47': 'بالابر ماسه(Elevator)',
        '48': 'ماشین ماهیچه کلد باکس',
        '49': 'ماشین تست لیک',
        '50': 'گونیا',
        '51': 'قلاویز',
        '52': 'ماشین آسیاب',
        '53': 'تراش QC',
        '54': 'سوراخ کاری',
        '55': 'قلاویزکاری',
        '56': 'سوراخ کاری و قلاویزکاری',
        '57': 'اسپات',
        '58': 'ماشین شمع',

    },
    'T': {
        '10': 'هلدر',
        '11': 'چکش بادی',
        '12': 'مولتی 10 محوره',
    },
    'V': {
        '10': 'مدل قطعه دیوایدر',
        '11': 'مدل مخروطی',
        '12': 'مدل لاست فوم',
        '30': 'طراحی مکانیزم',
        '31': 'عمومی',
        '32': 'فرز',
        '33': 'باکس رنگ',
        '34': 'لیفتراک',
        '35': 'نمونه کشش',
        '36': 'اره',
        '37': 'جانمایی دستگاه ها',
        '38': 'پرینتر 3بعدی',
        '39': 'قالب توری کاپی',
        '40': 'مدل سازی 3بعدی',
        '41': 'جرثقیل',
        '42': 'مدل سازی تفلونی',
        '43': "توری گذار"
    },
    'Q': {
        '10': "اهدا دارو"
    },
    'R': {
        '10': 'کوره آلیاژ سازی  5تن',
        '11': 'کوره آلیاژ سازی  10تن',
        '12': 'کوره ذوب براده',
        '13': 'دستگاه استریر',
        '14': 'دستگاه خشک کن براده',
        '15': 'دستگاه شمش ریزی',
        '16': 'دستگاه مگنت',
    },
    'N': {
        '10': 'Dah-Lih HM 500',
        '11': 'Dah-Lih HM 1020 OLD',
        '12': 'Dah-Lih HM 1020 NEW',
        '13': 'Dah-Lih HM 720 OLD',
        '14': 'Dah-Lih HM 720 NEW',
        '15': 'EXCEL',
        '16': 'Deckel 400',
        '17': 'Devo Rotary 500',
        '18': 'Mori-Seiki 63',
        '19': 'Mori-Seiki Vertical',
        '20': 'HENKER 400',
        '21': 'HENKER 250',
        '22': 'HENKER 25',
    },
    'S': {
        '10': 'CP',
        '11': 'SMEA',
        '12': 'OPC',
        '13': 'PROCESS',
        '14': 'برگه ویژگی های فنی محصول',
        '15': 'سوابق مشکلات کیفی',
        '16': 'ماتریس محصول فرآیند',
        '17': 'مشخصه های مهم فرآیند',
        '18': 'مشخصه های مهم محصول',
        '19': 'طرح کنترل اقلام ورودی'
    },
    'A': {

            '10': 'نقشه گاید دود',
            '11': 'نقشه گاید هوا',
            '12': 'نقشه گاید',
            '13': 'سیت دود',
            '14': 'سیت هوا',
            '15': 'پین حامل',
            '16': 'پیچ بلند حامل',
            '17': 'پیچ کوتاه حامل',
            '18': 'پیچ حامل',
            '19': 'پیچ کورکن',
            '20': 'سوپاپ دود',
            '21': 'سوپاپ هوا',
            '22': 'درپوش هوا',
            '23': 'درپوش ترموستات',
            '24': 'میل بادامک',
            '25': 'حامل میل اسبک'
    }

}

product_name = {
    '10': 'EC5',
    '11': 'IP20-L',
    '12': 'IP20-R',
    '13': 'K4',
    '14': 'ATV',
    '15': 'کپه یاتاقان 5و1',
    '16': 'ME16',
    '17': 'IK3',
    '18': 'پژو گرویتی',
    '19': 'پیکان',
    '20': 'پراید',
    '21': 'نیسان',
    '23': 'پژو LPDC',
    '24': 'EF7',
    '25': 'TU5',
    '26': 'پژوپارتنر',
    '27': 'کاماز',
    '28': 'M15',
    '29': 'فیات تمپرا',
    '30': 'مسترسیلندر سمند',
    '31': 'مسترسیلندر 206',
    '32': 'ME15',
    '33': 'کپه یاتاقان 3و3',
    '38': 'S81',
    '42': 'کپه یاتاقان 2و4',
    '44': 'E4',
    '57': 'TU3',
    '86': 'اقلام انبار (WH)',
    '87': 'OHVG',
    '88': 'X100',
    '89': 'XU8',
    '90': 'عمومی',
    '91': 'ربات',
    '92': 'قطعه گیر',
    '98': 'کوره',
    '99': 'متفرقه',
}

map_source = {
    '01': 'BT1',
    '02': 'BT2',
    '03': 'BT3',
    '04': 'BT4',
    '05': 'BT5',
    '06': 'BT6',
    '07': 'BT7',
    '08': 'BT8',
}

map_type = {
    'P': 'پروژه',
    'S': 'یدکی اصلاحی',
    'R': 'تحقیقاتی',
    'X': 'خرید خارجی',
    'E': 'مهندسی معکوس'
}

cylinder_head_area = {
    '01': 'سمت درپوش',
    '02': 'سمت محفظه',
    '03': 'منیفولد هوا',
    '04': 'منیفولد دود',
    '05': 'سمت ترموستات',
    '06': 'سمت پولکی',
}


def validate_code(code):
    if code != "000000000":
        # If BT2:
        if len(code) == 10:
            equipment, subset, product, map_src, map_tp, number = \
                code[:1], code[1:3], code[3:5], code[5:7], code[7], code[8:10]
            if equipment not in equipment_name:
                return False
            elif subset not in equipment_name_subset.get(equipment, {}):
                return False
            elif product not in product_name:
                return False
            elif map_src not in map_source:
                return False
            elif map_tp not in map_type:
                return False
            elif not number.isdigit() or not 1 <= int(number) <= 99:
                return False

        elif len(code) == 13:
            equipment, subset, product, map_src, map_tp, number, cy_ar = \
                (code[:1], code[1:3], code[3:5], code[5:7], code[7], code[8:10], code[11:])
            if equipment not in equipment_name:
                return False
            elif subset not in equipment_name_subset.get(equipment, {}):
                return False
            elif product not in product_name:
                return False
            elif map_src not in map_source:
                return False
            elif map_tp not in map_type:
                return False
            elif cy_ar not in cylinder_head_area:
                return False
            elif not number.isdigit() or not 1 <= int(number) <= 99:
                return False

        return True


def decode_code(code):
    code = code.upper()

    decoded_string = ""
    if code == "000000000":
        return "امور جاری"
    # If BT2:
    if len(code) == 10:
        equipment, subset, product, map_src, map_tp, number = \
            code[:1], code[1:3], code[3:5], code[5:7], code[7], code[8:10]
        # Provide a default message if the key is not found
        equipment_name_str = equipment_name.get(equipment, "Unknown Equipment")
        equipment_subset_str = equipment_name_subset.get(equipment, {}).get(subset, "Unknown Subset")
        product_name_str = product_name.get(product, "Unknown Product")
        map_source_str = map_source.get(map_src, "Unknown Source")
        map_tp_str = map_type.get(map_tp, "Unknown Type")
        decoded_string = (equipment_name_str + " " +
                          equipment_subset_str + " " +
                          product_name_str + " " +
                          " مربوط به واحد " + map_source_str + " " +
                          map_tp_str + " " +
                          "دست " + number
                          )
    elif len(code) == 13:
        equipment, subset, product, map_src, map_tp, number, cy_ar = \
            (code[:1], code[1:3], code[3:5], code[5:7], code[7], code[8:10], code[-2:])

        # Provide a default message if the key is not found
        equipment_name_str = equipment_name.get(equipment, "Unknown Equipment")
        equipment_subset_str = equipment_name_subset.get(equipment, {}).get(subset, "Unknown Subset")
        product_name_str = product_name.get(product, "Unknown Product")
        map_source_str = map_source.get(map_src, "Unknown Source")
        map_tp_str = map_type.get(map_tp, "Unknown Type")
        cy_ar_str = cylinder_head_area.get(cy_ar, "Unknown Type")
        if cy_ar != '00':
            decoded_string = (f"{equipment_name_str}\n{equipment_subset_str} \n{product_name_str} \n"
                              f"مربوط به واحد {map_source_str} \n {map_tp_str} \n"
                              f"دست {number}\n{cy_ar_str}")
        else:
            decoded_string = (f"{equipment_name_str}\n{equipment_subset_str}\n{product_name_str}\n"
                              f"مربوط به واحد {map_source_str}\n{map_tp_str}\n"
                              f"دست {number}")

    return decoded_string
