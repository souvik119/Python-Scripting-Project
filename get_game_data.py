import os
import json
import shutil
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"


def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        # this break is because we only care about top level dirs with game and not subdirs
        break
    
    return game_paths

def get_name_from_paths(paths, to_strip):
    new_names = []
    for path in paths:
        # split path in base path + directory
        _, dir_name = os.path.split(path) # this func will split from the end
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    # check if directory exists if not create it
    if not os.path.exists(path):
        os.mkdir(path)

def copy_and_overwrite(source, dest):
    # if dir already exists then overwrite it
    # this is a recursive copy
    if os.path.exists(dest):
        # remove file
        shutil.rmtree(dest)
    shutil.copytree(source, dest)

def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames": game_dirs,
        "numberofGames": len(game_dirs)
    }
    with open(path, "w") as f:
        json.dump(data, f)


def main(source, target):
    cwd = os.getcwd()
    # generate full path of source and target dirs
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    # get paths of source dirs which contain game
    game_paths = find_all_game_paths(source_path)

    # get dir names without _game at the end
    new_game_dirs = get_name_from_paths(game_paths, "_game")

    # create target directory
    create_dir(target_path)
    
    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path, new_game_dirs)
    

if __name__ == '__main__':
    # this is only if the file is run directly, if imported this is skipped
    # idea is to get source and target dirs like python get_game_data.py <source> <target>
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only")

    # if source and target are mentioned correctly  
    source, target = args[1:]
    main(source, target)