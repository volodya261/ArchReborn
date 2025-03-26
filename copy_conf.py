import shutil
import os

src_dir = 'conf'
dest_dir = os.path.join(os.environ['HOME'], '.config') 

shutil.copytree(src_dir, dest_dir, dirs_exist_ok=True) 
