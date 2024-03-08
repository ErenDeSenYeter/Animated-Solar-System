### source: https://www.youtube.com/watch?v=WTLPmUHTPqo&t=250s


import pygame
import math
pygame.init()

clock_ticks_per_second = 60  # 60  speeds up?

WIDTH, HEIGHT =  1000, 1000  # (0,0) point in the screen is top left corner. 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
DARK_BLUE = (100, 9, 250)
GRAY = (127, 127, 170)
RED = (188, 39, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PALE_GREEN =(152, 251, 152)

FONT = pygame.font.SysFont(" Comic Sans", 16)  # Arial , Comic Sans, Times New Roman

class Planet:
	AU = 149.6e6 * 1000  # Astronomical Units, distance to the earth to sun / 1000 makes is M from  KM
	G = 6.67428e-11      # Gravity
	SCALE = 125 / AU     # Fits the great distances into our Window /1AU = 100 pixels
	TIMESTEP = 3600*24   # Number of seconds in a hour / makes it 1 Day at a time 

	def __init__(self, x, y, radius, color, mass, nameP):# focus on moon ? / sun will rotate 
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.mass = mass
		self.nameP = nameP

		self.orbit = []  # The line comes behind the Planet
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0  # velocity = speed  
		self.y_vel = 0

	def draw(self, win):   # Makes the Center of the screen, avaliable to draw
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
		if not self.sun:
			nameP_text = FONT.render(self.nameP,2,WHITE)  # Writes the name
			win.blit(nameP_text, (x - nameP_text.get_width()/2, y - nameP_text.get_height()/2 - self.radius - 5))

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, self.color, False, updated_points, 2)

		pygame.draw.circle(win, self.color, (x, y), self.radius)
		
		#if not self.sun:   # Writes the distance                Writes to KM
		#	distance_text = FONT.render(f"{round(self.distance_to_sun/10000000, 1)}km", 1, WHITE)
		#	win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))


	def attraction(self, other):
		other_x, other_y = other.x, other.y
		distance_x = other_x - self.x
		distance_y = other_y - self.y
		distance = math.sqrt(distance_x ** 2 + distance_y ** 2) #Calculated distance between two objects

		if other.sun:
			self.distance_to_sun = distance

		force = self.G * self.mass * other.mass / distance**2   #force of attrection formula
		theta = math.atan2(distance_y, distance_x) #angle
		force_x = math.cos(theta) * force
		force_y = math.sin(theta) * force
		return force_x, force_y

	def update_position(self, planets):
		total_fx = total_fy = 0
		for planet in planets:
			if self == planet:
				continue

			fx, fy = self.attraction(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.mass * self.TIMESTEP
		self.y_vel += total_fy / self.mass * self.TIMESTEP  #Finding x and y velocity
        
        #F = m / a 
        #a = f / m

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))

def main():
    run = True
    paused = False
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, nameP= "Sun")# (x, y, radius, color,  mass)
    sun.sun = True                                  # x makes it further 

    mercury = Planet(0.387 * Planet.AU, 0, 8, ORANGE, mass =  3.30 * 10**23,nameP= "Mercury")
    mercury.y_vel = -47.4 * 1000 
	
    venus = Planet(0.723 * Planet.AU, 0, 14, PALE_GREEN , mass =  4.8685 * 10**24, nameP="Venus")
    venus.y_vel = -35.02 * 1000

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, mass =  5.9742 * 10**24, nameP="Venus")
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, mass =  6.39 * 10**23, nameP="Mars")
    mars.y_vel = 24.077 * 1000

    jupiter = Planet(-2 * Planet.AU, 0, 20, ORANGE, mass = 1.898 * 10**23, nameP="Jupiter")
    jupiter.y_vel = 21.1 * 1000 # y ekseninde gidicegi yüksekligi belirliyor

    saturn = Planet(-2.5 * Planet.AU, 0, 15, GRAY, mass =  5.68 * 10**23, nameP="Saturn")
    saturn.y_vel = 19.1* 1000
	
    uranus = Planet(-3 * Planet.AU, 0, 11, DARK_BLUE, mass =  8.68 * 10**23,nameP="Uranus")
    uranus.y_vel = 17.3 * 1000
	
    neptune = Planet(-3.24 * Planet.AU, 0, 9, BLUE, 10.2 * 10**23,nameP="Neptune")
    neptune.y_vel = 16.8 * 1000
    
    planets = [sun,  mercury, venus,earth, mars, jupiter, saturn, uranus, neptune]
    
    while run:
        clock.tick(clock_ticks_per_second )
        #WINDOW.fill(WHITE) #Fills the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused  # Pauses when the Space key is pressed
                elif event.key == pygame.K_ESCAPE:
                    run = False  # Exit when the Esc key is pressed
        
        if not paused:
            WINDOW.fill((0, 0, 0))
            pygame.draw.line(WINDOW, WHITE, (0, HEIGHT/2), (WIDTH, HEIGHT/2))
            pygame.draw.line(WINDOW, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
            for planet in planets:
                planet.update_position(planets)
                planet.draw(WINDOW)
            pygame.display.update()
    
    pygame.quit()

main()