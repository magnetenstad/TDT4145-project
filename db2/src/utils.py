
def ask(questions, types=None):
	try:
		if types == None:
			return [input(f'{q}: ') for q in questions]
		else:
			return [types[i](input(f'<{types[i].__name__}> {q}: ')) for i, q in enumerate(questions)]
	except Exception as e:
		print(f'ERROR - {e}')

