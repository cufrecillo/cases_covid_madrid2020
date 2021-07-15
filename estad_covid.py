
# 6. Crear un objeto estadística que reciba un valor X y otro valor Y, deben ser listas
class Statistics:
    def __init__(self, x, y) :
        self.x = x if type(x) == list else []
        self.y = y if type(y) == list else []

    @property
    def n(self):
        return len(self.x)

    @property
    def x_mean(self):
        return sum(self.x)/self.n

    @property
    def y_mean(self):
        return sum(self.y)/self.n

    @property
    def x_var(self):
        count = sum([(num - self.x_mean)**2 for num in self.x])
        return count/self.n

    @property
    def y_var(self):
        count = sum([(num - self.y_mean)**2 for num in self.y])
        return count/self.n

    @property
    def xy(self):
        xy = sum([tupla[0] * tupla[1] for tupla in zip(self.x, self.y)])
        return xy

    @property
    def cov(self):
        return (self.xy / self.n) - (self.x_mean * self.y_mean)




test = Statistics([7,11], [9,8])
test2 = Statistics([20,19], [9,8])


print(test.cov)