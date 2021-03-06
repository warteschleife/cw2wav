**Vorrede:** *Dies ist ein Miniprojekt unter vielen und bietet auch wirklich keine Funktionen, die nicht auch von anderen frei verfügbaren Programmen und Diensten bereitgestellt werden.*
 
# cw2wav
## Übersicht

Kern des Projekts ist eine Klasse, die aus einem Text eine WAV Sounddatei mit CW generieren kann. Rund um diese Klasse gibt es ein paar Skripte, mit denen Übrungstexte auf verschiedene Arten erzeugt werden können.

### cw2wav.py

Mit diesem Skript kann der Inhalt einer normalen Text Datei in ein Soundfile nach Wave Format umgewandelt werden, welches den Text als Morsezeichen enthält.

### randomwords.py

Dieses Skript spielt erzeugt eine Textdatei mit zufälligem Inhalt. Um den Text als CW zu hören, muss man auf cw2wav.py zurückgreifen.
### improve.py

Dieses Skript ist eine Art Weiterentwicklung von randomwords.py. Es wird ebenfalls in Verbindung mit cw2wav.py verwendet. Dem Skript kann man die eigenen Ergebnisse des letzten Durchgangs übergeben. Das Skript analysiert das Ergebnis und erkennt die Zeichen, die falsch erkannt wurden. Es führt eine ganze Historie. Anhand dieser Historie legt das Programm fest, welche Zeichen häufiger geübt werden sollen und welche weniger häufig.
### rss2cw.py

Mit diesem Skript kann man direkt auf RSS/Atom Feeds zugreifen und sich die Einträge vorlesen lassen. Das funktioniert mit einer Reihe von Webseiten. Der RSS/Atom Support ist allerdings eher rudimentär.

## Voraussetzungen

Da es sich um ein Python Projekt handelt, sollte ein Python Interpreter vorhanden sein. Ich habe es mit der Version `3.7.4` auf einem Windows-Rechner getestet. Eventuell müssen einige Python-Module nachinstalliert werden. Das sollte aber mit `pip` normalerweise kein Problem sein.

Nachdem die WAV Datei erzeugt wurde, spielt das Skript cw2wav.py diese auch ab, sofern das Modul 'winsound' installiert ist. Andernfalls endet das Skript mit dem Speichern der WAV-Datei

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
