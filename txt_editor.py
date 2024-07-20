class txtEditor:
    def __init__(self):
        self.file_name = "exchange_rate"

    def read_pairs(self):
        with open(self.file_name, 'r') as file:
            dict_list = []
            for line in file.readlines():
                dict = {"value_in": [],
                        "value_out": [],
                        "date": [],
                        "rate": [],
                        "type": []}

                items = line[:-1].split(' ')
                for enum, key in enumerate(dict.keys()):
                    dict[key] += [items[enum]]
                dict_list.append(dict)
            return dict_list

    def add_pairs(self, pair: dict):
        with open(self.file_name, 'a') as file:
            file.write("\n")
            for key in pair.values():
                file.write(str(key) + " ")

print(txtEditor().read_pairs())