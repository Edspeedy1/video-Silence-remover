from pydub import AudioSegment
import moviepy.editor as mp
import os

def detect_long_pauses(audio, silence_threshold=-25, min_silence_duration=100):
    # Convert stereo to mono if needed
    if audio.channels > 1:
        audio = audio.set_channels(1)
    
    # for i, j in enumerate(audio):
    #     print(j.dBFS)

    pauses = []
    silence_chunks = AudioSegment.silent(duration=0)
    
    for i, chunk in enumerate(audio):
        if chunk.dBFS < silence_threshold:
            silence_chunks += chunk
        else:
            if len(silence_chunks) >= min_silence_duration:
                # Append the start and end time of the pause
                start_time = i * len(chunk)
                end_time = start_time + len(silence_chunks)
                pauses.append((start_time, end_time))
            silence_chunks = AudioSegment.silent(duration=0)
    
    return pauses
 
from moviepy.editor import VideoFileClip, concatenate_videoclips

def concatenate_subclips(output_video, subclips):
    # Concatenate the specified subclips
    concatenated_clip = concatenate_videoclips(subclips)

    # Write the concatenated subclips to a new file
    concatenated_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    # Close the concatenated clip to release resources
    concatenated_clip.close()


# Specify subclips (start_time, end_time)
# subclip1 = (5, 10)
# subclip2 = (15, 20)
# subclip3 = (25, 30)

# subclips = []
# for start, end in [subclip1, subclip2, subclip3]:
#     subclips.append(VideoFileClip(input_video_path).subclip(start, end))

# concatenate_subclips(input_video_path, output_video_path, subclips)



video = mp.VideoFileClip("realTest.mp4")
audio = AudioSegment.from_file(video.audio.filename)

long_pauses = detect_long_pauses(audio)

clips = []

cuts = [0] + [item for sublist in long_pauses for item in sublist]

num_columns = 2
num_rows = len(cuts) // num_columns
# cuts = [cuts[i * num_columns:(i + 1) * num_columns] for i in range(num_rows)]

print(audio.duration_seconds, long_pauses)

previous_cut = 0
for start, end in long_pauses:
    print(f"Start: {start}ms,   \tEnd: {end}ms, \tDuration: {end - start}ms")
    if max(end, start) < audio.duration_seconds*1000 and start > previous_cut: clips.append(video.subclip(start/1000, end/1000))
    previous_cut = end


concatenate_subclips("output.mp4", clips)
