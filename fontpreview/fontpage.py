#!/usr/bin/env python3
# vim: se ts=4 et syn=python:

# created by: matteo.guadrini
# fontpage -- fontpreview
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

from pathlib import Path
from typing import Literal

from PIL import Image, ImageDraw

from .fontbanner import FontBanner, FontLogo
from .fontpreview import CALC_POSITION, FontPreview, get_font_size


class FontPage:
    """
    Class that represents the page of a font banners.
    """

    def __init__(
        self,
        template=None,
        dimension=(2480, 3508),
        header=None,
        logo=None,
        body=None,
        footer=None,
    ):
        """
        Object that represents the page of a font banners.

        :param template: template used to build the page
        :param dimension: dimension of page. Default A4 in pixels.
        :param header: header of fontpage object
        :param logo: logo of fontpage object on header part
        :param body: body of fontpage object
        :param footer: footer of fontpage object
        """
        self.template = template
        if self.template:
            self.dimension = (dimension[0], self.template.page_height)
        else:
            self.dimension = dimension

        self.color_system = 'RGB'
        self.page = Image.new(self.color_system, self.dimension, color='white')

        self.header: FontBanner | None
        self.logo: FontPreview | None
        self.body: FontPreview | None
        self.footer: FontPreview | None

        # Set header
        if header:
            self.set_header(header)
        else:
            self.header = None

        # Set logo
        if logo:
            self.set_logo(logo)
        else:
            self.logo = None

        # Set body
        if body:
            self.set_body(body)
        else:
            self.body = None

        # Set footer
        if footer:
            self.set_footer(footer)
        else:
            self.footer = None

    def __str__(self):
        """
        String representation of font page.

        :return: string
        """
        return f'header={self.header}, body={self.body}, footer={self.footer}'

    def __compose(self):
        """
        Dynamically compose the page.

        :return: None
        """
        # Check if the template is specified
        if not self.template:
            self.template = FontPageTemplate(self.dimension[1])

        if self.header is None or self.body is None or self.footer is None:
            msg = 'header, body and footer is mandatory object'
            raise AttributeError(msg)

        # Check height of each part

        # Compose background
        self.dimension = (self.dimension[0], self.template.page_height)
        self.page = Image.new(self.color_system, self.dimension, color='white')

        # Compose header
        self.set_header(self.header)
        if self.header.image.height != self.template.header_units:
            self.header.dimension = (self.page.width, self.template.header_units)
        self.header.set_font_size(self.template.header_font_size)
        self.header.set_text_position(self.template.header_text_position)

        # Compose body
        self.set_body(self.body)
        if self.body.image.height != self.template.body_units:
            self.body.dimension = (self.page.width, self.template.body_units)
        self.body.set_font_size(self.template.body_font_size)
        self.body.set_text_position(self.template.body_text_position)

        # Compose footer
        self.set_footer(self.footer)
        if self.footer.image.height != self.template.footer_units:
            self.footer.dimension = (self.page.width, self.template.footer_units)
        self.footer.set_font_size(self.template.footer_font_size)
        self.footer.set_text_position(self.template.footer_text_position)

    def set_header(self, header):
        """
        Set header of Font page.

        :param header: FontPreview object
        :return: None
        """
        # Check if header is FontPreview object
        if isinstance(header, FontBanner):
            # Check width of header
            if self.page.width != header.image.width:
                header.dimension = (self.page.width, header.image.height)
                header.draw()
            self.header = header
        else:
            msg = f'header must be FontPreview based object, not {header}'
            raise TypeError(msg)

    def set_logo(self, logo):
        """
        Set logo of Font page.

        :param logo: FontLogo object
        :return: None
        """
        if not isinstance(logo, FontLogo):
            msg = f'logo must be FontLogo object, not {logo}'
            raise TypeError(msg)

        if not self.header:
            msg = 'header attribute is None'
            raise ValueError(msg)

        # Check size of header
        if self.header.image.size < logo.image.size:
            logo.new_size((75, 75))

        # Add logo on header
        self.header.add_image(
            logo,
            CALC_POSITION['lcenter'](
                self.header.dimension,
                get_font_size(self.header.font, self.header.font_text),
            ),
        )

    def set_body(self, body):
        """
        Set body of Font page.

        :param body: FontPreview object
        :return: None
        """
        if not isinstance(body, FontPreview):
            msg = f'body must be FontPreview based object, not {body}'
            raise TypeError(msg)

        # Check width of body
        if self.page.width != body.image.width:
            body.dimension = (self.page.width, body.image.height)
            body.draw()

        self.body = body

    def set_footer(self, footer):
        """
        Set footer of Font page.

        :param footer: FontPreview object
        :return: None
        """
        if not isinstance(footer, FontPreview):
            msg = f'footer must be FontPreview based object, not {footer}'
            raise TypeError(msg)

        # Check width of footer
        if self.page.width != footer.image.width:
            footer.dimension = (self.page.width, footer.image.height)
            footer.draw()
        self.footer = footer

    def draw(self, *, separator=True, sep_color='black', sep_width=5):
        """
        Draw font page with header, logo, body and footer.

        :param separator: line that separates the parts
        :param sep_color: separator color
        :param sep_width: separator width
        :return: None
        """
        # Compose all parts
        self.__compose()

        assert self.header is not None
        assert self.body is not None
        assert self.footer is not None

        header_start = (0, 0)
        self.page.paste(self.header.image, header_start)

        body_start = (0, self.header.image.height)
        self.page.paste(self.body.image, body_start)

        footer_start = (0, (self.body.image.height + self.header.image.height))
        self.page.paste(self.footer.image, footer_start)

        # Draw line
        if separator:
            draw = ImageDraw.Draw(self.page)

            # Header/Body line
            body_finish = (self.page.width, self.header.image.height)
            draw.line([body_start, body_finish], fill=sep_color, width=sep_width)

            # Body/Footer line
            footer_finish = (
                self.page.width,
                self.body.image.height + self.header.image.height,
            )
            draw.line([footer_start, footer_finish], fill=sep_color, width=sep_width)

    def save(self, path=None):
        """
        Save the font page.

        :param path: path where you want to save the font page
        :return: None
        """
        path = path or Path() / 'fontpage.png'
        self.page.save(path)

    def show(self):
        """
        Displays this image.

        :return: None
        """
        self.page.show()


