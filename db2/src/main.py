from database import Database
from app import App, AppState

def main():
  
  state = AppState()
  state.db = Database(':memory:')

  print('\nVelkommen til Kaffedatabasen 😊\n')
  
  App(state)

  state.db.close()

if __name__ == '__main__':
  main()
