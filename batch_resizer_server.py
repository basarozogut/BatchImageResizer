import cherrypy
from cherrypy.lib import static
import io
import batch_resizer
import batch_resizer_config_helper
import os
from PIL import Image
import tempfile
import uuid
from zipfile import ZipFile
import shutil
import configparser

app_name = 'batch_resizer'

# handle the callback
cherrypy.config.update({'server.socket_port': 80})

class FileDemo(object):
    @cherrypy.expose
    def index(self):
        return """
        <html><body>
            <h2>Upload File</h2>
            <form action="upload" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="uploadedFile" /><br />
            <input type="submit" value="Submit" />
            </form>
        </body></html>
        """

    @cherrypy.expose
    def upload(self, uploadedFile):
        buffer = io.BytesIO()

        while True:
            data = uploadedFile.file.read(8192)
            if not data:
                break
            buffer.write(data)

        img = Image.open(buffer)

        root_dir = os.path.join(tempfile.gettempdir(), app_name)
        if not os.path.isdir(root_dir):
            os.mkdir(root_dir)

        uid = str(uuid.uuid4())
        target_path = os.path.join(root_dir, uid)
        os.mkdir(target_path)

        cfg = configparser.ConfigParser()
        cfg.read("config.ini")
        # read image sizes
        sizes_text = cfg["DEFAULT"]["ImageSizes"]
        sizes = batch_resizer_config_helper.parse_image_sizes(sizes_text)

        successful = batch_resizer.batch_resize_image(img, target_path, sizes,
                                         resample=Image.BICUBIC, max_size_kilobytes=95, max_quality=95, min_quality=1)

        if not successful:
            return 'Procedure failed!'

        zip_path = os.path.join(target_path, 'batch_resize.zip')
        with ZipFile(zip_path, 'w') as zip:
            # writing each file one by one
            for f in os.listdir(target_path):
                if (f.endswith('.' + "jpg")):
                    zip.write(os.path.join(target_path, f), f)

        return static.serve_file(zip_path, 'application/x-download',
                                 'attachment', 'batch_resize.zip')


cherrypy.quickstart(FileDemo())
