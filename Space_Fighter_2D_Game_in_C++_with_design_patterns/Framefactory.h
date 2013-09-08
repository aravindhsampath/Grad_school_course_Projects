#ifndef FRAMEFACTORY__H
#define FRAMEFACTORY__H
#include "factory.h"
#include "ioManager.h"
#include <vector>
class FrameFactory : public AbstractFactory {
public:
  static FrameFactory* getInstance();
  ~FrameFactory();

  std::vector<Frame*> getFrame(const string & name, const string& frameType);
private:
  static FrameFactory* instance;
  const Gamedata* gdata;
  const IOManager& io;
  std::map<string, std::vector<Frame*> > frames;
  FrameFactory();
  FrameFactory(const FrameFactory &);
  FrameFactory& operator=(const FrameFactory &);
};
#endif

