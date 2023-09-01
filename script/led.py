from lxml import etree
import time
import board
import neopixel
import threading
import asyncio

# 92.154.11.124
pixels1 = neopixel.NeoPixel(board.D18, 12, brightness=1)

def parse_music_xml(file_path):
    notes = []
    tempo = 60
    default_x_notes = {}

    tree = etree.parse(file_path)
    root = tree.getroot()

    for note_element in root.xpath('//note'):
        step_element = note_element.find('pitch/step')
        alter_element = note_element.find('pitch/alter')
        default_x_element = note_element.get('default-x')
        if step_element is not None:
            note = step_element.text
            if alter_element is not None:
                alter_value = int(alter_element.text)
                if alter_value > 0:
                    note += '#' * alter_value
                elif alter_value < 0:
                    note += 'b' * abs(alter_value)

            if default_x_element is not None:
                default_x = float(default_x_element)
                if default_x not in default_x_notes:
                    default_x_notes[default_x] = []
                default_x_notes[default_x].append(note)
            else:
                notes.append(note)

    tempo_element = root.find('.//per-minute')
    if tempo_element is not None:
        #tempo = int(tempo_element.text)
        tempo = 120

    return notes, default_x_notes, tempo

note_to_led_index = {
    'C': 0, 'C#': 1, 'Cs': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Ds': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Fs': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Gs': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'As': 10, 'Bb': 10, 'B': 11
}

def light_up_led(led_index_list):
    for led_index in led_index_list:
        if 0 <= led_index < 12:
            pixels1[led_index] = (0, 20, 255)

def turn_off_leds(led_indices):
    for led_index in led_indices:
        if 0 <= led_index < 12:
            pixels1[led_index] = (0, 0, 0)

def play_grouped_notes(led_index_list, note_duration):
    light_up_led(led_index_list)
    time.sleep(note_duration)
    turn_off_leds(led_index_list)

def play_music(notes, default_x_notes, tempo):
    note_duration = 60 / tempo

    for note_list in default_x_notes.values():
        led_indices = [note_to_led_index[note] for note in note_list]
        play_grouped_notes(led_indices, note_duration)

    for note in notes:
        if note not in [n for sublist in default_x_notes.values() for n in sublist]:
            led_index = note_to_led_index.get(note)
            if led_index is not None:
                light_up_led([led_index])
                turn_off_leds([led_index])
                
api_url = 'http://134.209.18.82/partitions/avengers_theme.xml'
#file_path = "/home/itroot/Téléchargements/Nouveau dossier/minecraft.xml"
notes, default_x_notes, tempo = parse_music_xml(api_url)

try:
    print(default_x_notes)
    print(tempo)
    play_music(notes, default_x_notes, tempo)
except KeyboardInterrupt:
    pixels1.fill((0, 0, 0))
