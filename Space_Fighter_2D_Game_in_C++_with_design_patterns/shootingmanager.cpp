#include "shootingmanager.h"
#include "gamedata.h"

ShootingManager::~ShootingManager() { 
	bullets.clear();
	aibullets.clear();
}

ShootingManager::ShootingManager() : bullets(),aibullets(),count(1){

}
void ShootingManager::shoot(float xPos,float yPos) {
	//std::cout<<"making a bullet"<<std::endl;
	bullets.push_back(new Sprite("bullet","bullet",xPos,yPos));
	//std::cout<<"created a bullet"<<std::endl;

}
void ShootingManager::aishoot(float xPos,float yPos) {
	//std::cout<<"making a bullet"<<std::endl;
	aibullets.push_back(new Sprite("aibullet","bullet",xPos,yPos));
	//std::cout<<"created an aibullet"<<std::endl;

}

void ShootingManager::draw() const {
	for (unsigned int i = 0; i < bullets.size(); ++i) {
		//std::cout<<"drawing a bullet"<<std::endl;
   	 bullets[i]->draw();
  	}
  	for (unsigned int i = 0; i < aibullets.size(); ++i) {
		//std::cout<<"drawing a bullet"<<std::endl;
   	 aibullets[i]->draw();
  	}

}

void ShootingManager::update(Uint32 ticks) {

	std::vector<Sprite*>::iterator it = bullets.begin();
	std::vector<Sprite*>::iterator aibit = aibullets.begin();
	while(aibit != aibullets.end()){
		if(count % 370 == 0){
				delete *aibit;
				aibit = aibullets.erase(aibit);
			}
			else { 
			(*aibit)->update(ticks);
			++aibit;
			}
			++count;
			if (count>1500) count =1;
			
	}
	while(it != bullets.end()){
		
		//if ((Gamedata::getInstance()->getXmlInt("worldWidth") - (*it)->X()) < 40){
		if((*it)->getName() == "aibullet1"){
			static unsigned int ctr1 = 1;
			if(ctr1 %3 == 0 ){
				delete *it;
				it = bullets.erase(it);
			}
			++ctr1;
		}
		else {
		if(((*it)->velocityX())-Gamedata::getInstance()->getXmlInt("bulletXspeed")>400){
			delete *it;
			it = bullets.erase(it);
		}else{
			//if((*it)->getName() == "aibullet") (*it)->velocityX((*it)->velocityX()-1);
			//else 
			(*it)->velocityX((*it)->velocityX()+1);
			(*it)->update(ticks);
			++it;
		}
	}
	}
}
void ShootingManager::deleteBullet(Uint32 bulletpos) {
	std::vector<Sprite*>::iterator delit = bullets.begin();
	Uint32 loopctr = 0;
	while(loopctr != bulletpos){
		++delit;
		++loopctr;
	}
	delit = bullets.erase(delit);
}

