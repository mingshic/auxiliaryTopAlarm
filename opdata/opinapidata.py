#!/usr/bin/env python



class apiData:

    def remove_unused_fields(self, data):
        data = eval(data)
        unparsed = []
        for i,j in data.items():
            if j == "":
                data[i] = "NULL"
        return data, unparsed


