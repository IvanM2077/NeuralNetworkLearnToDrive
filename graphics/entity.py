import math
import numpy as np
import pygame

class Entity:
    def __init__(
        self,
        x: float,
        y: float,
        color: tuple[int, int, int],
        mass: float = 1.0,
        width: int = 20,
        height: int = 20,
        is_static: bool = False
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.angle = 0.0

        self.color = color
        self.mass = float(mass)
        self.width = width
        self.height = height
        self.is_static = bool(is_static)
        self.radius = self.get_radius()

    def get_radius(self) -> float:
        """Radio basado en la mitad del lado más pequeño."""
        if not self.width or not self.height:
            return 1.0
        return min(self.width, self.height) / 2.0

    def get_local_vertices(self) -> np.ndarray:
        """Vértices en coordenadas locales homogéneas (x, y, 1) ordenados para dibujar."""
        hw = self.width / 2.0
        hh = self.height / 2.0
        return np.array([
            [ hw,  hh, 1.0],
            [-hw,  hh, 1.0],
            [-hw, -hh, 1.0],
            [ hw, -hh, 1.0]
        ], dtype=np.float64)

    def apply_force(self, fx: float, fy: float) -> None:
        """Acumula aceleración a partir de un vector de fuerza F = (fx, fy)."""
        if not self.is_static and self.mass > 0:
            self.ax += fx / self.mass
            self.ay += fy / self.mass

    def update(self, dt: float, drag: float = 0.99) -> None:
        if self.is_static:
            return

        # 1. Actualizar velocidad (Euler semi-implícito)
        self.vx += self.ax * dt
        self.vy += self.ay * dt

        # Fricción opcional
        self.vx *= drag
        self.vy *= drag

        # 2. Actualizar posición
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 3. Actualizar ángulo de dirección si hay movimiento
        if self.vx != 0 or self.vy != 0:
            self.angle = math.atan2(self.vy, self.vx)

        # 4. Reiniciar aceleración para el siguiente frame
        self.ax = 0.0
        self.ay = 0.0

    def get_transformed_vertices(self) -> list[tuple[float, float]]:
        """Aplica la matriz homogénea 2D (rotación + traslación) a los vértices."""
        c = math.cos(self.angle)
        s = math.sin(self.angle)

        # Matriz de transformación homogénea 3x3
        T = np.array([
            [c, -s, self.x],
            [s,  c, self.y],
            [0,  0, 1.0]
        ], dtype=np.float64)

        # Multiplicamos T por cada vértice local (transpuesto para operar todo de golpe)
        local_verts = self.get_local_vertices()
        world_verts = (T @ local_verts.T).T

        # Devolvemos lista de tuplas (x, y) lista para Pygame o colisiones
        return [(float(v[0]), float(v[1])) for v in world_verts]

    def check_collider_window(self, screen_width: int, screen_height: int) -> None:
        """Colisión simple con los bordes de la ventana."""
        if self.is_static:
            return

        coef_impact = 1.0
        if self.y + self.radius >= screen_height:  # abajo
            self.y = screen_height - self.radius
            self.vy = -self.vy * coef_impact
        elif self.y - self.radius <= 0:            # arriba
            self.y = self.radius
            self.vy = -self.vy * coef_impact
        if  self.x + self.radius >= screen_width:   # derecha
            self.x = screen_width - self.radius
            self.vx = -self.vx * coef_impact
        elif self.x - self.radius <= 0:            # izquierda
            self.x = self.radius
            self.vx = -self.vx * coef_impact

    def is_colliding_with_other_entity(self, other: "Entity") -> bool:
        distance = math.hypot(self.x - other.x, self.y - other.y)
        return distance <= (self.radius + other.radius)


    def resolve_collision_with_other_entity(self, other: "Entity", coef_impact: float = 0.8) -> None:
        """Resuelve el choque físico (separación + rebote) entre dos entidades."""
        # 1. Vector distancia y vector unitario (d_hat)
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)
        min_dist = self.radius + other.radius

        if dist >= min_dist or dist == 0:
            return
        nx = dx / dist
        ny = dy / dist
        # 2. Masas inversas (w1, w2)
        inv_m1 = 0.0 if self.is_static else 1.0 / self.mass
        inv_m2 = 0.0 if other.is_static else 1.0 / other.mass
        total_inv_m = inv_m1 + inv_m2
        if total_inv_m == 0:
            return

        # 3. Velocidad relativa sobre el eje del choque (v_n)
        rvx = other.vx - self.vx
        rvy = other.vy - self.vy
        vel_along_normal = rvx * nx + rvy * ny
        if vel_along_normal > 0:
            return

        # 4. Impulso escalar (j) y vectorial (J)
        j = -(1 + coef_impact) * vel_along_normal / total_inv_m
        impulse_x = j * nx
        impulse_y = j * ny

        # 5. Nuevas velocidades
        self.vx -= impulse_x * inv_m1
        self.vy -= impulse_y * inv_m1
        other.vx += impulse_x * inv_m2
        other.vy += impulse_y * inv_m2

    def drawVectorVelocities(self,screen: pygame.Surface) -> None:
        vectorx = self.vx
        vectory = self.vy
        pygame.draw.line(screen, (255, 0, 0), (self.x, self.y), (self.x+vectorx*1, self.y+vectory*1), 2)

    def draw(self, screen: pygame.Surface) -> None:
        # Dibuja el rectángulo ya rotado usando tu matriz homogénea
        vertices = self.get_transformed_vertices()
        pygame.draw.polygon(screen, self.color, vertices)
        self.drawVectorVelocities(screen)