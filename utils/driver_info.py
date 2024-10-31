import sys

drivers_2024 = {
    1: "Max Verstappen",
    2: "Logan Sargeant",
    3: "Daniel Ricciardo",
    4: "Lando Norris",
    5: "Sebastian Vettel",  # Retired (not racing in 2024)
    6: "Nico Rosberg",  # Retired (not racing in 2024)
    7: "Kimi Raikkönen",  # Retired (not racing in 2024)
    8: "Romain Grosjean",  # Retired (not racing in 2024)
    9: "Marcus Ericsson",  # Retired (not racing in 2024)
    10: "Pierre Gasly",
    11: "Sergio Perez",
    12: "Felipe Nasr",  # Retired (not racing in 2024)
    13: "Pastor Maldonado",  # Retired (not racing in 2024)
    14: "Fernando Alonso",
    16: "Charles Leclerc",
    18: "Lance Stroll",
    19: "Felipe Massa",  # Retired (not racing in 2024)
    20: "Kevin Magnussen",
    21: "Nyck de Vries",  # Not racing in 2024
    22: "Yuki Tsunoda",
    23: "Alexander Albon",
    24: "Zhou Guanyu",
    25: "Jean-Éric Vergne",  # Retired (not racing in 2024)
    26: "Daniil Kvyat",  # Retired (not racing in 2024)
    27: "Nico Hulkenberg",
    28: "Will Stevens",  # Retired (not racing in 2024)
    30: "Liam Lawson",  # Retired (not racing in 2024)
    31: "Esteban Ocon",
    33: "Max Verstappen",  # Reserved but now using #1
    38: "Oliver Bearman",
    35: "Sergey Sirotkin",  # Retired (not racing in 2024)
    43: "Franco Colapinto",
    44: "Lewis Hamilton",
    47: "Mick Schumacher",  # Not racing in 2024
    50: "Oliver Bearman",
    53: "Alexander Rossi",  # Retired (not racing in 2024)
    55: "Carlos Sainz Jr.",
    63: "George Russell",
    77: "Valtteri Bottas",
    81: "Oscar Piastri",
    88: "Rio Haryanto",  # Retired (not racing in 2024)
    89: "Jack Aitken",  # Retired (not racing in 2024)
    94: "Pascal Wehrlein",  # Retired (not racing in 2024)
    98: "Roberto Merhi",  # Retired (not racing in 2024)
    99: "Antonio Giovinazzi",  # Retired (not racing in 2024)
}

display_position_str = {
   1: "🥇",
   2: "🥈",
   3: "🥉",
   4: "P4",
   5: "P5",
   6: "P6",
   7: "P7",
   8: "P8",
   9: "P9",
   10: "P10",
   11: "P11",
   12: "P12",
   13: "P13",
   14: "P14",
   15: "P15",
   16: "P16",
   17: "P17",
   18: "P18",
   19: "P19",
   20: "P20",
}

# Circuits and their circuit_keys
sessions = {
    "63": "Sakhir, Bahrain",
    "149": "Jeddah, Saudi Arabia",
    "10": "Melbourne, Australia",
    "144": "Baku, Azerbaijan",
    "151": "Miami, United States",
    "22": "Monte Carlo, Monaco",
    "15": "Catalunya, Spain",
    "23": "Montreal, Canada",
    "19": "Spielberg, Austria",
    "2": "Silverstone, Great Britain",
    "4": "Hungaroring, Hungary",
    "7": "Spa-Francorchamps, Belgium",
    "55": "Zandvoort, Netherlands",
    "39": "Monza, Italy",
    "61": "Singapore, Singapore",
    "46": "Suzuka, Japan",
    "150": "Lusail, Qatar",
    "9": "Austin, United States",
    "65": "Mexico City, Mexico",
    "14": "Interlagos, Brazil",
    "152": "Las Vegas, United States",
    "70": "Yas Marina Circuit, United Arab Emirates",
    "49": "Shanghai, China",
    "6": "Imola, Italy"
}

