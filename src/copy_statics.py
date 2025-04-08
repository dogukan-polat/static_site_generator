import os, shutil

def copy_paste(source, destination):
    os.mkdir(destination)
    filelist = os.listdir(source)
    for filename in filelist:
        src_path = os.path.join(source, filename)
        dst_path = os.path.join(destination,filename)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            copy_paste(src_path, dst_path)

