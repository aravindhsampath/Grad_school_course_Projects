#ifndef MANAGER__H
#define MANAGER__H
#include <SDL.h>
#include <iostream>
#include <string>
#include <vector>

#include "ioManager.h"
//#include "clock.h"
#include "menuManager.h"
#include "gamedata.h"
#include "sprite.h"
#include "multisprite.h"
#include "world.h"
#include "viewport.h"
#include "drawable.h"
#include "lsystem.h"
#include "Framefactory.h"
#include "collisionStrategy.h"
#include "explodingSprite.h"

class Manager {
public:
  Manager ();
  ~Manager ();
  void play();
  bool getgameState(){return gameoverflag;};
  void setgameState(bool gameflag){gameoverflag = gameflag;};
  bool getscore(){return score;};
  void setscore(unsigned int sc){score = sc;};
  void setgamewon(bool gw){gamewon = gw;};
  bool getgamewon(){return gamewon;};

private:
  const bool env;
  const Gamedata* gdata;
  const IOManager& io;
  FrameFactory* frameFactory;
  Clock& clock;
  ShootingManager smanager;

  SDL_Surface *screen;
  World backgroundWorld;
  //SDL_Surface * const parallaxSurface1;
  World parallaxWorld1;
  //SDL_Surface * const parallaxSurface2;
  World parallaxWorld2;
  //SDL_Surface * const parallaxSurface3;
  World parallaxWorld3;
  World parallaxWorld4;
  World parallaxWorld5;
  //World end;

  //LSystem lsystem;
  /*SDL_Surface * const lsysSurface;
  Frame * const lsysFrame; */
  //Sprite lsysSprite;


  Viewport& viewport;
  // orbs removed from first assignment - will be used in the future.
  /*
  SDL_Surface * const redSurface;
  SDL_Surface * const yellowSurface;
  Frame * const redorbFrame;
  Frame * const yelloworbFrame; */
  std::vector<Sprite> orbs;
  std::vector<MultiframeSprite> characters;
  std::vector<MultiframeSprite*> asteroids;
  std::vector<MultiframeSprite*> opponents;
  std::vector<MultiframeSprite*> ai;
  std::vector<ExplodingSprite*> explosions;
  CollisionStrategy *collisionStrategy;
  unsigned currentOrb;
  bool helpFlag;
  bool done;
  bool rightFlag;
  bool aishootflag;
  bool gameoverflag;
  bool gamewon;
  unsigned int score;


  void draw() const;
  void update(Uint32);
  void randomizeAsteroids();
  void randomizeOpponents();
  void manageCollisions();
  
  Manager(const Manager&);
  Manager& operator=(const Manager&);
};
#endif
