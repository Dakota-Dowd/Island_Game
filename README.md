# Island_Game
A video game made with the Pygame module, entirely from scratch, designed and created by me.


# Structure Goal:

Island_Game/
├── game.py                 # Entry point - just creates Game and runs it
├── config/
│   └── settings.py         # WIDTH, HEIGHT, FPS, colors, asset paths
├── entities/
│   ├── _init__.py         # Exports Player, Bullet, Zombie, Island
│   ├── player.py
│   ├── bullet.py
│   ├── zombie.py
│   └── island.py
├── scenes/
│   ├── _init__.py         # Exports all scenes
│   ├── base_scene.py       # Abstract Scene class with handle_events/update/render
│   ├── menu_scene.py       # Start menu
│   ├── game_scene.py       # Main gameplay (most of your current main())
│   └── gameover_scene.py   # Game over screen
├── ui/
│   ├── _init__.py
│   ├── button.py           # Your existing Button class
│   └── text.py             # create_text() helper
└── assets/
    ├── fonts/
    └── images/


Settings (pure data, no dependencies)
    ↓
Entities (receive settings, manage own state)
    ↓
Scenes (orchestrate entities, receive screen)
    ↓
Game (owns screen/clock, switches scenes)