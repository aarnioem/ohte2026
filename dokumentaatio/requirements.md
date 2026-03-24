## Requirements specification

**NOTE:** If you need to familiarise yourself with Riichi Mahjong rules, you can do so on the wiki.
- [Rules overview](https://riichi.wiki/Rules_overview)
- [Terminology list](https://riichi.wiki/List_of_terminology_by_alphabetical_order)

### Purpose
Basic Japanese four player Riichi Mahjong.

### Planned features
- User can start a match with 3 AIs
- Valid hands get scored based on the han amount. A hand is not valid unless it has a yaku.
- Yaku detection and han calculation for the most common yakus.
    - [More information on yakus here](https://riichi.wiki/List_of_yaku)
    - Nagashi Mangan is so rare that it may be omitted from the basic version
    - There is a mahjong library for python for calculating hand scores that will be used for scoring.
- Dora indicators
- Uradora
- Tenpai indicator that shows waits when a hand is ready
- Furiten indicator
- Ryuukyoku/Exhaustive Draw points calculation
- No abortive draws in the basic version
- CLI

### Possible features
- Visible shanten counter (How many optimal draws are needed for a valid hand)
- Ukeire counter (Number of tiles that can improve the shanten count)
- Rule toggles for abortive draws
- All yakus, including Nagashi Mangan
- Choice between one or two round games
- Pygame interface
- Online multiplayer
    - Some sort of statistics tracking
