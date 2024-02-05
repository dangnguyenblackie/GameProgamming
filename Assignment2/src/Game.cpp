#include "../include/Game.hpp"
#include "../include/TextureManager.hpp"
#include "../include/GameObject.hpp"

#include "../include/ECS/ECS.hpp"
#include "../include/ECS/PositionComponent.hpp"

GameObject* tempObj;
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

    tempObj = new GameObject(TEST_TEXTURE_FILE_PATH, this->renderer);
    newPlayer.addComponent<PositionComponent>();
    newPlayer.getComponent<PositionComponent>().setTopLeftPos(500,500);

  }
  else
  {
    this->isRunning = false;
  }
}

void Game::handleEvent(){
  SDL_Event event;
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
  tempObj->update();
  manager.update();
  std::cout << newPlayer.getComponent<PositionComponent>().getTop() << "," << newPlayer.getComponent<PositionComponent>().getLeft() << std::endl;
}

void Game::render(){
  SDL_RenderClear(this->renderer);
  tempObj->render();
  SDL_RenderPresent(this->renderer);
}

void Game::clean(){
  delete tempObj;
  SDL_DestroyWindow(this->window);
  SDL_DestroyRenderer(this->renderer);
  SDL_Quit();
  printf("Game cleaned !\n");
}