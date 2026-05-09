# Arkkitehtuurikuvaus

- Pelin ymmärtämistä ja termejä suomeksi voi avata tällä sivulla, jos mahjong ei ole ennestään tuttu: https://www.mahjongopas.info/saannot/japanilainen-riichi/saannot/

## Rakenne

Sovellus on jaettu kolmeen osaan:

- `src/core`: Pelille tarpeelliset oliot ja funktiot (hand/kädet, pelaajat, wall/muurirakenne, melds/setit, pisteytys)
- `src/game`: Pelin kulun toteuttava luokka RoundManager. RoundManager luo tapahtumia, jotka se antaa rendereröinti luokalle. Renderöivä luokka on erotettu täysin pelilogiikasta, joten UI:n muutokset eivät vaikuta peliin.
- `src/ui`: UI hakemisto sisältää RichRenderer luokan, RichPrompts luoka sekä controller luokat. Controller luokkien kautta saadaan pelaajien tekemät päätökset. Ihmispelaajalta halutut päätökset delegoidaan RichPrompts luokalle, joka käyttää RichRenderer luokkaa informaation näyttämiseen pelaajalle.
- `src/main.py` alustaa pelin (pelaajat + UI + muuri) ja käynnistää kierroksen

### Luokkakaavio

```mermaid
classDiagram
    direction LR

	class Hand {
		tiles
        melds
        add_tile(tile)
        remove_tile(tile)
	}

    Player "1" --> "1" Hand
    Player "*" --> "1" PlayerController
	class Player {
        controller
        discards
        score
        riichi
        ippatsu
        hand
        receive_tile(tile_id)
        discard(tile)
        is_human()
	}

	class Wall {
		tiles
        draw_pointer
        draw_tile()
        live_tiles()
	}

    RoundManager ..> scoring
    RoundManager "*" --> "1" Wall
    RoundManager "*" --> "4" Player
    RoundManager "*" --> "1" RichRenderer
	class RoundManager {
		players
        wall
        renderer
        turn_pointer
        round_phase
        play_round()
	}

    class scoring {
        <<module>>
        can_tsumo(tiles_136, drawn_tile, riichi)
        can_ron(tiles_136, discarded_tile, riichi)
        calculate_win(tiles_136, win_tile, is_tsumo, riichi)
    }

    class PlayerController {
        is_human()
        get_discard_choice()
        get_tsumo_choice()
        get_ron_choice()
        get_pon_choice()
        get_kan_choice()
        get_riichi_choice()
        get_riichi_discard_choice()
        get_chii_choice()
    }

    PlayerController <|-- AIController

    class AIController {
    }

    PlayerController <|-- RichController

    RichController "*" --> "1" RichPrompts
    class RichController {
    }

	class RichRenderer {
        render()
        start_live()
        stop_live()
	}

    RichPrompts "*" --> "1" RichRenderer
    class RichPrompts {
        get_discard_choice()
        get_tsumo_choice()
        get_ron_choice()
        get_pon_choice()
        get_kan_choice()
        get_riichi_choice()
        get_riichi_discard_choice()
        get_chii_choice()
	}


```

## Käyttöliittymä
![Kuva pelinäkymästä](kuvat/table.png)
Sovelluksella on Rich pohjainen komentorivikäyttöliittymä. Peli päivittää pelinäkymää RoundManagerilta saatujen eventtien ja pelitilan mukaan ja kysyy pelaajalta tarvittavat päätökset. Viskattava tiili valitaan kädestä numeroilla 1-13, tai juuri nostettu tiili numerolla 0. Jos pelaaja on vaatinut settejä, on pelattavia tiiliä vähemmän, kuten tässä kuvassa.

## Sovelluslogiikka

Pelin päävastuu on `RoundManager`-luokalla, joka on toteutettu tilakoneena:

1. **Alustus/jako**: muuri (`Wall`) luodaan ja pelaajille jaetaan aloituskädet.
2. **Vuoro**: aktiivinen pelaaja nostaa tiilen, tarkistetaan mahdollinen tsumo (voittava käsi), sitten pelaaja valitsee minkä tiilen viskaa kädestä.
3. **Calls/vaatiminen**: muut pelaajat voivat vaatia viskauksen ja ottaa viskatun tiilen itselleen (ron, pon/kan, chii).
4. **Vuoron vaihtuminen**: jos vaadintaa ei tehdä, vuoro siirtyy seuraavalle pelaajalle. Vaadinta myös vaihtaa aktiivisen pelaajan.
5. **Kierroksen loppu**: kierros päättyy voittoon (tsumo/ron) tai tiilien loppumiseen muurista.

