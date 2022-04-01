from PIL import Image
import PIL.ExifTags
import os

class ImageMeta():
    def __init__(self, file: str) -> None:
        self.file = file
        self.image = Image.open(self.file)
        
    def get_image_meta(self) -> dict[str | float, str | float] | None:
        if os.path.isfile(self.file):
            exifdata = self.image.getexif()
            image_meta: dict[str | float, str | float] = {}
            for key, value in exifdata.items():
                tag = PIL.ExifTags.TAGS.get(key, key)
                image_meta[tag] = value
            return image_meta
        else:
            return None
        
    def pretty_print_meta(self) -> None:
        data = self.get_image_meta()
        if data != None:
            if len(data) > 0:
                for key, value in self.get_image_meta().items(): # type: ignore
                    print(f'{key}: {value}')
            else:
                print('>> No meta data.')
        else:
            print('>> File does not exist.')
    
    def remove_meta(self, save_path: str) -> None:
        if os.path.isfile(self.file):
            self.image.save(f'{save_path}\\NoMeta-{os.path.basename(self.file)}')
            print('>> Meta data removed.')
        else:
            print('>> File does not exist.')
