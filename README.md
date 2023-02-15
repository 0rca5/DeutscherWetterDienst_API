# DeutscherWetterDienst_API
Eine API um Wettermeldungen des DWD zu verarbeiten.

Diese Schnittstelle dient dazu die öffentlichen Daten der API des Deutschen Wetterdienstes in eine NoSQL Datenbank zu schreiben.
Anschließend sollen die Daten dann mittels GraphQL beliebig abgefragt werden können.

Link zur API des Deutschen Wetterdienstes: https://dwd.api.bund.dev/

Das Projekt besteht neben den Python-typischen Dateien (requirements,LICENSE,setup, etc.) aus den packages graphqlAPI, welches das modules-package enthält, 
und tests, welches die Tests für die API enthält.

modules-package:
- Persistence.py: Datenzugriffsschicht. Modul, dass die Datenzugriffsmethoden auf die Datenbank bereitstellt.
- Service.py: Geschäftslogik. Zwischenebene zwischen Persistenz- und Anwenderebene. Enthält Funktionen zum Erstellen, Lesen und Aktualisieren von Daten.
- graphql_Client.py: Enthält die Funktionalitäten, um die spezifischen graphQl-Anfragen aufzulösen.
- Model.py: Modelliert die Typen für den graphql_client.

test-package:
- Test_Service: Testet die Funktionalitäten der Geschäftslogik (Service.py).
- Test_graphql_client: Testet die Funktionalitäten der graphql_client.py.

Generischer Ablauf einer Abfrage mittels GraphQL:
Die Abfrage wird über die "/graphql"-Schnittstelle an den graphQL Client weitergeleitet und aufgelöst. 
Dieser ruft den Service auf, um die gewünschten Daten aus der Datenbank zu lesen.
Die Daten werden anschließend über den Client und die "/graphql"-Schnittstelle zurückgeschickt.