drivers = {
    1: "Max Verstappen",
    3: "Daniel Ricciardo",
    4: "Lando Norris",
    10: "Pierre Gasly",
    11: "Sergio Perez",
    14: "Fernando Alonso",
    16: "Charles Leclerc",
    18: "Lance Stroll",
    20: "Kevin Magnussen",
    22: "Yuki Tsunoda",
    23: "Alexander Albon",
    24: "Zhou Guanyu",
    27: "Nico Hulkenberg",
    31: "Esteban Ocon",
    43: "Franco Colapinto",
    44: "Lewis Hamilton",
    50: "Oliver Bearman",
    55: "Carlos Sainz Jr.",
    63: "George Russell",
    77: "Valtteri Bottas",
    81: "Oscar Piastri",
    30: "Liam Lawson"
}

driver_flags = {
    1: "🇳🇱",  # Max Verstappen (Netherlands)
    2: "🇺🇸",  # Logan Sargeant (USA)
    3: "🇦🇺",  # Daniel Ricciardo (Australia)
    4: "🇬🇧",  # Lando Norris (United Kingdom)
    5: "🇩🇪",  # Sebastian Vettel (Germany) - Retired
    6: "🇩🇪",  # Nico Rosberg (Germany) - Retired
    7: "🇫🇮",  # Kimi Raikkönen (Finland) - Retired
    8: "🇫🇷",  # Romain Grosjean (France) - Retired
    9: "🇸🇪",  # Marcus Ericsson (Sweden) - Retired
    10: "🇫🇷",  # Pierre Gasly (France)
    11: "🇲🇽",  # Sergio Perez (Mexico)
    12: "🇧🇷",  # Felipe Nasr (Brazil) - Retired
    13: "🇻🇪",  # Pastor Maldonado (Venezuela) - Retired
    14: "🇪🇸",  # Fernando Alonso (Spain)
    16: "🇲🇨",  # Charles Leclerc (Monaco)
    18: "🇨🇦",  # Lance Stroll (Canada)
    19: "🇧🇷",  # Felipe Massa (Brazil) - Retired
    20: "🇩🇰",  # Kevin Magnussen (Denmark)
    21: "🇳🇱",  # Nyck de Vries (Netherlands) - Not racing
    22: "🇯🇵",  # Yuki Tsunoda (Japan)
    23: "🇹🇭",  # Alexander Albon (Thailand)
    24: "🇨🇳",  # Zhou Guanyu (China)
    25: "🇫🇷",  # Jean-Éric Vergne (France) - Retired
    26: "🇷🇺",  # Daniil Kvyat (Russia) - Retired
    27: "🇩🇪",  # Nico Hulkenberg (Germany)
    28: "🇬🇧",  # Will Stevens (United Kingdom) - Retired
    30: "🇳🇿",  # Liam Lawson
    31: "🇫🇷",  # Esteban Ocon (France)
    33: "🇳🇱",  # Max Verstappen (Netherlands) - Reserved
    35: "🇷🇺",  # Sergey Sirotkin (Russia) - Retired
    38: "🇬🇧",  # Oliver Bearman
    43: "🇦🇷",  # Franco Colapinto (Argentina)
    44: "🇬🇧",  # Lewis Hamilton (United Kingdom)
    47: "🇩🇪",  # Mick Schumacher (Germany) - Not racing
    50: "🇬🇧",  # Oliver Bearman
    53: "🇺🇸",  # Alexander Rossi (USA) - Retired
    55: "🇪🇸",  # Carlos Sainz Jr. (Spain)
    63: "🇬🇧",  # George Russell (United Kingdom)
    77: "🇫🇮",  # Valtteri Bottas (Finland)
    81: "🇦🇺",  # Oscar Piastri (Australia)
    88: "🇲🇨",  # Rio Haryanto (Monaco) - Retired
    89: "🇰🇷",  # Jack Aitken (South Korea) - Retired
    94: "🇩🇪",  # Pascal Wehrlein (Germany) - Retired
    98: "🇪🇸",  # Roberto Merhi (Spain) - Retired
    99: "🇮🇹",  # Antonio Giovinazzi (Italy) - Retired
}
