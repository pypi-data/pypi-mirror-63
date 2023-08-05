"""
interface for puppet
"""
from __future__ import annotations

from abc import ABC
from enum import Enum
from .file_box import FileBox


class Puppet(ABC):
    """
    puppet interface class
    """

    def __init__(self):
        self.name: str = 'puppet'

    # pylint: disable=R0201
    async def message_image(
            self,
            message_id: str,
            image_type: Enum
    ) -> FileBox:
        """
        docstring
        :param message_id:
        :param image_type:
        :return:
        """
        raise NotImplementedError

    def start(self) -> None:
        """
        start the puppet
        :return:
        """
        raise NotImplementedError
