class Entity():
    #Positiion its a vector of points X, Y
    def __init__(self, position, mass, material):
        self.position = position
        self.mass = mass
        self.material = material

    def position(self, vector, dt):
        self.position[0] = position[0] + vector[0]*dt
        self.position[1] = position[1] + vector[1]*dt
    def velocity(self, vector, dt):
        self.velocity[0] = velocity[0] + vector[0]*dt
        self.velocity[1] = velocity[1] + vector[1]*dt


    