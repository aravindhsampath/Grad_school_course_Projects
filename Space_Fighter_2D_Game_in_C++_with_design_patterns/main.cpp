// "Spacefighter 2D" by Aravindh Sampathkumar based on the tracker framework by Brian Malloy 

//#include "manager.h"
#include "menuManager.h"
Gamedata* Gamedata::instance;

int main(int, char*[]) {
   try {
      //Manager game_manager;
      //game_manager.play();
   	MenuManager menu;
    menu.play();
   }
   catch (const string& msg) { std::cout << msg << std::endl; }
   catch (...) {
      std::cout << "Oops, someone threw an exception!" << std::endl;
   }
   return 0;
}
