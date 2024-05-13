import pygame
import numpy as np

class OBJLoader:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []
        self.load_obj(filename)

    def load_obj(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    self.vertices.append([float(x) for x in line.split()[1:]])
                elif line.startswith('f '):
                    face = []
                    for v in line.split()[1:]:
                        face.append(int(v.split('/')[0]) - 1)
                    self.faces.append(face)

class PerspectiveRenderer:
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.width = width
        self.height = height

    def project_point(self, point, camera_distance=-200):
        x, y, z = point
        # Simple perspective projection
        projected_x = x / (z + camera_distance) * self.width + self.width / 2
        projected_y = y / (z + camera_distance) * self.height + self.height / 2
        return projected_x, projected_y

    def render_obj(self, obj):
        self.screen.fill((0, 0, 0))  # Clear screen
        for face in obj.faces:
            points = [obj.vertices[i] for i in face]
            projected_points = [self.project_point(p) for p in points]
            pygame.draw.polygon(self.screen, (255, 255, 255), projected_points, 1)
        pygame.display.flip()

    def run(self, obj, compression_speed=0.1):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Compress the object
            compress_obj(obj, compression_speed)

            self.render_obj(obj)
            self.clock.tick(60)  # Limit frame rate to 60 FPS

        pygame.quit()







class BouncyTeapot:
    def __init__(self, obj, k=2, gravity=4, spring_constant=10, damping_factor=0.2,max_compression=0.8, max_extension=0.8):
        self.obj = obj
        self.velocities = [[0, 0, 0] for _ in obj.vertices]
        self.k = k  # Height of the ground
        self.gravity = gravity
        self.spring_constant = spring_constant
        self.damping_factor = damping_factor
        self.original_heights = [v[1] for v in obj.vertices]
        self.max_compression = max_compression
        self.max_extension = max_extension
    def apply_forces(self):
        for i, vertex in enumerate(self.obj.vertices):
            # Gravity
            self.velocities[i][1] += self.gravity

            # Hooke's Law (Ground collision)
            if vertex[1] < self.k:
                compression = self.original_heights[i] - vertex[1]
                if compression > self.max_compression:
                    force = self.spring_constant * (self.max_compression - compression)
                    self.velocities[i][1] += force
                    self.velocities[i][1] *= self.damping_factor
            else: # Apply extension limit
                extension = vertex[1] - self.original_heights[i]
                if extension > self.max_extension:
                    force = -self.spring_constant * (extension - self.max_extension) # Opposite direction
                    self.velocities[i][1] += force
                    self.velocities[i][1] *= self.damping_factor 
                    
            # Update vertex position based on velocity
            self.obj.vertices[i][0] += self.velocities[i][0]
            self.obj.vertices[i][1] += self.velocities[i][1]
            self.obj.vertices[i][2] += self.velocities[i][2]

if __name__ == "__main__":
    obj_file = "scout.obj"  # Replace with your OBJ file
    obj = OBJLoader(obj_file)
    renderer = PerspectiveRenderer(800, 600)
    bouncy_teapot = BouncyTeapot(obj, k=-2, max_compression=0.6, max_extension=0.7) 

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        # ... (same as before) ...

        # Apply physics
        bouncy_teapot.apply_forces()

        renderer.render_obj(bouncy_teapot.obj)
        renderer.clock.tick(3)  # Limit frame rate to 60 FPS

    pygame.quit()
