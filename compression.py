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

    def run(self, obj, compression_speed=200.6):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Compress the object
            compress_obj(obj, compression_speed)

            self.render_obj(obj)
            self.clock.tick(14400)  # Limit frame rate to 60 FPS

        pygame.quit()

def compress_obj(obj, compression_speed):
    """Compresses the obj downwards, affecting top vertices more."""
    min_y = min(v[1] for v in obj.vertices)
    max_y = max(v[1] for v in obj.vertices)

    for i, vertex in enumerate(obj.vertices):
        # Calculate compression factor based on vertex height
        height_ratio = (vertex[1] - min_y) / (max_y - min_y)
        compression_factor = 1 - height_ratio
        obj.vertices[i][1] += compression_speed * compression_factor

if __name__ == "__main__":
    obj_file = "scout.obj"  # Replace with your OBJ file
    obj = OBJLoader(obj_file)
    renderer = PerspectiveRenderer(800, 600)
    renderer.run(obj, compression_speed=0.1)
