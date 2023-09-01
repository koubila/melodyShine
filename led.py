from lxml import etree
import time
import board
import neopixel
import threading
import asyncio
import sys

if len(sys.argv) > 1:
   modified_id2 = sys.argv[1]
   testOne = "Script lancé"
else:
    print("Form ID not provided.")

pixels1 = neopixel.NeoPixel(board.D18, 24, brightness=1)

def parse_music_xml(file_path):
    notes = []
    tempo = 60
    default_x_notes = {}
    measures = []

    tree = etree.parse(file_path)
    root = tree.getroot()

    for measure_element in root.xpath('//measure'):
        measure_data = []

        for note_element in measure_element.xpath('.//note[@default-x]'):
            step_element = note_element.find('pitch/step')
            alter_element = note_element.find('pitch/alter')
            duration_element = note_element.find('duration')  # Get duration element
            default_x = float(note_element.get('default-x'))
            default_x_int = int(default_x)  # Convert to integer to ignore decimals
            default_y_element = note_element.get('default-y')  # Get default-y value

            if step_element is not None:
                note = step_element.text
                if alter_element is not None:
                    alter_value = int(alter_element.text)
                    if alter_value > 0:
                        note += '#' * alter_value
                    elif alter_value < 0:
                        note += 'b' * abs(alter_value)

                # Check default-y and add '2' if necessary
                if default_y_element is not None and float(default_y_element) < -80:
                    note = '2' + note

                duration = ''  # Initialize duration string

                if duration_element is not None:
                    duration_value = int(duration_element.text)
                    duration = f'dur{duration_value}'  # Add duration to the note

                found = False

                for entry in measure_data:
                    if int(entry['default-x']) == default_x_int:
                        entry['notes'].append(note + duration)  # Append duration to note
                        found = True
                        break

                if not found:
                    measure_data.append({
                        'default-x': default_x_int,
                        'notes': [note + duration]  # Append duration to note
                    })

        # Sort entries based on default-x
        measure_data.sort(key=lambda entry: entry['default-x'])

        measures.append(measure_data)

    return measures, tempo

note_to_led_index = {
    'C': 0, 'C#': 1, 'Cs': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Ds': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Fs': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Gs': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'As': 10, 'Bb': 10, 'B': 11,
    '2C': 12, '2C#': 13, '2Cs': 13, '2Db': 13, '2D': 14, '2D#': 15, '2Ds': 15,
    '2Eb': 15, '2E': 16, '2F': 17, '2F#': 18, '2Fs': 18, '2Gb': 18, '2G': 19,
    '2G#': 20, '2Gs': 20, '2Ab': 20, '2A': 21, '2A#': 22, '2As': 22, '2Bb': 22,
    '2B': 23
}

def light_up_led(led_index, duration):
    if 0 <= led_index < 24:
        pixels1[led_index] = (0, 20, 255)
        duration = float(duration)  # Convert duration to float
        time.sleep(duration)
        pixels1[led_index] = (0, 0, 0)  # Turn off LED

def play_grouped_notes(led_indices, durations):
    threads = []
    for led_index, duration in zip(led_indices, durations):
        thread = threading.Thread(target=light_up_led, args=(led_index, duration))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

def play_music(measures, tempo):
    for measure in measures:
        for entry in measure:
            notes_to_play = [note.split('dur')[0] for note in entry['notes']]
            durations = [note.split('dur')[1] for note in entry['notes']]
            led_indices = [note_to_led_index[note] for note in notes_to_play]

            # Démarrer toutes les LED en parallèle
            play_grouped_notes(led_indices, durations)

            # Attendre que toutes les LED aient terminé
            for led_index, duration in zip(led_indices, durations):
                light_up_led(led_index, duration)

api_url = 'http://134.209.18.82/partitions/minecraft.xml'
if modified_id2:
	api_url = modified_id2
    
measures, tempo = parse_music_xml(api_url)

try:
    play_music(measures, tempo)
except KeyboardInterrupt:
    pixels1.fill((0, 0, 0))
