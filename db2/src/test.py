import unittest
from unittest.mock import patch
from main import main

class Test(unittest.TestCase):

  # @patch('builtins.input', 
  #       side_effect=['Avslutte'])
  # def test_cancel(self, _):
  #   print('\n\n### 🤖 TEST 1 ###')
  #   main(':memory:')

  # @patch('builtins.input', 
  #       side_effect=['Logge inn', 'admin', 'admin', 'Logge ut', 'Avslutte'])
  # def test_login_admin(self, _):
  #   print('\n\n### 🤖 TEST 2 ###')
  #   main(':memory:')

  # @patch('builtins.input', 
  #       side_effect=['Logge inn', 'admin', 'admin', 'Skrive data', 'Kaffesmaking', 'Ingen av disse', 'KaffebrenneriNavn', 'KaffeNavn', '2021.01.01', 'Brenningsgrad', 'Beskrivelse', '14.5', 'Ingen av disse', '1998', '5.5', 'Ingen av disse', 'KaffegårdNavn', '100', 'Land', 'Region', 'Ja', 'Nei', 'Ja', 'Ingen av disse', 'ForedlingsmetodeNavn', 'ForedlingsmetodeBeskrivelse', 'Ja', 'Ja', 'Smaksnotater', '5', '2022.02.02', 'Nei', 'Lese data', 'Alle kaffesmakinger', 'Nei', 'Logge ut', 'Avslutte'])
  # def test_insert_kaffesmaking(self, _):
  #   print('\n\n### 🤖 TEST 3 ###')
  #   main(':memory:')
  
  @patch('builtins.input', 
      side_effect=['Registrere en ny bruker', 'bruker@ntnu.no',
      'bruker-passord', 'Bruker Bruker', 'Brukerland', 'Skrive data',
      'Kaffesmaking', '0', 'Wow - en odyssé for smaksløkene:\nsitrusskall, melkesjokolade, aprikos!',
      '10', '', 'Nei', 'Logge ut', 'Avslutte'])
  def test_brukerhistorie_1(self, _):
    print('\n\n### 🤖 TEST: Brukerhistorie 1 ###')
    main(':memory:')
  
  @patch('builtins.input', 
      side_effect=['Logge inn som gjest', 'Lese data',
      'Flest unike kaffer i år', 'Nei', 'Logge ut', 'Avslutte'])
  def test_brukerhistorie_2(self, _):
    print('\n\n### 🤖 TEST: Brukerhistorie 2 ###')
    main(':memory:')

  @patch('builtins.input', 
      side_effect=['Logge inn som gjest', 'Lese data',
      'Mest for pengene', 'Nei', 'Logge ut', 'Avslutte'])
  def test_brukerhistorie_3(self, _):
    print('\n\n### 🤖 TEST: Brukerhistorie 3 ###')
    main(':memory:')

  @patch('builtins.input', 
      side_effect=['Logge inn som gjest', 'Lese data',
      'Beskrevet som floral', 'Nei', 'Logge ut', 'Avslutte'])
  def test_brukerhistorie_4(self, _):
    print('\n\n### 🤖 TEST: Brukerhistorie 4 ###')
    main(':memory:')
  
  @patch('builtins.input', 
      side_effect=['Logge inn som gjest', 'Lese data',
      'Ikke vasket fra Rwanda eller Colombia', 'Nei', 'Logge ut', 'Avslutte'])
  def test_brukerhistorie_5(self, _):
    print('\n\n### 🤖 TEST: Brukerhistorie 5 ###')
    main(':memory:')
