**Vorrede:** *Dies ist ein Miniprojekt unter vielen und bietet auch wirklich keine Funktionen, die nicht auch von anderen frei verfügbaren Programmen und Diensten bereitgestellt werden.*
 
# cw2wav
## Übersicht

Kern des Projekts ist das Python Skript `cw2wav.py`. Mit diesem Skript kann der Inhalt einer normalen Text Datei in ein Soundfile nach Wave Format umgewandelt werden, welches den Text als Morsezeichen enthält. Nachdem die Sounddatei erzeugt wurde, wird sie auch sofort abgespielt.

In dem Projekt sind noch weitere Dateien enthalten:

- `cw2wav.yaml`: In dieser Datei sind Parameter gespeichert, die beim Erzeugen des Morsecodes beachtet werden sollen. Das sind Zeichenlängen, Tonfrequenz, Samplingrate usw.
- `alphabet.txt`: In dieser Datei sind die eigentlichen Morsezeichen definiert.

Zum Projekt gehört auch das Skript `randomwords.py`. Damit können Textdateien erzeugt werden, die Wörter aus 5 zufällig ausgewählten Zeichen beinhalten.

## Voraussetzungen

Da es sich um ein Python Projekt handelt, sollte ein Python Interpreter vorhanden sein. Ich habe es mit der Version `3.7.4` auf einem Windows-Rechner getestet. Eventuell müssen einige Python-Module nachinstalliert werden. Das sollte aber mit `pip` normalerweise kein Problem sein.

## Vorbereitung

Zunächst sollte man sich das ZIP-Archiv des Projekts von der Webseite laden. Diese Möglichkeit eröffnet sich, wenn man den grünen "Code"-Button oben rechts drückt.

Das Archiv kann man lokal in einem beliebigen Verzeichnis entpacken.
## Ein erster Versuch

Die folgende Beschreibung bezieht sich auf Windows 10.

Man öffnet ein Kommandozeilenfenster und wechselt in das Verzeichnis, in dem das Archiv entpackt wurde.

Im Archiv ist eine Beispieldatei, die sinnigerweise "beispiel.txt" heisst, enthalten. Diese kann man in eine WAV-Datei
umwandeln und sich zugleich vorspielen lassen, indem man folgendes Kommando eingibt:

`python cw2wav.py default beispiel.txt beispiel.wav`

Der Morsecode sollte jetzt zu hören sein. Außerdem sollte anschließend die Datei "beispiel.wav" auf der Festplatte zu finden sein.

## Konfiguration

Als ersten Parameter wurde im letzten Abschnitt `default` übergeben. Damit wurde die Konfiguration für die Umwandlung ausgewählt.

Vor der eigentlichen Umwandlung wird die Datei `cw2wav.yaml` eingelesen und hier nach der Konfiguration mit dem gewünschten Namen (in diesem Fall `default`) gesucht.

In einer Konfiguration können verschiedene Parameter festgelegt werden:

| Parameter | Bedeutung | Standardwert |
| --------- | --------- | ------------ |
| `sampling_rate` | Samplerate für die Sounddatei in Samples pro Sekunde. | 44000 |
| `len_dit` | Länge eines DIT in Sekunde(n). Die Länge des DAH wird daraus abgeleitet (dreifache Länge). | 0,1 |
| `character_gap` | Zeit zwischen zwei Morsezeichen in Sekunden. Wenn nicht angegeben, wird dieser Wert aus der Länge eine DIT abgeleitet. | 3 x `len_dit` |
| `ramp_time` | Tastung (Beschreibung weiter unten) | `len_dit` / 8 |
| `frequency` | Tonhöhe in Hz | 680 |

### Die `ramp_time`

Mit der `ramp_time` kann die Tastung eingestellt werden.

Bei einer harten Tastung würde der Morseton abrupt ein und wieder ausgeschaltet. Das hört man deutlich und ist sehr unangenehm. Ein einfacher Weg, diesen Effekt etwas abzuschwächen besteht darin, den Ton am Anfang langsam anschwellen zu lassen und am Ende langsam verstummen zu lassen. Das ist die Rampe.

Setzt man `ramp_time` auf 0,01, so wird ein Morseton zunächst in den ersten 0,01 Sekunden von 0 auf maximale Lautstärke anschwellen, dann konstant bleiben und am Ende für 0,01 Sekunden leiser werden. Die Dauer, während der der Ton eine Konstante Lautstärke hat, wird entsprechend kürzer. Daher sollte der Wert niemals größer sein als die halbe Länge eines DIT. 

Wird für `ramp_time` kein Wert angegeben, so wird als Wert ein Achtel der DIT-Zeit angenommen.

### Die Basiskonfiguration

Jede Konfiguration in der `cw2wav.yaml` hat einen Namen. Anhand dieses Namens wählt das Programm die richtige Konfiguration aus. Der Name hat aber noch einen zweiten Zweck: Eine Konfiguration kann sich auf eine Basiskonfiguration beziehen.

In einer Konfiguration kann mit `basis` ein Name einer anderen Konfiguration angegeben werden. Damit werden alle Einstellungen aus dieser Basiskonfiguration übernommen, soweit sie nicht durch die eigene Konfiguration überschrieben werden.
