import os
import shutil

SUBDIRS = {
    "VIDEOS": ['.mov', '.avi', '.mp4', '.m4v', '.ogv', '.webm', '.wmv']
}


# get files in directories and subdirectories using glob
def get_files(source_dir):
    """
    It takes a directory as an argument and returns a list of all the files in that directory and all of its subdirectories

    :param source_dir: the directory to get the files from
    :return: A list of all the files in the source directory and its subdirectories.
    """
    # get the files in the source directory
    files = os.listdir(source_dir)
    # create a list to store the files
    file_list = []
    # loop through the files
    for file in files:
        # get the file name
        file_name = os.path.join(source_dir, file)
        # if the file is a directory
        if os.path.isdir(file_name):
            # get the files in the subdirectory
            sub_files = get_files(file_name)
            # add the files to the list
            file_list.extend(sub_files)
        # if the file is a file
        else:
            # add the file to the list
            file_list.append(file)
    # return the list
    return file_list


# get files that endswith a video extension using get_files function
def get_videos(source_dir):
    """
    It takes a directory as an argument, gets the files in the directory, creates a list to store the files, loops through
    the files, gets the file name, checks if the file is a directory, gets the files in the subdirectory, adds the files to
    the list, checks if the file is a file, gets the file extension, checks if the file extension is a video extension, adds
    the file to the list, and returns the list

    :param source_dir: the directory to search for videos
    :return: A list of video files.
    """
    # get the files in the source directory
    files = get_files(source_dir)
    # create a list to store the files
    video_files = []
    # loop through the files
    for file in files:
        # get the file name
        file_name = os.path.join(source_dir, file)
        # if the file is a directory
        if os.path.isdir(file_name):
            # get the files in the subdirectory
            sub_files = get_videos(file_name)
            # add the files to the list
            video_files.extend(sub_files)
        # if the file is a file
        else:
            # get the file extension
            file_ext = os.path.splitext(file_name)[1]
            # if the file extension is a video extension
            if file_ext in SUBDIRS["VIDEOS"]:
                # add the file to the list
                video_files.append(file)
    # return the list
    return video_files


# move small files to small_files directory using get_videos function
def move_small(source_dir, size: int):
    """
    It takes a source directory and a size in megabytes as arguments, and moves all files smaller than the size to a new
    directory called small_files

    :param source_dir: the directory where the files are located
    :param size: the size of the file in megabytes
    :type size: int
    """

    # get current working directory and create dest_dir named small_files
    cwd = os.getcwd()
    dest_dir = os.path.join(cwd, 'small_files')
    # create a list to store the file sizes

    # get the files in the source directory
    files = get_videos(source_dir)
    # loop through the files
    for file in files:
        # check if file exists
        if os.path.exists(os.path.join(source_dir, file)):
            # get the file size
            file_size = os.path.getsize(os.path.join(source_dir, file))
            # convert the file size to megabytes
            file_size_mb = file_size / 1000000
            # if the file size is smaller than 100 megabytes
            if file_size_mb < size:
                # create a directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                # move the file to the destination directory
                shutil.move(os.path.join(source_dir, file), dest_dir)


def move_large(source_dir, size: int):
    """
    It takes a source directory and a size in megabytes as arguments, and moves all files larger than the specified size to
    a new directory called large_files

    :param source_dir: the directory where the files are located
    :param size: the size of the file in megabytes
    :type size: int
    """
    # get current working directory and create dest_dir named small_files
    cwd = os.getcwd()
    dest_dir = os.path.join(cwd, 'large_files')
    # create a list to store the file sizes

    # get the files in the source directory
    files = get_videos(source_dir)
    # loop through the files
    for file in files:
        # check if file exists
        if os.path.exists(os.path.join(source_dir, file)):
            # get the file size
            file_size = os.path.getsize(os.path.join(source_dir, file))
            # convert the file size to megabytes
            file_size_mb = file_size / 1000000
            # if the file size is smaller than 100 megabytes
            if file_size_mb > size:
                # create a directory if it doesn't exist
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                # move the file to the destination directory
                shutil.move(os.path.join(source_dir, file), dest_dir)


def get_file_sizes(source_dir):
    """
    It takes a directory as input and returns a list of files in that directory along with their sizes.

    :param source_dir: The directory from which you want to get the file sizes
    """
    f = lambda x: os.path.isfile(os.path.join(source_dir, x))
    files_list = filter(f, os.listdir(source_dir))

    # Create a list of files in directory along with the size
    size_of_file = [
        (f, os.stat(os.path.join(source_dir, f)).st_size)
        for f in files_list
    ]
    # Iterate over list of files along with size
    # and print them one by one.
    for f, s in size_of_file:
        print("{}: {} MB".format(f, round(s / (1024 * 1024), 3)))


def remove_directories():
    """
    If the large_files and small_files directories exist, remove them
    """
    # get current working directory
    cwd = os.getcwd()
    # get the large_files directory
    large_files_dir = os.path.join(cwd, 'large_files')
    # get the small_files directory
    small_files_dir = os.path.join(cwd, 'small_files')
    # if the large_files directory exists
    if os.path.exists(large_files_dir):
        # remove the large_files directory
        shutil.rmtree(large_files_dir)
    # if the small_files directory exists
    if os.path.exists(small_files_dir):
        # remove the small_files directory
        shutil.rmtree(small_files_dir)
