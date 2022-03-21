
def pinput(prompt):
  # Doesn't hide the prompt when testing with unittest
  print(prompt, end='')
  return input()

def ask(questions, types=None):
  if types == None:
    return [pinput(f'{q}: ') for q in questions]
  else:
    answers = []
    for i, q in enumerate(questions):
      while True:
        try:
          answers.append(
            types[i](pinput(f'<{types[i].__name__}> {q}: ').lower()))
          break
        except:
          print('\nUgyldig input! Prøv igjen.\n')
    return answers

def ask_select(question, options, return_int=False):
  options = list(options)
  indexed_options = '\t' + \
      '\n\t'.join([f'({i}) {option}' for i, option in enumerate(options)])
  while True:
    selected = pinput(f'{question}\n{indexed_options}\n').lower()
    for i, option in enumerate(options):
      if selected == option.lower():
        if return_int:
          return i
        else:
          return option
    try:
      option = options[int(selected)]
      if return_int:
        return int(selected)
      else:
        return option 
    except:
      print('\nUgyldig input! Prøv igjen.\n')

def ask_select_row(question, rows, key_end=None):
  if key_end != None:
    options = {str(x[:]): x[0:key_end] for x in rows}
  else:
    options = {str(x[:]): x[0] for x in rows}
  options['Ingen av disse.'] = -1
  return options[ask_select(question, options.keys())]

def ask_select_or_create(state, question, rows, ask_create, key_end=None):
  row_id = ask_select_row(question, rows, key_end)
  return ask_create(state) if row_id == -1 else row_id
