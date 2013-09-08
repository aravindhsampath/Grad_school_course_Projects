#ifndef SHOOTINGMANAGER__H
#define SHOOTINGMANAGER__H
#include <vector>
#include "sprite.h"
class ShootingManager {
public:
	ShootingManager ();
  	~ShootingManager ();
  	void play();
  	void draw() const;
  	void update(Uint32);
  	void shoot(float xPos,float yPos);
  	void aishoot(float xPos,float yPos);
  	std::vector<Sprite*> getBullets() {return bullets; }
  	int getBulletCount() {return bullets.size();}
  	void deleteBullet(Uint32);
 private:
 	std::vector<Sprite*> bullets;
 	std::vector<Sprite*> aibullets;
 	unsigned int count;
};
#endif