#include "ioManager.h"
#include "viewport.h"

Viewport& Viewport::getInstance() {
  static Viewport viewport;
  return viewport;
}

Viewport::Viewport() : 
  gdata(Gamedata::getInstance()),
  position(0, 0),
  viewWidth(gdata->getXmlInt("viewWidth")), 
  viewHeight(gdata->getXmlInt("viewHeight")),
  worldWidth(gdata->getXmlInt("worldWidth")),
  worldHeight(gdata->getXmlInt("worldHeight")),
  objWidth(0), objHeight(0),
  //spriteToTrack(NULL),
  multiframespriteToTrack(NULL),
  objectToTrack(NULL) 
{}

/*
void Viewport::setObjectToTrack(const Sprite *obj) { 
  
  objWidth = spriteToTrack->getFrame()->getWidth();
  objHeight = spriteToTrack->getFrame()->getHeight();
  objectToTrack = obj; 
}
*/
void Viewport::setObjectToTrack(const MultiframeSprite *obj) { 
  multiframespriteToTrack = obj;
  objWidth = multiframespriteToTrack->getPwidth();
  objHeight = multiframespriteToTrack->getPheight();
  objectToTrack = obj;
}

void Viewport::update() {
  const float x = objectToTrack->X();
  const float y = objectToTrack->Y();
  position[0] = (x + objWidth/2) - viewWidth/2;
  position[1] = (y + objHeight/2) - viewHeight/2;
  if (position[0] < 0) position[0] = 0;
  if (position[1] < 0) position[1] = 0;
  if (position[0] > (worldWidth - viewWidth)) {
    position[0] = worldWidth-viewWidth;
  }
  if (position[1] > (worldHeight - viewHeight)) {
    position[1] = worldHeight-viewHeight;
  }
}
