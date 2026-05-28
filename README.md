# Interaktiver_Plot

Wir starten im Terminal mit dem Befehl: pip install -r requirements.txt ! Damit installieren wir die benötigten Pakete

Alle unsere Funktionen befinden sich in der functions.py Datei die wir in unsere main.py Datei importieren.

Mithilfe eines Sliders kann man die eigene maximale Herzfrequenz einstellen.

Dann wird mithilfe von unseren Funktionen, den Daten aus der csv Datei und der gewählten Maximalherzfrequenz ein Plot erstellt der sowohl die Leistung als auch die Herzfrequenz in ihren #verschiedenen Zonen anzeigt.

Unter dem Plot sind die errechneten Leistungswerte gefolgt von zwei Tabellen in Tabs die die Zeit in den Zonen und die durschschnittliche Leistung in den Zonen anzeigen.

Wir führen es dann mit run streamlit .\main.py
