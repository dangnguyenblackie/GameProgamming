#include "../include/Game.hpp"
#include "../include/TextureManager.hpp"
#include "../include/ECS/Component.hpp"

// static attributes
SDL_Renderer* Game::renderer = nullptr;
SDL_Event Game::event;

// Game instances
Manager manager;
Entity& newPlayer = manager.addEntity();

Game::Game(){}
Game::~Game(){}

void Game::init(const char* title, int xPos, int yPos, int width, int height, bool fullscreen){
  int flag = 0;
  if(fullscreen)
  {
    flag = SDL_WINDOW_FULLSCREEN;
  }

  if(SDL_Init(SDL_INIT_EVERYTHING) == 0)
  {
    printf("Initialised\n");

    this->window = SDL_CreateWindow(title, xPos, yPos, width, height, flag);
    if(this->window)
    {
      printf("Window created\n");
    }
    this->renderer = SDL_CreateRenderer(this->window, -1, 0);

    if(this->renderer)
    {
      SDL_SetRenderDrawColor(this->renderer, 255, 255, 255, 255);
      printf("Renderer created\n");
    }

    this->isRunning = true;

    newPlayer.addComponent<TransformComponent>();
    newPlayer.addComponent<SpriteComponent>(TEST_TEXTURE_FILE_PATH, 0.2);
    newPlayer.addComponent<KeyboardController>();
  }
  else
  {
    this->isRunning = false;
  }
}

void Game::handleEvent(){

  SDL_PollEvent(&event);

  switch(event.type){

    case SDL_QUIT:
      this->isRunning = false;
      break;

    default:
      break;
  }

}

void Game::update(){
  manager.refresh();
  manager.update();
}

void Game::render(){
  SDL_RenderClear(this->renderer);
  manager.draw();
  SDL_RenderPresent(this->renderer);
}

void Game::clean(){

  SDL_DestroyWindow(this->window);
  SDL_DestroyRenderer(this->renderer);
  SDL_Quit();
  printf("Game cleaned !\n");
}