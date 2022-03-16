
def ask(questions, types=None):
  if types == None:
    return [input(f'{q}: ') for q in questions]
  else:
    answers = []
    for i, q in enumerate(questions):
      while True:
        try:
          answers.append(
            types[i](input(f'<{types[i].__name__}> {q}: ').lower()))
          break
        except:
          print('\nUgyldig input! Prøv igjen.\n')
    return answers

def ask_select(question, options, return_int=False):
  options = list(options)
  indexed_options = '\t' + \
      '\n\t'.join([f'({i}) {option}' for i, option in enumerate(options)])
  while True:
    selected = input(f'{question}\n{indexed_options}\n').lower()
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
