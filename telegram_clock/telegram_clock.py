from telegram_clock.config import Config
from telegram_clock.exceptions import SessionIsNotInit

from telethon.sync import connection, TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.photos import DeletePhotosRequest, UploadProfilePhotoRequest
from PIL import Image
from loguru import _Logger as Logger  # type: ignore
from socks import SOCKS5
from threading import Thread, Event

import tempfile
import getpass
import time
import os


class TelegramClockClient:
    def __init__(self, config_path: str = "./configs/config.yaml"):
        time.tzset()
        self.config = Config.from_yaml(config_path)
        self.logger: Logger = self.config.logger.get_logger()

        if not os.path.exists(os.path.join(tempfile.gettempdir(), "telegram_images")):
            self.logger.info("Create temp directory")
            os.mkdir(os.path.join(tempfile.gettempdir(), "telegram_images"))
        self.image_dir = os.path.join(tempfile.gettempdir(), "telegram_images")

    def _init(self) -> None:
        """Init connection"""
        self.logger.info("Create connection")
        proxy = None
        client_connection = connection.ConnectionTcpFull
        if self.config.proxy is not None:
            if self.config.proxy.type.upper() == "MTPROTO":
                client_connection = connection.ConnectionTcpMTProxyRandomizedIntermediate
                proxy = (self.config.proxy.host, self.config.proxy.port, self.config.proxy.secret)
            elif self.config.proxy.type.upper() == "SOCKS5":
                proxy = (SOCKS5, self.config.proxy.host, self.config.proxy.port)  # type: ignore
        self.client = TelegramClient(
            session=StringSession(self.config.session),
            api_id=self.config.api_id,
            api_hash=self.config.api_hash,
            connection=client_connection,
            timeout=self.config.timeout,
            proxy=proxy,
        )
        phone = (
            self.config.phone_number
            if self.config.phone_number is not None
            else lambda: input("Please enter your phone (or bot token): ")
        )
        password = (
            self.config.password
            if self.config.password is not None
            else lambda: getpass.getpass("Please enter your password: ")
        )
        self.client.start(phone=phone, password=password)

        self.logger.info("Connection successfully create")
        self.last_time = time.localtime()

    def close(self) -> None:
        """Delete temp files and close connection"""
        try:
            if os.listdir(self.image_dir):
                for file in os.listdir(self.image_dir):
                    os.remove(os.path.join(self.image_dir, file))
        finally:
            self.client.disconnect()

    def _check_is_minute_change(self, tm: time.struct_time) -> bool:
        """
        Сheck that the minutes have changed

        Args:
            tm (struct_time): current time
        Returns:
            True if the minutes have changed else False
        """
        return bool(tm.tm_min - self.last_time.tm_min)

    def _create_time_image(self, tm: time.struct_time) -> str:
        """
        Create current time image and return path to it

        Args:
            tm (struct_time): current time
        Returns:
            String path to created image
        """
        self.logger.info("Create image")
        hours = str(tm.tm_hour) if tm.tm_hour >= 10 else "0" + str(tm.tm_hour)
        minutes = str(tm.tm_min) if tm.tm_min >= 10 else "0" + str(tm.tm_min)

        first_hour = Image.open(os.path.join(self.config.data_dir, "{}.png".format(hours[0]))).convert("RGB")
        second_hour = Image.open(os.path.join(self.config.data_dir, "{}.png".format(hours[1]))).convert("RGB")
        delimiter = Image.open(os.path.join(self.config.data_dir, "del.png")).convert("RGB")
        first_minute = Image.open(os.path.join(self.config.data_dir, "{}.png".format(minutes[0]))).convert("RGB")
        second_minute = Image.open(os.path.join(self.config.data_dir, "{}.png".format(minutes[1]))).convert("RGB")

        result_size = (4000, 4000)
        background_color = second_hour.getpixel((1, 1))
        reuslt = Image.new(mode="RGB", size=result_size, color=background_color)
        coord_left = result_size[0] // 2 - delimiter.width // 2 - first_hour.width - second_hour.width
        coord_upper = result_size[1] // 2 - delimiter.height // 2

        for image in [
            first_hour,
            second_hour,
            delimiter,
            first_minute,
            second_minute,
        ]:
            coords = (coord_left, coord_upper)
            reuslt.paste(image, coords)
            coord_left += image.width

        reuslt.save(os.path.join(self.image_dir, "time.png"))
        self.logger.info("Image successfully create")
        return os.path.join(self.image_dir, "time.png")

    def _update_avatar(self, image_path: str) -> None:
        """
        Update telegram avatar. Function removed all old avatars and set new
        """
        self.logger.info("Delete old photos")
        self.client(DeletePhotosRequest(self.client.get_profile_photos("me")))
        self.logger.info("Create new photo")
        self.client(UploadProfilePhotoRequest(self.client.upload_file(image_path)))

    def init_session(self):
        """Check if sessin is exists"""

        def timer(timeout: int, stop_event: Event) -> None:
            """
            Timeout function. Raise SessionIsNotInit error if time is done.
            """
            start_time = time.monotonic()
            while True:
                if stop_event.is_set():
                    return
                if time.monotonic() - start_time > timeout:
                    raise SessionIsNotInit("Session is not init")
                time.sleep(0.1)

        if os.environ.get("TELEGRAM_SESSION") is None:
            raise SessionIsNotInit("Session string is not found")

        stop_event = Event()
        timer_job = Thread(target=timer, args=(10, stop_event))
        timer_job.start()
        self._init()
        stop_event.set()
        timer_job.join()

    def run_application(self):
        """Run application"""
        self.init_session()
        while True:
            tm = time.localtime()
            if self._check_is_minute_change(tm):
                self.logger.info("Change image")
                self.last_time = tm
                image_path = self._create_time_image(tm)
                if image_path:
                    self._update_avatar(image_path)
                    os.remove(image_path)
            time.sleep(1)

    def print_session_string(self):
        """Print current session string"""
        self._init()
        print(self.client.session.save())
