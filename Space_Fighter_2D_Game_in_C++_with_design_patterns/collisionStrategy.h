#include <cmath>
#include "sprite.h"
#include "multisprite.h"

class CollisionStrategy {
public:
  virtual bool execute(const Sprite&, const MultiframeSprite&) const = 0;
  virtual bool execute(const MultiframeSprite&, const MultiframeSprite&) const{ return false;};
  virtual ~CollisionStrategy() {}
};

class RectangularCollisionStrategy : public CollisionStrategy {
public:
  RectangularCollisionStrategy() {}
  virtual bool execute(const Sprite&, const Sprite&) const;
};

class MidPointCollisionStrategy : public CollisionStrategy {
public:
  MidPointCollisionStrategy() {}
  virtual bool execute(const Sprite&, const MultiframeSprite&) const;
  virtual bool execute(const MultiframeSprite&, const MultiframeSprite&) const;
  float distance(float, float, float, float) const;
};

class PerPixelCollisionStrategy : public CollisionStrategy {
public:
  PerPixelCollisionStrategy() {}
  virtual bool execute(const Sprite&, const Sprite&) const;
};

