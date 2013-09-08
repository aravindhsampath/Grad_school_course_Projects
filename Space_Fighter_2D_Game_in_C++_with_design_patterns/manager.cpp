#include <cmath>
#include "manager.h"
#include "sound.h"
#include  <sstream>


// The main driver class for the game.
// constructor creates the worlds for Background, parallax backgrounds and creates the player,Asteroids, opponents based on frames 
// from the framefactory.
// invokes the draw and update of all the sprites.
// handles the keystrokes
// Also handles collision and scoring

Manager::~Manager() { 
  
  delete Gamedata::getInstance();
}

Manager::Manager() :
  env( SDL_putenv(const_cast<char*>("SDL_VIDEO_CENTERED=center")) ),
  gdata( Gamedata::getInstance() ),
  io( IOManager::getInstance() ),
  frameFactory( FrameFactory::getInstance() ),
  clock( Clock::getInstance() ),
  smanager(),
  screen( io.getScreen() ),
  
  backgroundWorld(const_cast<Frame*>(frameFactory->getFrame("background","background")[0]),6),
  
  parallaxWorld1(const_cast<Frame*>(frameFactory->getFrame("parallax1","parallax")[0]),5),
  
  parallaxWorld2(const_cast<Frame*>(frameFactory->getFrame("parallax2","parallax")[0]),4),
  
  parallaxWorld3(const_cast<Frame*>(frameFactory->getFrame("parallax3","parallax")[0]),3),

  parallaxWorld4(const_cast<Frame*>(frameFactory->getFrame("parallax4","parallax")[0]),2),

  parallaxWorld5(const_cast<Frame*>(frameFactory->getFrame("parallax5","parallax")[0]),1),
 
  viewport( Viewport::getInstance() ),

  orbs(),
  characters(),
  asteroids(),
  opponents(),
  ai(),
  explosions(),
  collisionStrategy( new MidPointCollisionStrategy ),
  currentOrb(0),
  helpFlag(false),
  done(false),
  rightFlag(false),
  aishootflag(false),
  gameoverflag(false),
  gamewon(false),
  score(0)
{
  if (SDL_Init(SDL_INIT_VIDEO) != 0) {
    throw string("Unable to initialize SDL: ");
  }
  characters.push_back(MultiframeSprite("player1","player",smanager));
  for (int i = 0; i < 15; i++){
  asteroids.push_back(new MultiframeSprite("asteroid","asteroid",smanager));
  }
  for (int i = 0; i < 10; i++){
  opponents.push_back(new MultiframeSprite("opponent","asteroid",smanager));
  }
  for (int i = 0; i < 1; i++){
  ai.push_back(new MultiframeSprite("ai","player",smanager));
  }
  viewport.setObjectToTrack(&characters[currentOrb]);
  atexit(SDL_Quit);
}

void Manager::draw() const {
  std::cout << "in draw method" << endl;
  backgroundWorld.draw();
  parallaxWorld1.draw();
  parallaxWorld2.draw();
  parallaxWorld3.draw();
  parallaxWorld4.draw();
  parallaxWorld5.draw();
  io.printMessageCenteredAt("Current Score :", 10);

  io.printMessageCenteredAt(static_cast<std::ostringstream*>(&(std::ostringstream() << score))->str(), 20);
  if(helpFlag) {
    io.printMessageCenteredAt("   HELP MENU  ", 40);
    io.printMessageCenteredAt("   ===============  ", 55);
  }
  for (unsigned int i = 0; i < characters.size(); ++i) {
    characters[i].draw();
  }
  for (unsigned int i = 0; i < asteroids.size(); ++i) {
    asteroids[i]->draw();
  }
  for (unsigned int i = 0; i < opponents.size(); ++i) {
    opponents[i]->draw();
  }
  for (unsigned int i = 0; i < ai.size(); ++i) {
    ai[i]->draw();
  }
  for (unsigned int i = 0; i < explosions.size(); ++i) {
    explosions[i]->draw();
  }
  smanager.draw();


}

