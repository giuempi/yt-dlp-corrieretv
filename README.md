# yt-dlp-corrieretv

Plugin per [yt-dlp](https://github.com/yt-dlp/yt-dlp) che scarica i video **interi** da
**video.corriere.it** (Corriere TV).

> ⚠️ **Questo plugin è stato scritto con l'aiuto dell'intelligenza artificiale.**
> Il progetto yt-dlp vieta i contributi fatti con strumenti di IA
> ([NO AI / NO LLM POLICY](https://github.com/yt-dlp/yt-dlp/blob/master/CONTRIBUTING.md#no-ai--no-llm-policy)).
> **Non proporre questo codice a yt-dlp** e non usarlo come base per segnalazioni o pull request verso yt-dlp.

## Il problema

Oggi il modulo `RCS` incluso in yt-dlp non riesce a scaricare da Corriere TV:
- a volte si ferma con `Video data not found in the page`;
- a volte scarica solo **un minuto** (la sigla), perché nella pagina c'è ancora un vecchio
  link al canale in diretta del Corriere, che contiene solo l'ultimo minuto trasmesso.

I video veri stanno su **Dailymotion** come video privati. La pagina contiene il loro
codice privato (`videoProvider` → `privateId`), e questo plugin lo passa al modulo
Dailymotion di yt-dlp. Se il codice manca, il plugin prova con i vecchi link della pagina.

## Installazione

### Se usi `yt-dlp.exe` (Windows)
1. Scarica [`yt-dlp-corrieretv.zip`](yt-dlp-corrieretv.zip).
2. Estrailo **nella stessa cartella di `yt-dlp.exe`**. Dovresti ottenere
   `yt-dlp-plugins\yt-dlp-corrieretv\yt_dlp_plugins\extractor\corrieretv.py`
   accanto a `yt-dlp.exe`.

### Se hai installato yt-dlp con pip
```
python -m pip install -U https://github.com/giuempi/yt-dlp-corrieretv/archive/refs/heads/main.zip
```

### Verifica
```
yt-dlp -v --simulate "https://video.corriere.it/..."
```
Nell'output deve comparire `[debug] Extractor Plugins: CorriereTVFixIE`.

## Uso
Come sempre:
```
yt-dlp "https://video.corriere.it/cronaca/titolo-del-video/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

## Limiti
- Vale solo per `video.corriere.it`. Gli altri siti del gruppo RCS non sono stati provati.
- Se il Corriere cambia di nuovo le sue pagine, il plugin può smettere di funzionare.
- Provato il 27/09/2026 con yt-dlp 2026.08.19.

---

## English

yt-dlp plugin to download **full** videos from **video.corriere.it** (Corriere TV).

> ⚠️ **This plugin was written with the help of AI.** yt-dlp does not accept AI-assisted
> contributions ([policy](https://github.com/yt-dlp/yt-dlp/blob/master/CONTRIBUTING.md#no-ai--no-llm-policy)).
> **Do not submit this code to yt-dlp.**

Corriere TV videos are now hosted on Dailymotion as private videos. The page embeds their
private id (`videoProvider.privateId`); this plugin hands it to yt-dlp's Dailymotion
extractor. yt-dlp's built-in `RCS` extractor fails, or downloads only a one-minute loop
from a live channel URL that is still left in the page.

Install: unzip [`yt-dlp-corrieretv.zip`](yt-dlp-corrieretv.zip) next to `yt-dlp.exe`, or
`python -m pip install -U https://github.com/giuempi/yt-dlp-corrieretv/archive/refs/heads/main.zip`.

License: [Unlicense](LICENSE) (public domain).
