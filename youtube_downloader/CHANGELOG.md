# Changelog

## 1.1.0

- Dodano publiczne materiały Instagram obsługiwane przez `yt-dlp`: posty, reels, stories, tagi i profile.
- Dodano publiczne kanały live, VOD i klipy Kick obsługiwane przez `yt-dlp`.
- Uogólniono mechanizm zapisu aktywnego live i dodano nazwę rozpoznanego serwisu w wyniku analizy.
- Zachowano dotychczasowy slug oraz katalog pobrań, aby aktualizacja nie zmieniała lokalizacji danych.

## 1.0.5

- Dodano rozmiar pliku w historii pobrań na komputerze i telefonie.
- Rozmiar jest utrwalany w historii i pozostaje widoczny po usunięciu pliku.

## 1.0.4

- Dodano spinner, blokadę przycisku i komunikat oczekiwania po uruchomieniu analizy URL.

## 1.0.3

- Poprawiono katalog roboczy i ścieżkę importu Gunicorna dla aplikacji skopiowanej do `/app`.

## 1.0.2

- Usunięto zależność buildu od serwerów pakietów Alpine.
- Dodano statyczne wieloarchitekturowe binaria `ffmpeg` i `ffprobe`.
- Dodano lokalny wheelhouse Pythona instalowany offline podczas budowania obrazu.

## 1.0.1

- Dodano ponawianie instalacji pakietów Alpine podczas budowania obrazu po chwilowych błędach DNS.
- Dodano jawne limity czasu i ponawianie pobierania zależności Python.

## 1.0.0

- Pierwsze wydanie dodatku Home Assistant.
- Panel Ingress z analizą filmów, Shorts, playlist i transmisji live.
- Pobieranie w tle z postępem, prędkością i ETA.
- Kontrolowane uruchamianie i zatrzymywanie zapisu live.
- Trwała historia JSON oraz pliki w `/share` lub `/media`.
- Wieloarchitekturowe budowanie dla aktualnie wspieranych platform `amd64` i `aarch64`.
- Opcjonalna aktualizacja `yt-dlp` przy każdym starcie dodatku.
