
def pinput(prompt):
  # Doesn't hide the prompt when testing with unittest
  print(prompt, end='')
  i = input()
  return i if len(i) else None

def ask(questions, types=None):
  if types == None:
    return [pinput(f'{q}: ') for q in questions]
  else:
    answers = []
    for i, q in enumerate(questions):
      while True:
        try:
          answers.append(
            types[i](pinput(f'<{types[i].__name__}> {q}: ')))
          break
        except:
          print('\nUgyldig input! Prøv igjen.\n')
    return answers

def ask_select(question, options, return_int=False):
  options = list(options)
  indexed_options = '\t' + \
      '\n\t'.join([f'({i}) {option}' for i, option in enumerate(options)])
  while True:
    selected = pinput(f'{question}\n{indexed_options}\n> ').lower()
    for i, option in enumerate(options):
      if selected == option.lower():
        return i if return_int else option
    try:
      option = options[int(selected)]
      return int(selected) if return_int else option
    except:
      print('\nUgyldig input! Prøv igjen.\n')

def ask_select_row(question, rows, key_end=None):
  if key_end != None:
    options = {str(x[:]): x[0:key_end] for x in rows}
  else:
    options = {str(x[:]): x[0] for x in rows}
  options['Ingen av disse'] = -1
  return options[ask_select(question, options.keys())]

def ask_select_or_create(state, question, rows, ask_create, key_end=None):
  row_id = ask_select_row(question, rows, key_end)
  return ask_create(state) if row_id == -1 else row_id

from datetime import datetime

class Date(str):
  def __new__(cls, date_str):
    """Date validation: 
    Must be a valid date (yyyy.mm.dd)
    and cannot be in the future."""

    if date_str == None:
      return None

    yyyy, mm, dd = date_str.split('.')
    
    if not (len(yyyy) == 4 and len(mm) == 2 and len(dd) == 2):
      raise Exception()

    yyyy, mm, dd = map(lambda x: int(x), (yyyy, mm, dd))

    then = datetime(yyyy, mm, dd)
    now = datetime.now()
    
    if then > now:
      raise Exception()

    return str.__new__(cls, date_str)
