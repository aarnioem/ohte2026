import unittest
from maksukortti import Maksukortti

class TestMaksukortti(unittest.TestCase):
    def setUp(self):
        self.maksukortti = Maksukortti(1000)

    def test_luotu_kortti_on_olemassa(self):
        self.assertNotEqual(self.maksukortti, None)

    def test_saldo_alussa_oikein(self):
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)

    def test_rahan_lataaminen_toimii(self):
        self.maksukortti.lataa_rahaa(500)
        self.assertEqual(self.maksukortti.saldo_euroina(), 15.00)

    def test_rahan_ottaminen_kun_rahaa_on_tarpeeksi(self):
        self.maksukortti.ota_rahaa(400)
        self.assertEqual(self.maksukortti.saldo_euroina(), 6.00)

    def test_rahan_ottaminen_kun_rahaa_ei_ole_tarpeeksi(self):
        self.maksukortti.ota_rahaa(1100)
        self.assertEqual(self.maksukortti.saldo_euroina(), 10.00)

    def test_ota_rahaa_metodi_palauttaa_true(self):
        self.assertTrue(self.maksukortti.ota_rahaa(100))

    def test_ota_rahaa_metodi_palauttaa_false(self):
        self.assertFalse(self.maksukortti.ota_rahaa(1500))
