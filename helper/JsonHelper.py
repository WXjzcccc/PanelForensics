class JsonHelper:
    def __init__(self):
        self.dic = {}

    def list2json(self,key: list,lst: list) -> dict:
        if lst == []:
            return {}
        if len(key) != len(lst[0]):
            return {}
        length = len(key)
        cnt = 0
        for v in lst:
            tmp_dic = {}
            for i in range(length):
                tmp_dic.update({key[i]:v[i]})
            self.dic.update({cnt:tmp_dic})
            cnt += 1
        retval = self.dic
        return retval