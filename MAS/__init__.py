from MAS.config import FIRST_START, ROOT


print("CHECKING IF MODELS ARE DOWNLOADED")

if FIRST_START:
	import zipfile
	import gdown
	url = 'https://drive.google.com/uc?id=1PNR0ztzzbm1dguC0SC7GYl6dO9EI-ya4'
	output = ROOT+ '\Models.zip'
	gdown.download(url, output, quiet=False)
	with zipfile.ZipFile(output,"r") as zip_ref:
		zip_ref.extractall(ROOT)

