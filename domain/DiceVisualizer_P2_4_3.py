class DiceVisualizer:
    """
    Diese Klasse stellt ASCII-Art Grafiken für Würfelaugen bereit.
    Sie stellt sicher, dass alle Würfel die gleiche geometrische Form haben.
    """
    
    # Definition der Würfelseiten als Listen von Strings (Akzeptanzkriterium P2.4.3)
    DICE_ART = {
        1: [
            "┌─────────┐",
            "│         │",
            "│    ●    │",
            "│         │",
            "└─────────┘"
        ],
        2: [
            "┌─────────┐",
            "│  ●      │",
            "│         │",
            "│      ●  │",
            "└─────────┘"
        ],
        3: [
            "┌─────────┐",
            "│  ●      │",
            "│    ●    │",
            "│      ●  │",
            "└─────────┘"
        ],
        4: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│         │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        5: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│    ●    │",
            "│  ●   ●  │",
            "└─────────┘"
        ],
        6: [
            "┌─────────┐",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "│  ●   ●  │",
            "└─────────┘"
        ]
    }

    @staticmethod
    def get_dice_art(value: int) -> list:
        """Gibt die ASCII-Grafik für einen bestimmten Würfelwert zurück."""
        return DiceVisualizer.DICE_ART.get(value, ["Fehler: Ungültiger Wert"])