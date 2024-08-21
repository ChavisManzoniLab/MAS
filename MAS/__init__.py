from MAS.config import  ROOT
import os
import tensorflow as tf
import torch

print("███████████████████████████████████████████████████████████")
print("GPU CHECK")
print("███████████████████████████████████████████████████████████")

if  tf.test.is_built_with_cuda():
	print("TENSORFLOW AND GPU WORKING")
else :
	("TENSORFLOW NOT WORKING WITH GPU")

print("███████████████████████████████████████████████████████████")

if torch.cuda.is_available():
	print("TORCH IS WORKING WITH GPU")
else: 
	("TORCH NOT WORKING ON GPU")

print("███████████████████████████████████████████████████████████")


print("CHECKING IF MODELS ARE DOWNLOADED")



if not os.path.isdir(ROOT + 'Models'):
	import zipfile
	import gdown
	url = 'https://drive.google.com/uc?id=1PNR0ztzzbm1dguC0SC7GYl6dO9EI-ya4'
	output = ROOT+ '\Models.zip'
	gdown.download(url, output, quiet=False)
	with zipfile.ZipFile(output,"r") as zip_ref:
		zip_ref.extractall(ROOT)
	os.remove(ROOT + '\Models.zip') 

