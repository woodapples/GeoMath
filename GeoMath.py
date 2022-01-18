# -*- coding: utf-8 -*-
import math as m
import datetime

gon_faktor = float(10 / 9)
rundungs_faktor = 8


def file_handler(*args):
    try:
        with open(datetime.datetime.today().strftime('GeoMath_' + '%Y%m%d.txt'), mode='x') as file:
            file.write('-' * 50 + '\n')
            file.write('Protokoll ' + datetime.datetime.today().strftime('%A, den %d %B %Y') + '\n')
            file.write('Eintrag vorgenommen: ' + datetime.datetime.today().strftime('%X') + '\n')
            file.write('-' * 50 + '\n')
            file.write('\n')
            for arg in args:
                file.writelines(arg + '\n' + '*' * 50 + '\n')

    except FileExistsError:
        with open(datetime.datetime.today().strftime('GeoMath_' + '%Y%m%d.txt'), mode='a+') as file:
            file.write('-' * 50 + '\n')
            file.write('Neuer Eintrag in das Protokoll.' + '\n')
            file.write('Letzter Eintrag: ' + datetime.datetime.today().strftime('%X') + '\n')
            file.write('-' * 50 + '\n')
            file.write('\n')
            for arg in args:
                file.writelines(arg + '\n' + '*' * 50 + '\n')


# PolFunktion aus dem Taschenrechner.
# Errechnet die Strecke zwischen zwei Punkten, sowie die den Richtungswinkel.
# Pol(x2-x1;y2-y1)
def pol_function(koord_east_pkt1, koord_north_pkt1, koord_east_pkt2, koord_north_pkt2):
    delta_east = koord_east_pkt1 - koord_east_pkt2
    delta_east_qm = m.pow(delta_east, 2)
    delta_north = koord_north_pkt1 - koord_north_pkt2
    delta_north_qm = m.pow(delta_north, 2)
    hypotenuse = m.sqrt(delta_east_qm + delta_north_qm)
    rounded_hypotenuse = round(hypotenuse, rundungs_faktor)

    riwi_rad = m.atan(delta_east / delta_north)
    riwi_gon = m.degrees(riwi_rad) * gon_faktor
    rounded_riwi_gon = round(riwi_gon, rundungs_faktor)
    if rounded_riwi_gon < 0:
        rounded_riwi_gon += 400
        richtungswinkel_gon = rounded_riwi_gon

    elif rounded_riwi_gon >= 400:
        rounded_riwi_gon -= 400
        richtungswinkel_gon = rounded_riwi_gon

    else:
        richtungswinkel_gon = rounded_riwi_gon
    return rounded_hypotenuse, richtungswinkel_gon


# RecFunktion aus dem Taschenrechner.
# Errechnet die Koord von einem Punkt mit hilfe der Strecke und des Richtungswinkels.
# Rec(Strecke;Riwi)
def rec_function(strecke, richtungswinkel):

    riwi_rad = m.radians(richtungswinkel / gon_faktor)
    koord_north = m.cos(riwi_rad) * strecke
    koord_north = round(koord_north, rundungs_faktor)

    riwi_rad = m.radians(richtungswinkel / gon_faktor)
    koord_east = m.sin(riwi_rad) * strecke
    koord_east = round(koord_east, rundungs_faktor)
    return koord_east, koord_north


# Rechnet den North-/Hochwert des Schnittpunketes aus.
def interception_point_north(koord_east_1, koord_north_1, koord_east_3, koord_north_3, riwi_t1_2, riwi_t3_4, pos_a_deci_point=2):
    zaehler = (koord_east_3 - koord_east_1) - (koord_north_3 - koord_north_1) * m.tan(m.radians(riwi_t1_2 / gon_faktor))
    nenner = m.tan(m.radians(riwi_t1_2 / gon_faktor)) - m.tan(m.radians(riwi_t3_4 / gon_faktor))
    inter_point_north = koord_north_3 + (zaehler / nenner)
    inter_point_north = round(inter_point_north, pos_a_deci_point)
    return inter_point_north


# Rechnet den East-/Rechtswert des Schnittpunktes aus.
def interception_point_east(koord_east, koord_north, riwi, inter_point_north, pos_a_deci_point=2):
    inter_point_east = koord_east + (inter_point_north - koord_north) * m.tan(m.radians(riwi / gon_faktor))
    inter_point_east = round(inter_point_east, pos_a_deci_point)
    return inter_point_east


# Erzeugt den Eintrag für die Klasse Koordinaten.
def create_koord(east, north, radius=0, richtungswinkel=0):
    return Koordinaten(float(east), float(north), float(radius), float(richtungswinkel))


# Klasse Koordinaten.
class Koordinaten:
    def __init__(self, east, north, radius, richtungswinkel):
        self.east = east
        self.north = north
        self.radius = radius
        self.richtungswinkel = richtungswinkel

    def show(self):
        return f' East: {self.east}' + ' \n ' \
               f'North: {self.north}' + ' \n ' \
               f'Radius: {self.radius}' + ' \n ' \
               f'Richtungswinkel: {self.richtungswinkel}'


class Geradenschnitt:
    def __init__(self, strecke, richtungswinkel, schnittpkt_east, schnittpkt_north):
        self.strecke = strecke
        self.richtungswinkel = richtungswinkel
        self.schnittpkt_east = schnittpkt_east
        self.schnittpkt_north = schnittpkt_north

    def show(self):
        return f' Strecke: {self.strecke}' + ' \n ' \
               f'Richtungswinkel: {self.richtungswinkel}' + ' \n ' \
               f'Schnittpunkt East: {self.schnittpkt_east}' + ' \n ' \
               f'Schnittpunkt North: {self.schnittpkt_north}'



