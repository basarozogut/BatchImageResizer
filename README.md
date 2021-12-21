# Batch Image Resizer
A batch image resizer written in python.

A friend of mine needed a batch image resizer with some spesific constraints:
- The images needed to be downsized to spesific sizes (7 different sizes to be exact) like: 1024x768, 640x480 etc.
- The images needed to be smaller than 100kb.

He was struggling to resize the images every time manually, creating several copies of images and reducing the JPEG quality until it is smaller than 100kb. It took too much time and effort for a simple automatable task. So I wrote a simple python code with a basic UI. While I was at it, I isolated the core part into another module and programmed 3 different user modules:
- A desktop application using tkinter. It allows user to batch resize images directly on a pc.
- A web application using cherrypy. It allows users to batch resize on a server and the server returns a zip file containing all of the resized images.
- A telegram bot using telegram.ext. It allows users to send an uncompressed image to the bot and bot returns a zip file containing all of the resized images.

Images are resized on the fly and brute forced to worse qualities until they conform the file size restriction.

### Telegram bot preview:

<p align="center">
  <img width="764" src="https://github.com/basarozogut/BatchImageResizer/blob/main/preview/preview_telegram.png">
</p>

### Contents of the zip file:

<p align="center">
  <img width="849" src="https://github.com/basarozogut/BatchImageResizer/blob/main/preview/preview_download.png">
</p>

### Usage
If you want to give it a try, download/clone the repository, copy the config.ini.sample as config.ini and fill in the required fields. Then run the module of choice.

#### Dependencies:
- PIL is required for every module.
- cherrypy is required for web application
- telegram.ext is required for telegram bot.
