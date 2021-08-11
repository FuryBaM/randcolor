import os,glob,random,sys,json,datetime,time
from tqdm import tqdm
from PIL import Image, ImageDraw

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def start():
	print(os.getcwd())
	inputNum=str(input(colors.OKGREEN+"Enter number to start a process\n1. Before fill provinces I recommend to calibrate\n2. Fill provinces with random color\n3. Remove borders\n4. Crop image for provinces\n5. Get a sample of the world map\n6. Exit\n"))
	switch = {
		1: Calibrate,
		2: FillProvinces,
		3: ClearBorders,
		4: CropImage,
		5: getExampleImage,
		6: sys.exit
	}
	clear()
	try:
		func = switch.get(int(inputNum), lambda: 6)
	except:
		sys.exit("Stopped")
	try:
		func()
	except Exception as error:
		clear()
		for val in range(len(sys.exc_info())):
			print(sys.exc_info()[val])
		start()
def getExampleImage():
	if os.name=='nt':
		os.system(f'copy {os.path.dirname(os.path.realpath(__file__))}/img.png {os.getcwd()}')
	else:
		os.system(f'cp {os.path.dirname(os.path.realpath(__file__))}/img.png {os.getcwd()}')
	print("Done!")
	start()
def Calibrate():
	imagename=printPictureList()
	img = Image.open(imagename)
	img = img.convert("RGB")
	width, height = img.size
	clear()
	print (f"{imagename}\nWidth: {width}\nHeight: {height}\n")	
	black = (0,0,0)
	water = (0,0,255)
	
	curPoint = 0
	for y in tqdm(range(round(height)), ascii=" ░▒▓"):
		for x in range(round(width)):
			curPoint=curPoint+1
			point = (x, y)
			if img.getpixel(point) != black and img.getpixel(point) != water:
				img.putpixel(point, (255,255,255)) 
	img.save(f"{imagename}")
	start()
def FillProvinces():
	WCRED = 0
	WCGREEN = 0
	WCBLUE = 255
	waterColor = WCRED, WCGREEN, WCBLUE
	fillProvsWithColor = str(input("\nDo you need to fill provinces with random color? Y/N\n")).upper()
	if fillProvsWithColor=="Y":
		imagename=printPictureList()
		img = Image.open(imagename)
		img.convert("RGB")
		img.save(f"temp.{imagename.split('.')[-1]}")
		imgP = Image.open(fR"temp.{imagename.split('.')[-1]}")
		imgP = imgP.convert("RGB")
	
		width, height = imgP.size
		clear()
		print (f"{imagename}\nWidth: {width}\nHeight: {height}\n")
		white = (255,255,255)
		black = (0, 0, 0)
		index = 0
		width = round(width/1)
		height = round(height/1)
		print("\nCalculating number of provinces\n")
		for y in tqdm(range(round(height)), ascii=" ░▒▓"):
			for x in range(round(width)):
				point = x, y
				if imgP.getpixel(point)==white:
					col=128, 128, 128
					index = index + 1
					ImageDraw.floodfill(imgP, point, col)
		os.remove(f"temp.{imagename.split('.')[-1]}")
		print(f"Provinces {index}")
		colorNumber = index
		filename = "colors"
	else:
		colorNumber = int(input("\nEnter number of colors\n"))
		filename = str(input("\nEnter file name to save color list\n"))
	try:
		colorListFile = open(f"{filename}.txt", "x")
	except:
		print(f"\nFile {filename}.txt exists. Skipping...\n")
		colorListFile = open(f"{filename}.txt", "w+")
		colorListFile.truncate(0)
		colorListFile.close()
	colors=[]
	print("\nGenerating colors\n")
	colorListFile = open(f"{filename}.txt", "w+")
	for i in tqdm(range(int(colorNumber)), ascii=" ░▒▓"):
		isDublicate=True
		while isDublicate==True:
			color= (random.randint(0,255), random.randint(0,255), random.randint(0,255))
			hex = '%02x%02x%02x' % color
			if hex not in colorListFile.read():
				colors.append(color)
				isDublicate=False
		colorListFile.write(f"#{hex}\n")
	print ("\nRandom colors generated!\n")
	
	if fillProvsWithColor=="Y":
		img = Image.open(imagename)
		width, height = img.size
		index = 0
		curPoint=0
		width = round(width/1)
		height = round(height/1)
		print("\nFloodfilling provinces\n")
		for y in tqdm(range(round(height)), ascii=" ░▒▓"):
			for x in range(round(width)):
				curPoint=curPoint+1
				point = x, y
				if img.getpixel(point)==white:
					r, g, b=colors[index]
					col=(r,g,b)
					index = index + 1
					ImageDraw.floodfill(img, point, col)
		img.save(f"result.{imagename.split('.')[-1]}")
	
	print (f"\nDone!\n")
	start()
	
