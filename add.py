import subprocess
import ffmpeg
import os
def extract_video_segment(input_video, start_time, duration, output_video):
    # 截取视频并将音频通道转换为 4 声道，并使用Vorbis音频编码
    ffmpeg.input(input_video, ss=start_time, t=duration) \
        .output(output_video, vcodec="libvpx", acodec="libvorbis", ac=4, audio_bitrate="128k") \
        .run(overwrite_output=True)
    print(f"Saved as {output_video}")

def convert_webm_to_mp4(input_file, output_file):
    """
    Converts a .webm file to .mp4 while keeping the 4-channel audio intact.
    
    Args:
        input_file (str): Path to the input .webm file.
        output_file (str): Path to the output .mp4 file.
    """
    # Ensure ffmpeg is available
    ffmpeg_path = 'ffmpeg'  # Make sure ffmpeg is installed and available in the system PATH

    if not os.path.exists(input_file):
        print(f"Input file {input_file} does not exist.")
        return

    # Command to convert .webm to .mp4, keeping 4-channel audio
    command = [
        ffmpeg_path,
        '-i', input_file,                 # Input file
        '-c:v', 'libx264',                # Video codec: H.264 for .mp4
        '-c:a', 'aac',                    # Audio codec: AAC
        '-ac', '4',                       # Set audio channels to 4
        '-b:a', '192k',                   # Audio bitrate (can adjust if necessary)
        '-strict', 'experimental',        # Necessary for using some codecs
        output_file                        # Output file
    ]

    try:
        # Run the ffmpeg command
        subprocess.run(command, check=True)
        print(f"Conversion successful: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")

def replace_audio_in_video(input_video, new_audio, output_video):
    command = [
        "ffmpeg",
        "-i", input_video,  # 输入视频
        "-i", new_audio,  # 输入新的 FLAC 音频
        "-c:v", "copy",  # 复制视频流，不重新编码
        "-c:a", "libvorbis",  
        "-ac", "4", 
        "-b:a", "128k",  # 设定音频比特率（可调整）
        "-map", "0:v:0",  # 选择第一个输入的视频流
        "-map", "1:a:0",  # 选择第二个输入的音频流
        "-af", "pan=4c|c0=c0|c1=c1|c2=c2|c3=c3",  # 确保 4 声道映射正确
        "-y", output_video  # 覆盖输出文件
    ]
    subprocess.run(command, check=True)
    print(f"Audio replaced successfully: {output_video}")

# 使用示例
name="V_To4k9AJXc"
start_time = 20

input_video = os.path.join("videos_gt", name + ".webm")
output_video = os.path.join("videos_gt", name + f"_{start_time}.webm")
try:
    extract_video_segment(input_video, start_time, 10, output_video)
except ffmpeg.Error as e:
    print(e.stderr)
convert_webm_to_mp4(input_video, os.path.join("videos_gt", name + f"_{start_time}.mp4"))



input_video = os.path.join("videos_gt", name + f"_{start_time}.webm")
new_audio = os.path.join("audio_gen", name + f"_{start_time}.flac")
output_video = os.path.join("videos_gen", name + f"_{start_time}.webm")
replace_audio_in_video(input_video, new_audio, output_video)
convert_webm_to_mp4(output_video, os.path.join("videos_gen", name + f"_{start_time}.mp4"))

new_audio = os.path.join("audio_mmaudio", name + f"_{start_time}.wav")
output_video = os.path.join("videos_mmaudio", name + f"_{start_time}.webm")
replace_audio_in_video(input_video, new_audio, output_video)
convert_webm_to_mp4(output_video, os.path.join("videos_mmaudio", name + f"_{start_time}.mp4"))

new_audio = os.path.join("audio_visage", name + f"_{start_time}.wav")
output_video = os.path.join("videos_visage", name + f"_{start_time}.webm")
replace_audio_in_video(input_video, new_audio, output_video)
convert_webm_to_mp4(output_video, os.path.join("videos_visage", name + f"_{start_time}.mp4"))


