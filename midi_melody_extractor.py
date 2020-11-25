import mido
import copy


def get_note(msg):
    dict = msg.dict()
    if 'note' not in dict.keys():
        return -999
    else:
        return dict['note']

def break_track_into_moments(track):
    moments = []
    temp_list = []
    for msg in track:
        time_incr = msg.dict()['time']
        if time_incr == 0:
            temp_list.append(msg)
        else:
            moments.append(temp_list)
            temp_list = []
            temp_list.append(msg)
    return moments

def single_track_upper_melody(track):
    temp_time_to_add = 0
    new_list = []

    for msg in track:
        dict = msg.dict()
        if 'channel' in dict.keys() and dict['channel'] != 0:
            time_to_add = dict['time']
            temp_time_to_add = temp_time_to_add + time_to_add
        else:
            msg.time = msg.time + temp_time_to_add
            temp_time_to_add = 0
            new_list.append(msg)

    moments = break_track_into_moments(new_list)
    watchlist = []
    result_list = []

    temp_time_to_add = 0
    for m in moments:
        tmp_block_list = []
        highest_note_value = max([get_note(x) for x in m])
        for msg in m:
            # not top voice begin:
            if msg.type == 'note_on' and msg.dict()['note'] < highest_note_value and msg.dict()['velocity'] > 0:
                note = msg.dict()['note']
                watchlist.append(note)
                temp_time_to_add = temp_time_to_add + msg.dict()['time']
            # not top voice end:
            elif msg.type == 'note_on' and  msg.dict()['velocity'] == 0 and msg.dict()['note'] in watchlist:
                note = msg.dict()['note']
                watchlist.remove(note)
                temp_time_to_add = temp_time_to_add + msg.dict()['time']
            # top voice:
            else:
                msg.time = msg.dict()['time'] + temp_time_to_add
                temp_time_to_add = 0
                tmp_block_list.append(msg)
        result_list.extend(tmp_block_list)

    result_track = copy.deepcopy(track)
    result_track.clear()
    # result_track = mido.MidiTrack()
    result_track.extend(result_list)
    return result_track

def midi_file_melody_only(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path, clip=True)
    track = midi_file.tracks[0]
    resulted_track = single_track_upper_melody(track)

    midi_file.tracks[0] = resulted_track

    return midi_file