`ui` renderöi eventit ja kysyy pelaajien valinnat, kun taas `core` toteuttaa sääntöihin liittyvät operaatiot (esim. käden muokkaus, vaadintojen tarkistus, voittokäden validointi, pisteytyksen laskenta).

### Pelilogiikan sekvenssikaaviot

#### Pelin aloitus ja ensimmäisen pelaajan vuoro

```mermaid
sequenceDiagram
    participant Main
    participant RoundManager
    participant Wall
    participant Player
    participant PlayerController
    participant RichPrompts
    actor User
    participant RichRenderer

    Main->>RoundManager: play_round()
    RoundManager->>RoundManager: _start_round()

    loop Deal tiles to each player
        RoundManager->>Wall: draw_tile()
        Wall-->>RoundManager: tile
        RoundManager->>Player: player.hand.add_tile(tile)
    end


    RoundManager->>RoundManager: next_phase()
    RoundManager->>RichRenderer: render(event, self._current_player())

    RoundManager->>Wall: draw_tile()
    Wall-->>RoundManager: tile
    RoundManager->>Player: receive_tile(tile)
    RoundManager->>RoundManager: _try_tsumo()
    Note over RoundManager: no tsumo


    RoundManager->>Player: get_discard_choice()
    Player->>PlayerController: get_discard_choice()
    PlayerController->>RichPrompts: get_discard_choice()
    RichPrompts->>RichRenderer:
    User->>RichPrompts: choice
    RichPrompts-->PlayerController: discard_index
    PlayerController-->>Player: discard_index
    Player-->>RoundManager: discard_index

    RichRenderer-->>RoundManager: 
    RoundManager->>Player: discard(tile)
    Player-->>RoundManager: tile discarded

    RoundManager->>RoundManager: _calls_phase()
    Note over RoundManager: no calls made
    RoundManager->>RoundManager: advance_turn()

```

Kaavio kuvaa pelin alkua. Aluksi pelaajille jaetaan tiilet, jonka jälkeen peli kutsuu next_phase() metodia joka aloittaa varsinaisen pelin. RoundManager ottaa muurista tiilen ja laittaa sen vuorossa olevan pelaajan käteen. Jos (kun) pelaaja ei voita, RoundManager kutsuu Player luokalta päätöstä get_discard_choice() metodilla.

Player luokalla on riippuvuus PlayerControlleriin, jolta saadaan varsinaiset päätökset. Koska kyseessä on ihmispelaaja ja RichController eikä AIController, RichController kysyy päätöstä RichPrompts luokan kautta. Pelaajan tekemä päätös palautuu RoundManagerille, joka poistaa oikean tiilen pelaajalta.

Seuraavaksi RoundManager tarkistaa haluaako muut pelaajat vaatia viskauttua tiiltä, jonka jälkeen siirrytään seuraavan pelaajan vuoroon, joka etenee samaan tapaan.


## Rakenteelliset ongelmat

RoundManagerin tuottamat eventit eivät sisällä koko pelin tilaa, joka oli ehkä hieman huono rakenteellinen lopputulos. Tämä tuli korjattua myöhemmin metodilla joka palauttaa pelitilan erillisenä. En osannut odottaa, että RoundManagerista tulisi niin monimutkainen, ja tällaiset pienet projektin alussa tehdyt päätökset aiheuttivat vaivaa myöhemmin.

Toinen todella huono kehitystä hidastava rakenteellinen päätös oli tiilien käsitteleminen pelkkinä tile_id lukuina. Ajattelin että tämä olisi kätevää, koska Mahjong kirjasto käsittelee ne samassa formaatissa, mutta tiilelle olisi kuitenkin parempi olla oma luokkansa. Syy tähän on läpinäkyvyys ja testattavuus. Nyt on hyvin vaikeaa nähdä mitkä tiilet on mitäkin pelkistä numeroista, ja testien tekemisestä tuli todella vaikeaa.
