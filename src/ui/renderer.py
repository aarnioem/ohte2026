from core.player import Player


class CLIRenderer:
    # This rendering method turned out to be really difficult to read in the terminal.
    # Clean this up later.
    def render(self, event: dict, player: Player):
        """Render a single round event"""
        event_type = event.get("type")

        if event_type == "draw":
            if "tile" in event and not player.is_human():
                return
            self._render_draw(event, player)
            return

        if event_type == "discard":
            self._render_discard(event)
            return

        if event_type == "tsumo":
            self._render_tsumo(event)
            return

        if event_type == "ron":
            self._render_ron(event)
            return

        if event_type == "calls":
            # this creates unnecessary spam so it's disabled for now
            # self._render_calls()
            return

        if event_type == "pon":
            self._render_pon(event)
            return

        if event_type == "kan":
            self._render_kan(event)
            return

        if event_type == "chii":
            self._render_chii(event)
            return

        if event_type == "end":
            self._render_end()
            return

        print(f"Unknown event: {event}")

    def _render_draw(self, event, player):
        self.separator("DRAW")
        if "tile" in event and player.is_human():
            tile = self.tile_to_text(event["tile"])
            print(f"Player {event['player']} draws {tile}")

        elif "tile" in event:
            print(f"Player {event['player']} draws a tile")
        else:
            print("No live tiles left. Exhaustive draw!")
        print()

    def _render_discard(self, event):
        self.separator("DISCARD")
        tile = self.tile_to_text(event["tile"])
        print(f"Player {event['player']} discards {tile}")
        self.render_player_discards_and_melds(
            event.get("player"),
            event.get("player_discards", []),
            event.get("player_melds", [])
        )
        print()

    def _render_tsumo(self, event):
        self.separator("TSUMO")
        tile = self.tile_to_text(event["tile"])
        han = event.get("han")
        fu = event.get("fu")

        print(f"Player {event['player']} declares tsumo with {tile} ({han} han, {fu} fu)")
        print()

    def _render_ron(self, event):
        self.separator("RON")
        tile = self.tile_to_text(event["tile"])
        han = event.get("han")
        fu = event.get("fu")

        print(f"Player {event['player']} declares ron with {tile} ({han} han, {fu} fu)")
        print()

    def _render_calls(self):
        self.separator("CALLS")
        print("No calls. Next player.")
        print()

    def _render_pon(self, event):
        self.separator("PON")
        tile = self.tile_to_text(event["tile"])
        print(f"Player {event['player']} calls pon on {tile}")
        print()

    def _render_kan(self, event):
        self.separator("KAN")
        tile = self.tile_to_text(event["tile"])
        print(f"Player {event['player']} calls kan on {tile}")
        print()

    def _render_chii(self, event):
        self.separator("CHII")
        tile = self.tile_to_text(event["tile"])
        print(f"Player {event['player']} calls chii on {tile}")
        print()

    def _render_end(self):
        self.separator("END")
        print("Round ended.")
        print()

    def tile_to_text(self, tile_id: int):
        # 136-id -> 34-index (ignore copy)
        tile34 = tile_id // 4

        if tile_id == 16:
            return "r5m"
        if tile_id == 52:
            return "r5p"
        if tile_id == 88:
            return "r5s"

        if tile34 < 9:
            value = tile34 + 1
            return f"{value}m"
        if tile34 < 18:
            value = tile34 - 9 + 1
            return f"{value}p"
        if tile34 < 27:
            value = tile34 - 18 + 1
            return f"{value}s"

        honors = ["E", "S", "W", "N", "Wh", "G", "R"]
        return f"{honors[tile34 - 27]}"

    def separator(self, label: str = "", width: int = 36):
        if label:
            text = f" {label} "
            line = text.center(width, "-")
        else:
            line = "-" * width
        print(line)

    def render_dora_indicators(self, dora_indicators=None):
        if not dora_indicators:
            print("Dora indicators: -")
            return

        dora_text = " ".join(self.tile_to_text(tile) for tile in dora_indicators)
        print(f"Dora indicators: {dora_text}")

    def render_melds(self, player: Player):
        melds = getattr(player.hand, "melds", None)
        if not melds:
            return

        formatted = [self.format_meld(meld) for meld in melds]
        print("Melds:", " ".join(formatted))

    def format_meld(self, meld):
        tiles = list(meld.tiles)
        called_tile = getattr(meld, "called_tile", None)
        from_player = getattr(meld, "from_player", None)
        called_used = False
        rendered = []

        for tile in tiles:
            text = self.tile_to_text(tile)
            if called_tile is not None and not called_used and tile == called_tile:
                text = f"{{{text}}}"
                called_used = True
            rendered.append(text)

        prefix = ""
        if from_player is not None:
            prefix = f"P{from_player} "

        return prefix + "[" + " ".join(rendered) + "]"

    def render_player_discards_and_melds(self, player_index, discards, melds):
        if player_index is None:
            return

        tiles = " ".join(self.tile_to_text(tile) for tile in discards)
        if not tiles:
            tiles = "-"
        print(f"P{player_index} discard pile: {tiles}")
        if melds:
            meld_text = " ".join(self.format_meld(meld) for meld in melds)
            print(f"P{player_index} melds: {meld_text}")
