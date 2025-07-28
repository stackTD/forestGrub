import pygame
import random
import sys
import os
import math

# Initialize Pygame
pygame.init()

# Try to import sound generator
try:
    from sounds.sound_generator import generate_jump_sound, generate_hit_sound, generate_point_sound
    SOUNDS_AVAILABLE = True
except ImportError:
    SOUNDS_AVAILABLE = False
    print("Sound generation not available. Running in silent mode.")

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 50
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 128, 0)
BROWN = (139, 69, 19)
BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

# Game states
RUNNING = 0
GAME_OVER = 1

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.ground_y = y
        self.jump_height = 120
        self.velocity_y = 0
        self.gravity = 0.8
        self.jump_strength = -15
        self.is_jumping = False
        self.is_ducking = False
        self.duck_height = 30
        self.animation_frame = 0
        self.run_animation_speed = 0.2
        
    def jump(self):
        if not self.is_jumping and not self.is_ducking:
            self.is_jumping = True
            self.velocity_y = self.jump_strength
    
    def duck(self):
        if not self.is_jumping:
            self.is_ducking = True
    
    def stop_duck(self):
        self.is_ducking = False
    
    def update(self):
        # Handle jumping physics
        if self.is_jumping:
            self.velocity_y += self.gravity
            self.y += self.velocity_y
            
            # Land on ground
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.velocity_y = 0
        
        # Update animation
        if not self.is_jumping:
            self.animation_frame += self.run_animation_speed
    
    def get_rect(self):
        if self.is_ducking:
            return pygame.Rect(self.x, self.y + (self.height - self.duck_height), 
                             self.width, self.duck_height)
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        rect = self.get_rect()
        
        # Draw dinosaur body
        if self.is_ducking:
            # Draw ducking dinosaur (oval shape)
            pygame.draw.ellipse(screen, GREEN, rect)
        else:
            # Draw standing dinosaur
            pygame.draw.rect(screen, GREEN, rect, border_radius=5)
            
            # Draw head
            head_size = 15
            head_rect = pygame.Rect(rect.x + rect.width - head_size, rect.y - head_size//2, 
                                  head_size, head_size)
            pygame.draw.ellipse(screen, GREEN, head_rect)
        
        # Draw eye
        eye_x = rect.x + rect.width - 8
        eye_y = rect.y + 8 if not self.is_ducking else rect.y + 5
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), 2)
        
        # Draw legs with animation (simple running effect)
        if not self.is_jumping and not self.is_ducking:
            leg_offset = int(math.sin(self.animation_frame) * 3)
            leg1_y = rect.y + rect.height
            leg2_y = rect.y + rect.height
            
            # Left leg
            pygame.draw.line(screen, DARK_GREEN, 
                           (rect.x + 10, leg1_y), 
                           (rect.x + 8 + leg_offset, leg1_y + 15), 3)
            # Right leg  
            pygame.draw.line(screen, DARK_GREEN, 
                           (rect.x + 20, leg2_y), 
                           (rect.x + 22 - leg_offset, leg2_y + 15), 3)
        
        # Draw tail
        tail_points = [
            (rect.x, rect.y + rect.height//2),
            (rect.x - 10, rect.y + rect.height//2 - 5),
            (rect.x - 8, rect.y + rect.height//2 + 5)
        ]
        pygame.draw.polygon(screen, DARK_GREEN, tail_points)

class Obstacle:
    def __init__(self, x, obstacle_type):
        self.x = x
        self.type = obstacle_type  # 'cactus' or 'bird'
        self.speed = 8
        
        if self.type == 'cactus':
            self.width = 20
            self.height = random.randint(40, 70)
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.height
            self.color = GREEN
            self.spikes = random.randint(3, 6)
        else:  # bird
            self.width = 30
            self.height = 20
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(60, 120)  # Random flying height
            self.color = GRAY
            self.wing_animation = 0
    
    def update(self):
        self.x -= self.speed
        if self.type == 'bird':
            self.wing_animation += 0.3
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, screen):
        rect = self.get_rect()
        
        if self.type == 'cactus':
            # Draw cactus body
            pygame.draw.rect(screen, self.color, rect, border_radius=3)
            
            # Draw spikes
            for i in range(self.spikes):
                spike_y = rect.y + (i * rect.height // self.spikes)
                # Left spikes
                pygame.draw.polygon(screen, DARK_GREEN, [
                    (rect.x - 3, spike_y),
                    (rect.x - 8, spike_y + 5),
                    (rect.x - 3, spike_y + 10)
                ])
                # Right spikes
                pygame.draw.polygon(screen, DARK_GREEN, [
                    (rect.x + rect.width + 3, spike_y + 5),
                    (rect.x + rect.width + 8, spike_y + 10),
                    (rect.x + rect.width + 3, spike_y + 15)
                ])
        else:  # bird
            # Draw bird body
            pygame.draw.ellipse(screen, self.color, rect)
            
            # Draw animated wings
            wing_flap = math.sin(self.wing_animation) * 5
            # Left wing
            pygame.draw.ellipse(screen, BLACK, 
                              (rect.x - 5, rect.y + 5 + wing_flap, 8, 10))
            # Right wing
            pygame.draw.ellipse(screen, BLACK, 
                              (rect.x + rect.width - 3, rect.y + 5 - wing_flap, 8, 10))
            
            # Draw beak
            pygame.draw.polygon(screen, ORANGE, [
                (rect.x + rect.width, rect.y + rect.height//2),
                (rect.x + rect.width + 8, rect.y + rect.height//2 - 2),
                (rect.x + rect.width + 8, rect.y + rect.height//2 + 2)
            ])

class Ground:
    def __init__(self):
        self.x = 0
        self.speed = 8
        self.dust_particles = []
        
    def update(self):
        self.x -= self.speed
        if self.x <= -20:
            self.x = 0
        
        # Update dust particles
        for particle in self.dust_particles[:]:
            particle['x'] -= self.speed
            particle['life'] -= 1
            if particle['life'] <= 0 or particle['x'] < 0:
                self.dust_particles.remove(particle)
        
        # Add new dust particles randomly
        if random.randint(1, 10) == 1:
            self.dust_particles.append({
                'x': SCREEN_WIDTH + random.randint(0, 50),
                'y': SCREEN_HEIGHT - GROUND_HEIGHT - random.randint(0, 10),
                'life': random.randint(20, 40)
            })
    
    def draw(self, screen):
        # Draw ground
        ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)
        pygame.draw.rect(screen, BROWN, ground_rect)
        
        # Draw ground pattern with more detail
        for i in range(0, SCREEN_WIDTH + 40, 20):
            x = (i + self.x) % (SCREEN_WIDTH + 40)
            if x < SCREEN_WIDTH:
                # Draw ground texture lines
                pygame.draw.line(screen, BLACK, (x, SCREEN_HEIGHT - GROUND_HEIGHT), 
                               (x + 10, SCREEN_HEIGHT - GROUND_HEIGHT + 5), 2)
                # Draw small rocks
                if random.randint(1, 20) == 1:
                    rock_size = random.randint(2, 4)
                    pygame.draw.circle(screen, GRAY, 
                                     (x + random.randint(0, 20), 
                                      SCREEN_HEIGHT - GROUND_HEIGHT + random.randint(5, 15)), 
                                     rock_size)
        
        # Draw dust particles
        for particle in self.dust_particles:
            alpha = particle['life'] / 40.0
            dust_color = (139 + int(50 * alpha), 69 + int(50 * alpha), 19 + int(50 * alpha))
            pygame.draw.circle(screen, dust_color, 
                             (int(particle['x']), int(particle['y'])), 2)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dinosaur Game")
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.dinosaur = Dinosaur(100, SCREEN_HEIGHT - GROUND_HEIGHT - 60)
        self.ground = Ground()
        self.obstacles = []
        
        # Game state
        self.state = RUNNING
        self.score = 0
        self.high_score = 0
        self.speed_increase_timer = 0
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = 90  # frames
        self.base_speed = 8
        self.current_speed = self.base_speed
        
        # Visual effects
        self.day_night_cycle = 0
        self.sky_color = BLUE
        
        # Font for text
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Load sounds
        self.sounds = {}
        if SOUNDS_AVAILABLE:
            try:
                self.sounds['jump'] = generate_jump_sound()
                self.sounds['hit'] = generate_hit_sound()
                self.sounds['point'] = generate_point_sound()
                print("Sounds loaded successfully")
            except Exception as e:
                print(f"Could not load sounds: {e}")
                self.sounds = {}
        
    def play_sound(self, sound_name):
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass  # Ignore sound errors
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if self.state == RUNNING:
                    if event.key == pygame.K_SPACE:
                        self.dinosaur.jump()
                        self.play_sound('jump')
                    elif event.key == pygame.K_c:
                        self.dinosaur.duck()
                elif self.state == GAME_OVER:
                    if event.key == pygame.K_SPACE:
                        self.restart_game()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_c:
                    self.dinosaur.stop_duck()
        
        return True
    
    def update(self):
        if self.state == RUNNING:
            # Update score
            self.score += 1
            
            # Progressive difficulty
            self.speed_increase_timer += 1
            if self.speed_increase_timer >= 300:  # Every 5 seconds
                self.current_speed += 0.5
                self.speed_increase_timer = 0
                if self.obstacle_spawn_delay > 30:
                    self.obstacle_spawn_delay -= 2
            
            # Update day/night cycle
            self.day_night_cycle += 0.02
            cycle_pos = (math.sin(self.day_night_cycle) + 1) / 2
            
            # Interpolate sky color from day to night
            day_r, day_g, day_b = BLUE
            night_r, night_g, night_b = (25, 25, 112)  # Midnight blue
            
            self.sky_color = (
                int(day_r + (night_r - day_r) * cycle_pos),
                int(day_g + (night_g - day_g) * cycle_pos),
                int(day_b + (night_b - day_b) * cycle_pos)
            )
            
            # Update game objects
            self.dinosaur.update()
            self.ground.speed = self.current_speed
            self.ground.update()
            
            # Play point sound every 100 points
            if self.score > 0 and self.score % 100 == 0:
                self.play_sound('point')
            
            # Spawn obstacles
            self.obstacle_spawn_timer += 1
            if self.obstacle_spawn_timer >= self.obstacle_spawn_delay:
                obstacle_type = random.choice(['cactus', 'bird', 'cactus'])  # More cacti than birds
                new_obstacle = Obstacle(SCREEN_WIDTH, obstacle_type)
                new_obstacle.speed = self.current_speed
                self.obstacles.append(new_obstacle)
                self.obstacle_spawn_timer = 0
            
            # Update obstacles
            for obstacle in self.obstacles[:]:
                obstacle.speed = self.current_speed
                obstacle.update()
                if obstacle.x + obstacle.width < 0:
                    self.obstacles.remove(obstacle)
            
            # Check collisions
            dinosaur_rect = self.dinosaur.get_rect()
            for obstacle in self.obstacles:
                if dinosaur_rect.colliderect(obstacle.get_rect()):
                    self.state = GAME_OVER
                    self.play_sound('hit')
                    if self.score > self.high_score:
                        self.high_score = self.score
    
    def draw(self):
        # Clear screen with dynamic sky color
        self.screen.fill(self.sky_color)
        
        if self.state == RUNNING:
            # Draw game objects
            self.ground.draw(self.screen)
            self.dinosaur.draw(self.screen)
            
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Draw score
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            high_score_text = self.small_font.render(f"High Score: {self.high_score}", True, BLACK)
            self.screen.blit(high_score_text, (10, 50))
            
            # Draw speed indicator
            speed_text = self.small_font.render(f"Speed: {self.current_speed:.1f}", True, BLACK)
            self.screen.blit(speed_text, (10, 75))
            
            # Draw controls hint
            controls_text = self.small_font.render("SPACE: Jump | C: Duck", True, BLACK)
            self.screen.blit(controls_text, (SCREEN_WIDTH - 200, 10))
            
        elif self.state == GAME_OVER:
            # Draw game over screen
            self.ground.draw(self.screen)
            self.dinosaur.draw(self.screen)
            
            for obstacle in self.obstacles:
                obstacle.draw(self.screen)
            
            # Game over overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            
            # Game over text
            game_over_text = self.font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(game_over_text, text_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            text_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(score_text, text_rect)
            
            if self.score == self.high_score and self.score > 0:
                new_record_text = self.small_font.render("NEW HIGH SCORE!", True, ORANGE)
                text_rect = new_record_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
                self.screen.blit(new_record_text, text_rect)
            
            restart_text = self.font.render("Press SPACE to restart", True, WHITE)
            text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(restart_text, text_rect)
        
        pygame.display.flip()
    
    def restart_game(self):
        self.dinosaur = Dinosaur(100, SCREEN_HEIGHT - GROUND_HEIGHT - 60)
        self.obstacles = []
        self.score = 0
        self.obstacle_spawn_timer = 0
        self.obstacle_spawn_delay = 90
        self.current_speed = self.base_speed
        self.speed_increase_timer = 0
        self.day_night_cycle = 0
        self.sky_color = BLUE
        self.state = RUNNING
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()