void Manager::update(Uint32 ticks) {
  viewport.update();
  backgroundWorld.update();
  parallaxWorld1.update();
  parallaxWorld2.update();
  parallaxWorld3.update();
  parallaxWorld4.update();
  parallaxWorld5.update();
  for (unsigned int i = 0; i < characters.size(); ++i) {
    characters[i].update(ticks);
  }
  for (unsigned int i = 0; i < asteroids.size(); ++i) {
    asteroids[i]->update(ticks);
  }
  for (unsigned int i = 0; i < opponents.size(); ++i) {
    opponents[i]->update(ticks);
  } 
  for (unsigned int i = 0; i < explosions.size(); ++i) {
    explosions[i]->update(ticks);
  } 
  smanager.update(ticks);
}
void Manager::manageCollisions() {
  std::vector<Sprite*> bullets = smanager.getBullets();
  std::vector<Sprite*>::iterator it = bullets.begin();
  bool bulletErasedflag = false; 
  int bulletctr = 0;

  while (it != bullets.end() && (*it)->getName() != "aibullet"){
    //check allasteroids
    std::cout << "for a bullet" <<bulletctr <<std::endl;

    std::vector<MultiframeSprite*>::iterator astit = asteroids.begin();
    int astctr = 0;
    while (astit != asteroids.end()) {
      //check for collision between the bullet and the asteroid.
      //If yes...
          //explode the asteroid
      if (( collisionStrategy->execute(*(*it), *(*astit))) && bulletErasedflag !=true)  {
          std::cout << "EXPLOSION!!!!!!" <<endl;
          ++score;
          explosions.push_back(new ExplodingSprite(*(*astit)));
          delete *astit;
          astit = asteroids.erase(astit);
          bulletErasedflag = true;
      }
      else{
          std::cout << "no collision found !" << endl;
          ++astit;
          ++astctr;
      }
    }
    /* Added for opponent */
    std::vector<MultiframeSprite*>::iterator optit = opponents.begin();
    if(!bulletErasedflag){
      while (optit != opponents.end()) {
      if (( collisionStrategy->execute(*(*it), *(*optit))) && bulletErasedflag !=true)  {
          std::cout << "EXPLOSION of opponent!!!!!!" <<endl;
          ++score;
          explosions.push_back(new ExplodingSprite(*(*optit)));
          delete *optit;
          optit = opponents.erase(optit);
          bulletErasedflag = true;
      }
      else{
          std::cout << "no collision found !" << endl;
          ++optit;
      }
    }
    }

    if (!bulletErasedflag){
      ++it;
    }
    else {
      bulletErasedflag = false;
      delete *it;
      it = bullets.erase(it);
      smanager.deleteBullet(bulletctr); 
    }
  ++bulletctr;
}
  /* checking for collision of asteroids with the player*/
  std::vector<MultiframeSprite*>::iterator astit = asteroids.begin();
  std::vector<MultiframeSprite>::iterator plit = characters.begin();
  while (astit != asteroids.end()) {
    if ( collisionStrategy->execute((*plit), *(*astit))){
      std::cout << "Player crashed!!!!!!" <<endl;
      gameoverflag = true;
      done = true;
    }
    ++astit;
  }

  /* collision Check for the AI component */
  plit = characters.begin();
  std::vector<MultiframeSprite*>::iterator aiit = ai.begin();
  static unsigned int bulletcount = 1;
  while(aiit != ai.end()) {
    if ( collisionStrategy->execute((*plit), *(*aiit))){
      if (bulletcount % 37 == 0 && bulletcount > 15){
      (*aiit)->shoot();
      ++score;

    }
    ++bulletcount;
    }
    ++aiit;
  }

  if(characters[0].X() > (atoi(gdata->getXmlStr("worldWidth").c_str())-80) ){
    gamewon = true;
    done=true;
  }


}
//randomizing the position and speed of the asteroids at the beginning of the game.
void Manager::randomizeAsteroids() {
  for (unsigned int i = 0; i < asteroids.size(); ++i) {
    //std::cout << "randomizing asteroids" << endl;
    asteroids[i]->randomize();
  }
}
void Manager::randomizeOpponents() {
  for (unsigned int i = 0; i < opponents.size(); ++i) {
    opponents[i]->randomize();
  }
}

void Manager::play() {
  SDL_Event event;
  if ( clock.isPaused() ) {
              clock.unpause();
            }
  SDLSound sound;
  sound.startMusic();
  done = false;
  bool keyCatch = false;
  randomizeAsteroids();
  randomizeOpponents();
  while ( not done ) {
    draw();
    SDL_Flip(screen);
    std::vector<ExplodingSprite*>::iterator expit = explosions.begin();
    while (expit != explosions.end()) {
      int ccount = 0;
      ccount = (*expit)->chunkCount();
      if(ccount == 0){
        delete *expit;
        explosions.erase(expit);
      }
      
      else {
        ++expit;
      }
    }
 
    Uint32 ticks = clock.getElapsedTicks();
    manageCollisions();
    update(ticks);
    
    SDL_PollEvent(&event);
    if (event.type ==  SDL_QUIT) { break; }
    if(event.type == SDL_KEYUP) { keyCatch = false; }
    if(event.type == SDL_KEYDOWN) {
      switch ( event.key.keysym.sym ) {
        case SDLK_ESCAPE : 
         if ( clock.isPaused() ) {
              clock.unpause();
            }
            else {
              clock.pause();
          }
          done = true; break;
        case SDLK_q      : 
         if ( clock.isPaused() ) {
              clock.unpause();
            }
            else {
              clock.pause();
          }
          done = true; break;
        case SDLK_t :
          if ( !keyCatch ) {
            keyCatch = true;
            currentOrb = (currentOrb+1) % characters.size(); 
            viewport.setObjectToTrack(&characters[currentOrb]);
          }
          break;
        case SDLK_p      : {
          if (!keyCatch) {
            keyCatch = true;
            if ( clock.isPaused() ) clock.unpause();
            else clock.pause();
          }
          break;
        }
        case SDLK_RIGHT  : 
          characters[currentOrb].moveRight();
          break;
        
         
        case SDLK_LEFT  : 
          characters[currentOrb].moveLeft();
          break;
        
        
        case SDLK_UP  : {
          characters[currentOrb].moveUp();
        }
          break;
        
        case SDLK_DOWN  : {
          characters[currentOrb].moveDown();
        }
          break;

        case SDLK_SPACE  : {
           if (!keyCatch) {
            keyCatch = true;
          characters[currentOrb].shoot();
        }
        }
          break;
        
        case SDLK_F1     : {
          if (!keyCatch) {
            keyCatch = true;
            if ( clock.isPaused() ) {
              clock.unpause();
              helpFlag = false;
            }
            else {
              clock.pause();
              helpFlag = true;
          }
          }
          
          break;
        }
        default :        break;
      }
      
    }
  }
  
}
