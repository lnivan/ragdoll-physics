import numpy as np



class Physics_System:

    def __init__(self, gravity=9.81):

        self.points = []
        self.spring_damper_joints = []
        self.fixed_joints = []  
        self.gravity = gravity


    class Point:

        def __init__(self, r, mass, radius, gravity=True):

            #Point properties and variables
            self.r = r
            self.v = np.array([0.0, 0.0])
            self.a = np.array([0.0, 0.0])
            self.f = np.array([0.0, 0.0])

            self.mass = mass
            self.radius = radius
            self.gravity = gravity

        def update(self, dt):

            #Take force and update point variables in a time step
            self.a = self.f / self.mass
            self.v = self.v + self.a * dt
            self.r = self.r + self.v * dt

            #################################
            if self.r[1] < 0:
                self.r[1] = 0
                self.v[0] = self.v[0] * 0.5
            #################################

            self.f = np.array([0.0, 0.0])        
    
        def add_force(self, force):

            self.f = self.f + force

    def add_point(self, r, mass, width, gravity=True):

        self.points.append(Physics_System.Point(r, mass, width, gravity))
        return(self.points[-1])


    class Spring:

        def __init__(self, point1, point2, rest_length, k):

            self.point1 = point1
            self.point2 = point2
            self.rest_length = rest_length
            self.k = k

        def update(self):

            # Calculate spring force
            dr = self.point2.r - self.point1.r
            distance = np.linalg.norm(dr)

            if distance > 0:
                direction = dr / distance
                force_magnitude = self.k * (distance - self.rest_length)
                force = direction * force_magnitude

                # Apply forces to the points
                self.point1.add_force(force)
                self.point2.add_force(-force)


    class Damper:

        def __init__(self, point1, point2, c):

            self.point1 = point1
            self.point2 = point2
            self.c = c

        def update(self):

            # Calculate damping force
            dv = self.point2.v - self.point1.v
            dr = self.point2.r - self.point1.r
            distance = np.linalg.norm(dr)

            if distance > 0:
                direction = dr / distance
                relative_velocity = np.dot(dv, direction)
                damping_force_magnitude = self.c * relative_velocity
                damping_force = direction * damping_force_magnitude

                # Apply forces to the points
                self.point1.add_force(damping_force)
                self.point2.add_force(-damping_force)

    
    class Spring_Damper_Joint:

        def __init__(self, point1, point2, rest_length, k, c):

            self.spring = Physics_System.Spring(point1, point2, rest_length, k)
            self.damper = Physics_System.Damper(point1, point2, c)

            self.point1 = point1
            self.point2 = point2
            self.rest_length = rest_length
            self.k = k
            self.c = c

        def update(self):

            self.spring.update()
            self.damper.update()

    def add_spring_damper_joint(self, point1, point2, rest_length, k, c):

        self.spring_damper_joints.append(Physics_System.Spring_Damper_Joint(point1, point2, rest_length, k, c))
        return(self.spring_damper_joints[-1])


    class Fixed_Joint:

        def __init__(self, point1, point2, length):

            self.point1 = point1
            self.point2 = point2
            self.length = length

        def update(self):
            
            dr = self.point2.r - self.point1.r
            distance = np.linalg.norm(dr)

            if distance > 0:
                direction = dr / distance
                '''# Move points to maintain fixed length
                displacement = self.length - distance
                self.point1.r = self.point1.r - direction * displacement * self.point2.mass / (self.point1.mass + self.point2.mass)
                self.point2.r = self.point2.r + direction * displacement * self.point1.mass / (self.point1.mass + self.point2.mass)
'''
            #Calculate tension force
            dv = self.point2.v - self.point1.v
            t = (np.dot(dv, dv) + np.dot(dr, (self.point2.f/self.point1.mass - self.point1.f/self.point1.mass)))/(self.length*(1/self.point1.mass + 1/self.point2.mass))
            tension_force = direction * t
            
            self.point1.add_force(tension_force)
            self.point2.add_force(-tension_force)





    def add_fixed_joint(self, point1, point2, length):

        self.fixed_joints.append(Physics_System.Fixed_Joint(point1, point2, length))
        return(self.fixed_joints[-1])


    def update(self, dt):

        # Apply gravity to points
        for point in self.points:
            if point.gravity:
                point.add_force(np.array([0.0, -point.mass * self.gravity]))

        #Apply air friction to points
        for point in self.points:
            point.add_force(-0.3 * point.v)

        #Update spring-damper joints
        for joint in self.spring_damper_joints: 
            joint.update()

        #update fixed joints 
        for joint in self.fixed_joints: 
            joint.update()

        # Update points
        for point in self.points:
            point.update(dt)