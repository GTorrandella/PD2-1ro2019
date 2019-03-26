'''
Created on Mar 19, 2019

@author: Gabriel Torrandella
'''
import pytest
import xmlschema
from xmlschema.etree import ParseError

class TestXML(object):
    def test_Invalid_Schema(self):
        with pytest.raises(ParseError) as excinfo:
            xmlschema.XMLSchema("formacion_invalido.xsd")
        
        print("ParseError: %s" % excinfo.value)

    def test_is_Valid_XML(self):
        XSFormacion = xmlschema.XMLSchema("BancoSchema.xsd")
        assert XSFormacion.is_valid("Banco.xml")

    def test_is_Invalid_XML(self):
        XSFormacion = xmlschema.XMLSchema("BancoSchema.xsd")
        assert not XSFormacion.is_valid("Banco_Invalido.xml")
    