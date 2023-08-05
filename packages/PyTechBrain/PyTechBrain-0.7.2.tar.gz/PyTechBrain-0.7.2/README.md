PyTechBrain - innowacyjna nauka programowania

Chciałbym przedstawić inspirację dla nauczycieli, w pełni zgodną z nową podstawą programową. To innowacyjny projekt - wprowadzający do tematu IoT. 
Łączy elektronikę i programowanie w jednym pudełku, pozwala uczyć od klasy 4 szkoły podstawowej do końca liceum. 
Zaczynamy środowiskiem opartym o Scratch, po czym przechodzimy do Pythona. Wszystko z czujnikami i diodami w tle...

PyTechBrain to nowa platforma wprowadzająca uczniów w dziedzinę IoT - Internet of Things (Internet Rzeczy). 
Pozwala na nauczanie elektroniki i programowania w jednym. Jest w pełni zgodna z nową Podstawą Programową. 
Łaczy prostotę wykonania i olbrzymie mozliwości nauczania programowania. Możemy wykorzystywać ją do budowania stacji pogodowych, podstaw inteligentnego miasta.  Kompatybilny z Arduino UNO R3, obsługiwany przez Scratch 2.0 offline i Python 3

Aby zainicjować układ w programie, konieczne są polecenia:

from PyTechBrain import *

uklad = PyTechBrain()



==============================================


Dla układów PyTechBrain z firmy ABIX Edukacja biblioteka samodzielnie znajduje port COM (ttyUSB) - nie ma potrzeby niczego sprawdzać.

Dla innych układów kompatybilnych z Arduino UNO R3 należy samodzielnie sprawdzić port COM (ttyUSB) i podac jako parametr, np.:

from PyTechBrain import *

uklad = PyTechBrain('COM12')

uklad = PyTechBrain('/dev/ttyUSB2')


