# Ohjelmistotekniikan harjoitustyö

Harjoitustyön aiheena on _japanilainen mahjong_, eli **riichi mahjong** peli.


## Dokumentaatio

[Määrittelydokumentti](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/requirements.md)  
[Tuntikirjanpito](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/tuntikirjanpito.md)  
[Changelog](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/changelog.md)

### Pelin asentaminen

Riippuvuuksien asennus:
```
poetry install
```
Pelin käynnistäminen:
```
poetry run invoke start
```

### Testaaminen ja kattavuus
Testit voi ajaa komennolla
```
poetry run invoke test
```
Testikattavuusraportin voi kerätä komennolla
```
poetry run invoke coverage-report
```
