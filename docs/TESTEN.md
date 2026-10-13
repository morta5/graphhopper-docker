# GraphHopper-Staging prüfen

`scripts/test.sh --fast` und `--full` prüfen das bestehende Autoprofil und
versionierte Speicherpfade. Ohne lokale Python-/YAML-Installation:
`scripts/test-docker.sh`. `scripts/install-hooks.sh` aktiviert Git-Prüfungen.

## Laufzeit am 12.10.2026

Auch das unveränderte neueste Release-JAR 11.1 enthielt im lokalen Scan
16 HIGH-Befunde. Das separate Staging-Image baut deshalb den Quellstand
`ebb578f4e94db72e82f2f8d3bc69417758e16e1c` mit geprüfter Archiv-Prüfsumme.
Das Abhängigkeits-Overlay liegt ausschließlich in diesem Repository;
Upstream-Repositories werden nicht geschrieben. Dropwizard 5.0.2, Jetty
12.1.14, Jackson 2.21.7, Protobuf 3.25.9 und HttpCore 5.4.3 ersetzen die
beanstandeten Linien. Drei generierte Protobuf-Methoden benötigen den
bereits vorhandenen Typparameter statt eines Platzhalters; Felder und
Drahtformat bleiben unverändert. Die alte Snake-Case-Testkonstante wird
über ihre aktuelle Jackson-Entsprechung angesprochen.

Der Quellbuild kompiliert auch die Upstream-Tests, führt deren vollständige
Suite jedoch nicht aus. Die eigenen Konfigurationsprüfungen, reale
Routing-Imageprüfung und das HIGH-/CRITICAL-Gate bleiben verbindlich.
`python3 scripts/image-smoke.py --image <Image>` prüft eine echte Autofahrt
auf synthetischen OSM-Straßen und die unprivilegierte Benutzerkennung.
Der erste Wolfi-Start fand Java nicht im PATH; das korrigierte Image
startet und routet. Lokaler Betriebssystem-/JAR-Scan: keine HIGH-/CRITICAL-
Befunde.

Offen: regionale Daten, Last-/Ressourcennachweis und gemeinsame
Routing-/Fahrerabläufe im Kubernetes-Cluster. Die kleinen Testdaten
beweisen keine flächendeckende Abdeckung.
