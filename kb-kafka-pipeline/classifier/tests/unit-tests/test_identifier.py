import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../..')) 

import pytest
from utils.sensitiveDataIdentifier import SensitiveDataIdentifier

def test_identify_sensitive_data_menor_infrator():
    identifier = SensitiveDataIdentifier()    
    
    assert identifier.identify_sensitive_data({'subject': 'Menor infrator em julgamento'}) == 'MENOR_INFRATOR'

def test_identify_sensitive_data_violencia_domestica():
    identifier = SensitiveDataIdentifier()    

    assert identifier.identify_sensitive_data({'subject': 'Violência doméstica contra a mulher'}) == 'VIOLENCIA_DOMESTICA'

def test_identify_sensitive_data_crime_odio():
    identifier = SensitiveDataIdentifier()    

    assert identifier.identify_sensitive_data({'subject': 'Ato de racismo foi registrado'}) == 'CRIME_ODIO'

def test_identify_sensitive_data_none():
    identifier = SensitiveDataIdentifier()    

    assert identifier.identify_sensitive_data({'subject': 'Um caso qualquer sem temas sensíveis'}) is None
