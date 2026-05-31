# Home Assistant YouTube Downloader Add-ons

Repozytorium zawiera dodatek **YouTube Web Downloader** dla Home Assistant Supervisor. Dodatek uruchamia panel webowy oparty o Flask, Bootstrap 5 i `yt-dlp`. Służy do analizy oraz pobierania materiałów z YouTube wyłącznie wtedy, gdy użytkownik ma do nich prawa lub może je legalnie pobrać.

Dodatek jest budowany dla oficjalnie wspieranych obecnie architektur Home Assistant: `amd64` oraz `aarch64`. Home Assistant wycofał wsparcie systemów 32-bitowych, w tym `armv7`.

## Dodanie repozytorium

1. Otwórz Home Assistant.
2. Przejdź do: **Ustawienia → Dodatki → Sklep z dodatkami → trzy kropki → Repozytoria**.
3. Dodaj adres tego repozytorium GitHub.
4. W sklepie znajdź **YouTube Web Downloader** i wybierz **Zainstaluj**.
5. Po instalacji uruchom dodatek i włącz widoczność w panelu bocznym, jeśli Home Assistant jej automatycznie nie aktywował.

Przed publikacją własnego forka zmień placeholder URL w `repository.yaml` oraz `youtube_downloader/config.yaml`.

## Panel i Ingress

Dodatek korzysta z natywnego Home Assistant Ingress. Panel **YouTube Downloader** z ikoną `mdi:youtube` jest dostępny w lewym menu Home Assistant i otwiera pełny interfejs aplikacji: analizę URL, formaty, pobieranie, historię, aktywne zadania oraz zapis transmisji live.

Port `8099/tcp` jest domyślnie niewystawiony na hosta. W typowej instalacji wystarcza bezpieczny dostęp przez Ingress.

## Przykładowe adresy

```text
https://www.youtube.com/watch?v=VIDEO_ID
https://youtu.be/VIDEO_ID
https://www.youtube.com/shorts/VIDEO_ID
https://www.youtube.com/playlist?list=PLAYLIST_ID
https://www.youtube.com/live/VIDEO_ID
```

## Trwałe dane

Pobrane materiały trafiają domyślnie do:

```text
/share/youtube_downloader
```

Historia pobrań jest przechowywana w `/data/jobs/history.json`. Katalogi `/share` oraz `/data` zachowują dane po restarcie i aktualizacji kontenera dodatku.

## Aktualizacja yt-dlp

Opcja `update_ytdlp_on_start` jest domyślnie aktywna. Przy starcie kontenera dodatek próbuje zaktualizować `yt-dlp`, czyli backend i zestaw extractorów używanych do obsługi zmian po stronie serwisu. Nie jest aktualizowany YouTube. Chwilowy brak sieci nie blokuje uruchomienia dodatku.

## Ograniczenia

Dodatek nie omija DRM ani paywalli. Nie obsługuje cookies YouTube, logowania do konta, prywatnych filmów ani mechanizmów obchodzenia zabezpieczeń. Użytkownik odpowiada za zgodność pobierania z prawem i warunkami korzystania z usługi.

Szczegóły konfiguracji znajdują się w [README dodatku](youtube_downloader/README.md) oraz w [dokumentacji](youtube_downloader/DOCS.md).