def ClearBorders():
	imagename=printPictureList()
	img = Image.open(imagename)
	img = img.convert("RGB")
	clear()
	width, height = img.size
	print (f"{imagename}\nWidth: {width}\nHeight: {height}\n")
	black = 0, 0, 0
	curPoint=0
	width = round(width/1)
	height = round(height/1)
	print("\nRemoving borders\n")
	for y in tqdm(range(round(height)), ascii=" ░▒▓"):
		for x in range(round(width)):
			curPoint=curPoint+1
			point = x, y
			if img.getpixel(point)==black:
				isColorFound=False
				i=0
				j=0
				k=1
				checker=0
				fillColor = img.getpixel(point)
				sides=[]
				while fillColor==black:
					def one():
						i=x
						j=y+k
						return i,j
					def two():
						i=x
						j=y-k
						return i,j
					def three():
						i=x+k
						j=y
						return i,j
					def four():
						i=x-k
						j=y
						return i,j
					cells={
					1: one,
					2: two,
					3: three,
					4: four
					}
					randomSide=random.randint(1,4)
					cell = cells.get(randomSide, lambda: sys.exit)
					if cell not in sides:
						sides.append(cell)
					if len(sides)>=len(cells):
						k=k+1
						sides.clear()
						continue
					fillColor=img.getpixel(cell())
				img.putpixel(point, fillColor)
	img.save(f"resultWithColor.{imagename.split('.')[-1]}")
	start()

	
	
def CropImage():
	imagename=printPictureList()
	img = Image.open(imagename)
	img = img.convert("RGB")
	width, height = img.size
	clear()
	print (f"{imagename}\nWidth: {width}\nHeight: {height}\n")
	regions = []
	c = []#colors
	water = (0, 0, 255)
	c=list(img.getdata())
	regions=(list(set(c)))
	if water in regions:
		regions.remove(water)
	print(f"\nNumber of regions: {len(regions)}\n")
	ind = 0
	try:
		data=open("data.json","r+")
		data.truncate(0)
		data.write("{}")
		data.close()
	except:
		data=open("data.json", "x")
		data.write("{}")
		data.close()
	with open("data.json", "r+") as file:
		json_dump = json.load(file)
		json_dump["Regions"] = []
		print("\nFinding the border of the provinces and writing it in JSON format...\n")
		for color in tqdm(regions, ascii=" ░▒▓"):
			startX = (0, 0)
			endX = (0, 0)
			startY = (0, 0)
			endY = (0, 0)
			for y in range(height):
				for x in range(width):
					if (c[x + (width*y)] == color):
						if c[startX[0]+ (width * startX[1])] != color:
							startX = (x, y)
							endX = (x, y)
						if c[startY[0] + (width * startY[1])] != color:
							startY = (x, y)
							endY = (x, y)
						if startX[0] >= x:
							startX = (x, y)
						if endX[0] <= x:
							endX = (x, y)
						if startY[1] >= y:
							startY = (x, y)
						if endY[1] <= y:
							endY = (x, y)
			xs = startX[0] - 1
			ys = height - startY[1] - 2
			ws = endX[0] - startX[0] + 3
			hs = startY[1] - endY[1] + 3
			if hs < 0:
				ys = height-(ys - (ys - endY[1] + 3) + 5)
				hs = endY[1] - startY[1] + 3
			pos = ((startX[0]+endX[0])/2-(width/2)+1,(startY[1]+endY[1])/2-(height/2))
			json_dump["Regions"].append({"id":ind, "position": pos, "color": color, "hex": '%02x%02x%02x' % color, "xs": xs, "ys": ys, "ws": ws, "hs": hs})
			ind = ind + 1
		file.seek(0)
		json.dump(json_dump, file, indent=2)
		start()
    
def clear(): 
    if os.name== 'nt': 
        _ = os.system('cls') 
    else: 
        _ = os.system('clear')
        
def printPictureList():
	extensions=['png', 'bmp', 'jpg']
	files=[]
	pictures=[]
	for extension in extensions:
		if len(glob.glob(f'./*.{extension}'))>0:
			files.append(glob.glob(f'./*.{extension}'))
	i=1
	for file in files:
		for f in file:
			f=f.replace("./", "")
			pictures.append(f)
			print(f"{i}. {f}")
			i+=1
	pic=int(input("\nEnter picture number\n"))
	return pictures[pic-1]
        
if __name__ == "__main__":
    try:
    	from tqdm import tqdm
    	from PIL import Image, ImageDraw
    except:
    	os.system("pip install -r requirements.txt")
    	time.sleep(1)
    	os.system("python main.py")
    clear()
    try:
    	start()
    except Exception as error:
    	clear()
    	time.sleep(1)
    	sys.exit(colors.FAIL+str(error)+"\nsomething went wrong:("+colors.WARNING)