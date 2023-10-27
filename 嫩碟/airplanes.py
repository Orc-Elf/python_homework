class Airplane:
    def __init__(self, module, key, seats_number, miles):
        self.module = module
        self.key = key
        self.seats_number = seats_number
        self.miles = float(miles)

    def log_trip(self, miles):
        self.miles += float(miles)

    def __eq__(self, other):
        return (self.module == other.module and self.key == other.key and 
                self.seats_number == other.seats_number and self.miles == other.miles)


class Flight:
    def __init__(self, plane):
        self.plane = plane
        self.passengers = []  # 初始化passengers列表

    def conversion(self):
        return f"Airplane({self.plane.module}, {self.plane.key}, {self.plane.seats_number}, {self.plane.miles})"

    def add(self, passenger):
        if len(self.passengers) < self.plane.seats_number:
            self.passengers.append(passenger)
            return True
        else:
            return False

    def change_planes(self, other_planes):
        if other_planes.seats_number >= len(self.passengers):
            self.plane = other_planes
            self.plane.seats_number = other_planes.seats_number - len(self.passengers)  # 更新飞机的座位数
        else:
            rest = self.plane.seats_number - len(self.passengers)
        return rest