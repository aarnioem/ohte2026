# NotenMahjong

Peli toteuttaa yhden erän japanilaista riichi mahjongia. Riichi mahjongin sääntöihin ja termistöön voi tutustua suomeksi [mahjong-oppaasta](https://www.mahjongopas.info/saannot/japanilainen-riichi/saannot/) tai englanniksi [riichi wikissä](https://riichi.wiki/Rules_overview).


## Dokumentaatio

[Määrittelydokumentti](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/requirements.md)  
[Tuntikirjanpito](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/tuntikirjanpito.md)  
[Changelog](https://github.com/aarnioem/ohte2026/tree/main/dokumentaatio/changelog.md)  
[Arkkitehtuurikuvaus](https://github.com/aarnioem/ohte2026/blob/main/dokumentaatio/arkkitehtuuri.md)
[Käyttöohje](dokumentaatio/kayttohje.md)

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
Pylint raportin saa komennolla
```
poetry run invoke lint
```
