# KULLANIMA HAZIR DEĞİL
# PYGAME SIRALI LİSTE OLUŞTURMA TESTİ - CHAT KISMI İÇİN
import pygame, pygame.font
from pygame.locals import *
import os.path

def command_file_master(screen):
	font = pygame.font.Font(None, 15)
	(screen_pause, place, marker) = (0, 0, 0)
	x = []
	f = open("filelist") 
	file_names = f.readlines()
	if len(file_names) == 0:
		return (file_names, x, 1, place, marker)
	f.close()
	for count in range(len(file_names)):
		"get rid of any newlines in the list names"
		file_names[count] = file_names[count].strip()
	while 1:
		event = pygame.event.poll()
		if screen_pause == 1:
			while 1:
				event = pygame.event.wait()
				cursor = pygame.mouse.get_pos()
				if event.type == QUIT:
					raise SystemExit
				if event.type == MOUSEBUTTONDOWN and\
				pygame.mouse.get_pressed()[0]:
					for item in x:
						if item[0].collidepoint(cursor):
							print('you clicked ', item[1])
				if event.type == KEYDOWN and event.key == K_SPACE:
					print('space bar hit')
					if not place >= len(file_names):
						screen_pause = 0
						marker = 0
						x = []
						break
				if event.type == KEYDOWN and event.key == K_BACKSPACE:
					print('backspace hit')
					if ((place - marker) > 0):
						screen.fill(0)
						pygame.display.flip()
						screen_pause = 0
						place -= (165 + marker)
						marker = 0
						x = [] 
						break
		(file_names, x, screen_pause, place, marker) = file_master(screen,\
		font, file_names, place, marker, x)
		pygame.time.delay(5)


def file_master(screen, font, file_names, place, marker, x):
	screen.fill((0, 0, 0, 0))
	pygame.display.update()

	font_height = font.size(file_names[0])[1]
	screen_height = screen.get_height()
	max_file_width = 116
	name_max = 16 # how many maximum characters a list name can be 
	line = 65 # leave room at top of screen for other stuff
	col = 30 # where to start the first column
	count = 0
	for name in file_names[place:]:
		count += 1
		place += 1
		marker += 1
		if count >= 165 or place >= len(file_names):
			ren_name = os.path.basename(name)
			if len(ren_name) > name_max:
				ren_name = ren_name[:name_max] + '~'
			ren = font.render(ren_name, 1, (255, 255, 255), (0, 0, 0))
			ren_rect = ren.get_rect()
			ren_rect[0] = col
			ren_rect[1] = line
			x.append((ren_rect, name))
			screen.blit(ren, ren_rect)
			pygame.display.update(ren_rect)
			print('space for next page, backspace for last page')
			return (file_names, x, 1, place, marker)
		ren_name = os.path.basename(name)
		if len(ren_name) > name_max:
			ren_name = ren_name[:name_max] + '~'
		ren = font.render(ren_name, 1, (255, 255, 255), (0, 0, 0))
		ren_rect = ren.get_rect()
		ren_rect[0] = col
		ren_rect[1] = line
		x.append((ren_rect, name))
		screen.blit(ren, ren_rect)
		line += 12
		if (line + font_height) >= (screen_height - 15):
			line = 65
			col += max_file_width
		pygame.display.update(ren_rect)
	return (file_names, x, 0, place, marker)


def main():
	pygame.init()
	screen = pygame.display.set_mode((640, 480))
	print('hit i to start')
	while 1:
		event = pygame.event.wait()
		if event.type == QUIT:
			break
		if event.type == KEYDOWN and event.key == K_i:
			command_file_master(screen)
	pygame.quit()


if __name__=='__main__': main()
