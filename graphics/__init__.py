import pygame
from entity import Entity


class TestSimulation:
    def __init__(self, width: int = 800, height: int = 600):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Prueba de Entity - Física y Colisiones")
        self.clock = pygame.time.Clock()
        self.running = True

        # Entidad móvil (controlada con teclado)
        self.player = Entity(
            x=self.width / 2,
            y=self.height / 2,
            color=(220, 50, 50),
            mass=100.0,
            width=50,
            height=25,
            is_static=False
        )

        # Entidad estática (muro fijo)
        self.obstacle = Entity(
            x=250,
            y=250,
            color=(50, 150, 220),
            width=40,
            height=40,
            is_static=True
        )

        # Segunda entidad móvil (para probar transferencia de impulso)
        self.other_car = Entity(
            x=550,
            y=300,
            color=(50, 200, 100),
            mass=15.0,
            width=50,
            height=30,
            is_static=False
        )

        # Segunda entidad móvil (para probar transferencia de impulso)
        self.other_other_car_ = Entity(
            x=550,
            y=400,
            color=(50, 100, 10),
            mass=1.0,
            width=50,
            height=30,
            is_static=False
        )

        self.entities = [self.player, self.obstacle, self.other_car, self.other_other_car_]

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()

        base_force = 80000.0
        force_increase_per_sec = 20000.0
        max_force = 200000.0

        moving = (
                keys[pygame.K_RIGHT] or keys[pygame.K_d] or
                keys[pygame.K_LEFT] or keys[pygame.K_a] or
                keys[pygame.K_DOWN] or keys[pygame.K_s] or
                keys[pygame.K_UP] or keys[pygame.K_w]
        )

        if moving:
            now = pygame.time.get_ticks()
            if self.move_start_time is None:
                self.move_start_time = now
            elapsed_seconds = (now - self.move_start_time) / 1000.0
        else:
            self.move_start_time = None
            elapsed_seconds = 0.0

        force_magnitude = min(base_force + (elapsed_seconds * force_increase_per_sec), max_force)

        fx, fy = 0.0, 0.0
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            fx += force_magnitude
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            fx -= force_magnitude
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            fy += force_magnitude
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            fy -= force_magnitude

        self.player.apply_force(fx, fy)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.handle_input()

            # 1. Actualizar física y colisión con los bordes de la ventana
            for ent in self.entities:
                ent.update(dt, drag=0.96)
                ent.check_collider_window(self.width, self.height)

            # 2. Detectar y resolver colisiones entre todos los pares
            for i in range(len(self.entities)):
                for j in range(i + 1, len(self.entities)):
                    ent_a = self.entities[i]
                    ent_b = self.entities[j]
                    if ent_a.is_colliding_with_other_entity(ent_b):
                        ent_a.resolve_collision_with_other_entity(ent_b, coef_impact=0.8)

            # 3. Renderizar
            self.screen.fill((30, 30, 35))
            for ent in self.entities:
                ent.draw(self.screen)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    sim = TestSimulation()
    sim.run()