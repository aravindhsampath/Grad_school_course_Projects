#include "Framefactory.h"
#include "ioManager.h"
#include "lsystem.h"
#include <vector>

FrameFactory* FrameFactory::instance;
FrameFactory* FrameFactory::getInstance() {
  if ( !instance ) instance = new FrameFactory;
  return instance;
}

FrameFactory::~FrameFactory() {
  std::map<string, std::vector<Frame*> >::iterator pos = frames.begin();
  while ( pos != frames.end() ) {
    std::vector<Frame*>::iterator it = pos->second.begin();
    while (it != pos->second.end()){
      SDL_Surface* surface = (*it)->getSurface();
      SDL_FreeSurface(surface);
      delete *it;
      ++it;
    }
    ++pos;
  }
  frames.clear();
}

FrameFactory::FrameFactory() :
  gdata( Gamedata::getInstance() ),
  io( IOManager::getInstance() ),
  frames( std::map<string, std::vector<Frame*> >() )
{

}

std::vector<Frame*> FrameFactory::getFrame( const string& framename, const string& frameType) {
  // Frames are stored by filename, which is unique
  std::map<string, std::vector<Frame*> >::iterator pos = frames.find(framename);
  if ( pos == frames.end() ) {
    const string filename = framename+"File";
    std::vector<Frame*> vectorOfFrames;
    SDL_Surface* surface;
    if (frameType == "background" || frameType == "parallax" || frameType == "sprite"){
      surface = io.loadAndSet(gdata->getXmlStr(filename), true);
      Frame* frame = new Frame(surface,
                gdata->getXmlInt(framename+"Width"), 
                gdata->getXmlInt(framename+"Height"), 0, 0);
      vectorOfFrames.push_back(frame);
      frames[framename] = vectorOfFrames;
      return vectorOfFrames;
    }
    else if (frameType == "player"){
      surface = io.loadAndSet(gdata->getXmlStr(filename), true);
      unsigned numberOfFrames = gdata->getXmlInt(framename+"numberOfFrames");
      Uint16 pwidth = gdata->getXmlInt(framename+"Width")/numberOfFrames;
      Uint16 pheight = gdata->getXmlInt(framename+"Height");
      Uint16 srcX = gdata->getXmlInt(framename+"SrcX");
      Uint16 srcY = gdata->getXmlInt(framename+"SrcY");
      for (unsigned i = 0; i < numberOfFrames; ++i) {
        unsigned frameX = i * pwidth + srcX;
        vectorOfFrames.push_back( 
        new Frame(surface, pwidth, pheight, frameX, srcY));
      }
      frames[framename] = vectorOfFrames;
      return vectorOfFrames;
    }
    else if (frameType == "asteroid"){
      surface = io.loadAndSet(gdata->getXmlStr(filename), true);
      unsigned numberOfFrames = gdata->getXmlInt(framename+"numberOfFrames");
      Uint16 pwidth = gdata->getXmlInt(framename+"Width")/numberOfFrames;
      Uint16 pheight = gdata->getXmlInt(framename+"Height");
      Uint16 srcX = gdata->getXmlInt(framename+"SrcX");
      Uint16 srcY = gdata->getXmlInt(framename+"SrcY");
      for (unsigned i = 0; i < numberOfFrames; ++i) {
        unsigned frameX = i * pwidth + srcX;
        vectorOfFrames.push_back( 
        new Frame(surface, pwidth, pheight, frameX, srcY));
      }
      frames[framename] = vectorOfFrames;
      return vectorOfFrames;
    }

  }
  else return pos->second;
}

