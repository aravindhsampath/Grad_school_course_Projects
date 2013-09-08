#ifndef MENUMANAGER__H
#define MENUMANAGER__H
#include <SDL.h>
#include "world.h"
#include "Framefactory.h"
#include <iostream>
#include <string>
using std::cout; using std::endl; 
using std::string;

#include "ioManager.h"
#include "menu.h"
#include "clock.h"

class MenuManager {
public:
  MenuManager ();
  void play();
  int getStars() const { return numberOfStars; }
  virtual ~MenuManager() { std::cout << "menu manager"<<std::endl;} 

private:
  bool env;
  SDL_Surface *screen1;
  const Clock& clock;
  FrameFactory* frameFactory;
  World mbackgroundWorld;
  SDL_Color bakColor;
  Menu menu;
  int numberOfStars;
  bool helpflag;

  void drawBackground() const;
  MenuManager(const MenuManager&);
  MenuManager& operator=(const MenuManager&);
  void getNumberOfStars();
};
#endif
