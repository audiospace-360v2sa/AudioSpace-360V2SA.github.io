import subprocess
import ffmpeg
import os



def convert_webm_to_mp4(input_file, output_file):
    ffmpeg_path = 'ffmpeg'

    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    command = [
        ffmpeg_path,
        '-i', input_file,
        '-c:v', 'libx264',
        '-c:a', 'aac',
        '-ac', '4',
        '-b:a', '192k',
        '-strict', 'experimental',
        output_file
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def replace_audio_in_video(input_video, new_audio, output_video):
    command = [
        "ffmpeg",
        "-i", input_video,
        "-i", new_audio,
        "-c:v", "copy",
        "-c:a", "libvorbis",
        "-ac", "4",
        "-b:a", "128k",
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-af", "pan=4c|c0=c0|c1=c1|c2=c2|c3=c3",
        "-y", output_video
    ]
    subprocess.run(command, check=True)
    print(f"Audio replaced successfully: {output_video}")

def process_video(input_video, audio_directories):
    output_video = os.path.join("videos_gt", os.path.basename(input_video))
    #convert_webm_to_mp4(input_video, output_video.replace(".webm", ".mp4"))

    for audio_dir in audio_directories:
        base_name = os.path.splitext(os.path.basename(input_video))[0]
        audio_files = [f for f in os.listdir(audio_dir) if f.startswith(base_name)]

        for audio_file in audio_files:
            audio_path = os.path.join(audio_dir, audio_file)
            if audio_file.endswith(".flac") or audio_file.endswith(".wav"):
                output_video = input_video.replace("videos_gt", f"videos_{audio_dir.replace('audio_', '')}")
                replace_audio_in_video(input_video, audio_path, output_video)
                convert_webm_to_mp4(output_video, output_video.replace(".webm", ".mp4"))

# 获取 video_gt 目录下的所有 .webm 文件
video_dir = "videos_gt"
audio_dirs = ["audio_gen"]
webm_files = [f for f in os.listdir(video_dir) if f.endswith(".webm")]

for webm_file in webm_files:
    input_video_path = os.path.join(video_dir, webm_file)
    process_video(input_video_path,  audio_directories=audio_dirs)
