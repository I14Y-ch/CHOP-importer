# Title
Schweizerische Operationsklassifikation (CHOP) - Systematisches Verzeichnis - Version {YEAR}
# Description
Die schweizerische Operationsklassifikation (CHOP) dient der Erfassung von Behandlungen im Rahmen der Erhebung Spitalstationäre Gesundheitsversorgung (SpiGes).

In der Einleitung des systematischen Verzeichnisses (PDF) der CHOP können die Informationen zur Grundlage, zu den inhaltlichen Änderungen und zu den technischen Bemerkungen entnommen werden. Die deutschsprachige PDF-Version des systematischen Verzeichnisses ist die Referenzversion.
Die PDF- und CSV-Dateien der systematischen und alphabetischen Verzeichnisse sowie die Überleitungstabelle und die Multilang-Tabelle stehen auf folgender Internetseite des BFS zur Verfügung: https://www.bfs.admin.ch/bfs/de/home/statistiken/gesundheit/nomenklaturen/medkk/instrumente-medizinische-kodierung.html

Die Publikation auf der I14Y-Interoperabilitätsplattform dient primär der Bereitstellung des JSON-Formats. (Auf der I14Y steht ebenfalls eine CSV-Datei der CHOP zum Download zur Verfügung. Diese entspricht nicht den oben genannten CSV-Dateien.)

Über den Reiter «Inhalt» haben Sie Zugriff zur Baumstruktur der Klassifikation. Die Baumstruktur mit den Kode-Nummern und Kode-Titeln erscheint links auf der Internetseite. Die Zusatzinformationen der jeweiligen Klassifikationsebene können, per Klick auf die betroffene Zeile, rechts angezeigt werden.

Die Zusatzinformationen werden unter «Annotationen» wie folgt angezeigt:
Unter dem Header «Typ» kann es folgende Einträge geben: «CodeWithoutPunctuation», die Kürzel «B, I, S, X, N» (B: ergänzende Beschreibung; I: Inklusivum; S: Kodiere ebenso; X: Exklusivum; N: Beachte), «Lateral» oder «Codable».
Ein «Typ» kann mit einer Zeile mit dem Header «Titel» oder «Text» ergänzt werden. (Die Zeilen mit dem Header «Titel» enthalten nicht den «Kode-Titel».)
«CodeWithoutPunctuation» gibt unter dem Header «Titel» den Kode ohne Punkte an.
«B», «I», «S», «X» und «N» geben unter dem Header «Text» den Text an.
«Lateral» wird unter dem Header «Typ» nur angegeben, wenn die Seitigkeit für diesen Kode erfasst werden muss. Fehlt die Angabe «Lateral», ist die Erfassung der Seitigkeit optional.
«Codable» gibt unter dem Header «Titel» die Werte «Yes», «No» oder «Complement» an.

Kontakt: MedNom@bfs.admin.ch