
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
        except:
          print('Ugyldig input!')

def ask_select(question, options, indexed=False):
  if indexed:
    options = [f'({i})' + option for i, option in enumerate(options)]
    # question += '\n(skriv tallet)'
  options_str = '\t' + '\n\t'.join(options)
  while True:
    selected = input(f'{question}\n{options_str}\n').lower()
    if selected in options:
      return selected
    try:
      return options[int(selected)]
    except:
      pass
    print('Ugyldig input!')

