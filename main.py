import os
import platform
from moviepy.editor import *
from moviepy.video.fx.resize import resize

TARGET_HEIGHT = 720
TARGET_WIDTH = 1280
FPS = 30
IMAGE_DURATION = 5
BUFFER_DURATION = 0.5

IS_WINDOWS = (platform.system() == "Windows")
FILE_PATH_SPLIT_TOKEN = "\\" if IS_WINDOWS else "/"
SCRIPT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
FILE_PREFIX_WHITELIST_PATH = os.path.join(SCRIPT_DIRECTORY, "file_prefixes_whitelist.txt")
FILE_EXTENSION_WHITELIST_PATH = os.path.join(SCRIPT_DIRECTORY, "file_extension_whitelist.txt")


def get_working_directory_as_list():
    return os.getcwd().split(FILE_PATH_SPLIT_TOKEN)


def get_files_in_directory():
    return [ f for f in os.listdir( os.curdir ) if os.path.isfile(f) ] #list comprehension version.


def get_sanitised_unordered_list_from_file(file_path):
    file_contents = []
    with open(file_path) as f:
        file_contents = f.readlines()
    stripped_contents = list(map(lambda val : val.strip(), file_contents))
    length_pairs = list(map(lambda v : (-len(v), v), stripped_contents))
    length_pairs.sort()
    return list(map(lambda pair : pair[1], length_pairs))


def create_clip(file_path):
    IMAGE_EXTENSIONS = ["jpg", "jpeg", "png"]
    is_image = any(filter(lambda ext : file_path.endswith(ext), IMAGE_EXTENSIONS))
    return resize(ImageClip(file_path, duration=IMAGE_DURATION), width=TARGET_WIDTH, height=TARGET_HEIGHT) if is_image \
        else VideoFileClip(file_path, target_resolution=(TARGET_HEIGHT, TARGET_WIDTH)).set_fps(FPS)


def create_final_video(file_paths):
    print("Compiling video")
    full_cwd_path = get_working_directory_as_list()
    final_clip_name = full_cwd_path[-1] if full_cwd_path else "result"
    final_clip_name += ".mp4"
    clips = []
    for path in file_paths:
        try:
            print(f"Creating clip for {path}...")
            new_clip = create_clip(path)
            clips.append(new_clip)
        except AttributeError:
            print(f"The file {path} could not be converted into a clip! It will be skipped.")
    
    final_clip = concatenate_videoclips(clips, method="compose", padding=BUFFER_DURATION)
    final_clip.write_videofile(final_clip_name, fps=FPS)
    print(f"Wrote to file with name \"{final_clip_name}\".")


def run():
    file_prefixes = get_sanitised_unordered_list_from_file(FILE_PREFIX_WHITELIST_PATH)
    file_extensions = get_sanitised_unordered_list_from_file(FILE_EXTENSION_WHITELIST_PATH)
    files_in_directory = get_files_in_directory()
    print(f"Prefix whitelist: {file_prefixes}")
    print(f"Extension whitelist: {file_extensions}")
    filtered_file_pairs = []
    for file in files_in_directory:
        extension_valid = any(filter(lambda ext : file.endswith(ext), file_extensions))
        matching_prefs = list(filter(lambda pref : file.startswith(pref), file_prefixes))
        
        if extension_valid and matching_prefs:
            filtered_file_pairs.append( (file.removeprefix(matching_prefs[0]), file) )

    print(f"Found { len(files_in_directory) } files. { len(filtered_file_pairs) } match the whitelists.")
    filtered_file_pairs.sort()
    resulting_files = list(map(lambda pair : pair[1], filtered_file_pairs))
    if resulting_files:
        create_final_video(resulting_files)
    else:
        print("Unable to create video")


if __name__ == "__main__":
    run()