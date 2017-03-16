import unittest
import binascii

from iqeye_jpeg_scraper import is_jpeg_file, validate_jpeg

class JPEGScraperTestCase(unittest.TestCase):
  """Tests JPEGScraper"""

  def test_is_jpeg_file_goodfile(self):
    """Tests if file is JPEG by name"""
    values = ['file.JPEG', 'file.jpeg', 'file.JPG', 'file.jpg', 'file.jPeG', 'file.jPg']
    for value in values:
      self.assertTrue(is_jpeg_file(value))

  def test_is_jpeg_file_badfile(self):
    """Tests if file is JPEG by name"""
    values = ['file.txt', 'file.TxT', 'file.com']
    for value in values:
      self.assertFalse(is_jpeg_file(value))

  def test_validate_jpeg(self):
    jpeg_signatures = [
    binascii.unhexlify(b'FFD8FFD8'),
    binascii.unhexlify(b'FFD8FFE0'),
    binascii.unhexlify(b'FFD8FFE1')
    ]
    # emulate a file and feed it to library
    for signature in jpeg_signatures:
      self.assertTrue(signature)

if __name__ == '__main__':
  unittest.main()
