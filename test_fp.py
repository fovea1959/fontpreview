# ruff: noqa: PLR2004 PTH110

import os
import unittest

import pytest

from fontpreview import (
    FontBanner,
    FontBooklet,
    FontLogo,
    FontPage,
    FontPageTemplate,
    FontPreview,
    FontWall,
)

font = 'source/Roboto-Regular.ttf'
if not os.path.exists(font):
    msg = f"file font {font} doesn't exists"
    raise FileNotFoundError(msg)


class TestFontPreview(unittest.TestCase):
    fp, fb, fl = FontPreview(font), FontBanner(font), FontLogo(font, 'Fl')
    fw, fpage, fpage_t = FontWall([fb]), FontPage(), FontPageTemplate(3508)
    book = FontBooklet(fpage, fpage)

    def test_instance(self):
        # test if instance has been created
        assert isinstance(self.fp, FontPreview)
        assert isinstance(self.fb, FontBanner)
        assert isinstance(self.fl, FontLogo)
        assert isinstance(self.fw, FontWall)
        assert isinstance(self.fpage, FontPage)
        assert isinstance(self.fpage_t, FontPageTemplate)
        assert isinstance(self.book, FontBooklet)

    def test_set_color_with_name(self):
        # change background color
        self.fp.bg_color = self.fb.bg_color = self.fl.bg_color = 'blue'

        # change background color
        self.fp.fg_color = self.fb.fg_color = self.fl.fg_color = 'yellow'

        # test draw it
        self.fp.draw()
        self.fb.draw()
        self.fl.draw()

    def test_set_color_with_tuple(self):
        # change background color
        self.fp.bg_color = self.fb.bg_color = self.fl.bg_color = (51, 153, 193)

        # change background color
        self.fp.fg_color = self.fb.fg_color = self.fl.fg_color = (253, 194, 45)

        # test draw it
        self.fp.draw()
        self.fb.draw()
        self.fl.draw()

    def test_set_dimension(self):
        # test dimension of FontPreview object
        self.fp.dimension = (1000, 1000)

        # test draw it
        self.fp.draw()
        assert self.fp.image.size == self.fp.dimension

        # test dimension of FontBanner object
        self.fb.set_orientation((1000, 1000))

        # test draw it
        self.fb.draw()
        assert self.fb.image.size == self.fb.dimension

        # test dimension of FontBanner object and font position
        self.fb.set_orientation('landscape', 'lcenter')

        # test draw it
        self.fb.draw()
        assert self.fb.image.size == self.fb.dimension

        # test dimension of FontLogo object
        self.fl.new_size((75, 75))
        self.fl.new_size((100, 100))
        self.fl.new_size((150, 150))
        self.fl.new_size((170, 170))

        # test draw it
        self.fp.draw()
        assert self.fl.image.size == self.fl.dimension

        # test dimension of FontPage
        self.fpage.set_header(self.fb)
        self.fpage.set_body(self.fb)
        self.fpage.set_footer(self.fb)
        self.fpage.dimension = (1000, 1000)

        # test draw it
        self.fpage.draw()
        assert self.fpage.page.size == self.fpage.dimension

    def test_add_image(self):
        # test add image to FontBanner
        self.fb.add_image(self.fp, (500, 500))

        # test resize in add image
        fb_big = FontBanner(font, (2000, 2000))
        self.fb.add_image(fb_big, (500, 500))

    def test_font_size(self):
        # Test FontPreview font size
        self.fp.set_font_size(70)
        assert self.fp.font.size == 70

        # Test FontBanner font size
        self.fb.set_font_size(80)
        assert self.fb.font.size == 80

        # Test FontBanner font size
        self.fl.set_font_size(50)
        assert self.fl.font.size == 50

        # Test FontPage and FontPageTemplate font size
        template = FontPageTemplate()
        template.set_header(90, 1, 'lcenter')
        template.set_body(90, 3, 'lcenter')
        template.set_footer(90, 2, 'lcenter')
        fpage = FontPage(template=template)
        fpage.set_header(self.fb)
        fpage.set_body(self.fb)
        fpage.set_footer(self.fb)
        fpage.draw()

        # FontPageTemplate font size
        assert template.header_font_size == 90
        assert template.body_font_size == 90
        assert template.footer_font_size == 90

        # FontPage font size
        assert fpage.header is not None
        assert fpage.body is not None
        assert fpage.footer is not None
        assert fpage.header.font.size == 90
        assert fpage.body.font.size == 90
        assert fpage.footer.font.size == 90

    def test_text_position(self):
        # Test FontPreview font size
        self.fp.set_text_position('lcenter')

        # Test FontBanner font size
        self.fb.set_text_position('rcenter')

        # Test FontBanner font size
        self.fl.set_text_position('center')

        # Test FontPreview font size
        self.fp.set_text_position((100, 100))

        # Test FontBanner font size
        self.fb.set_text_position((100, 100))

        # Test FontBanner font size
        self.fl.set_text_position((100, 100))

    def test_set_text(self):
        # Test FontPreview font size
        self.fp.font_text = 'unittest'
        self.fp.draw(align='center')
        assert self.fp.font_text == 'unittest'

        # Test FontBanner font size
        self.fb.set_mode('fontname')
        self.fb.draw(align='center')
        assert self.fb.font_text == f'{self.fb.font.getname()[0]}'

        # Test FontBanner font size
        self.fl.font_text = 'ut'
        self.fl.draw(align='center')
        assert self.fl.font_text == 'ut'

    def test_add_to_wall(self):
        # Create FontWall
        fw = FontWall([self.fb, self.fp, self.fl])
        assert isinstance(fw, FontWall)
        fw.draw(fw.max_tile)

        # Create FontWall with max_tile args
        fw = FontWall([self.fb, self.fp, self.fl], max_tile=3)
        assert isinstance(fw, FontWall)
        fw.draw(fw.max_tile)

        # Create FontWall with max_tile args and
        fw = FontWall([self.fb, self.fp, self.fl], max_tile=3, mode='vertical')
        assert isinstance(fw, FontWall)
        fw.draw(fw.max_tile)

    def test_template_page(self):
        # Create FontPage
        page = FontPage(template=self.fpage_t)

        # Test instance
        assert isinstance(page, FontPage)

        # Test method FontPageTemplate
        self.fpage_t.set_header(120, 1, 'center')
        self.fpage_t.set_body(170, 3, 'left')
        self.fpage_t.set_footer(100, 2, 'right')

        # Test value of header
        assert self.fpage_t.header_text_position == 'center'
        assert self.fpage_t.header_font_size == 120
        assert self.fpage_t.header_units == self.fpage_t.unit * 1

        # Test value of header
        assert self.fpage_t.body_text_position == 'left'
        assert self.fpage_t.body_font_size == 170
        assert self.fpage_t.body_units == self.fpage_t.unit * 3

        # Test value of header
        assert self.fpage_t.footer_text_position == 'right'
        assert self.fpage_t.footer_font_size == 100
        assert self.fpage_t.footer_units == self.fpage_t.unit * 2

    def test_declarative_object(self):  # noqa: PLR6301
        # FontPreview object
        fp = FontPreview(
            font,
            font_size=50,
            font_text='some text',
            color_system='RGB',
            bg_color='blue',
            fg_color='yellow',
            dimension=(800, 400),
        )
        # FontBanner object
        fb = FontBanner(
            font,
            orientation='portrait',
            bg_color='blue',
            fg_color='yellow',
            mode='paragraph',
            font_size=70,
            color_system='RGB',
        )
        # FontLogo object
        fl = FontLogo(
            font,
            'Fl',
            size=(170, 170),
            bg_color='yellow',
            fg_color='blue',
            font_size=50,
            color_system='RGB',
        )

        # FontPage object
        fpage = FontPage(header=fb, logo=fl, body=fb, footer=fb)

        # test if instance has been created
        assert isinstance(fp, FontPreview)
        assert isinstance(fb, FontBanner)
        assert isinstance(fl, FontLogo)
        assert isinstance(fpage, FontPage)

    def test_other_color_system(self):
        fp = self.fp
        fb = self.fb
        fl = self.fl

        # define new color system
        fp.color_system = 'CMYK'

        # change background color
        fp.bg_color = fb.bg_color = fl.bg_color = (51, 153, 193)

        # change background color
        fp.fg_color = fb.fg_color = fl.fg_color = (253, 194, 45)

        # test draw it
        fp.draw()
        fb.draw()
        fl.draw()

    def test_hex_color(self):
        fp = self.fp
        fb = self.fb
        fl = self.fl

        # define new color system
        fp.color_system = 'CMYK'

        # change background color
        fp.bg_color = fb.bg_color = fl.bg_color = '#269cc3'

        # change background color
        fp.fg_color = fb.fg_color = fl.fg_color = '#ff0000'

        # test draw it
        fp.draw()
        fb.draw()
        fl.draw()

    def test_parse_not_fontpage_on_fontbooklet(self):
        with pytest.raises(TypeError):
            FontBooklet(self, self.fp, self.fw)  # type: ignore[arg-type]

    def test_iter_fontbooklet(self):
        self.fpage.set_header(self.fb)
        self.fpage.set_body(self.fb)
        self.fpage.set_footer(self.fb)
        for page in self.book:
            page.draw()


if __name__ == '__main__':
    unittest.main()
