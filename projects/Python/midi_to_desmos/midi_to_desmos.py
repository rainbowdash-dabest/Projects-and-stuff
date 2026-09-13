import pretty_midi
import numpy as np

## I'm too lazy to code in cc midi fetching, so do it manually as a func_change 0->1->0 abs 0^0^i loop or sm

def midi_data_extract(midi_path):
    midi_data = pretty_midi.PrettyMIDI(midi_path)
    est_global_tempo = midi_data.estimate_tempo()
    song_start = float('inf')

    note_cum_list = []
    inst_list = []

    for instrument in midi_data.instruments:
        if not instrument.notes:
            continue

        t_init = min(note.start for note in instrument.notes)
        if t_init < song_start:
            song_start = t_init
    
        track_name = instrument.name if instrument.name else f"Program {instrument.program}"
        inst_list.append(str(track_name))
 
        l_i = []
        for note in instrument.notes:
            l_i.append([
                float(note.start),                 # Absolute seconds
                int(note.pitch),                   # 0-127
                float(note.end - note.start),      # Duration
                int(note.velocity)                 # 0-127
            ])
        l_i.sort(key=lambda x: x[0]) #sort by starttime
        note_cum_list.append(l_i)
    if song_start == float('inf'):
        song_start = 0.0     
    return note_cum_list, est_global_tempo, inst_list, song_start

def bpm_extract(bpm):
    bpm1 = bpm
    p1=[i for i, s in enumerate(inst) if ('drum' in s.lower())]

    idx_trk = p1[0] if p1 else 0

    if len(l) > 0 and len(l[idx_trk]) > 0:
        trk = np.array(l[idx_trk][:int(note_apx/2)])
        start_times = trk[:, 0]
        l2 = np.diff(start_times) #deltas
        l2 = l2[l2 > 0.02]  # filtered
    
        quant_l2 = np.round(l2 / 0.05) * 0.05

        vals, counts = np.unique(quant_l2, return_counts=True)
        main_beat_dur = vals[np.argmax(counts)]

        bpm1 = 60 / main_beat_dur

        while bpm1 > 190:
            bpm1 /= 2
        while bpm1 < 50:
            bpm1 *= 2
    return bpm1
def quant(BPM=120, drop_calcs=False):
    if not drop_calcs:
        b = BPM
    else:
        b = 60
    for i in range(len(l)):
        p = np.array(l[i][:])
        if p.size > 0:
            p[:, 0] = (p[:, 0] - song_str) * b / 60  # Re-zero time anchor
            p[:, 2] = p[:, 2] * b / 60  # Convert duration to beats
            p[:, 0] = np.round(p[:, 0] * quant_pb) / quant_pb
            p[:, 2] = np.round(p[:, 2] * quant_pb) / quant_pb
            p[p[:, 2] == 0, 2] = round(1/quant_pb,4)
        l1.append(p)

def print_and_csv(title=''):
    for idx, track_arr in enumerate(l1):
        print(f"Track {idx+1}, {inst[idx]} Matrix Shape: {track_arr.shape}")

    print(f"Estimated Global Tempo: {bpm1} BPM")

    for idx, track_arr in enumerate(l1):
        if track_arr.size == 0:
            continue
            
        safe_name = inst[idx].replace(' ', '_').replace('/', '_').replace('\\', '_') #change weird names
        filename = f"{title}_track_{idx+1}_{safe_name}.csv"
        
        # autosaves as csv from np array
        np.savetxt(filename, track_arr, delimiter=",", 
            header="start,pitch,duration,velocity", fmt=["%.4f", "%d", "%.4f", "%d"]  # prevents scientific notation
        )

def print_and_txt(title=''):
    for idx, track_arr in enumerate(l1):
        print(f"Track {idx+1} ({inst[idx]}) Matrix Shape: {track_arr.shape}")

    print(f"Estimated Global Tempo: {bpm1} BPM")

    for idx, track_arr in enumerate(l1):
        if track_arr.size == 0:
            continue
        
        flat_earth = track_arr.flatten()
        flatter=[]
        for idx1, val in enumerate(flat_earth):
            if idx1 % 4 == 0 or idx1 % 4 == 2:  # start time or duration
                flatter.append(f"{val:.4f}")
            else:
                flatter.append(str(int(val)))  # pitch or velocity
    
        boo=''
        iterator2000=(len(flatter) + (4 * max_notes) - 1)
        for i in range(iterator2000//(4*max_notes)):
            r=",".join(flatter[i*4*max_notes:(i+1)*4*max_notes])
            boo+=f"[{r}]\n"

        safe_name = inst[idx].replace(' ', '_').replace('/', '_').replace('\\', '_') #change weird names
        filename = f"{title}_track_{idx+1}_{safe_name}.txt"
        
        with open(filename, "w") as f:
            f.write(boo)


#mid='~/Desktop/Happy-Birthday-To-You-4.mid'
#mid="~/Desktop/[folder_name]/audios for desmusico/mario_1 desmusico.mid"
mid="~/Desktop/The Spectre(download).mid"
l, bpm, inst, song_str = midi_data_extract(mid)

title='spectre_1'
force_bpm = 128
drop_calc = False
note_apx = 2000
max_notes = 2500 #10,000 elements a list in desmos, needs to be modular instead.
quant_pb = 64 #quantisation per beat

l1=[]
bpm1 = bpm_extract(bpm)
quant(BPM=force_bpm, drop_calcs=drop_calc)
print_and_csv(title=title)

'''
with open('mid_extract.txt', 'w') as f:
    for idx, track_arr in enumerate(l1):
        f.write(f"--- Track: {inst[idx]} ---\n")
        f.write(str(track_arr) + '\n')

# sustain possible dealing (new CSVs)
s_i = []
        sustain_events = [cc for cc in instrument.control_changes if cc.number == 64]
        sustain_events.sort(key=lambda x: x.time)
        
        last_state = None
        for cc in sustain_events:
            binary_state = 1 if cc.value >= 64 else 0
            # Only capture the exact timestamp when the pedal actually switches state
            if binary_state != last_state:
                s_i.append([float(cc.time), binary_state])
                last_state = binary_state
            
        sustain_cum_list.append(s_i)
'''