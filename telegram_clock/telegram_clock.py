import os 
import telethon
import numpy as np
import time
time.tzset()

import tempfile
import logging

from telethon import TelegramClient, sync
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from skimage.io import imread, imsave 

logger = logging.getLogger('telegram_clock.app')

class Telegram_clock():
   
    def __init__(self, datadir, con_name, api_id, api_hash, proxy=None):
        self.__API_ID = int(api_id)
        self.__API_HASH = api_hash
        self.__proxy = proxy
        self.__datadir = datadir
        self.__con_name = con_name
        self.connection = None
        self.image_dir = None
        self.last_time = time.localtime() 


    def __enter__(self):
        if not os.path.exists(os.path.join(tempfile.gettempdir(), 'telegram_images')):
            logger.info('Create temp directory')
            os.mkdir(os.path.join(tempfile.gettempdir(), 'telegram_images'))
        self.image_dir = os.path.join(tempfile.gettempdir(), 'telegram_images')
        logger.info('Create connection')
        self.connection = TelegramClient(self.__con_name, self.__API_ID, self.__API_HASH, proxy=self.__proxy).start()

        logger.info('Connection successfully create')
        return self

    def __exit__(self, *args, **kwargs):
        try:
            if os.listdir(self.image_dir):
                for file in os.listdir(self.image_dir):
                    os.remove(os.path.join(self.image_dir, file))
        except:
            # Не обращаем внимания на ошибки, поскольк все происходи во временной папке
            pass 
        self.connection.disconnect()
        

    def _check_time_change(self, tm):
        return bool(tm.tm_min - self.last_time.tm_min)


    def _create_time_image(self, tm):
        logger.info('Create image')
        hours = str(tm.tm_hour) if tm.tm_hour >= 10 else '0'+str(tm.tm_hour)
        minutes = str(tm.tm_min) if tm.tm_min >= 10 else '0'+str(tm.tm_min)
        
        first_hour = imread(os.path.join(self.__datadir, '{}.png'.format(hours[0])))
        second_hour = imread(os.path.join(self.__datadir, '{}.png'.format(hours[1])))
        delimiter = imread(os.path.join(self.__datadir, 'del.png'))
        first_minute = imread(os.path.join(self.__datadir, '{}.png'.format(minutes[0])))
        second_minute = imread(os.path.join(self.__datadir, '{}.png'.format(minutes[1])))

        background_color = second_hour[0,0,:]

        reuslt = np.concatenate([first_hour, second_hour, delimiter, first_minute, second_minute], axis=1)
        size = reuslt.shape[0], reuslt.shape[1]
        plaseholder =  np.full(( (4000-reuslt.shape[0])//2 ,reuslt.shape[1], 4), background_color)
        reuslt = np.concatenate([plaseholder, reuslt, plaseholder], axis=0)
        plaseholder =  np.full(( reuslt.shape[0], (4000-reuslt.shape[1])//2 , 4), background_color)
        reuslt = np.concatenate([plaseholder, reuslt, plaseholder], axis=1)

        imsave(os.path.join(self.image_dir, 'time.png') ,reuslt)
        logger.info('Image successfully create')
        return os.path.join(self.image_dir, 'time.png')


    def _update_avatar(self, image_path):
        logger.info('Delete old photos')
        self.connection(DeletePhotosRequest(self.connection.get_profile_photos('me')))
        file = self.connection.upload_file(image_path)
        logger.info('Create new photo')
        self.connection(UploadProfilePhotoRequest(file))
    
    def run(self):
        tm = time.localtime()
        if self._check_time_change(tm):
            logger.info('Change image')
            self.last_time = tm
            image_path = self._create_time_image(tm)
            if image_path:
                self._update_avatar(image_path)

        time.sleep(1)
