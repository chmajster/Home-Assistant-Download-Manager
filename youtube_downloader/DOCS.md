# Dokumentacja działania

## Analiza przez yt-dlp

Po przesłaniu URL aplikacja sprawdza schemat i domenę, a następnie uruchamia `yt-dlp` w trybie pobierania samych metadanych. Extractor zwraca tytuł, kanał, miniaturę, czas trwania, status transmisji i dostępne formaty. Dla playlist aplikacja pokazuje elementy zwrócone przez extractor.

Przy właściwym pobieraniu aplikacja nie przyjmuje ścieżki docelowej od użytkownika. Wybiera szablon nazwy wewnątrz skonfigurowanego katalogu trwałego i ogranicza nazwy plików do bezpiecznego zestawu znaków obsługiwanego przez `yt-dlp`.

## Ingress i panel Home Assistant

W `config.yaml` aktywne są:

```yaml
ingress: true
ingress_port: 8099
panel_icon: mdi:youtube
panel_title: YouTube Downloader
```

Supervisor przekazuje ruch z panelu bocznego do wewnętrznego portu `8099`. Aplikacja uwzględnia nagłówek `X-Ingress-Path` przy generowaniu formularzy, linków do CSS i JavaScriptu, wywołań API oraz adresów pobieranych plików. Dzięki temu nie zakłada uruchomienia pod ścieżką `/`.

## Zadania i historia

Zwykłe pobrania wykonują się w workerach tła. Liczba równoległych zadań jest ograniczona przez `max_concurrent_jobs`. Aktywne zadania są przechowywane w pamięci procesu Gunicorn, więc po restarcie dodatku lista aktywnych operacji zaczyna się od nowa.

Po zakończeniu operacji wynik jest zapisywany w historii JSON:

```text
/data/jobs/history.json
```

Historia przetrwa restart kontenera. Po skasowaniu materiału rekord pozostaje widoczny, ale panel oznacza brak pliku.

## Zapis transmisji live

Aktywna transmisja live jest zapisywana przez osobny proces `yt-dlp`. Menedżer zadań przechowuje PID procesu, czyta jego postęp i pozwala wysłać bezpieczny sygnał przerwania z interfejsu. Jednoczesny drugi zapis tego samego URL jest odrzucany.

Zaplanowana transmisja może zostać przeanalizowana, ale przycisk nagrywania pozostaje niedostępny do chwili rozpoczęcia transmisji.

## Lokalizacja plików

Domyślny katalog:

```text
/share/youtube_downloader
```

Pliki są dostępne w udziale Home Assistant `/share`. Można przenieść je zwykłym narzędziem obsługującym udział Samba, dodatkiem File editor, SSH lub innym rozwiązaniem administracyjnym używanym w danej instalacji Home Assistant. Alternatywnie ustaw `download_dir` na katalog wewnątrz `/media`, aby udostępnić pliki w obszarze multimediów.

## Zmiana limitu zadań

Na karcie **Konfiguracja** dodatku ustaw `max_concurrent_jobs` na wartość od `1` do `5`, zapisz opcje i uruchom dodatek ponownie. Większy limit zwiększa obciążenie CPU, pamięci, sieci i miejsca docelowego.

## Aktualizacja extractora

Gdy `update_ytdlp_on_start` ma wartość `true`, skrypt usługi próbuje wykonać:

```sh
/venv/bin/python -m pip install --no-cache-dir --upgrade yt-dlp
```

Niepowodzenie jest logowane, ale nie blokuje startu panelu. Aktualizowany jest extractor `yt-dlp`, nie YouTube.
