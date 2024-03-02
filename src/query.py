import asyncio
import re
from typing import Optional, Dict, Any, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

from src.config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URL

SEARCH_LIMIT = 50
MAX_TRACK_LENGTH_WORDS = 10

class BuildTracklist:
    def __init__(self, phrase: str, minimize_track_count: bool) -> None:
        self._phrase: str = phrase
        self._minimize_track_count: bool = minimize_track_count
        self._sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET))


    def _sanitized_phrase(self, phrase: str) -> str:
        """Sanitize the input phrase by removing non-alphanumeric characters (except spaces) and converting to lowercase."""
        return re.sub(r'[^a-zA-Z0-9 ]', '', phrase).lower()
    

    async def _find_track_with_string(self, target_string: str) -> Optional[Dict[str, Any]]:
        """Asynchronously find a Spotify track that exactly matches the sanitized target string."""
        sanitized_target_string = self._sanitized_phrase(target_string)
        search_result = self._sp.search(q=f'track:"{sanitized_target_string}"', type='track', limit=SEARCH_LIMIT)
        
        tracks: List[Dict[str, Any]] = [
            {
                'name': item['name'],
                'id': item['id'],
                'artists': ', '.join(artist['name'] for artist in item.get('artists', [])),
                'albumArtURL': item['album']['images'][1]['url'] if len(item['album']['images']) > 1 else None
            }
            for item in search_result.get('tracks', {}).get('items', [])
            if self._sanitized_phrase(item['name']) == sanitized_target_string
        ]
        
        tracks.sort(key=lambda x: len(x['name']))
        return tracks[0] if tracks else None
    

    async def get_tracks_for_phrase(self) -> Dict[str, Any]:
        sanitized_target_string = self._sanitized_phrase(self._phrase).replace(' +', ' ').strip()
        input_arr = sanitized_target_string.split(' ')
        n = len(input_arr)

        is_possible = [False] * (n + 1)
        word_count_in_latest_phrase = [0] * (n + 1)
        track_for_latest_phrase = [None] * (n + 1)
        is_possible[0] = True

        checked_tracks = []

        for i in range(1, n + 1):
            await asyncio.sleep(0.1)  # To mitigate hitting rate limits
            phrases_to_check = [input_arr[i-j-1:i] for j in range(i) if len(input_arr[i-j-1:i]) <= MAX_TRACK_LENGTH_WORDS]

            for phrase in phrases_to_check:
                joined_phrase = ' '.join(phrase)
                track = await self._find_track_with_string(joined_phrase)
                if track is not None:
                    checked_tracks.append(track)
                    phrase_length = len(phrase)
                    if is_possible[i - phrase_length]:
                        comparison_factor = 1 if self._minimize_track_count else -1
                        current_difference = word_count_in_latest_phrase[i] - phrase_length
                        is_better_option = track_for_latest_phrase[i] is None or (current_difference * comparison_factor > 0)
                        
                        if is_better_option:
                            is_possible[i] = True
                            word_count_in_latest_phrase[i] = phrase_length
                            track_for_latest_phrase[i] = track

        if not is_possible[n]:
            return {
                'is_success': False,
                'checked_tracks': list({track['id']: track for track in checked_tracks}.values())  # Deduplicate
            }

        result_tracks = []
        i = n
        while i > 0:
            result_tracks.insert(0, track_for_latest_phrase[i])
            i -= word_count_in_latest_phrase[i]

        return {
            'is_success': True,
            'result_tracks': result_tracks
        }

    def _generate_suggestions(self, tracks: List[Dict[str, Any]], original_phrase: str, checked_tracks: List[Dict[str, Any]]) -> List[str]:
            """Generate alternative phrases considering exact matches and suggesting alternatives for unmatched segments."""
            exact_matches = [track for track in checked_tracks if track]
            unmatched_tracks = [track for track in tracks if track not in exact_matches]
            input_tokens = set(original_phrase.lower().split())
            suggestions = []
            
            if exact_matches:
                base_phrase = " ".join([track['name'] for track in exact_matches])
                suggestions.append(base_phrase)
            
            for track in unmatched_tracks:
                track_name = track['name']
                track_tokens = set(track_name.lower().split())
                similarity = len(input_tokens.intersection(track_tokens))
                if similarity > 0:  
                    suggestions.append(track_name)
            
            # If there are too many suggestions, prioritize by similarity
            if len(suggestions) > 3:
                suggestions.sort(key=lambda name: -len(set(name.lower().split()).intersection(input_tokens)))
                suggestions = suggestions[:3]

            # Combine exact matches with top unmatched suggestions to form final suggestions
            final_suggestions = []
            for suggestion in suggestions:
                combined = base_phrase + " " + suggestion if 'base_phrase' in locals() else suggestion
                final_suggestions.append(combined.strip())

            return list(dict.fromkeys(final_suggestions))[:3]

class SpotifyPlaylistCreator:
    def __init__(self, tracks: List[Dict[str, Any]], playlist_name: str = "MemoMixtape", playlist_description: str = "A playlist generated from a phrase."):
        self._tracks = tracks
        self._playlist_name = playlist_name
        self._playlist_description = playlist_description
        self._sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                             client_secret=CLIENT_SECRET,
                                                             redirect_uri=REDIRECT_URL,
                                                             scope="playlist-modify-private"))

    async def create_playlist(self) -> Optional[str]:
        """Create a Spotify playlist with tracks that spell out the input phrase."""
        user_id = self._sp.me()['id']
        playlist = self._sp.user_playlist_create(user_id, self._playlist_name, description=self._playlist_description, public=False)
        
        track_uris = [f'spotify:track:{track["id"]}' for track in self._tracks if track]
        if track_uris:
            self._sp.user_playlist_add_tracks(user_id, playlist['id'], track_uris)
            return playlist['external_urls']['spotify']
        return None
