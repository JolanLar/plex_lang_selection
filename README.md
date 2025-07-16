# Plex Audio & Subtitle Stream Selector

A Python script to automatically select the preferred audio and subtitle streams for TV show episodes in a specified Plex library. 

The script connects to your Plex server, scans all TV shows in a given library section, and for each episode:

- Sets the audio stream to a specified language (default: Japanese)
- Sets the subtitle stream to a specified language (default: French) with forced subtitles (e.g. "forced" or "forcé" in the subtitle title)

Multiple shows are processed concurrently for faster execution.

---

## Features

- Connects to Plex via `plexapi`
- Processes all TV shows in a specified library section
- Automatically selects audio and subtitle streams based on configured languages
- Supports forced subtitle detection
- Runs in parallel using thread pool for performance
- Logs changes and errors with timestamps

---

## Requirements

- Docker

---

## Configuration

The script is configured via environment variables:

| Variable      | Description                                     | Default        | Required |
|---------------|-------------------------------------------------|----------------|----------|
| `PLEX_URL`    | Base URL of your Plex server                    | -              | No       |
| `PLEX_TOKEN`  | Your Plex API token (required)                  | -              | Yes      |
| `PLEX_LIBRARY`| Name of the Plex TV show library to process     | `Animes`       | No       |
| `AUDIO_LANG`  | Preferred audio language code (e.g., Japanese)  | `Japanese`     | No       |
| `SUB_LANG`    | Preferred subtitle language code (e.g., French) | `French`       | No       |
| `MAX_WORKERS` | Maximum concurrent threads for processing       | `5`            | No       |

---

## Usage with Docker Compose

Create a `docker-compose.yml` file with the following content:

```yaml
services:
  plex_lang_selection:
    image: tefox/plex_lang_selection:latest
    container_name: plex_lang_selection
    environment:
      # Plex variables
      PLEX_URL: ""
      PLEX_TOKEN: ""
      PLEX_LIBRARY: "Animes"
      AUDIO_LANG: "Japanese"
      SUB_LANG: "French"
      MAX_WORKERS: "5"
    restart: "no"
```

Then run the container:

```bash
docker compose up
```

---

## How It Works

- Retrieves all TV shows from the specified Plex library.
- For each show, iterates through all seasons and episodes.
- For each episode's media parts:
  - Selects the first audio stream matching the configured `AUDIO_LANG` if not already selected.
  - Selects the first subtitle stream matching `SUB_LANG` that contains "forced" or "forcé" in its title if not already selected.
- Uses a thread pool executor to process multiple shows in parallel.

---

## Troubleshooting

- Make sure the `PLEX_TOKEN` environment variable is set with a valid Plex API token.
- Verify the Plex server URL (`PLEX_URL`) is reachable.
- Confirm the library name (`PLEX_LIBRARY`) matches exactly the name of the TV show section in Plex.
- Check your language codes (`AUDIO_LANG` and `SUB_LANG`) correspond to available audio and subtitle languages.

---

## License

This script is provided as-is under the MIT License.

---

## Acknowledgements

- Uses the [`plexapi`](https://github.com/pkkid/python-plexapi) library by pkkid.

---

Feel free to contribute or request features by opening an issue or pull request.
