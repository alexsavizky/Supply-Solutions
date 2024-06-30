class User:
    def __init__(self):
        self.id = None
        self.email = None
        self.password = None
        self.type = 1
        self.name = None
        self.lastname = None

    def insert(self, email, password, name, lastname, type=1):
        self.id = None
        self.email = email
        self.password = password
        self.type= int(type)
        self.name = name
        self.lastname = lastname

    def tupple_insert(self, tupple_insert):
        self.id = tupple_insert[0]
        self.email = tupple_insert[1]
        self.password = tupple_insert[2]
        self.type= int(tupple_insert[3])
        self.name = tupple_insert[4]
        self.lastname = tupple_insert[5]

    def totuple(self):
        if not self.id:
            return (self.email, self.password, self.type, self.name, self.lastname)
        else:
            return (self.id, self.email, self.password, self.type, self.name, self.lastname)

    def __str__(self):
        return str(self.totuple())


class Supply:
    def __init__(self):
        self.id = None
        self.type = None
        self.name = None
        self.all_units = None
        self.available_units = None
        self.description = None
        self.broken_units = None

    def insert(self, id, type, name, all_units, available_units,description,broken_units):
        self.id = id
        self.type = type
        self.name = name
        self.all_units = all_units
        self.available_units = available_units
        self.description = description
        self.broken_units = broken_units

    def tupple_insert(self, tupple_insert):
        self.id = tupple_insert[0]
        self.name = tupple_insert[1]
        self.all_units = tupple_insert[2]
        self.available_units = tupple_insert[3]
        self.type = tupple_insert[4]
        self.description = tupple_insert[5]
        self.broken_units= tupple_insert[6]

    def borrow(self, how_much_items):
        if self.available_units - how_much_items >= 0:
            self.available_units -= how_much_items
            return self.available_units
        return False


    def return_item(self, how_much_items):
        self.available_units += how_much_items
        return self.available_units

    def totuple(self):
        return (self.id, self.name, self.all_units, self.available_units, self.type,self.description,self.broken_units)

    def __str__(self):
        return str(self.totuple())


class SupplyList:
    def __init__(self):
        self.list = []

    def insert_list(self, list):
        for i in list:
            supply = Supply()
            supply.tupple_insert(i)
            self.list.append(supply)

    def borrow_item_by_id(self, id, how_much_items):
        supply = None
        for i in self.list:
            if i.id == id:
                supply = i
                break
        if not supply:
            return False
        remain = supply.borrow(how_much_items)
        if remain:
            return remain
        return False

    def return_item_by_id(self, id, how_much_items):
        supply = None
        for i in self.list:
            if i.id == id:
                supply = i
                break
        if not supply:
            return False
        remain = supply.return_item(how_much_items)
        if remain:
            return remain
        return False

    def get_avl_item_by_id(self, id):
        for i in self.list:
            if i.id == id:
                return i.available_units
        return False

    def get_items_names(self):
        return [x.name for x in self.list]

    def get_id_by_name(self, name):
        for i in self.list:
            if i.name == name:
                return i.id
        return False


    def get_supply_avl_by_name(self, name):
        for i in self.list:
            if i.name == name:
                return i.available_units

    def get_name_by_id(self,id):
        for i in self.list:
            if i.id == id:
                return i.name
        return False
    
    def insert_item(self,id, type, name, all_units,des,broken):
        temp = Supply()
        temp.insert(id, type, name, all_units,all_units,des,broken)
        self.list.append(temp)

    def get_des_by_name(self,name):
        for i in self.list:
            if i.name == name:
                return i.description
        return False

    def report_item(self,name,units):
        for i in self.list:
            if i.name ==name :
                i.broken_units += units
    def __str__(self):
        string = ''.join([str(i) for i in self.list])
        return string
