#ifndef MULTISPRITE__H
#define MULTISPRITE__H

#include <string>
#include <iostream>
#include <vector>
using std::string;

#include "drawable.h"
#include "frame.h"
#include "Framefactory.h"
#include "shootingmanager.h"

class MultiframeSprite : public Drawable {
public:
  MultiframeSprite(const string& n, const string& type, ShootingManager& smanager);
  //MultiframeSprite(const Vector2f& pos, const Vector2f& vel,
  //       const string& n, const std::vector<Frame*>& fms);
  MultiframeSprite(const MultiframeSprite& s);
  virtual ~MultiframeSprite() { std::cout << "deleting mfsprite"<<std::endl;} 
  MultiframeSprite& operator=(const MultiframeSprite&);
  void setName(const string& n) { name = n; }
  //void setFrames(const std::vector<Frame *> f)  {frames = f; }
  void setdt(const float& d) {dt = d;}
  void setNumberOfFrames(const unsigned& no) {numberOfFrames = no;}
  void setPwidth(const Uint16& pw) {pwidth = pw; }
  void setPheight(const Uint16& ph) {pheight = ph; }
  void setSrcX(const Uint16& sx) {srcX = sx; }
  void setSrcY(const Uint16& sy) {srcY = sy; }
  void setCurrentFrame(const unsigned& cf) {currentFrame = cf; }
  void setFrameInterval(const unsigned& fi) {frameInterval = fi; }


  const string& getName() const { return name; }
  //const std::vector<Frame *> getFrames() const {return frames; }
  const float& getdt() const { return dt; }
  const unsigned& getNumberOfFrames() const { return numberOfFrames; }
  const Uint16& getPwidth() const {return pwidth;}
  const Uint16& getPheight() const {return pheight;}
  const Uint16& getSrcX() const {return srcX;}
  const Uint16& getSrcY() const {return srcY;}
  const unsigned& getCurrentFrame() const { return currentFrame; }
  const Frame* getCurrentFrameref() const{ return frames[currentFrame]; }
  const unsigned& getFrameInterval() const { return frameInterval; }
  //ShootingManager& getsManager() { return sManager; }
  ShootingManager& getsManager() const { return sManager; }
  void moveRight();
  void moveLeft();
  void moveUp();
  void moveDown();
  void randomize();
  void shoot();
  virtual void draw() const;
  virtual void update(Uint32 ticks);

private:
  string name;
  std::vector<Frame *> frames;
  ShootingManager& sManager;
  float dt;
  unsigned numberOfFrames;
  Uint16 pwidth;
  Uint16 pheight;
  Uint16 srcX;
  Uint16 srcY;
  unsigned currentFrame;
  unsigned frameInterval;
  void advanceFrame(Uint32 ticks);
};
#endif
