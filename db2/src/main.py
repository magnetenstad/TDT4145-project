from database import Database
from app import App, AppState


def main(db_path='database.db'):
  
  state = AppState()
  state.db = Database(db_path) 

  App(state)

  state.db.close()


if __name__ == '__main__':
  main()