class FontPageTemplate:
    """
    Class representing the template of a FontPage object.
    """

    def __init__(self, page_height=3508, units_number=6):
        """
        Object representing the template of a FontPage object.

        :param page_height: height of FontPage object. Default is 3508.
        :param units_number: division number to create the units
        """
        # Calculate units
        self.page_height = page_height
        self.unit = self.page_height // units_number

        # header
        self.header_font_size = 120
        self.header_units = self.unit
        self.header_text_position = 'center'

        # body
        self.body_font_size = 140
        self.body_units = self.unit * 3
        self.body_text_position = 'center'

        # footer
        self.footer_font_size = 120
        self.footer_units = self.unit * 2
        self.footer_text_position = 'center'

    def __str__(self):
        """
        String representation of font page.

        :return: string
        """
        return f'page_height={self.page_height}, unit={self.unit}'

    def __check_units(self, context: Literal['header', 'body', 'footer'], unit):
        """
        Check the overrun of the units.

        :param context: context is part of page; header, body or footer
        :param unit: height of unit
        :return: None
        """
        # Check context
        if context == 'header':
            total_units = unit + self.body_units + self.footer_units
        elif context == 'body':
            total_units = self.header_units + unit + self.footer_units
        elif context == 'footer':
            total_units = self.header_units + self.body_units + unit
        else:
            msg = 'context must be "header","body" or "footer"'
            raise ValueError(msg)

        # Check if total units overrun maximum height
        if total_units > self.page_height:
            msg = (
                'The height of the units exceed the maximum allowed: '
                f'{self.page_height}'
            )
            raise ValueError(msg)

    def set_header(self, font_size, units, text_position):
        """
        Setting the header properties.

        :param font_size: the header font size
        :param units: the header units number
        :param text_position: the header text position
        :return: None
        """
        # header
        self.header_font_size = font_size
        unit = self.unit * units
        self.__check_units('header', unit)
        self.header_units = unit
        self.header_text_position = text_position

    def set_body(self, font_size, units, text_position):
        """
        Setting the body properties.

        :param font_size: the body font size
        :param units: the body units number
        :param text_position: the body text position
        :return: None
        """
        # header
        self.body_font_size = font_size
        unit = self.unit * units
        self.__check_units('body', unit)
        self.body_units = unit
        self.body_text_position = text_position

    def set_footer(self, font_size, units, text_position):
        """
        Setting the footer properties.

        :param font_size: the footer font size
        :param units: the footer units number
        :param text_position: the footer text position
        :return: None
        """
        # header
        self.footer_font_size = font_size
        unit = self.unit * units
        self.__check_units('footer', unit)
        self.footer_units = unit
        self.footer_text_position = text_position


class FontBooklet:
    """
    Class that represents the booklet of a font page.
    """

    def __init__(self, *pages: FontPage):
        """
        Object that represents the booklet of a font page.

        :param pages: FontPage's object
        """
        for page in pages:
            if not isinstance(page, FontPage):
                msg = f"{page} isn't FontPage object"
                raise TypeError(msg)

        self.pages = pages

    def __iter__(self):
        """
        Iterating on each FontPage.

        :return: next value
        """
        return iter(self.pages)

    def save(self, folder, extension='png'):
        """
        Save on each FontPage image.

        :param folder: path folder where you want to save each font page
        :param extension: extension of imge file. Default is 'png'
        :return: None
        """
        folder = Path(folder)

        if not folder.is_dir():
            raise NotADirectoryError(folder)

        # Check folder path exists
        if not folder.exists():
            folder.mkdir(parents=True)

        # Save all page in folder path
        for idx, page in enumerate(self):
            page.save(folder / f'page{idx + 1}.{extension}')
