
ifeq ("$(shell whoami)", "malloy")
  CXX = clang++
else
  CXX = g++
endif
CXX_LINK = g++

# Warnings frequently signal eventual errors:
CXXFLAGS=`sdl-config --cflags` -g -W -Wall -Weffc++ -Wextra -pedantic -O0
LDFLAGS = `sdl-config --libs` -lSDL_ttf -lSDL_image -lexpat -lSDL_mixer

OBJS = \
	main.o \
	viewport.o \
	world.o \
	manager.o \
	gamedata.o \
	parseXML.o \
	parseLsysXML.o \
	menu.o \
	menuManager.o \
	clock.o \
	vector2f.o \
	frame.o \
	Framefactory.o \
	sprite.o \
	multisprite.o \
	aaline.o \
	sound.o \
	lsystem.o \
	explodingSprite.o \
	chunk.o \
	shootingmanager.o \
	collisionStrategy.o \
	ioManager.o

EXEC = run

# $< refers to the first dependency
%.o: %.cpp
	$(CXX_LINK) $(CXXFLAGS) -c $< -o $@

# $@ refers to the target
$(EXEC): $(OBJS)
	g++ $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS)

main.o: main.cpp
manager.o: manager.cpp manager.h gamedata.h ioManager.h sprite.h clock.h multisprite.h drawable.h lsystem.h Framefactory.h collisionStrategy.h
collisionStrategy.o: collisionStrategy.h
ioManager.o: ioManager.cpp ioManager.h gamedata.h
viewport.o: viewport.cpp viewport.h drawable.h multisprite.h
Framefactory.o: Framefactory.h Framefactory.cpp factory.h frame.h
aaline.o: aaline.cpp aaline.h
lsystem.o: lsystem.cpp lsystem.h aaline.h ioManager.h parseLsysXML.h
world.o: world.cpp world.h
parseXML.o: parseXML.cpp parseXML.h
parseLsysXML.o: parseLsysXML.cpp parseLsysXML.h
gamedata.o: gamedata.cpp gamedata.h parseXML.h
spriteFactory.o: spriteFactory.cpp spriteFactory.h factory.h frame.h
menuManager.o: menuManager.cpp menuManager.h
menu.o: menu.cpp menu.h frame.h
clock.o: clock.cpp clock.h
vector2f.o: vector2f.cpp vector2f.h
frame.o: frame.cpp frame.h
sound.o: sound.cpp sound.h
sprite.o: sprite.cpp sprite.h drawable.h frame.h Framefactory.h
shootingmanager.o: shootingmanager.h manager.h
multisprite.o: multisprite.cpp multisprite.h drawable.h frame.h gamedata.h ioManager.h Framefactory.h
frame.o: frame.cpp frame.h ioManager.h
explodingSprite.o: explodingSprite.cpp explodingSprite.h chunk.h
chunk.o: chunk.cpp chunk.h sprite.h gamedata.h

clean:
	rm -rf $(OBJS)
	rm -rf $(EXEC)
