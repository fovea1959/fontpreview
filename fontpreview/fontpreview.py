#!/usr/bin/env python3
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# fontpreview -- fontpreview
#
#     Copyright (C) 2020 Matteo Guadrini <matteo.guadrini@hotmail.it>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Callable
from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw, ImageFont

_Size = tuple[int, int]

CALC_POSITION: dict[str, Callable[[_Size, _Size], _Size]] = {
    'center': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, (ixy[1] - fxy[1]) // 2),
    'top': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, 0),
    'below': lambda ixy, fxy: ((ixy[0] - fxy[0]) // 2, (ixy[1] - fxy[1])),
    'rcenter': lambda ixy, fxy: ((ixy[0] - fxy[0]), (ixy[1] - fxy[1]) // 2),
    'rtop': lambda ixy, fxy: ((ixy[0] - fxy[0]), 0),
    'rbelow': lambda ixy, fxy: ((ixy[0] - fxy[0]), (ixy[1] - fxy[1])),
    'lcenter': lambda ixy, fxy: (0, (ixy[1] - fxy[1]) // 2),
    'ltop': lambda _ixy, _fxy: (0, 0),
    'lbelow': lambda ixy, fxy: (0, (ixy[1] - fxy[1])),
}


def _bbox2size(bbox: tuple[int, int, int, int]) -> _Size:
    # bounding box: (left, top, right, bottom)
    return bbox[2] - bbox[0], bbox[1] - bbox[3]


def get_font_size(font: ImageFont.FreeTypeFont, text, **kwargs):
    return _bbox2size(font.getbbox(text, **kwargs))


def get_multiline_textsize(draw: ImageDraw.ImageDraw, text, font=None, **kwargs):
    return _bbox2size(
        draw.multiline_textbbox(xy=[0, 0], text=text, font=font, **kwargs)
    )


class FontPreview:
    """
    Class that represents the preview of a font.
    """

    def __init__(
        self,
        font,
        font_size=64,
        font_text='a b c d e f',
        color_system='RGB',
        bg_color='white',
        fg_color='black',
        dimension=(700, 327),
    ):
        """
        Object that represents the preview of a font.

        :param font: font file
        :param font_size: font size. Default is 64.
        :param font_text: font text representation. Default is 'a b c d e f'.
        :param color_system: color system string. Default is 'RGB'.
        :param bg_color: background color of preview. Default is 'white'.
        :param fg_color: foreground or font color of preview. Default is 'black'.
        :param dimension: dimension of preview. Default is 700x327.
        """
        # Define properties
        self.image: Image.Image
        self.font_size = font_size
        self.font_text = font_text
        self.font = ImageFont.truetype(font=font, size=self.font_size)
        self.color_system = color_system
        self.bg_image = None
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.dimension = dimension
        self.font_position: tuple[float, float] = CALC_POSITION['center'](
            self.dimension,
            get_font_size(self.font, self.font_text),
        )

        # Create default image
        self.draw()

    def __str__(self):
        """
        String representation of font preview.

        :return: string
        """
        return (
            f'font_name:{self.font.getname()},font_size:{self.font_size},'
            f'text:{self.font_text},text_position:{self.font_position},'
            f'dimension:{self.dimension}'
        )

    def __resize(self):
        """
        Resize the font if it exceeds the size of the background.

        :return: None
        """
        draw = ImageDraw.Draw(self.image)

        # Check font size
        text_size = get_multiline_textsize(
            draw=draw, text=self.font_text, font=self.font
        )
        while text_size > self.dimension:
            self.font_size -= 2
            self.font = ImageFont.truetype(font=self.font.path, size=self.font_size)
            text_size = get_multiline_textsize(
                draw=draw, text=self.font_text, font=self.font
            )

    def save(self, path=None):
        """
        Save the preview font.

        :param path: path where you want to save the preview font
        :return: None
        """
        path = path or Path() / 'fontpreview.png'
        self.image.save(path)

    def draw(self, align='left'):
        """
        Draw image with text based on properties of this object.

        :param align: alignment of text. Available 'left', 'center' and 'right'
        :return: None
        """
        # Set an image
        if self.bg_image:
            self.image = Image.open(self.bg_image)

        # Draw background with flat color
        else:
            self.image = Image.new(
                self.color_system, self.dimension, color=self.bg_color
            )

        draw = ImageDraw.Draw(self.image)
        draw.text(
            self.font_position,
            self.font_text,
            fill=self.fg_color,
            font=self.font,
            align=align,
        )

    def show(self):
        """
        Displays this image.

        :return: None
        """
        self.image.show()

    def set_font_size(self, size):
        """
        Set size of font.

        :param size: size of font
        :return: None
        """
        # Set size of font
        self.font_size = size
        self.font = ImageFont.truetype(font=self.font.path, size=self.font_size)
        self.__resize()

        # Create image
        self.draw()

    def set_text_position(
        self,
        position: tuple[float, float]
        | Literal[
            'center',
            'top',
            'below',
            'rcenter',
            'rtop',
            'rbelow',
            'lcenter',
            'ltop',
            'lbelow',
        ],
    ):
        """
        Set position of text.

        :param position: Position can be a tuple with x and y axis, or a string.
            The strings available are 'center', 'top', 'below', 'rcenter',
            'rtop', 'rbelow', 'lcenter', 'ltop' and 'lbelow'.

        :return: None
        """
        # Create image drawer
        if isinstance(position, tuple):
            self.font_position = position
        else:
            draw = ImageDraw.Draw(self.image)
            fxy = get_multiline_textsize(draw=draw, text=self.font_text, font=self.font)
            fn = CALC_POSITION.get(position, CALC_POSITION['center'])
            self.font_position = fn(self.dimension, fxy)

        # Create image
        self.draw()
