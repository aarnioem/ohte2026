import unittest
from kassapaate import Kassapaate
from maksukortti import Maksukortti

class TestKassapaate(unittest.TestCase):
    def setUp(self):
        self.kassapaate = Kassapaate()
        self.kortti = Maksukortti(1000)

    def test_alkutila_eurot(self):
        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_alkutila_lounaat(self):
        lounaat = self.kassapaate.edulliset + self.kassapaate.maukkaat

        self.assertEqual(lounaat, 0)


    # edulliset käteinen

    def test_edullinen_kateisosto_kasvattaa_kassaa(self):
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1002.40)

    def test_edullinen_kateisosto_kasvattaa_myytyja(self):
        self.kassapaate.syo_edullisesti_kateisella(500)
        self.kassapaate.syo_edullisesti_kateisella(500)

        self.assertEqual(self.kassapaate.edulliset, 2)

    def test_edullinen_kateisosto_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(500), 260)

    def test_edullinen_kateinen_ei_riita_kassa(self):
        self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_edullinen_kateinen_ei_riita_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_edullisesti_kateisella(200), 200)

    def test_edullinen_kateinen_ei_riita_myydyt(self):
        self.kassapaate.syo_edullisesti_kateisella(200)

        self.assertEqual(self.kassapaate.edulliset, 0)


    # maukkaat käteinen

    def test_maukas_kateisosto_kasvattaa_kassaa(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1004.00)

    def test_maukas_kateisosto_kasvattaa_myytyja(self):
        self.kassapaate.syo_maukkaasti_kateisella(500)
        self.kassapaate.syo_maukkaasti_kateisella(500)

        self.assertEqual(self.kassapaate.maukkaat, 2)

    def test_maukas_kateisosto_vaihtoraha_oikein(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(500), 100)

    def test_maukas_kateinen_ei_riita_kassa(self):
        self.kassapaate.syo_maukkaasti_kateisella(300)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_maukas_kateinen_ei_riita_vaihtoraha(self):
        self.assertEqual(self.kassapaate.syo_maukkaasti_kateisella(300), 300)

    def test_maukas_kateinen_ei_riita_myydyt(self):
        self.kassapaate.syo_maukkaasti_kateisella(200)

        self.assertEqual(self.kassapaate.maukkaat, 0)


    # edulliset kortti

    def test_edullinen_korttiosto_saldo_riittaa_palauttaa_true(self):
        self.assertTrue(self.kassapaate.syo_edullisesti_kortilla(self.kortti))

    def test_edullinen_korttiosto_saldo_riittaa_veloitus_toimii(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo_euroina(), 7.60)

    def test_edullinen_korttiosto_saldo_riittaa_kassa_ei_kasva(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_edullinen_korttiosto_saldo_riittaa_myydyt_kasvaa(self):
        self.kassapaate.syo_edullisesti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.edulliset, 1)

    def test_edullinen_korttiosto_saldo_ei_riita_palauttaa_false(self):
        kortti = Maksukortti(100)
        self.assertFalse(self.kassapaate.syo_edullisesti_kortilla(kortti))

    def test_edullinen_korttiosto_saldo_ei_riita_saldo_pysyy_samana(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(kortti.saldo_euroina(), 1.00)

    def test_edullinen_korttiosto_saldo_ei_riita_kassa_ei_kasva(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_edullinen_korttiosto_saldo_ei_riita_myydyt_ei_kasva(self):
        kortti = Maksukortti(100)
        self.kassapaate.syo_edullisesti_kortilla(kortti)

        self.assertEqual(self.kassapaate.edulliset, 0)


    # maukkaat kortti

    def test_maukas_korttiosto_saldo_riittaa_palauttaa_true(self):
        self.assertTrue(self.kassapaate.syo_maukkaasti_kortilla(self.kortti))

    def test_maukas_korttiosto_saldo_riittaa_veloitus_toimii(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kortti.saldo_euroina(), 6.00)

    def test_maukas_korttiosto_saldo_riittaa_kassa_ei_kasva(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_maukas_korttiosto_saldo_riittaa_myydyt_kasvaa(self):
        self.kassapaate.syo_maukkaasti_kortilla(self.kortti)

        self.assertEqual(self.kassapaate.maukkaat, 1)

    def test_maukas_korttiosto_saldo_ei_riita_palauttaa_false(self):
        kortti = Maksukortti(300)
        self.assertFalse(self.kassapaate.syo_maukkaasti_kortilla(kortti))

    def test_maukas_korttiosto_saldo_ei_riita_saldo_pysyy_samana(self):
        kortti = Maksukortti(300)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(kortti.saldo_euroina(), 3.00)

    def test_maukas_korttiosto_saldo_ei_riita_kassa_ei_kasva(self):
        kortti = Maksukortti(300)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(self.kassapaate.kassassa_rahaa_euroina(), 1000.00)

    def test_maukas_korttiosto_saldo_ei_riita_myydyt_ei_kasva(self):
        kortti = Maksukortti(300)
        self.kassapaate.syo_maukkaasti_kortilla(kortti)

        self.assertEqual(self.kassapaate.maukkaat, 0)
