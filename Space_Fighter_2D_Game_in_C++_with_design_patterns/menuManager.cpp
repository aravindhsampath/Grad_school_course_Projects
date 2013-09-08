#include <cmath>
#include <sstream>
#include "menuManager.h"
#include "manager.h"

MenuManager::MenuManager() :
  env( SDL_putenv(const_cast<char*>("SDL_VIDEO_CENTERED=center")) ),
  screen1( IOManager::getInstance().getScreen() ),
  clock( Clock::getInstance() ),
  frameFactory( FrameFactory::getInstance() ),
  mbackgroundWorld(const_cast<Frame*>(frameFactory->getFrame("mbackground","background")[0]),1),
  bakColor(),
  menu(),
  numberOfStars(-1),
  helpflag(false)

{ 
  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    throw string("Unable to initialize SDL: ");
  }
  bakColor.r = Gamedata::getInstance()->getXmlInt("backgroundRed");
  bakColor.g = Gamedata::getInstance()->getXmlInt("backgroundGreen");
  bakColor.b = Gamedata::getInstance()->getXmlInt("backgroundBlue");
  atexit(SDL_Quit); 
}

void MenuManager::drawBackground() const {
  
  /*
  SDL_FillRect( screen1, NULL, 
    SDL_MapRGB(screen1->format, bakColor.r, bakColor.g, bakColor.b) );
  SDL_Rect dest = {0, 0, 0, 0};
  SDL_BlitSurface( screen1, NULL, screen1, &dest );
  */
  mbackgroundWorld.draw();
}

void MenuManager::getNumberOfStars() {
  IOManager& io = IOManager::getInstance().getInstance();
  SDL_Event event;
  bool done = false;
  bool nameDone = false;
  const string msg("How many yellow stars: ");
  io.clearString();
  while ( not done ) {
    Uint8 *keystate = SDL_GetKeyState(NULL);
    if ( SDL_PollEvent(&event) )
    switch (event.type) {
      case SDL_KEYDOWN: {
        if (keystate[SDLK_ESCAPE] || keystate[SDLK_q]) {
          done = true;
        }
        if (keystate[SDLK_RETURN]) {
          nameDone = true;
        }
        io.buildString(event);
      }
    }
    drawBackground();
    io.printStringAfterMessage(msg, 20, 120);
    if ( nameDone ) {
      std::string number = io.getString();
      std::stringstream strm;
      strm << number;
      strm >> numberOfStars;
      strm.clear(); // clear error flags
      strm.str(std::string()); // clear contents
      strm << "Okay -- you'll see " << numberOfStars << " stars";
      cout << strm.str() << endl;
      io.printMessageAt(strm.str(), 20, 160);
      SDL_Flip(screen1);
      SDL_Delay(400);
      done = true;
    }
    if ( !done ) {
      SDL_Flip(screen1);
    }
  }
}

void MenuManager::play() {
  bool keyCatch = false; // To get only 1 key per keydown
  SDL_Event event;
  bool done = false;
  std::cout<<"in play method of menuManager"<<std::endl;
  //GameManager gameMan;
  Manager gameMan;
  std::cout<<"after manager initialization"<<std::endl;
  while ( not done ) {
    if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    throw string("Unable to initialize SDL: ");
    }
    drawBackground();
    if (gameMan.getgamewon() == true){
      IOManager::getInstance().printMessageAt("!!!! You Won !!!!", 100, 30);
    }
    if (gameMan.getgameState() == true){
      IOManager::getInstance().printMessageAt("!!!!!!  GAME OVER   !!!!!", 100, 30);
      IOManager::getInstance().printMessageAt(" Score ", 100, 40);
      unsigned int score = gameMan.getscore();
      IOManager::getInstance().printMessageAt(static_cast<std::ostringstream*>(&(std::ostringstream() << score))->str(), 100, 30);

    }
    
    menu.draw();
    if (helpflag){
      IOManager::getInstance().printMessageAt("Help - Menu", 50, 280);
      IOManager::getInstance().printMessageAt("===========", 50, 290);
      IOManager::getInstance().printMessageAt("Use the arrow keys to move", 50, 305);
      IOManager::getInstance().printMessageAt("Use the space bar to shoot ", 50, 325);

    }
    SDL_Flip(screen1);

    SDL_PollEvent(&event);
    if (event.type ==  SDL_QUIT) { break; }
    if(event.type == SDL_KEYDOWN) {
      switch ( event.key.keysym.sym ) {
        case SDLK_ESCAPE :
        case SDLK_q : {
          done = true;
          break;
        }
        case SDLK_RETURN : {
          if ( !keyCatch ) {
            menu.lightOn();
            if ( menu.getIconClicked() == "Start Game" ) {
              if (gameMan.getgameState() == true) gameMan.setscore(0);
              gameMan.setgamewon(false);
              gameMan.setgameState(false);
              
              gameMan.play();
            }
            if ( menu.getIconClicked() == "Exit" ) {
              drawBackground();
              menu.draw();
              SDL_Flip(screen1);
              SDL_Delay(250);
              done = true;
            }
            if ( menu.getIconClicked() == "Help" ) {
              drawBackground();
              helpflag = true;
              menu.draw();
              SDL_Flip(screen1);
              //SDL_Delay(250);
            }
            if ( menu.getIconClicked() == "Parameters" ) {
              getNumberOfStars();
              //gameMan.setNumberOfStars( numberOfStars );
            }
          }
          break;
        }
        case SDLK_DOWN   : {
          if ( !keyCatch ) {
            menu.increment();
          }
          break;
        }
        case SDLK_UP   : {
          if ( !keyCatch ) {
            menu.decrement();
          }
          break;
        }
        default          : break;
      }
      keyCatch = true;
    }
    if(event.type == SDL_KEYUP) { 
      keyCatch = false; 
      menu.lightOff();
    }
  }
}
