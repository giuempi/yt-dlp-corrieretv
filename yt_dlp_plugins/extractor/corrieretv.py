# Plugin per yt-dlp: video di video.corriere.it (Corriere TV).
# Il modulo ufficiale "RCS" non trova piu' i dati del video. I video stanno su Dailymotion
# come video privati: la pagina ne contiene il codice privato ("videoProvider" -> "privateId"),
# che passiamo al modulo Dailymotion di yt-dlp. Se manca, proviamo i vecchi link "mediaFile".
# Scritto con l'aiuto dell'IA: non proporlo al progetto yt-dlp (vieta i contributi fatti con l'IA).
import json
import re

from yt_dlp.extractor.common import InfoExtractor
from yt_dlp.utils import ExtractorError, int_or_none, parse_duration, unescapeHTML, unified_timestamp


class CorriereTVFixIE(InfoExtractor):
    IE_NAME = 'corrieretv:plugin'
    _VALID_URL = r'https?://video\.corriere\.it/(?:[^/?#]+/)*(?P<id>[\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\w]{12})'

    def _media_files(self, webpage):
        files = []
        for m in re.finditer(r'"mediaFile"\s*:\s*(\[)', webpage):
            try:
                arr, _ = json.JSONDecoder().raw_decode(webpage[m.start(1):])
            except ValueError:
                continue
            files.extend(f for f in arr if isinstance(f, dict) and f.get('value'))
        return files

    def _real_extract(self, url):
        video_id = self._match_id(url)
        webpage = self._download_webpage(url, video_id)

        # Dal 2026 i video del Corriere stanno su Dailymotion come video privati: la pagina
        # contiene "videoProvider" con il codice privato (privateId) che li rende visibili.
        # Il vecchio "mediaFile" invece punta al canale in diretta (solo l'ultimo minuto).
        provider = self._search_regex(
            r'"videoProvider"\s*:\s*(\{[^{}]*\})', webpage, 'video provider', default=None)
        if provider:
            try:
                provider = json.loads(provider)
            except ValueError:
                provider = None
        if provider and (provider.get('name') or '').lower() == 'dailymotion':
            dm_id = provider.get('privateId') or provider.get('dmId')
            if dm_id:
                return self.url_result(
                    f'https://www.dailymotion.com/video/{dm_id}', 'Dailymotion', url_transparent=True,
                    id=video_id, title=self._og_search_title(webpage, default=None))

        formats, seen = [], set()
        for f in self._media_files(webpage):
            src = f['value']
            if src in seen:
                continue
            seen.add(src)
            if '.m3u8' in src or 'mpegurl' in (f.get('mimeType') or '').lower():
                formats.extend(self._extract_m3u8_formats(
                    src, video_id, 'mp4', m3u8_id='hls', fatal=False,
                    headers={'Referer': url}))
            elif src.startswith('http'):
                formats.append({
                    'url': src,
                    'width': int_or_none(f.get('width')),
                    'height': int_or_none(f.get('height')),
                    'tbr': int_or_none(f.get('bitrate')),
                    'http_headers': {'Referer': url},
                })
        if not formats:
            raise ExtractorError('Nessun flusso video trovato nella pagina', expected=True)

        def field(name):
            v = self._search_regex(r'"%s"\s*:\s*"([^"]+)"' % name, webpage, name, default=None)
            return unescapeHTML(v) if v else None

        return {
            'id': video_id,
            'title': self._og_search_title(webpage, default=None) or field('title') or video_id,
            'description': self._og_search_description(webpage, default=None),
            'thumbnail': self._og_search_thumbnail(webpage, default=None),
            'duration': parse_duration(field('duration')),
            'timestamp': unified_timestamp(field('pubDate')),
            'formats': formats,
            'http_headers': {'Referer': url},
        }
