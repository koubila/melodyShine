# melodyShine

Devenez un virtuose du piano avec MelodyShine!
Ce code est une application Python qui lit un fichier XML contenant des données musicales au format MusicXML et les joue à l'aide de LEDs pour créer un effet lumineux en fonction des notes et des durées de la musique.

Voici une description détaillée des principales parties du code :

1. Importation de bibliothèques :
   - `lxml.etree` est utilisé pour analyser et manipuler le XML.
   - `time` est utilisé pour gérer les temps d'attente.
   - `board` et `neopixel` sont utilisés pour contrôler les LEDs connectées à une carte (probablement une Raspberry Pi).
   - `threading` est utilisé pour exécuter les LEDs en parallèle.
   - `sys` est utilisé pour récupérer des arguments de ligne de commande.

2. Lecture des arguments de ligne de commande :
   - Si au moins un argument est passé lors de l'exécution du script, le premier argument est stocké dans `modified_id2` et `testOne` est défini sur "Script lancé".
   - Sinon, un message est imprimé indiquant que l'ID de formulaire n'a pas été fourni.

3. Initialisation des LEDs :
   - Un objet `NeoPixel` est créé pour gérer une bande de 24 LEDs, connectées au GPIO D18.

4. `parse_music_xml(file_path)` :
   - Cette fonction analyse le fichier XML fourni (peut être une URL) à l'aide de `lxml.etree` et extrait les informations musicales telles que les notes, les durées et les positions X/Y.
   - Les données extraites sont stockées dans la liste `measures` et la valeur du tempo est également renvoyée.

5. `note_to_led_index` :
   - Un dictionnaire qui mappe les noms des notes aux indices des LEDs correspondantes dans la bande de LEDs. Cela permet de faire correspondre les notes de la musique aux LEDs spécifiques.

6. `light_up_led(led_index, duration)` :
   - Cette fonction allume la LED correspondante pendant la durée spécifiée, puis l'éteint.

7. `play_grouped_notes(led_indices, durations)` :
   - Cette fonction lance des threads pour allumer les LEDs correspondantes en parallèle avec les durées spécifiées.

8. `play_music(measures, tempo)` :
   - Cette fonction itère à travers les mesures musicales et les entrées (notes et durées).
   - Elle convertit les noms de notes en indices de LEDs, puis joue les LEDs correspondantes avec les durées spécifiées.

9. Récupération du fichier XML :
   - Une URL est définie par défaut pour récupérer le fichier XML contenant les données musicales. Si `modified_id2` est fourni, l'URL est remplacée par sa valeur.

10. Appel des fonctions principales :
   - Le fichier XML est analysé à l'aide de `parse_music_xml()` pour obtenir les mesures et le tempo.
   - La musique est jouée à l'aide de `play_music()` en utilisant les mesures et le tempo.

11. Gestion de l'interruption :
   - Le bloc `try`/`except` capture une interruption (probablement un signal `KeyboardInterrupt` tel que Ctrl+C) et éteint toutes les LEDs avant de quitter le programme.

En résumé, ce code utilise des LEDs pour créer des effets lumineux basés sur une partition musicale au format MusicXML. Chaque note de la musique est associée à une LED spécifique, et les LEDs sont allumées et éteintes en fonction des notes et des durées de la musique pour que l’utilisateur puisse en temps réelle jouer du piano.