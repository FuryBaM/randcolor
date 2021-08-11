from randcolor import menu
try:
    from tqdm import tqdm
    from PIL import Image, ImageDraw
except:
    os.system("pip install -r requirements.txt")
    time.sleep(1)
    os.system("randcolor")