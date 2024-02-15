#ifndef TRANSFORM_COMPONENT_HPP
#define TRANSFORM_COMPONENT_HPP
#pragma once
#include "ECS.hpp"
#include "../Vector2.hpp"

class TransformComponent : public Component {
  public:
    Vector2 position;
    Vector2 velocity;
    float scale = 1;

    int height;
    int width;
    int speed = 3;

    TransformComponent(){
      this->position.Zero();
    }

    TransformComponent(float scale){
      this->position.Zero();
      this->scale = scale;
    }

    TransformComponent(float x, float y, float scale = 1){
      this->position.x = x;
      this->position.y = y;
      this->scale = scale;
    }

    ~TransformComponent(){

    };

    void init() override{
      this->velocity.Zero();
      // printf("Position added completely\n");
    }

    void update() override{
      this->position.x = this->position.x + this->velocity.x * this->speed;
      this->position.y = this->position.y + this->velocity.y * this->speed;
      // printf("Position update() being called\n");
    }

    void setTopLeftPos(int top, int left){
      this->position.x = left;
      this->position.y = top;
    }

    void setTopLeftPos(Vector2 position){
      this->position.x = position.x;
      this->position.y = position.y;
    }
};
#endif