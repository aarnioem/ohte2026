## Requirements specification

**NOTE:** If you need to familiarise yourself with Riichi Mahjong rules, you can do so on the wiki.
- [Rules overview](https://riichi.wiki/Rules_overview)
- [Terminology list](https://riichi.wiki/List_of_terminology_by_alphabetical_order)

### Purpose
One round simulation of Japanese four player Riichi Mahjong.

### Features
- [x] User can start a match with 3 AIs
- [x] Valid hands get scored based on the han amount. A hand is not valid unless it has a yaku.
- [x] Yaku detection and han calculation for the most common yakus.
    - [More information on yakus here](https://riichi.wiki/List_of_yaku)
    - [x] Nagashi Mangan is so rare that it may be omitted from the basic version
    - [x] There is a mahjong library for python for calculating hand scores that will be used for scoring.
    - [x] Some rare yakus are missing, such as blessing of heaven and blessing of earth, but these are incredibly rare. It is possible to play hundreds of thousands of rounds without seeing any of them.
- [x] Chii, Pon, Kan calls
- [x] Dora indicators
- [x] Riichi declaration
- [x] Uradora
- [x] Furiten
- [x] Ryuukyoku/Exhaustive Draw
- [x] No abortive draws in the basic version
    - [x] Four kan abortive draw is necessary
- [x] CLI
    - [x] more complex UI with colours using Rich

### Possible features for future development (outside the scope of the course)
- Visible shanten counter (How many optimal draws are needed for a valid hand)
- Ukeire counter (Number of tiles that can improve the shanten count)
- Rule toggles for abortive draws
- All yakus, including Nagashi Mangan
- Multiple playable rounds.
- Pygame interface
- Online multiplayer
    - Some sort of statistics tracking
