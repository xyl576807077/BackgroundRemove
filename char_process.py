from langconv import Converter
class CharProcess():
    def __init__(self):
        self.chinese = set()
        self.half_char = set()
        self.half_digit = set()
        self.half_symbol = set()
        self.full_char = set()
        self.full_digit = set()
        self.full_symbol = set()
    

    def ishan(self, text):
        return '\u4e00' <= text <= '\u9fff' 

    def isSimplifyChinese(self, text):
        if self.ishan(text):
            t = Converter('zh-hans').convert(text)
            if t == text:
                return True
            else:
                return False
        else:
            return False
    
    def isTraditionalChinese(self, text):
        if self.ishan(text):
            if self.isSimplifyChinese(text):
                return False
            else:
                return True
        else:
            return False

    def is_half_width_digit(self, text):
        return '\u0030' <= text <= '\u0039'


    def is_half_width_char(self, text):
        return '\u0041' <= text <= '\u005A' or '\u0061' <= text <= '\u007A'


    def is_half_width_symbol(self, text):
        if self.b2q(text) == text or self.is_half_width_char(text) or self.is_half_width_digit(text):
            return False
        else:
            return True


    def is_full_width_digit(self, text):
        return '\uFF10' <= text <= '\uFF19'


    def is_full_width_char(self, text):
        return '\uFF21' <= text <= '\uFF3A' or '\uFF41' <= text <= '\uFF5A'

    def is_half(self, text):
        if self.is_half_width_char(text) or self.is_half_width_digit(text) or self.is_half_width_symbol(text):
            return True
        else:
            return False
    
    def is_full_width_symbol(self, text):
        if self.ishan(text) or self.is_half(text):
            return False
        else:
            return True
    

    def b2q(self, ustr):  
            return ''.join(chr(0x3000 if c == 0x0020 else c+0xfee0 if 0x0020 < c < 0x0080 else c) 
                        for c in map(ord, ustr))

    def q2b(self, text):
        ss = []
        for s in text:
            rstring = ""
            for uchar in s:
                inside_code = ord(uchar)
                if inside_code == 12288:  # 全角空格直接转换
                    inside_code = 32
                elif (inside_code >= 65281 and inside_code <= 65374):  # 全角字符（除空格）根据关系转化
                    inside_code -= 65248
                rstring += chr(inside_code)
            ss.append(rstring)
        return ''.join(ss)




    def is_pure_chinese(self, text):
        flag = True
        for w in text:
            flag = flag and self.ishan(w)
        return flag


    def is_pure_char(self, text):
        flag = True
        for w in text:
            flag = flag and (self.is_full_width_char(w) or 
                                self.is_full_width_digit(w) or
                                self.is_half_width_char(w) or
                                self.is_half_width_digit(w))
        return flag


    def is_pure_symbol(self, text):
        flag = True
        for w in text:
            # print(self.is_full_width_symbol(w), self.is_half_width_symbol(w))
            flag = flag and (self.is_full_width_symbol(w) or self.is_half_width_symbol(w))
        return flag

    def process_sequence(self, origin_dict, char_dict, data_list):
        res_dict = dict()
        for data in data_list:
            text = origin_dict[data]
            res = []
            for w in text:
                res.append(char_dict[w])
            res.append(4427)
            res_dict[data] = res
        return res_dict


# cp = CharProcess()
# print(cp.is_pure_symbol('REALSHINETECHNOLOGYCO..LTD'))