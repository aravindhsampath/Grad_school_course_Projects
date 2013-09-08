#ifndef FACTORY__H
#define FACTORY__H

#include <string>
using std::string;
#include <map>
#include <vector>
#include "frame.h"
#include "gamedata.h"

class AbstractFactory {
public:
  AbstractFactory() {}
  virtual ~AbstractFactory() {}

  virtual std::vector<Frame*> getFrame(const string& framename, const string& frameType) = 0;

private:
  static AbstractFactory* instance;
  AbstractFactory(const AbstractFactory&);
  AbstractFactory& operator=(const AbstractFactory&);
};
#endif