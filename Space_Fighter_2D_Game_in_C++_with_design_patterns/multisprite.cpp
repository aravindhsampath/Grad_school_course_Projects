#include <iostream>
#include <cmath>
#include "multisprite.h"
#include "gamedata.h"
#include "ioManager.h"


void MultiframeSprite::advanceFrame(Uint32 ticks) {
  float ms = 1000.0/frameInterval;
  dt += ticks;
  int df = dt / ms;
  dt -= df * ms;
  currentFrame = (currentFrame + df) % numberOfFrames;
}

MultiframeSprite::MultiframeSprite(const string& n, const string& type, ShootingManager& smanager) :
  Drawable(Vector2f(Gamedata::getInstance()->getXmlInt(n+"X"), 
                 Gamedata::getInstance()->getXmlInt(n+"Y")), 
                Vector2f(Gamedata::getInstance()->getXmlInt(n+"Xspeed"),
                 Gamedata::getInstance()->getXmlInt(n+"Yspeed")),Vector2f(Gamedata::getInstance()->getXmlInt(n+"Xspeed"),
                 Gamedata::getInstance()->getXmlInt(n+"Yspeed"))), 
  name(n),
  // Get the frames vector from the frame factory
  frames(FrameFactory::getInstance()->getFrame(n,type)),
  sManager(smanager),
  dt(0),
  numberOfFrames( Gamedata::getInstance()->getXmlInt(n+"numberOfFrames" )),
  pwidth(Gamedata::getInstance()->getXmlInt(n+"Width" )/numberOfFrames),
  pheight( Gamedata::getInstance()->getXmlInt(n+"Height" )),
  srcX( Gamedata::getInstance()->getXmlInt(n+"SrcX" )),
  srcY( Gamedata::getInstance()->getXmlInt(n+"SrcY" )),
  currentFrame(0),
  frameInterval( Gamedata::getInstance()->getXmlInt(n+"frameInterval" ))
{ 
  }



MultiframeSprite& MultiframeSprite::operator=(const MultiframeSprite& rhs) {
  setName( rhs.getName() );
  //setsetFrames(rhs.getFrames());
  frames = rhs.frames;
  //sManager(rhs.getsManager());
  setdt(rhs.getdt());
  setNumberOfFrames(rhs.getNumberOfFrames());
  setPwidth(rhs.getPwidth());
  setPheight(rhs.getPheight());
  setSrcX(rhs.getSrcX());
  setSrcY(rhs.getSrcY());
  setCurrentFrame(rhs.getCurrentFrame());
  setFrameInterval(rhs.getFrameInterval());
  return *this;
}



/*
//remove the following constructor before Submission !!! Important !!!
MultiframeSprite::MultiframeSprite(const Vector2f& pos, 
                                   const Vector2f& vel, 
               const string& n, const std::vector<Frame*> & fms) :
  Drawable(pos, vel, vel), 
  name(n),
  frames(fms),
  dt(0),
  currentFrame(0),
  numberOfFrames( NUMBER_FRAMES ),
  frameInterval( FRAME_INTERVAL )
{ }
*/


MultiframeSprite::MultiframeSprite(const MultiframeSprite& rhs) :


  Drawable(rhs.getPosition(), rhs.getVelocity(), rhs.getMaxVelocity()),
  name( rhs.getName() ),
  //setsetFrames(rhs.getFrames());
  frames (rhs.frames),
  sManager(const_cast<ShootingManager&>(rhs.getsManager())),
  dt(rhs.getdt()),
  numberOfFrames(rhs.getNumberOfFrames()),
  pwidth(rhs.getPwidth()),
  pheight(rhs.getPheight()),
  srcX(rhs.getSrcX()),
  srcY(rhs.getSrcY()),
  currentFrame(rhs.getCurrentFrame()),
  frameInterval(rhs.getFrameInterval())



  { }

  

void MultiframeSprite::draw() const { 
  Uint32 x = static_cast<Uint32>(X());
  Uint32 y = static_cast<Uint32>(Y());
  frames[currentFrame]->draw(x, y);
}

void MultiframeSprite::update(Uint32 ticks) { 
  advanceFrame(ticks);
  float incr = velocityY() * static_cast<float>(ticks) * 0.001;
  Y( Y()+incr );
  float height = static_cast<float>(frames[currentFrame]->getHeight());
  
  if (name == "asteroid1"){
    velocityY( -abs( velocityY() ) );
  }
  else {
    if ( Y() < 0) {
    velocityY( abs( velocityY() ) );
    }

   if ( Y() > Gamedata::getInstance()->getXmlInt("worldHeight")-height) {
    velocityY( -abs( velocityY() ) );
    }
}
  incr = velocityX() * static_cast<float>(ticks) * 0.001;
  if(name =="asteroid") X( X()-incr );
  else  X( X()+incr );
  float width = static_cast<float>(frames[currentFrame]->getWidth());
  if ( X() + width < 0) {
    X( Gamedata::getInstance()->getXmlInt("worldWidth") );
  }
  if ( X() > Gamedata::getInstance()->getXmlInt("worldWidth") ) {
    X( -width );
  }
}
void MultiframeSprite::moveRight() { 
  X(X()+1);
}
void MultiframeSprite::moveLeft() { 
  X(X()-1);
}
void MultiframeSprite::moveUp() { 
  Y(Y()-1);
}
void MultiframeSprite::moveDown() { 
  Y(Y()+1);
}
void MultiframeSprite::randomize() { 
  std::cout << "in sprite randomize" << endl;
  Uint16 worldWidth = Gamedata::getInstance()->getXmlInt("worldWidth");
  Uint16 worldHeight = Gamedata::getInstance()->getXmlInt("worldHeight");
  static int seedctr = 1;
  srand(++seedctr);
  X(rand() % worldWidth);
  Y(rand() % worldHeight);
  std::cout << X() << endl;
  velocityX(static_cast<float>(rand() % static_cast<int>(maxVelocityX())));
  velocityY(0);
  //velocityY(static_cast<float>(rand() % static_cast<int>(maxVelocityY())));
}
void MultiframeSprite::shoot() {
  if(name=="ai"){
    static int seedctr = 16;
    srand(++seedctr);
    sManager.aishoot(X()+pwidth,Y()+(rand() % pheight));

  }
  else  sManager.shoot(X()+pwidth,Y()+(pheight/2));

}
