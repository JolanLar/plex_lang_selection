import os
import datetime
from plexapi.server import PlexServer
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load config from environment variables
PLEX_URL = os.environ.get('PLEX_URL')
PLEX_TOKEN = os.environ.get('PLEX_TOKEN')
PLEX_LIBRARY = os.environ.get('PLEX_LIBRARY', 'Animes')
AUDIO_LANG = os.environ.get('AUDIO_LANG', 'Japanese')
SUB_LANG = os.environ.get('SUB_LANG', 'French')
MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 5))

if not PLEX_URL:
    raise ValueError("PLEX_URL environment variable must be set!")

if not PLEX_TOKEN:
    raise ValueError("PLEX_TOKEN environment variable must be set!")

# Connect to Plex
plex = PlexServer(PLEX_URL, PLEX_TOKEN)

# Get all TV shows in the library
tv_library = plex.library.section(PLEX_LIBRARY)
tv_shows = tv_library.all()

def process_season(season):
    outputs = []
    for episode in season.episodes():
        changed = False
        episode.reload()
        for media in episode.media:
            for part in media.parts:
                # Set audio stream only if not already selected
                for audio in part.audioStreams():
                    if audio.language == AUDIO_LANG:
                        if not audio.selected:
                            changed = True
                            part.setSelectedAudioStream(audio)
                        break
                # Set subtitle stream only if not already selected
                for subtitle in part.subtitleStreams():
                    if subtitle.language == SUB_LANG and not any(substring in subtitle.extendedDisplayTitle for substring in ['forced', 'forcé']):
                        if not subtitle.selected:
                            changed = True
                            part.setSelectedSubtitleStream(subtitle)
                        break
        if changed:
            outputs.append(
                f"{datetime.datetime.now()} [INFO] - {episode.grandparentTitle} S{episode.parentIndex:02}E{episode.index:02} changed"
            )
    return outputs

def process_show(show):
    try:
        results = []
        for season in show.seasons():
            season_results = process_season(season)
            if season_results:
                results.extend(season_results)
        if not results:
            return f"{datetime.datetime.now()} [INFO] - {show.title} - No changes"
        else:
            results.append(f"{datetime.datetime.now()} [INFO] - {show.title} - DONE")
            return "\n".join(results)
    except Exception as e:
        return f"{datetime.datetime.now()} [ERROR] - {show.title} - {e}"

def main():
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = [executor.submit(process_show, show) for show in tv_shows]
        for future in as_completed(futures):
            result = future.result()
            print(result)
    print("Update completed for all shows!")

if __name__ == "__main__":
    main()
