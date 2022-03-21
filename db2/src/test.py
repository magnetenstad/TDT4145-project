import unittest
from unittest.mock import patch
from main import main

class Test(unittest.TestCase):

  @patch('builtins.input', 
        side_effect=['Avslutte'])
  def test_cancel(self, _):
    print('\n\n### TEST 1 ###')
    main()

  @patch('builtins.input', 
        side_effect=['Logge inn', 'admin', 'admin', 'Logge ut', 'Avslutte'])
  def test_login_admin(self, _):
    print('\n\n### TEST 2 ###')
    main()

  @patch('builtins.input', 
        side_effect=['Logge inn', 'admin', 'admin', 'Skrive data', 'Kaffesmaking', 'Ingen av disse.', 'KaffebrenneriNavn', 'KaffeNavn', 'Brenningsdato', 'Brenningsgrad', 'Beskrivelse', '14.5', 'Ingen av disse.', '1998', '5.5', 'Ingen av disse.', 'KaffegårdNavn', '100', 'Land', 'Region', 'Ja', 'Nei', 'Ja', 'Ingen av disse.', 'ForedlingsmetodeNavn', 'ForedlingsmetodeBeskrivelse', 'Ja', 'Nei', 'Ja', 'Smaksnotater', '5', 'Smaksdato', 'Lese data', 'Alle kaffesmakinger', 'Nei', 'Logge ut', 'Avslutte'])
  def test_insert_kaffesmaking(self, _):
    print('\n\n### TEST 3 ###')
    main()
  
