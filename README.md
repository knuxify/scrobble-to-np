# last.fm scrobbles -> #np

Python application that gets your X last scrobbles and, if they're all the same, posts the song as a #np/#nowplaying post. Currently only supports Mastodon.

# Setup

1. Copy the ``settings.json.example`` file to ``settings.json`` and put it in the same directory as run.py.
2. Fill in the settings file.
  * If you're planning to use this program as a backend for a public-facing app where everybody can add their own account, set ``"mastodon_use_app"`` to ``"true"``.
  * If you want to run the program yourself from e.g. a cron job, rather than letting it run and handle the sleeping intervals by itself, set ``"run_once"`` to ``"true"``.
3. Install ``mastodon.py`` with pip3.

Note: settings.json must be in the same directory as the one you're running the script from. (TODO: Add an argument that will allow users to override the default settings file location.)

# TODO

- custom settings file location + argument parsing
- web interface
- better crash handlers
