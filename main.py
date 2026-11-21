import os
import shutil

source = os.path.join(os.path.dirname(__file__), "output", "entry.png")
os.makedirs("/output", exist_ok=True)
shutil.copyfile(source, "/output/entry.png")
