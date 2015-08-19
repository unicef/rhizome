# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0002_load_base_metadata'),
    ]

    operations = [
    migrations.RunSQL("""

INSERT INTO source_data_document
            (created_by_id,guid,doc_text,is_processed,created_at)
            SELECT id, 'init_ng_regions','init_ng_regions', CAST(1 AS BOOLEAN),NOW()
            FROM auth_user
            WHERE NOT EXISTS (
                SELECT 1 FROM source_data_document sdd
                WHERE guid = 'init_ng_regions'
            )
            LIMIT 1;
	    DROP TABLE IF EXISTS _tmp_ng_regions;
	    CREATE TABLE _tmp_ng_regions
	    (
		    region_code VARCHAR
		    ,region_name VARCHAR
		    ,region_type VARCHAR
		    ,country VARCHAR
	    );
	    INSERT INTO _tmp_ng_regions
	    (region_code, region_name, region_type, country)
        SELECT 42, 'Bauchi (Province)','Province','Nigeria' UNION ALL
        SELECT 43, 'Borno','Province','Nigeria' UNION ALL
        SELECT 18, 'Jigawa (Province)','Province','Nigeria' UNION ALL
        SELECT 19, 'Kaduna','Province','Nigeria' UNION ALL
        SELECT 20, 'Kano','Province','Nigeria' UNION ALL
        SELECT 22, 'Kebbi','Province','Nigeria' UNION ALL
        SELECT 34, 'Sokoto','Province','Nigeria' UNION ALL
        SELECT 36, 'Yobe','Province','Nigeria' UNION ALL
        SELECT 37, 'Zamfara','Province','Nigeria' UNION ALL
        SELECT 21, 'Katsina','Province','Nigeria' UNION ALL
        SELECT 4301, 'Abadam','District','Nigeria' UNION ALL
        SELECT 2001, 'Ajingi (Kano)','District','Nigeria' UNION ALL
        SELECT 2002, 'Albasu (Kano)','District','Nigeria' UNION ALL
        SELECT 2201, 'Aleiro','District','Nigeria' UNION ALL
        SELECT 4201, 'Alkaleri','District','Nigeria' UNION ALL
        SELECT 3701, 'Anka','District','Nigeria' UNION ALL
        SELECT 2202, 'Arewa Dandi','District','Nigeria' UNION ALL
        SELECT 2203, 'Argungu','District','Nigeria' UNION ALL
        SELECT 4302, 'Askira/Uba','District','Nigeria' UNION ALL
        SELECT 2204, 'Augie','District','Nigeria' UNION ALL
        SELECT 1801, 'Auyo (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2004, 'b (Kano)','District','Nigeria' UNION ALL
        SELECT 1802, 'Babura (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2205, 'Bagudo','District','Nigeria' UNION ALL
        SELECT 2003, 'Bagwai (Kano)','District','Nigeria' UNION ALL
        SELECT 2101, 'Bakori','District','Nigeria' UNION ALL
        SELECT 3702, 'Bakura (Zamfara)','District','Nigeria' UNION ALL
        SELECT 4303, 'Bama','District','Nigeria' UNION ALL
        SELECT 3601, 'Barde (Yobe)','District','Nigeria' UNION ALL
        SELECT 2102, 'Batagarawa (Katsina)','District','Nigeria' UNION ALL
        SELECT 2103, 'Batsari (Katsina)','District','Nigeria' UNION ALL
        SELECT 4202, 'Bauchi (District)','District','Nigeria' UNION ALL
        SELECT 2104, 'Baure (Katsina)','District','Nigeria' UNION ALL
        SELECT 4304, 'Bayo','District','Nigeria' UNION ALL
        SELECT 2005, 'Bichi (Kano)','District','Nigeria' UNION ALL
        SELECT 2105, 'Bindawa (Katsina)','District','Nigeria' UNION ALL
        SELECT 3401, 'Binji (Sokoto)','District','Nigeria' UNION ALL
        SELECT 1901, 'Birnin Gwari','District','Nigeria' UNION ALL
        SELECT 2206, 'Birnin Kebbi','District','Nigeria' UNION ALL
        SELECT 1803, 'Birnin Kudu (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3703, 'Birnin Magaji/Kiyaw','District','Nigeria' UNION ALL
        SELECT 1804, 'Birniwa (Jigawa)','District','Nigeria' UNION ALL
        SELECT 4305, 'Biu','District','Nigeria' UNION ALL
        SELECT 3402, 'Bodinga','District','Nigeria' UNION ALL
        SELECT 4203, 'Bogoro (Bauchi)','District','Nigeria' UNION ALL
        SELECT 3602, 'Borsari','District','Nigeria' UNION ALL
        SELECT 1805, 'Buji (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3704, 'Bukkuyum (Zamfara)','District','Nigeria' UNION ALL
        SELECT 3705, 'Bungudu (Zamfara)','District','Nigeria' UNION ALL
        SELECT 2006, 'Bunkure (Kano)','District','Nigeria' UNION ALL
        SELECT 2207, 'Bunza','District','Nigeria' UNION ALL
        SELECT 2106, 'Charanchi (Katsina)','District','Nigeria' UNION ALL
        SELECT 4306, 'Chibok','District','Nigeria' UNION ALL
        SELECT 1902, 'Chikun (Kaduna)','District','Nigeria' UNION ALL
        SELECT 2007, 'Dala (Kano)','District','Nigeria' UNION ALL
        SELECT 3603, 'Damaturu','District','Nigeria' UNION ALL
        SELECT 4204, 'Damban','District','Nigeria' UNION ALL
        SELECT 2008, 'Dambatta','District','Nigeria' UNION ALL
        SELECT 4307, 'Damboa (Borno)','District','Nigeria' UNION ALL
        SELECT 2107, 'Dan Musa','District','Nigeria' UNION ALL
        SELECT 2208, 'Dandi (Kebbi)','District','Nigeria' UNION ALL
        SELECT 2108, 'Dandume','District','Nigeria' UNION ALL
        SELECT 3403, 'Dange-Shuni','District','Nigeria' UNION ALL
        SELECT 2109, 'Danja','District','Nigeria' UNION ALL
        SELECT 4205, 'Darazo','District','Nigeria' UNION ALL
        SELECT 4206, 'Dass','District','Nigeria' UNION ALL
        SELECT 2110, 'Daura (Katsina)','District','Nigeria' UNION ALL
        SELECT 2009, 'Dawakin Kudu','District','Nigeria' UNION ALL
        SELECT 2010, 'Dawakin Tofa','District','Nigeria' UNION ALL
        SELECT 4308, 'Dikwa (Borno)','District','Nigeria' UNION ALL
        SELECT 2011, 'Doguwa (Kano)','District','Nigeria' UNION ALL
        SELECT 1806, 'Dutse','District','Nigeria' UNION ALL
        SELECT 2111, 'Dutsi','District','Nigeria' UNION ALL
        SELECT 2112, 'Dutsin Ma','District','Nigeria' UNION ALL
        SELECT 2012, 'Fagge','District','Nigeria' UNION ALL
        SELECT 2209, 'Fakai','District','Nigeria' UNION ALL
        SELECT 2113, 'Faskari (Katsina)','District','Nigeria' UNION ALL
        SELECT 3604, 'Fika','District','Nigeria' UNION ALL
        SELECT 3605, 'Fune','District','Nigeria' UNION ALL
        SELECT 2114, 'Funtua','District','Nigeria' UNION ALL
        SELECT 2013, 'Gabasawa (Kano)','District','Nigeria' UNION ALL
        SELECT 3404, 'Gada (Sokoto)','District','Nigeria' UNION ALL
        SELECT 1807, 'Gagarawa','District','Nigeria' UNION ALL
        SELECT 4207, 'Gamawa','District','Nigeria' UNION ALL
        SELECT 4208, 'Ganjuwa','District','Nigeria' UNION ALL
        SELECT 1808, 'Garki (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2014, 'Garko (Kano)','District','Nigeria' UNION ALL
        SELECT 2015, 'Garun Malam (Kano)','District','Nigeria' UNION ALL
        SELECT 2016, 'Gaya','District','Nigeria' UNION ALL
        SELECT 3606, 'Geidam','District','Nigeria' UNION ALL
        SELECT 2017, 'Gezawa (Kano)','District','Nigeria' UNION ALL
        SELECT 4209, 'Giade','District','Nigeria' UNION ALL
        SELECT 1903, 'Giwa (Kaduna)','District','Nigeria' UNION ALL
        SELECT 3405, 'Goronyo (Sokoto)','District','Nigeria' UNION ALL
        SELECT 4309, 'Gubio','District','Nigeria' UNION ALL
        SELECT 3406, 'Gudu','District','Nigeria' UNION ALL
        SELECT 3607, 'Gujba (Yobe)','District','Nigeria' UNION ALL
        SELECT 3608, 'Gulani (Yobe)','District','Nigeria' UNION ALL
        SELECT 1809, 'Gumel (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3706, 'Gummi','District','Nigeria' UNION ALL
        SELECT 1810, 'Guri (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3707, 'Gusau (Zamfara)','District','Nigeria' UNION ALL
        SELECT 4310, 'Guzamala','District','Nigeria' UNION ALL
        SELECT 3407, 'Gwadabawa (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2018, 'Gwale (Kano)','District','Nigeria' UNION ALL
        SELECT 2210, 'Gwandu','District','Nigeria' UNION ALL
        SELECT 1811, 'Gwaram (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2019, 'Gwarzo (Kano)','District','Nigeria' UNION ALL
        SELECT 1812, 'Gwiwa (Jigawa)','District','Nigeria' UNION ALL
        SELECT 4311, 'Gwoza','District','Nigeria' UNION ALL
        SELECT 1813, 'Hadejia','District','Nigeria' UNION ALL
        SELECT 4312, 'Hawul','District','Nigeria' UNION ALL
        SELECT 1904, 'Igabi (Kaduna)','District','Nigeria' UNION ALL
        SELECT 1905, 'Ikara (Kaduna)','District','Nigeria' UNION ALL
        SELECT 3408, 'Illela (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2115, 'Ingawa (Katsina)','District','Nigeria' UNION ALL
        SELECT 3409, 'Isa','District','Nigeria' UNION ALL
        SELECT 4210, 'Itas/Gadau','District','Nigeria' UNION ALL
        SELECT 1906, 'Jaba (Kaduna)','District','Nigeria' UNION ALL
        SELECT 1814, 'Jahun (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3609, 'Jakusko (Yobe)','District','Nigeria' UNION ALL
        SELECT 4211, 'Jama''Are','District','Nigeria' UNION ALL
        SELECT 2211, 'Jega','District','Nigeria' UNION ALL
        SELECT 1907, 'Jema''A','District','Nigeria' UNION ALL
        SELECT 4313, 'Jere','District','Nigeria' UNION ALL
        SELECT 2116, 'Jibia','District','Nigeria' UNION ALL
        SELECT 2020, 'Kabo (Kano)','District','Nigeria' UNION ALL
        SELECT 1908, 'Kachia (Kaduna)','District','Nigeria' UNION ALL
        SELECT 1909, 'Kaduna North','District','Nigeria' UNION ALL
        SELECT 1910, 'Kaduna South','District','Nigeria' UNION ALL
        SELECT 1815, 'Kafin Hausa (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2117, 'Kafur (Katsina)','District','Nigeria' UNION ALL
        SELECT 4314, 'Kaga','District','Nigeria' UNION ALL
        SELECT 1911, 'Kagarko','District','Nigeria' UNION ALL
        SELECT 2118, 'Kaita (Katsina)','District','Nigeria' UNION ALL
        SELECT 1912, 'Kajuru (Kaduna)','District','Nigeria' UNION ALL
        SELECT 4315, 'Kala/Balge','District','Nigeria' UNION ALL
        SELECT 2212, 'Kalgo (Kebbi)','District','Nigeria' UNION ALL
        SELECT 2119, 'Kankara (Katsina)','District','Nigeria' UNION ALL
        SELECT 2120, 'Kankia','District','Nigeria' UNION ALL
        SELECT 2021, 'Kano Municipal','District','Nigeria' UNION ALL
        SELECT 3610, 'Karasuwa','District','Nigeria' UNION ALL
        SELECT 2022, 'Karaye (Kano)','District','Nigeria' UNION ALL
        SELECT 4212, 'Katagum (Bauchi)','District','Nigeria' UNION ALL
        SELECT 2121, 'Katsina (District)','District','Nigeria' UNION ALL
        SELECT 1816, 'Kaugama (Jigawa)','District','Nigeria' UNION ALL
        SELECT 1913, 'Kaura (Kaduna)','District','Nigeria' UNION ALL
        SELECT 3708, 'Kaura Namoda','District','Nigeria' UNION ALL
        SELECT 1914, 'Kauru','District','Nigeria' UNION ALL
        SELECT 1817, 'Kazaure','District','Nigeria' UNION ALL
        SELECT 3410, 'Kebbe','District','Nigeria' UNION ALL
        SELECT 2023, 'Kibiya','District','Nigeria' UNION ALL
        SELECT 4213, 'Kirfi (Bauchi)','District','Nigeria' UNION ALL
        SELECT 1818, 'Kiri Kasamma (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2024, 'Kiru (Kano)','District','Nigeria' UNION ALL
        SELECT 1819, 'Kiyawa (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2213, 'Koko/Besse','District','Nigeria' UNION ALL
        SELECT 4316, 'Konduga (Borno)','District','Nigeria' UNION ALL
        SELECT 1915, 'Kubau (Kaduna)','District','Nigeria' UNION ALL
        SELECT 1916, 'Kudan (Kaduna)','District','Nigeria' UNION ALL
        SELECT 4317, 'Kukawa (Borno)','District','Nigeria' UNION ALL
        SELECT 2025, 'Kumbotso (Kano)','District','Nigeria' UNION ALL
        SELECT 2026, 'Kunchi (Kano)','District','Nigeria' UNION ALL
        SELECT 2027, 'Kura (Kano)','District','Nigeria' UNION ALL
        SELECT 2122, 'Kurfi','District','Nigeria' UNION ALL
        SELECT 2123, 'Kusada (Katsina)','District','Nigeria' UNION ALL
        SELECT 3411, 'Kware (Sokoto)','District','Nigeria' UNION ALL
        SELECT 4318, 'Kwaya Kusar (Borno)','District','Nigeria' UNION ALL
        SELECT 1917, 'Lere (Kaduna)','District','Nigeria' UNION ALL
        SELECT 3611, 'Machina (Yobe)','District','Nigeria' UNION ALL
        SELECT 2028, 'Madobi (Kano)','District','Nigeria' UNION ALL
        SELECT 4319, 'Mafa (Borno)','District','Nigeria' UNION ALL
        SELECT 4320, 'Magumeri (Borno)','District','Nigeria' UNION ALL
        SELECT 2124, 'Mai''Adua','District','Nigeria' UNION ALL
        SELECT 4321, 'Maiduguri','District','Nigeria' UNION ALL
        SELECT 1820, 'Maigatari','District','Nigeria' UNION ALL
        SELECT 2214, 'Maiyama (Kebbi)','District','Nigeria' UNION ALL
        SELECT 1918, 'Makarfi (Kaduna)','District','Nigeria' UNION ALL
        SELECT 2029, 'Makoda (Kano)','District','Nigeria' UNION ALL
        SELECT 1821, 'Malam Maduri (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2125, 'Malumfashi','District','Nigeria' UNION ALL
        SELECT 2126, 'Mani (Katsina)','District','Nigeria' UNION ALL
        SELECT 3709, 'Maradun','District','Nigeria' UNION ALL
        SELECT 4322, 'Marte (Borno)','District','Nigeria' UNION ALL
        SELECT 3710, 'Maru (Zamfara)','District','Nigeria' UNION ALL
        SELECT 2127, 'Mashi (Katsina)','District','Nigeria' UNION ALL
        SELECT 2128, 'Matazu','District','Nigeria' UNION ALL
        SELECT 1822, 'Miga (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2030, 'Minjibir (Kano)','District','Nigeria' UNION ALL
        SELECT 4214, 'Misau','District','Nigeria' UNION ALL
        SELECT 4323, 'Mobbar','District','Nigeria' UNION ALL
        SELECT 4324, 'Monguno (Borno)','District','Nigeria' UNION ALL
        SELECT 2129, 'Musawa (Katsina)','District','Nigeria' UNION ALL
        SELECT 3612, 'Nangere (Yobe)','District','Nigeria' UNION ALL
        SELECT 2031, 'Nassarawa (Kano)','District','Nigeria' UNION ALL
        SELECT 4325, 'Ngala (Borno)','District','Nigeria' UNION ALL
        SELECT 4326, 'Nganzai','District','Nigeria' UNION ALL
        SELECT 2215, 'Ngaski (Kebbi)','District','Nigeria' UNION ALL
        SELECT 3613, 'Nguru','District','Nigeria' UNION ALL
        SELECT 4215, 'Ningi','District','Nigeria' UNION ALL
        SELECT 3614, 'Potiskum','District','Nigeria' UNION ALL
        SELECT 3412, 'Rabah (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2032, 'Rano (Kano)','District','Nigeria' UNION ALL
        SELECT 2130, 'Rimi (Katsina)','District','Nigeria' UNION ALL
        SELECT 2033, 'Rimin Gado (Kano)','District','Nigeria' UNION ALL
        SELECT 1823, 'Ringim (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2034, 'Rogo','District','Nigeria' UNION ALL
        SELECT 1824, 'Roni (Jigawa)','District','Nigeria' UNION ALL
        SELECT 3413, 'Sabon Birni (Sokoto)','District','Nigeria' UNION ALL
        SELECT 1919, 'Sabon Gari (Kaduna)','District','Nigeria' UNION ALL
        SELECT 2131, 'Sabuwa','District','Nigeria' UNION ALL
        SELECT 2132, 'Safana (Katsina)','District','Nigeria' UNION ALL
        SELECT 2216, 'Sakaba (Kebbi)','District','Nigeria' UNION ALL
        SELECT 2133, 'Sandamu (Katsina)','District','Nigeria' UNION ALL
        SELECT 1920, 'Sanga','District','Nigeria' UNION ALL
        SELECT 3414, 'Shagari (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2217, 'Shanga (Kebbi)','District','Nigeria' UNION ALL
        SELECT 4327, 'Shani (Borno)','District','Nigeria' UNION ALL
        SELECT 2035, 'Shanono (Kano)','District','Nigeria' UNION ALL
        SELECT 3711, 'Shinkafi','District','Nigeria' UNION ALL
        SELECT 4216, 'Shira (Bauchi)','District','Nigeria' UNION ALL
        SELECT 3415, 'Silame (Sokoto)','District','Nigeria' UNION ALL
        SELECT 1921, 'Soba (Kaduna)','District','Nigeria' UNION ALL
        SELECT 3416, 'Sokoto North','District','Nigeria' UNION ALL
        SELECT 3417, 'Sokoto South','District','Nigeria' UNION ALL
        SELECT 1825, 'Sule Tankakar','District','Nigeria' UNION ALL
        SELECT 2036, 'Sumaila (Kano)','District','Nigeria' UNION ALL
        SELECT 2218, 'Suru (Kebbi)','District','Nigeria' UNION ALL
        SELECT 4217, 'Tafawa-Balewa','District','Nigeria' UNION ALL
        SELECT 2037, 'Takai (Kano)','District','Nigeria' UNION ALL
        SELECT 3712, 'Talata Mafara','District','Nigeria' UNION ALL
        SELECT 3418, 'Tambuwal','District','Nigeria' UNION ALL
        SELECT 3419, 'Tangaza (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2038, 'Tarauni (Kano)','District','Nigeria' UNION ALL
        SELECT 3615, 'Tarmua','District','Nigeria' UNION ALL
        SELECT 1826, 'Taura (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2039, 'Tofa (Kano)','District','Nigeria' UNION ALL
        SELECT 4218, 'Toro (Bauchi)','District','Nigeria' UNION ALL
        SELECT 3713, 'Tsafe','District','Nigeria' UNION ALL
        SELECT 2040, 'Tsanyawa (Kano)','District','Nigeria' UNION ALL
        SELECT 2041, 'Tudun Wada (Kano)','District','Nigeria' UNION ALL
        SELECT 3420, 'Tureta (Sokoto)','District','Nigeria' UNION ALL
        SELECT 2042, 'Ungogo (Kano)','District','Nigeria' UNION ALL
        SELECT 3421, 'Wamako','District','Nigeria' UNION ALL
        SELECT 2043, 'Warawa (Kano)','District','Nigeria' UNION ALL
        SELECT 4219, 'Warji','District','Nigeria' UNION ALL
        SELECT 2219, 'Wasagu/Danko','District','Nigeria' UNION ALL
        SELECT 2044, 'Wudil (Kano)','District','Nigeria' UNION ALL
        SELECT 3422, 'Wurno (Sokoto)','District','Nigeria' UNION ALL
        SELECT 3423, 'Yabo','District','Nigeria' UNION ALL
        SELECT 1827, 'Yankwashi (Jigawa)','District','Nigeria' UNION ALL
        SELECT 2220, 'Yauri','District','Nigeria' UNION ALL
        SELECT 3616, 'Yunusari (Yobe)','District','Nigeria' UNION ALL
        SELECT 3617, 'Yusufari','District','Nigeria' UNION ALL
        SELECT 4220, 'Zaki','District','Nigeria' UNION ALL
        SELECT 2134, 'Zango (Katsina)','District','Nigeria' UNION ALL
        SELECT 1922, 'Zangon Kataf','District','Nigeria' UNION ALL
        SELECT 1923, 'Zaria','District','Nigeria' UNION ALL
        SELECT 3714, 'Zurmi (Zamfara)','District','Nigeria' UNION ALL
        SELECT 2221, 'Zuru','District','Nigeria' UNION ALL
        SELECT 191701, 'Abadawa','Sub-District','Nigeria' UNION ALL
        SELECT 210301, 'Abadua/Kagara','Sub-District','Nigeria' UNION ALL
        SELECT 180601, 'Abaya','Sub-District','Nigeria' UNION ALL
        SELECT 430301, 'Abbaram','Sub-District','Nigeria' UNION ALL
        SELECT 421001, 'Abdallawa (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
        SELECT 211801, 'Abdallawa (Kaita)','Sub-District','Nigeria' UNION ALL
        SELECT 192001, 'Aboro','Sub-District','Nigeria' UNION ALL
        SELECT 213001, 'Abukur','Sub-District','Nigeria' UNION ALL
        SELECT 181001, 'Abunabo','Sub-District','Nigeria' UNION ALL
        SELECT 342201, 'Achida','Sub-District','Nigeria' UNION ALL
        SELECT 204401, 'Achika','Sub-District','Nigeria' UNION ALL
        SELECT 182701, 'Achilafiya','Sub-District','Nigeria' UNION ALL
        SELECT 370401, 'Adabka','Sub-District','Nigeria' UNION ALL
        SELECT 221601, 'Adai','Sub-District','Nigeria' UNION ALL
        SELECT 200701, 'Adakawa','Sub-District','Nigeria' UNION ALL
        SELECT 421601, 'Adamami','Sub-District','Nigeria' UNION ALL
        SELECT 181002, 'Adiyani','Sub-District','Nigeria' UNION ALL
        SELECT 431001, 'Aduwa','Sub-District','Nigeria' UNION ALL
        SELECT 190401, 'Afaka','Sub-District','Nigeria' UNION ALL
        SELECT 191201, 'Afogo','Sub-District','Nigeria' UNION ALL
        SELECT 361301, 'Afunori','Sub-District','Nigeria' UNION ALL
        SELECT 430801, 'Afuye','Sub-District','Nigeria' UNION ALL
        SELECT 211501, 'Agayawa','Sub-District','Nigeria' UNION ALL
        SELECT 191301, 'Agban','Sub-District','Nigeria' UNION ALL
        SELECT 190801, 'Agunu','Sub-District','Nigeria' UNION ALL
        SELECT 180501, 'Ahoto','Sub-District','Nigeria' UNION ALL
        SELECT 432001, 'Ai Yesku','Sub-District','Nigeria' UNION ALL
        SELECT 182601, 'Ajaura','Sub-District','Nigeria' UNION ALL
        SELECT 430701, 'Ajigin A','Sub-District','Nigeria' UNION ALL
        SELECT 430702, 'Ajigin B','Sub-District','Nigeria' UNION ALL
        SELECT 421401, 'Ajili','Sub-District','Nigeria' UNION ALL
        SELECT 200101, 'Ajingi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431901, 'Ajiri','Sub-District','Nigeria' UNION ALL
        SELECT 210201, 'Ajiwa','Sub-District','Nigeria' UNION ALL
        SELECT 200801, 'Ajumawa','Sub-District','Nigeria' UNION ALL
        SELECT 421402, 'Akuyam','Sub-District','Nigeria' UNION ALL
        SELECT 432201, 'Ala','Sub-District','Nigeria' UNION ALL
        SELECT 432202, 'Ala-Lawanti','Sub-District','Nigeria' UNION ALL
        SELECT 360501, 'Alagarno (Fune)','Sub-District','Nigeria' UNION ALL
        SELECT 420701, 'Alagarno (Gamawa)','Sub-District','Nigeria' UNION ALL
        SELECT 431701, 'Alagarno (Kukawa)','Sub-District','Nigeria' UNION ALL
        SELECT 203501, 'Alajawa','Sub-District','Nigeria' UNION ALL
        SELECT 422001, 'Alangwari','Sub-District','Nigeria' UNION ALL
        SELECT 432601, 'Alarge','Sub-District','Nigeria' UNION ALL
        SELECT 431301, 'Alau','Sub-District','Nigeria' UNION ALL
        SELECT 200201, 'Albasu (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 182501, 'Albasu (Sule Tankakar)','Sub-District','Nigeria' UNION ALL
        SELECT 221101, 'Alelu','Sub-District','Nigeria' UNION ALL
        SELECT 180901, 'Alhaji Barka','Sub-District','Nigeria' UNION ALL
        SELECT 221801, 'Aljannare','Sub-District','Nigeria' UNION ALL
        SELECT 420101, 'Alkaleri East','Sub-District','Nigeria' UNION ALL
        SELECT 420102, 'Alkaleri West','Sub-District','Nigeria' UNION ALL
        SELECT 342202, 'Alkammu','Sub-District','Nigeria' UNION ALL
        SELECT 220301, 'Alwasa','Sub-District','Nigeria' UNION ALL
        SELECT 182502, 'Amanga','Sub-District','Nigeria' UNION ALL
        SELECT 204301, 'Amarawa','Sub-District','Nigeria' UNION ALL
        SELECT 422002, 'Amarmari','Sub-District','Nigeria' UNION ALL
        SELECT 182401, 'Amaryawa 3','Sub-District','Nigeria' UNION ALL
        SELECT 220601, 'Ambursa','Sub-District','Nigeria' UNION ALL
        SELECT 430302, 'Amchaka','Sub-District','Nigeria' UNION ALL
        SELECT 200401, 'Anadariya','Sub-District','Nigeria' UNION ALL
        SELECT 191501, 'Anchau','Sub-District','Nigeria' UNION ALL
        SELECT 430303, 'Andara','Sub-District','Nigeria' UNION ALL
        SELECT 221401, 'Andarai','Sub-District','Nigeria' UNION ALL
        SELECT 181901, 'Andaza','Sub-District','Nigeria' UNION ALL
        SELECT 421602, 'Andubun','Sub-District','Nigeria' UNION ALL
        SELECT 211401, 'Ang. Ibrahim','Sub-District','Nigeria' UNION ALL
        SELECT 211402, 'Ang. Musa','Sub-District','Nigeria' UNION ALL
        SELECT 190802, 'Ankwa','Sub-District','Nigeria' UNION ALL
        SELECT 340801, 'Araba','Sub-District','Nigeria' UNION ALL
        SELECT 192002, 'Arak','Sub-District','Nigeria' UNION ALL
        SELECT 181601, 'Arbus','Sub-District','Nigeria' UNION ALL
        SELECT 430901, 'Ardimini','Sub-District','Nigeria' UNION ALL
        SELECT 432002, 'Ardoram','Sub-District','Nigeria' UNION ALL
        SELECT 212101, 'Arewa 1','Sub-District','Nigeria' UNION ALL
        SELECT 212102, 'Arewa 2','Sub-District','Nigeria' UNION ALL
        SELECT 430101, 'Arge','Sub-District','Nigeria' UNION ALL
        SELECT 421501, 'Ari','Sub-District','Nigeria' UNION ALL
        SELECT 191101, 'Aribi','Sub-District','Nigeria' UNION ALL
        SELECT 182101, 'Arki','Sub-District','Nigeria' UNION ALL
        SELECT 342101, 'Arkilla','Sub-District','Nigeria' UNION ALL
        SELECT 432301, 'Asaga','Sub-District','Nigeria' UNION ALL
        SELECT 340701, 'Asara','Sub-District','Nigeria' UNION ALL
        SELECT 360601, 'Asheikiri  1','Sub-District','Nigeria' UNION ALL
        SELECT 360602, 'Asheikiri  2','Sub-District','Nigeria' UNION ALL
        SELECT 431101, 'Ashigashiya','Sub-District','Nigeria' UNION ALL
        SELECT 181602, 'Askandu','Sub-District','Nigeria' UNION ALL
        SELECT 430201, 'Askira E','Sub-District','Nigeria' UNION ALL
        SELECT 190701, 'Asso','Sub-District','Nigeria' UNION ALL
        SELECT 181301, 'Atafi','Sub-District','Nigeria' UNION ALL
        SELECT 421002, 'Atafowa','Sub-District','Nigeria' UNION ALL
        SELECT 340702, 'Attakwanyo','Sub-District','Nigeria' UNION ALL
        SELECT 190702, 'Atuku','Sub-District','Nigeria' UNION ALL
        SELECT 221701, 'Atuwo','Sub-District','Nigeria' UNION ALL
        SELECT 190501, 'Auchan','Sub-District','Nigeria' UNION ALL
        SELECT 220401, 'Augie North','Sub-District','Nigeria' UNION ALL
        SELECT 220402, 'Augie South','Sub-District','Nigeria' UNION ALL
        SELECT 181401, 'Aujara','Sub-District','Nigeria' UNION ALL
        SELECT 431601, 'Auno','Sub-District','Nigeria' UNION ALL
        SELECT 180101, 'Auyakayi','Sub-District','Nigeria' UNION ALL
        SELECT 180102, 'Auyo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 190803, 'Awon','Sub-District','Nigeria' UNION ALL
        SELECT 340601, 'Awulkiti','Sub-District','Nigeria' UNION ALL
        SELECT 180103, 'Ayama','Sub-District','Nigeria' UNION ALL
        SELECT 180104, 'Ayan','Sub-District','Nigeria' UNION ALL
        SELECT 192003, 'Ayu (Sanga)','Sub-District','Nigeria' UNION ALL
        SELECT 221901, 'Ayu (Wasagu/Danko)','Sub-District','Nigeria' UNION ALL
        SELECT 430703, 'Azir Multe','Sub-District','Nigeria' UNION ALL
        SELECT 203001, 'Azore','Sub-District','Nigeria' UNION ALL
        SELECT 210401, 'B/Mutum','Sub-District','Nigeria' UNION ALL
        SELECT 211802, 'Ba''Awa','Sub-District','Nigeria' UNION ALL
        SELECT 181701, 'Baauzini','Sub-District','Nigeria' UNION ALL
        SELECT 202401, 'Baawa','Sub-District','Nigeria' UNION ALL
        SELECT 421301, 'Baba','Sub-District','Nigeria' UNION ALL
        SELECT 213201, 'Baban Duhu ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213202, 'Baban Duhu ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 361501, 'Babangida','Sub-District','Nigeria' UNION ALL
        SELECT 201701, 'Babawa','Sub-District','Nigeria' UNION ALL
        SELECT 203801, 'Babban Giji','Sub-District','Nigeria' UNION ALL
        SELECT 202901, 'Babbar Riga','Sub-District','Nigeria' UNION ALL
        SELECT 180201, 'Babura (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 204101, 'Baburi','Sub-District','Nigeria' UNION ALL
        SELECT 220201, 'Bachaka (Arewa Dandi)','Sub-District','Nigeria' UNION ALL
        SELECT 340602, 'Bachaka (Gudu)','Sub-District','Nigeria' UNION ALL
        SELECT 204201, 'Bachirawa','Sub-District','Nigeria' UNION ALL
        SELECT 202402, 'Badafi','Sub-District','Nigeria' UNION ALL
        SELECT 420301, 'Badagari','Sub-District','Nigeria' UNION ALL
        SELECT 432203, 'Badairi','Sub-District','Nigeria' UNION ALL
        SELECT 421302, 'Badara','Sub-District','Nigeria' UNION ALL
        SELECT 190901, 'Badarawa (Kaduna North)','Sub-District','Nigeria' UNION ALL
        SELECT 371101, 'Badarawa (Shinkafi)','Sub-District','Nigeria' UNION ALL
        SELECT 340201, 'Badau/Darhela','Sub-District','Nigeria' UNION ALL
        SELECT 191001, 'Badiko','Sub-District','Nigeria' UNION ALL
        SELECT 342102, 'Bado','Sub-District','Nigeria' UNION ALL
        SELECT 432602, 'Badu','Sub-District','Nigeria' UNION ALL
        SELECT 191401, 'Badurum','Sub-District','Nigeria' UNION ALL
        SELECT 431702, 'Baga','Sub-District','Nigeria' UNION ALL
        SELECT 211201, 'Bagagadi','Sub-District','Nigeria' UNION ALL
        SELECT 340202, 'Bagarawa','Sub-District','Nigeria' UNION ALL
        SELECT 220403, 'Bagaye Meira','Sub-District','Nigeria' UNION ALL
        SELECT 370101, 'Bagega','Sub-District','Nigeria' UNION ALL
        SELECT 420601, 'Bagel','Sub-District','Nigeria' UNION ALL
        SELECT 341801, 'Bagida/Lukkingo','Sub-District','Nigeria' UNION ALL
        SELECT 212601, 'Bagiwa','Sub-District','Nigeria' UNION ALL
        SELECT 200402, 'Baguda','Sub-District','Nigeria' UNION ALL
        SELECT 220501, 'Bagudo/Tuga','Sub-District','Nigeria' UNION ALL
        SELECT 200301, 'Bagwai (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 203701, 'Bagwaro','Sub-District','Nigeria' UNION ALL
        SELECT 220502, 'Bahindi/Kaliel 1 (Bagudo)','Sub-District','Nigeria' UNION ALL
        SELECT 220503, 'Bahindi/Kaliel 2 (Bagudo)','Sub-District','Nigeria' UNION ALL
        SELECT 421901, 'Baima','Sub-District','Nigeria' UNION ALL
        SELECT 220901, 'Bajida','Sub-District','Nigeria' UNION ALL
        SELECT 342301, 'Bakale','Sub-District','Nigeria' UNION ALL
        SELECT 421201, 'Bakin Kasuwa','Sub-District','Nigeria' UNION ALL
        SELECT 200702, 'Bakin Ruwa','Sub-District','Nigeria' UNION ALL
        SELECT 210202, 'Bakiyawa','Sub-District','Nigeria' UNION ALL
        SELECT 210101, 'Bakori A','Sub-District','Nigeria' UNION ALL
        SELECT 210102, 'Bakori B','Sub-District','Nigeria' UNION ALL
        SELECT 370201, 'Bakura (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221802, 'Bakuwai','Sub-District','Nigeria' UNION ALL
        SELECT 181902, 'Balago','Sub-District','Nigeria' UNION ALL
        SELECT 201601, 'Balan','Sub-District','Nigeria' UNION ALL
        SELECT 361302, 'Balanguwa','Sub-District','Nigeria' UNION ALL
        SELECT 182001, 'Balarabe','Sub-District','Nigeria' UNION ALL
        SELECT 200102, 'Balare','Sub-District','Nigeria' UNION ALL
        SELECT 360603, 'Balle (Geidam)','Sub-District','Nigeria' UNION ALL
        SELECT 340603, 'Balle (Gudu)','Sub-District','Nigeria' UNION ALL
        SELECT 421502, 'Balma','Sub-District','Nigeria' UNION ALL
        SELECT 421003, 'Bambal','Sub-District','Nigeria' UNION ALL
        SELECT 212701, 'Bamle','Sub-District','Nigeria' UNION ALL
        SELECT 221803, 'Bandan','Sub-District','Nigeria' UNION ALL
        SELECT 370801, 'Banga','Sub-District','Nigeria' UNION ALL
        SELECT 340203, 'Bangi/Dabaga','Sub-District','Nigeria' UNION ALL
        SELECT 421603, 'Bangire','Sub-District','Nigeria' UNION ALL
        SELECT 220902, 'Bangu','Sub-District','Nigeria' UNION ALL
        SELECT 220504, 'Bani/Tsamiya 1 (Bagudo)','Sub-District','Nigeria' UNION ALL
        SELECT 220505, 'Bani/Tsamiya 2 (Bagudo)','Sub-District','Nigeria' UNION ALL
        SELECT 220801, 'Banizumbu','Sub-District','Nigeria' UNION ALL
        SELECT 341101, 'Bankanu/Rigakade','Sub-District','Nigeria' UNION ALL
        SELECT 430304, 'Banki','Sub-District','Nigeria' UNION ALL
        SELECT 430102, 'Banowa','Sub-District','Nigeria' UNION ALL
        SELECT 210601, 'Banye','Sub-District','Nigeria' UNION ALL
        SELECT 420302, 'Bar','Sub-District','Nigeria' UNION ALL
        SELECT 360801, 'Bara (Gulani)','Sub-District','Nigeria' UNION ALL
        SELECT 421303, 'Bara (Kirfi)','Sub-District','Nigeria' UNION ALL
        SELECT 182402, 'Baragumi 1','Sub-District','Nigeria' UNION ALL
        SELECT 431703, 'Barati','Sub-District','Nigeria' UNION ALL
        SELECT 210203, 'Barawa','Sub-District','Nigeria' UNION ALL
        SELECT 370102, 'Barayar Zaki','Sub-District','Nigeria' UNION ALL
        SELECT 420602, 'Baraza','Sub-District','Nigeria' UNION ALL
        SELECT 221804, 'Barbarejo','Sub-District','Nigeria' UNION ALL
        SELECT 430401, 'Barbaya','Sub-District','Nigeria' UNION ALL
        SELECT 190703, 'Barde (Jema''A)','Sub-District','Nigeria' UNION ALL
        SELECT 210103, 'Barde/K/Kwaram','Sub-District','Nigeria' UNION ALL
        SELECT 370601, 'Bardoki','Sub-District','Nigeria' UNION ALL
        SELECT 361401, 'Bare-Bari','Sub-District','Nigeria' UNION ALL
        SELECT 340901, 'Bargaja','Sub-District','Nigeria' UNION ALL
        SELECT 202403, 'Bargoni','Sub-District','Nigeria' UNION ALL
        SELECT 432701, 'Bargu','Sub-District','Nigeria' UNION ALL
        SELECT 341802, 'Barkeji/Nabaguda','Sub-District','Nigeria' UNION ALL
        SELECT 212201, 'Barkiya','Sub-District','Nigeria' UNION ALL
        SELECT 200601, 'Barkum','Sub-District','Nigeria' UNION ALL
        SELECT 191002, 'Barnawa','Sub-District','Nigeria' UNION ALL
        SELECT 341102, 'Basansan/Lemi','Sub-District','Nigeria' UNION ALL
        SELECT 191901, 'Basawa','Sub-District','Nigeria' UNION ALL
        SELECT 421503, 'Bashe','Sub-District','Nigeria' UNION ALL
        SELECT 341803, 'Bashire/Maikada','Sub-District','Nigeria' UNION ALL
        SELECT 181101, 'Basirka','Sub-District','Nigeria' UNION ALL
        SELECT 210204, 'Batagarawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 200202, 'Bataiya','Sub-District','Nigeria' UNION ALL
        SELECT 180202, 'Batali','Sub-District','Nigeria' UNION ALL
        SELECT 210302, 'Batsari (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 180401, 'Batu','Sub-District','Nigeria' UNION ALL
        SELECT 181801, 'Baturiya','Sub-District','Nigeria' UNION ALL
        SELECT 202404, 'Bauda','Sub-District','Nigeria' UNION ALL
        SELECT 212301, 'Bauranya','Sub-District','Nigeria' UNION ALL
        SELECT 213203, 'Baure ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213204, 'Baure ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 210402, 'Baure 1 (Baure)','Sub-District','Nigeria' UNION ALL
        SELECT 210501, 'Baure 2 (Bindawa)','Sub-District','Nigeria' UNION ALL
        SELECT 360201, 'Bayamari','Sub-District','Nigeria' UNION ALL
        SELECT 220404, 'Bayawa North','Sub-District','Nigeria' UNION ALL
        SELECT 220405, 'Bayawa South','Sub-District','Nigeria' UNION ALL
        SELECT 200403, 'Bebeji (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 222101, 'Bedi','Sub-District','Nigeria' UNION ALL
        SELECT 430704, 'Bego Karwa','Sub-District','Nigeria' UNION ALL
        SELECT 180902, 'Bekarya','Sub-District','Nigeria' UNION ALL
        SELECT 370501, 'Bela/Rawayya','Sub-District','Nigeria' UNION ALL
        SELECT 182702, 'Belas','Sub-District','Nigeria' UNION ALL
        SELECT 203401, 'Beli (Rogo)','Sub-District','Nigeria' UNION ALL
        SELECT 421604, 'Beli (Shira)','Sub-District','Nigeria' UNION ALL
        SELECT 221902, 'Bena','Sub-District','Nigeria' UNION ALL
        SELECT 342302, 'Bengaji','Sub-District','Nigeria' UNION ALL
        SELECT 421304, 'Beni','Sub-District','Nigeria' UNION ALL
        SELECT 431401, 'Benisheikh','Sub-District','Nigeria' UNION ALL
        SELECT 211502, 'Beruruwa/Ruruma','Sub-District','Nigeria' UNION ALL
        SELECT 221301, 'Besse','Sub-District','Nigeria' UNION ALL
        SELECT 421403, 'Beti','Sub-District','Nigeria' UNION ALL
        SELECT 200501, 'Bichi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421202, 'Bidir','Sub-District','Nigeria' UNION ALL
        SELECT 431801, 'Bilagusi','Sub-District','Nigeria' UNION ALL
        SELECT 361001, 'Bilal Jawa','Sub-District','Nigeria' UNION ALL
        SELECT 371301, 'Bilbis','Sub-District','Nigeria' UNION ALL
        SELECT 431201, 'Bilingwi','Sub-District','Nigeria' UNION ALL
        SELECT 421004, 'Bilkicheri','Sub-District','Nigeria' UNION ALL
        SELECT 210502, 'Bindawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360301, 'Bindigari / Pawari','Sub-District','Nigeria' UNION ALL
        SELECT 371001, 'Bindin','Sub-District','Nigeria' UNION ALL
        SELECT 371002, 'Bingi','Sub-District','Nigeria' UNION ALL
        SELECT 370502, 'Bingi North','Sub-District','Nigeria' UNION ALL
        SELECT 370503, 'Bingi South','Sub-District','Nigeria' UNION ALL
        SELECT 340101, 'Binji (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 342303, 'Binjin Muza','Sub-District','Nigeria' UNION ALL
        SELECT 212202, 'Birchi','Sub-District','Nigeria' UNION ALL
        SELECT 420103, 'Birin Gigyara','Sub-District','Nigeria' UNION ALL
        SELECT 361502, 'Biriri','Sub-District','Nigeria' UNION ALL
        SELECT 340501, 'Birjingo','Sub-District','Nigeria' UNION ALL
        SELECT 180301, 'Birnin Kudu (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370301, 'Birnin Magaji','Sub-District','Nigeria' UNION ALL
        SELECT 370602, 'Birnin Magaji-Gmm','Sub-District','Nigeria' UNION ALL
        SELECT 342304, 'Birnin Ruwa','Sub-District','Nigeria' UNION ALL
        SELECT 220903, 'Birnin Tudu','Sub-District','Nigeria' UNION ALL
        SELECT 220406, 'Birnin Tudu Gudale','Sub-District','Nigeria' UNION ALL
        SELECT 370202, 'Birnin Tudu-Bka','Sub-District','Nigeria' UNION ALL
        SELECT 370603, 'Birnin Tudu/Gmm','Sub-District','Nigeria' UNION ALL
        SELECT 221501, 'Birnin Yauri','Sub-District','Nigeria' UNION ALL
        SELECT 190402, 'Birnin Yero (Igabi)','Sub-District','Nigeria' UNION ALL
        SELECT 371102, 'Birnin Yero (Shinkafi)','Sub-District','Nigeria' UNION ALL
        SELECT 180402, 'Birniwa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420201, 'Birshi','Sub-District','Nigeria' UNION ALL
        SELECT 190804, 'Bishini','Sub-District','Nigeria' UNION ALL
        SELECT 431102, 'Bita Izge','Sub-District','Nigeria' UNION ALL
        SELECT 191402, 'Bital','Sub-District','Nigeria' UNION ALL
        SELECT 190601, 'Bitaro/Dura','Sub-District','Nigeria' UNION ALL
        SELECT 430802, 'Boboshe','Sub-District','Nigeria' UNION ALL
        SELECT 340301, 'Bodai','Sub-District','Nigeria' UNION ALL
        SELECT 340204, 'Bodinga/Tauma','Sub-District','Nigeria' UNION ALL
        SELECT 361101, 'Bogo','Sub-District','Nigeria' UNION ALL
        SELECT 430305, 'Bogomari','Sub-District','Nigeria' UNION ALL
        SELECT 420303, 'Bogoro (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 432302, 'Bogum','Sub-District','Nigeria' UNION ALL
        SELECT 420304, 'Boi','Sub-District','Nigeria' UNION ALL
        SELECT 192004, 'Bokana','Sub-District','Nigeria' UNION ALL
        SELECT 212302, 'Boko (Kusada)','Sub-District','Nigeria' UNION ALL
        SELECT 371401, 'Boko (Zurmi)','Sub-District','Nigeria' UNION ALL
        SELECT 361402, 'Bolewa A','Sub-District','Nigeria' UNION ALL
        SELECT 361403, 'Bolewa B','Sub-District','Nigeria' UNION ALL
        SELECT 432101, 'Bolori I','Sub-District','Nigeria' UNION ALL
        SELECT 432102, 'Bolori Ii','Sub-District','Nigeria' UNION ALL
        SELECT 191902, 'Bomo','Sub-District','Nigeria' UNION ALL
        SELECT 191302, 'Bondong','Sub-District','Nigeria' UNION ALL
        SELECT 200602, 'Bono','Sub-District','Nigeria' UNION ALL
        SELECT 431402, 'Borgozo','Sub-District','Nigeria' UNION ALL
        SELECT 212501, 'Borindawa','Sub-District','Nigeria' UNION ALL
        SELECT 360604, 'Borko','Sub-District','Nigeria' UNION ALL
        SELECT 360502, 'Borno Kiji','Sub-District','Nigeria' UNION ALL
        SELECT 432003, 'Borno Yesu','Sub-District','Nigeria' UNION ALL
        SELECT 432204, 'Borsori','Sub-District','Nigeria' UNION ALL
        SELECT 340502, 'Boyekai','Sub-District','Nigeria' UNION ALL
        SELECT 430402, 'Briyel','Sub-District','Nigeria' UNION ALL
        SELECT 220407, 'Bubuche','Sub-District','Nigeria' UNION ALL
        SELECT 191202, 'Buda','Sub-District','Nigeria' UNION ALL
        SELECT 180801, 'Buduru','Sub-District','Nigeria' UNION ALL
        SELECT 360901, 'Buduwa','Sub-District','Nigeria' UNION ALL
        SELECT 211601, 'Bugaje','Sub-District','Nigeria' UNION ALL
        SELECT 420305, 'Bugun','Sub-District','Nigeria' UNION ALL
        SELECT 212602, 'Bujawa/Gewayau','Sub-District','Nigeria' UNION ALL
        SELECT 180502, 'Buji (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370402, 'Bukkuyum (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421605, 'Bukul','Sub-District','Nigeria' UNION ALL
        SELECT 431103, 'Bulabulin (Gwoza)','Sub-District','Nigeria' UNION ALL
        SELECT 432103, 'Bulabulin (Maiduguri)','Sub-District','Nigeria' UNION ALL
        SELECT 361303, 'Bulabulin (Nguru)','Sub-District','Nigeria' UNION ALL
        SELECT 421701, 'Bulangawo A','Sub-District','Nigeria' UNION ALL
        SELECT 421702, 'Bulangawo B','Sub-District','Nigeria' UNION ALL
        SELECT 181501, 'Bulangu','Sub-District','Nigeria' UNION ALL
        SELECT 360802, 'Bularafa','Sub-District','Nigeria' UNION ALL
        SELECT 361701, 'Bulatura','Sub-District','Nigeria' UNION ALL
        SELECT 421203, 'Bulkachuwa','Sub-District','Nigeria' UNION ALL
        SELECT 361601, 'Bultuwa','Sub-District','Nigeria' UNION ALL
        SELECT 181802, 'Bulunchai','Sub-District','Nigeria' UNION ALL
        SELECT 220802, 'Buma (Dandi)','Sub-District','Nigeria' UNION ALL
        SELECT 432702, 'Buma (Shani)','Sub-District','Nigeria' UNION ALL
        SELECT 202601, 'Bumai','Sub-District','Nigeria' UNION ALL
        SELECT 212401, 'Bumbum A','Sub-District','Nigeria' UNION ALL
        SELECT 212402, 'Bumbum B','Sub-District','Nigeria' UNION ALL
        SELECT 420603, 'Bundot','Sub-District','Nigeria' UNION ALL
        SELECT 431704, 'Bundur','Sub-District','Nigeria' UNION ALL
        SELECT 370504, 'Bungudu (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360701, 'Buni Gari','Sub-District','Nigeria' UNION ALL
        SELECT 360702, 'Buni Yadi','Sub-District','Nigeria' UNION ALL
        SELECT 340102, 'Bunkari','Sub-District','Nigeria' UNION ALL
        SELECT 200603, 'Bunkure (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360803, 'Bunsa','Sub-District','Nigeria' UNION ALL
        SELECT 181201, 'Buntusu','Sub-District','Nigeria' UNION ALL
        SELECT 421703, 'Bununu A','Sub-District','Nigeria' UNION ALL
        SELECT 420604, 'Bununu Central','Sub-District','Nigeria' UNION ALL
        SELECT 420605, 'Bununu East','Sub-District','Nigeria' UNION ALL
        SELECT 420606, 'Bununu South','Sub-District','Nigeria' UNION ALL
        SELECT 420607, 'Bununu West','Sub-District','Nigeria' UNION ALL
        SELECT 430501, 'Buratai','Sub-District','Nigeria' UNION ALL
        SELECT 211901, 'Burdugau','Sub-District','Nigeria' UNION ALL
        SELECT 202801, 'Burji','Sub-District','Nigeria' UNION ALL
        SELECT 421504, 'Burra','Sub-District','Nigeria' UNION ALL
        SELECT 422003, 'Bursali','Sub-District','Nigeria' UNION ALL
        SELECT 204102, 'Burun-Burun','Sub-District','Nigeria' UNION ALL
        SELECT 421204, 'Buskuri','Sub-District','Nigeria' UNION ALL
        SELECT 430103, 'Busuna','Sub-District','Nigeria' UNION ALL
        SELECT 203301, 'Butu-Butu','Sub-District','Nigeria' UNION ALL
        SELECT 421005, 'Buzawa','Sub-District','Nigeria' UNION ALL
        SELECT 342203, 'Chacho/Marnona','Sub-District','Nigeria' UNION ALL
        SELECT 182301, 'Chaichai','Sub-District','Nigeria' UNION ALL
        SELECT 202501, 'Challawa','Sub-District','Nigeria' UNION ALL
        SELECT 432303, 'Chamba','Sub-District','Nigeria' UNION ALL
        SELECT 180602, 'Chamo','Sub-District','Nigeria' UNION ALL
        SELECT 210602, 'Charanchi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221001, 'Cheberu','Sub-District','Nigeria' UNION ALL
        SELECT 202101, 'Chedi','Sub-District','Nigeria' UNION ALL
        SELECT 371302, 'Chediya','Sub-District','Nigeria' UNION ALL
        SELECT 220202, 'Chibiku','Sub-District','Nigeria' UNION ALL
        SELECT 191903, 'Chikaji','Sub-District','Nigeria' UNION ALL
        SELECT 431104, 'Chikide Jahode','Sub-District','Nigeria' UNION ALL
        SELECT 190201, 'Chikun (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361201, 'Chilariye','Sub-District','Nigeria' UNION ALL
        SELECT 340604, 'Chillas','Sub-District','Nigeria' UNION ALL
        SELECT 340703, 'Chimola','Sub-District','Nigeria' UNION ALL
        SELECT 421205, 'Chinade','Sub-District','Nigeria' UNION ALL
        SELECT 420901, 'Chinkani','Sub-District','Nigeria' UNION ALL
        SELECT 202502, 'Chiranchi','Sub-District','Nigeria' UNION ALL
        SELECT 180503, 'Chirbin','Sub-District','Nigeria' UNION ALL
        SELECT 200604, 'Chirin','Sub-District','Nigeria' UNION ALL
        SELECT 201501, 'Chiromawa','Sub-District','Nigeria' UNION ALL
        SELECT 190602, 'Chori','Sub-District','Nigeria' UNION ALL
        SELECT 361202, 'Chukiriwa','Sub-District','Nigeria' UNION ALL
        SELECT 182602, 'Chukuto','Sub-District','Nigeria' UNION ALL
        SELECT 182603, 'Chukwikwiwa','Sub-District','Nigeria' UNION ALL
        SELECT 200103, 'Chula','Sub-District','Nigeria' UNION ALL
        SELECT 222001, 'Chulu/Gumbi','Sub-District','Nigeria' UNION ALL
        SELECT 202802, 'Cinkoso','Sub-District','Nigeria' UNION ALL
        SELECT 220101, 'D/Galadima 1','Sub-District','Nigeria' UNION ALL
        SELECT 220102, 'D/Galadima 11','Sub-District','Nigeria' UNION ALL
        SELECT 221302, 'D/Meri D/Mereu','Sub-District','Nigeria' UNION ALL
        SELECT 181702, 'Daba','Sub-District','Nigeria' UNION ALL
        SELECT 210901, 'Dabai (Danja)','Sub-District','Nigeria' UNION ALL
        SELECT 222102, 'Dabai (Zuru)','Sub-District','Nigeria' UNION ALL
        SELECT 222103, 'Dabai Seme','Sub-District','Nigeria' UNION ALL
        SELECT 210205, 'Dabaibayawa','Sub-District','Nigeria' UNION ALL
        SELECT 200901, 'Dabar Kwari','Sub-District','Nigeria' UNION ALL
        SELECT 211202, 'Dabawa','Sub-District','Nigeria' UNION ALL
        SELECT 181703, 'Dabaza','Sub-District','Nigeria' UNION ALL
        SELECT 181202, 'Dabi (Gwiwa)','Sub-District','Nigeria' UNION ALL
        SELECT 182302, 'Dabi (Ringim)','Sub-District','Nigeria' UNION ALL
        SELECT 200104, 'Dabin-Kanawa','Sub-District','Nigeria' UNION ALL
        SELECT 430902, 'Dabira','Sub-District','Nigeria' UNION ALL
        SELECT 361304, 'Dabule','Sub-District','Nigeria' UNION ALL
        SELECT 181603, 'Dabuwaran','Sub-District','Nigeria' UNION ALL
        SELECT 221303, 'Dada/Alelu','Sub-District','Nigeria' UNION ALL
        SELECT 204001, 'Daddarawa','Sub-District','Nigeria' UNION ALL
        SELECT 190603, 'Daddu','Sub-District','Nigeria' UNION ALL
        SELECT 190902, 'Dadi Riba','Sub-District','Nigeria' UNION ALL
        SELECT 201101, 'Dadin Kowa','Sub-District','Nigeria' UNION ALL
        SELECT 360703, 'Dadingel','Sub-District','Nigeria' UNION ALL
        SELECT 421206, 'Dagaro','Sub-District','Nigeria' UNION ALL
        SELECT 420401, 'Dagauda','Sub-District','Nigeria' UNION ALL
        SELECT 342305, 'Dagawa/Rugar','Sub-District','Nigeria' UNION ALL
        SELECT 360101, 'Dagona','Sub-District','Nigeria' UNION ALL
        SELECT 421902, 'Dagu','Sub-District','Nigeria' UNION ALL
        SELECT 204402, 'Dagumawa','Sub-District','Nigeria' UNION ALL
        SELECT 200203, 'Daho','Sub-District','Nigeria' UNION ALL
        SELECT 431501, 'Daima','Sub-District','Nigeria' UNION ALL
        SELECT 421704, 'Dajin','Sub-District','Nigeria' UNION ALL
        SELECT 181604, 'Dakaiyyawa','Sub-District','Nigeria' UNION ALL
        SELECT 201502, 'Dakasoye','Sub-District','Nigeria' UNION ALL
        SELECT 203101, 'Dakata','Sub-District','Nigeria' UNION ALL
        SELECT 221805, 'Dakin Gari','Sub-District','Nigeria' UNION ALL
        SELECT 370203, 'Dakko','Sub-District','Nigeria' UNION ALL
        SELECT 201401, 'Dal','Sub-District','Nigeria' UNION ALL
        SELECT 431302, 'Dala (Jere)','Sub-District','Nigeria' UNION ALL
        SELECT 200703, 'Dala (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 204103, 'Dalawa','Sub-District','Nigeria' UNION ALL
        SELECT 221002, 'Dalijan','Sub-District','Nigeria' UNION ALL
        SELECT 421903, 'Dallaji','Sub-District','Nigeria' UNION ALL
        SELECT 210503, 'Dallaji/Faru','Sub-District','Nigeria' UNION ALL
        SELECT 202701, 'Dalli','Sub-District','Nigeria' UNION ALL
        SELECT 431602, 'Dalori','Sub-District','Nigeria' UNION ALL
        SELECT 431603, 'Dalwa','Sub-District','Nigeria' UNION ALL
        SELECT 370901, 'Damaga/Gamagiwa','Sub-District','Nigeria' UNION ALL
        SELECT 360503, 'Damagum A.','Sub-District','Nigeria' UNION ALL
        SELECT 360504, 'Damagum B.','Sub-District','Nigeria' UNION ALL
        SELECT 361102, 'Damai','Sub-District','Nigeria' UNION ALL
        SELECT 360302, 'Damakasu','Sub-District','Nigeria' UNION ALL
        SELECT 191403, 'Damakasuwa','Sub-District','Nigeria' UNION ALL
        SELECT 432401, 'Damakuli','Sub-District','Nigeria' UNION ALL
        SELECT 432603, 'Damaram','Sub-District','Nigeria' UNION ALL
        SELECT 190101, 'Damari (Birnin Gwari)','Sub-District','Nigeria' UNION ALL
        SELECT 213101, 'Damari (Sabuwa)','Sub-District','Nigeria' UNION ALL
        SELECT 432304, 'Damasau','Sub-District','Nigeria' UNION ALL
        SELECT 360303, 'Damaturu Central','Sub-District','Nigeria' UNION ALL
        SELECT 200404, 'Damau (Bebeji)','Sub-District','Nigeria' UNION ALL
        SELECT 191502, 'Damau (Kubau)','Sub-District','Nigeria' UNION ALL
        SELECT 340802, 'Damba','Sub-District','Nigeria' UNION ALL
        SELECT 221304, 'Damba/Bakoshi','Sub-District','Nigeria' UNION ALL
        SELECT 420402, 'Dambam A','Sub-District','Nigeria' UNION ALL
        SELECT 420403, 'Dambam B','Sub-District','Nigeria' UNION ALL
        SELECT 192301, 'Dambo','Sub-District','Nigeria' UNION ALL
        SELECT 430705, 'Damboa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370302, 'Damfani/S.Birni','Sub-District','Nigeria' UNION ALL
        SELECT 370204, 'Damri','Sub-District','Nigeria' UNION ALL
        SELECT 420104, 'Dan','Sub-District','Nigeria' UNION ALL
        SELECT 210701, 'Dan - Ali','Sub-District','Nigeria' UNION ALL
        SELECT 202102, 'Dan Agundi','Sub-District','Nigeria' UNION ALL
        SELECT 191702, 'Dan Alhaji','Sub-District','Nigeria' UNION ALL
        SELECT 180903, 'Dan Ama','Sub-District','Nigeria' UNION ALL
        SELECT 420202, 'Dan Amar A','Sub-District','Nigeria' UNION ALL
        SELECT 420203, 'Dan Amar B','Sub-District','Nigeria' UNION ALL
        SELECT 211101, 'Dan Auani','Sub-District','Nigeria' UNION ALL
        SELECT 420204, 'Dan Dango','Sub-District','Nigeria' UNION ALL
        SELECT 210702, 'Dan Dire A','Sub-District','Nigeria' UNION ALL
        SELECT 210703, 'Dan Dire B','Sub-District','Nigeria' UNION ALL
        SELECT 211403, 'Dan Dutse','Sub-District','Nigeria' UNION ALL
        SELECT 220602, 'Dan Galadima','Sub-District','Nigeria' UNION ALL
        SELECT 371003, 'Dan Gulbi','Sub-District','Nigeria' UNION ALL
        SELECT 202702, 'Dan Hassan','Sub-District','Nigeria' UNION ALL
        SELECT 370802, 'Dan Isa','Sub-District','Nigeria' UNION ALL
        SELECT 420205, 'Dan Iya','Sub-District','Nigeria' UNION ALL
        SELECT 371004, 'Dan Kurmi','Sub-District','Nigeria' UNION ALL
        SELECT 210704, 'Dan Musa A','Sub-District','Nigeria' UNION ALL
        SELECT 210705, 'Dan Musa B','Sub-District','Nigeria' UNION ALL
        SELECT 371005, 'Dan Sadau','Sub-District','Nigeria' UNION ALL
        SELECT 221903, 'Dan Umaru','Sub-District','Nigeria' UNION ALL
        SELECT 220103, 'Dan Warai','Sub-District','Nigeria' UNION ALL
        SELECT 210303, 'Dan-Alhaji/Yangayya','Sub-District','Nigeria' UNION ALL
        SELECT 360202, 'Danani / Lawanti','Sub-District','Nigeria' UNION ALL
        SELECT 200902, 'Danbagina','Sub-District','Nigeria' UNION ALL
        SELECT 202503, 'Danbare','Sub-District','Nigeria' UNION ALL
        SELECT 200802, 'Danbatta 1','Sub-District','Nigeria' UNION ALL
        SELECT 200803, 'Danbatta 2','Sub-District','Nigeria' UNION ALL
        SELECT 340205, 'Danchadi','Sub-District','Nigeria' UNION ALL
        SELECT 361404, 'Danchuwa','Sub-District','Nigeria' UNION ALL
        SELECT 201801, 'Dandago','Sub-District','Nigeria' UNION ALL
        SELECT 210206, 'Dandagoro','Sub-District','Nigeria' UNION ALL
        SELECT 191801, 'Dandamisa','Sub-District','Nigeria' UNION ALL
        SELECT 221806, 'Dandane','Sub-District','Nigeria' UNION ALL
        SELECT 203901, 'Dandare','Sub-District','Nigeria' UNION ALL
        SELECT 181704, 'Dandi (Kazaure)','Sub-District','Nigeria' UNION ALL
        SELECT 341401, 'Dandin Mahe','Sub-District','Nigeria' UNION ALL
        SELECT 210801, 'Dandume A','Sub-District','Nigeria' UNION ALL
        SELECT 210802, 'Dandume B','Sub-District','Nigeria' UNION ALL
        SELECT 213301, 'Daneji ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213302, 'Daneji ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 200302, 'Dangada','Sub-District','Nigeria' UNION ALL
        SELECT 370103, 'Dangaladima (Anka)','Sub-District','Nigeria' UNION ALL
        SELECT 220701, 'Dangaladima (Bunza)','Sub-District','Nigeria' UNION ALL
        SELECT 221102, 'Dangamaji','Sub-District','Nigeria' UNION ALL
        SELECT 212901, 'Dangani','Sub-District','Nigeria' UNION ALL
        SELECT 340302, 'Dange','Sub-District','Nigeria' UNION ALL
        SELECT 421606, 'Dango','Sub-District','Nigeria' UNION ALL
        SELECT 221201, 'Dangoma/Gayi','Sub-District','Nigeria' UNION ALL
        SELECT 202405, 'Dangora','Sub-District','Nigeria' UNION ALL
        SELECT 201001, 'Danguguwa','Sub-District','Nigeria' UNION ALL
        SELECT 342001, 'Dangulbi','Sub-District','Nigeria' UNION ALL
        SELECT 191802, 'Danguzuri','Sub-District','Nigeria' UNION ALL
        SELECT 180403, 'Dangwaleri','Sub-District','Nigeria' UNION ALL
        SELECT 182503, 'Dangwanki','Sub-District','Nigeria' UNION ALL
        SELECT 182201, 'Dangyatun','Sub-District','Nigeria' UNION ALL
        SELECT 210902, 'Danja A','Sub-District','Nigeria' UNION ALL
        SELECT 210903, 'Danja B','Sub-District','Nigeria' UNION ALL
        SELECT 212902, 'Danjanku/Karachi','Sub-District','Nigeria' UNION ALL
        SELECT 371303, 'Danjibga','Sub-District','Nigeria' UNION ALL
        SELECT 211803, 'Dankaba','Sub-District','Nigeria' UNION ALL
        SELECT 420206, 'Dankade','Sub-District','Nigeria' UNION ALL
        SELECT 370205, 'Dankadu','Sub-District','Nigeria' UNION ALL
        SELECT 211804, 'Dankama','Sub-District','Nigeria' UNION ALL
        SELECT 204403, 'Dankaza','Sub-District','Nigeria' UNION ALL
        SELECT 221904, 'Danko/Maga','Sub-District','Nigeria' UNION ALL
        SELECT 221602, 'Dankolo','Sub-District','Nigeria' UNION ALL
        SELECT 210403, 'Dankum/Agala','Sub-District','Nigeria' UNION ALL
        SELECT 182002, 'Dankumbo','Sub-District','Nigeria' UNION ALL
        SELECT 182504, 'Danladi','Sub-District','Nigeria' UNION ALL
        SELECT 204302, 'Danlasan','Sub-District','Nigeria' UNION ALL
        SELECT 190301, 'Danmahawayi','Sub-District','Nigeria' UNION ALL
        SELECT 202504, 'Danmaliki','Sub-District','Nigeria' UNION ALL
        SELECT 370206, 'Danmanau','Sub-District','Nigeria' UNION ALL
        SELECT 211902, 'Danmurabu','Sub-District','Nigeria' UNION ALL
        SELECT 212502, 'Dansarai','Sub-District','Nigeria' UNION ALL
        SELECT 202406, 'Dansoshiya','Sub-District','Nigeria' UNION ALL
        SELECT 182403, 'Dansure 1','Sub-District','Nigeria' UNION ALL
        SELECT 210803, 'Dantakari','Sub-District','Nigeria' UNION ALL
        SELECT 180904, 'Dantanoma','Sub-District','Nigeria' UNION ALL
        SELECT 211701, 'Dantutture','Sub-District','Nigeria' UNION ALL
        SELECT 192101, 'Danwata','Sub-District','Nigeria' UNION ALL
        SELECT 212403, 'Danyashe','Sub-District','Nigeria' UNION ALL
        SELECT 200502, 'Danzabuwa','Sub-District','Nigeria' UNION ALL
        SELECT 182505, 'Danzomo','Sub-District','Nigeria' UNION ALL
        SELECT 360203, 'Dapchi','Sub-District','Nigeria' UNION ALL
        SELECT 211503, 'Dara','Sub-District','Nigeria' UNION ALL
        SELECT 340803, 'Daran Sabon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 420501, 'Darazo East','Sub-District','Nigeria' UNION ALL
        SELECT 420502, 'Darazo West','Sub-District','Nigeria' UNION ALL
        SELECT 213401, 'Dargage','Sub-District','Nigeria' UNION ALL
        SELECT 361203, 'Darin/ Langawa','Sub-District','Nigeria' UNION ALL
        SELECT 181203, 'Darina','Sub-District','Nigeria' UNION ALL
        SELECT 210304, 'Darini/Magaji Abu','Sub-District','Nigeria' UNION ALL
        SELECT 204404, 'Darki','Sub-District','Nigeria' UNION ALL
        SELECT 203802, 'Darmanawa','Sub-District','Nigeria' UNION ALL
        SELECT 340804, 'Darnar Tsolawo','Sub-District','Nigeria' UNION ALL
        SELECT 202407, 'Dashi','Sub-District','Nigeria' UNION ALL
        SELECT 211301, 'Daudawa','Sub-District','Nigeria' UNION ALL
        SELECT 371304, 'Dauki','Sub-District','Nigeria' UNION ALL
        SELECT 211504, 'Daunaka/Bakinkori','Sub-District','Nigeria' UNION ALL
        SELECT 202201, 'Daura (Karaye)','Sub-District','Nigeria' UNION ALL
        SELECT 360505, 'Daura A','Sub-District','Nigeria' UNION ALL
        SELECT 360506, 'Daura B.','Sub-District','Nigeria' UNION ALL
        SELECT 371402, 'Daura/B.Tsaba','Sub-District','Nigeria' UNION ALL
        SELECT 203803, 'Daurawa','Sub-District','Nigeria' UNION ALL
        SELECT 181003, 'Dawa','Sub-District','Nigeria' UNION ALL
        SELECT 420207, 'Dawaki (Bauchi)','Sub-District','Nigeria' UNION ALL
        SELECT 200903, 'Dawaki (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
        SELECT 191404, 'Dawaki (Kauru)','Sub-District','Nigeria' UNION ALL
        SELECT 203201, 'Dawaki (Rano)','Sub-District','Nigeria' UNION ALL
        SELECT 201002, 'Dawaki East','Sub-District','Nigeria' UNION ALL
        SELECT 201003, 'Dawaki West','Sub-District','Nigeria' UNION ALL
        SELECT 200904, 'Dawakiji','Sub-District','Nigeria' UNION ALL
        SELECT 203302, 'Dawakin Gulu','Sub-District','Nigeria' UNION ALL
        SELECT 182703, 'Dawan Gawo','Sub-District','Nigeria' UNION ALL
        SELECT 210104, 'Dawan Musa','Sub-District','Nigeria' UNION ALL
        SELECT 201004, 'Dawanau','Sub-District','Nigeria' UNION ALL
        SELECT 361204, 'Dawasa /G/Baba','Sub-District','Nigeria' UNION ALL
        SELECT 360102, 'Dawayo','Sub-District','Nigeria' UNION ALL
        SELECT 212503, 'Dayi','Sub-District','Nigeria' UNION ALL
        SELECT 420306, 'Dazara','Sub-District','Nigeria' UNION ALL
        SELECT 361205, 'Dazigau','Sub-District','Nigeria' UNION ALL
        SELECT 361602, 'Degeltura','Sub-District','Nigeria' UNION ALL
        SELECT 361206, 'Degubi','Sub-District','Nigeria' UNION ALL
        SELECT 361603, 'Dekwa','Sub-District','Nigeria' UNION ALL
        SELECT 421305, 'Dewu','Sub-District','Nigeria' UNION ALL
        SELECT 421006, 'Diga','Sub-District','Nigeria' UNION ALL
        SELECT 221202, 'Diggi','Sub-District','Nigeria' UNION ALL
        SELECT 180404, 'Diginsa','Sub-District','Nigeria' UNION ALL
        SELECT 220302, 'Dikko','Sub-District','Nigeria' UNION ALL
        SELECT 430803, 'Dikwa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361604, 'Dilala/Kalgi','Sub-District','Nigeria' UNION ALL
        SELECT 430202, 'Dille/Huy','Sub-District','Nigeria' UNION ALL
        SELECT 342204, 'Dimbiso','Sub-District','Nigeria' UNION ALL
        SELECT 342205, 'Dinawa','Sub-District','Nigeria' UNION ALL
        SELECT 181102, 'Dingaya','Sub-District','Nigeria' UNION ALL
        SELECT 421505, 'Dingis','Sub-District','Nigeria' UNION ALL
        SELECT 340206, 'Dingyadi','Sub-District','Nigeria' UNION ALL
        SELECT 430306, 'Dipchari','Sub-District','Nigeria' UNION ALL
        SELECT 421607, 'Disina','Sub-District','Nigeria' UNION ALL
        SELECT 201802, 'Diso','Sub-District','Nigeria' UNION ALL
        SELECT 212801, 'Dissi','Sub-District','Nigeria' UNION ALL
        SELECT 221003, 'Dodoru','Sub-District','Nigeria' UNION ALL
        SELECT 191904, 'Dogarawa','Sub-District','Nigeria' UNION ALL
        SELECT 361405, 'Dogo Nini','Sub-District','Nigeria' UNION ALL
        SELECT 361406, 'Dogo Tebo','Sub-District','Nigeria' UNION ALL
        SELECT 431403, 'Dogoma/ J','Sub-District','Nigeria' UNION ALL
        SELECT 421101, 'Dogon  Jeji A','Sub-District','Nigeria' UNION ALL
        SELECT 421102, 'Dogon  Jeji B','Sub-District','Nigeria' UNION ALL
        SELECT 190102, 'Dogon Dawa','Sub-District','Nigeria' UNION ALL
        SELECT 421103, 'Dogon Jeji C','Sub-District','Nigeria' UNION ALL
        SELECT 201102, 'Dogon Kawo','Sub-District','Nigeria' UNION ALL
        SELECT 200704, 'Dogon Nama','Sub-District','Nigeria' UNION ALL
        SELECT 341804, 'Dogondaji/Salah','Sub-District','Nigeria' UNION ALL
        SELECT 431705, 'Dogoshi','Sub-District','Nigeria' UNION ALL
        SELECT 212702, 'Doguru A','Sub-District','Nigeria' UNION ALL
        SELECT 212703, 'Doguru B','Sub-District','Nigeria' UNION ALL
        SELECT 420902, 'Doguwa (Giade)','Sub-District','Nigeria' UNION ALL
        SELECT 201103, 'Doguwa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 210603, 'Doka (Charanchi)','Sub-District','Nigeria' UNION ALL
        SELECT 190805, 'Doka (Kachia)','Sub-District','Nigeria' UNION ALL
        SELECT 191601, 'Doka (Kudan)','Sub-District','Nigeria' UNION ALL
        SELECT 203902, 'Doka (Tofa)','Sub-District','Nigeria' UNION ALL
        SELECT 203303, 'Doka Dawa','Sub-District','Nigeria' UNION ALL
        SELECT 221603, 'Doka/Bere','Sub-District','Nigeria' UNION ALL
        SELECT 180802, 'Doko','Sub-District','Nigeria' UNION ALL
        SELECT 360804, 'Dokshi','Sub-District','Nigeria' UNION ALL
        SELECT 371403, 'Dole','Sub-District','Nigeria' UNION ALL
        SELECT 361103, 'Dole  Machina','Sub-District','Nigeria' UNION ALL
        SELECT 220803, 'Dolekaina','Sub-District','Nigeria' UNION ALL
        SELECT 431404, 'Dongo','Sub-District','Nigeria' UNION ALL
        SELECT 180203, 'Dorawa','Sub-District','Nigeria' UNION ALL
        SELECT 201503, 'Dorawar Sallau','Sub-District','Nigeria' UNION ALL
        SELECT 201803, 'Dorayi','Sub-District','Nigeria' UNION ALL
        SELECT 210504, 'Doro (Bindawa)','Sub-District','Nigeria' UNION ALL
        SELECT 431706, 'Doro (Kukawa)','Sub-District','Nigeria' UNION ALL
        SELECT 200905, 'Dosan','Sub-District','Nigeria' UNION ALL
        SELECT 370902, 'Dosara/Birni Kaya','Sub-District','Nigeria' UNION ALL
        SELECT 420608, 'Dott','Sub-District','Nigeria' UNION ALL
        SELECT 181302, 'Dubantu','Sub-District','Nigeria' UNION ALL
        SELECT 361207, 'Duddaye / Pakarau','Sub-District','Nigeria' UNION ALL
        SELECT 212303, 'Dudunni','Sub-District','Nigeria' UNION ALL
        SELECT 202001, 'Dugabau','Sub-District','Nigeria' UNION ALL
        SELECT 430502, 'Dugja','Sub-District','Nigeria' UNION ALL
        SELECT 221702, 'Dugu Tsoho','Sub-District','Nigeria' UNION ALL
        SELECT 211505, 'Dugul','Sub-District','Nigeria' UNION ALL
        SELECT 203304, 'Dugurawa','Sub-District','Nigeria' UNION ALL
        SELECT 200204, 'Duja','Sub-District','Nigeria' UNION ALL
        SELECT 432305, 'Duji','Sub-District','Nigeria' UNION ALL
        SELECT 340401, 'Dukamaje','Sub-District','Nigeria' UNION ALL
        SELECT 202703, 'Dukawa','Sub-District','Nigeria' UNION ALL
        SELECT 211404, 'Dukke','Sub-District','Nigeria' UNION ALL
        SELECT 421705, 'Dull A','Sub-District','Nigeria' UNION ALL
        SELECT 421706, 'Dull B','Sub-District','Nigeria' UNION ALL
        SELECT 342002, 'Duma','Sub-District','Nigeria' UNION ALL
        SELECT 181502, 'Dumadumi Toka','Sub-District','Nigeria' UNION ALL
        SELECT 360902, 'Dumbari','Sub-District','Nigeria' UNION ALL
        SELECT 221103, 'Dumbegu','Sub-District','Nigeria' UNION ALL
        SELECT 361305, 'Dumsai','Sub-District','Nigeria' UNION ALL
        SELECT 182102, 'Dunari','Sub-District','Nigeria' UNION ALL
        SELECT 204002, 'Dunbulum','Sub-District','Nigeria' UNION ALL
        SELECT 342103, 'Dundaye','Sub-District','Nigeria' UNION ALL
        SELECT 180603, 'Dundubus','Sub-District','Nigeria' UNION ALL
        SELECT 200105, 'Dundun','Sub-District','Nigeria' UNION ALL
        SELECT 213102, 'Dungum Muazu','Sub-District','Nigeria' UNION ALL
        SELECT 421404, 'Dunkurmi','Sub-District','Nigeria' UNION ALL
        SELECT 202301, 'Durba','Sub-District','Nigeria' UNION ALL
        SELECT 341103, 'Durbawa','Sub-District','Nigeria' UNION ALL
        SELECT 203702, 'Durbunde','Sub-District','Nigeria' UNION ALL
        SELECT 202902, 'Durma','Sub-District','Nigeria' UNION ALL
        SELECT 200405, 'Durmawa','Sub-District','Nigeria' UNION ALL
        SELECT 420609, 'Durr','Sub-District','Nigeria' UNION ALL
        SELECT 180604, 'Duru','Sub-District','Nigeria' UNION ALL
        SELECT 202002, 'Durun','Sub-District','Nigeria' UNION ALL
        SELECT 431303, 'Dusuman','Sub-District','Nigeria' UNION ALL
        SELECT 420307, 'Dutsen  Lawan','Sub-District','Nigeria' UNION ALL
        SELECT 192302, 'Dutsen Abba','Sub-District','Nigeria' UNION ALL
        SELECT 203502, 'Dutsen Bakoshi','Sub-District','Nigeria' UNION ALL
        SELECT 211702, 'Dutsen Kura','Sub-District','Nigeria' UNION ALL
        SELECT 191503, 'Dutsen Wai','Sub-District','Nigeria' UNION ALL
        SELECT 211102, 'Dutsi A','Sub-District','Nigeria' UNION ALL
        SELECT 211103, 'Dutsi B','Sub-District','Nigeria' UNION ALL
        SELECT 211203, 'Dutsinma A','Sub-District','Nigeria' UNION ALL
        SELECT 211204, 'Dutsinma B','Sub-District','Nigeria' UNION ALL
        SELECT 212603, 'Duwan/Makau','Sub-District','Nigeria' UNION ALL
        SELECT 221203, 'Etene','Sub-District','Nigeria' UNION ALL
        SELECT 203703, 'F Alali','Sub-District','Nigeria' UNION ALL
        SELECT 190604, 'Fada (Jaba)','Sub-District','Nigeria' UNION ALL
        SELECT 191303, 'Fada (Kaura)','Sub-District','Nigeria' UNION ALL
        SELECT 221604, 'Fada (Sakaba)','Sub-District','Nigeria' UNION ALL
        SELECT 211602, 'Fafaru','Sub-District','Nigeria' UNION ALL
        SELECT 341805, 'Faga/Alasan','Sub-District','Nigeria' UNION ALL
        SELECT 420404, 'Fagam (Damban)','Sub-District','Nigeria' UNION ALL
        SELECT 181103, 'Fagam (Gwaram)','Sub-District','Nigeria' UNION ALL
        SELECT 420405, 'Fagarau','Sub-District','Nigeria' UNION ALL
        SELECT 201201, 'Fagge A','Sub-District','Nigeria' UNION ALL
        SELECT 201202, 'Fagge B','Sub-District','Nigeria' UNION ALL
        SELECT 201203, 'Fagge C','Sub-District','Nigeria' UNION ALL
        SELECT 201204, 'Fagge D1','Sub-District','Nigeria' UNION ALL
        SELECT 201205, 'Fagge D2','Sub-District','Nigeria' UNION ALL
        SELECT 421608, 'Faggo A','Sub-District','Nigeria' UNION ALL
        SELECT 421609, 'Faggo B','Sub-District','Nigeria' UNION ALL
        SELECT 180405, 'Fagi','Sub-District','Nigeria' UNION ALL
        SELECT 213303, 'Fago ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213304, 'Fago ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 200503, 'Fagolo','Sub-District','Nigeria' UNION ALL
        SELECT 420903, 'Faguji','Sub-District','Nigeria' UNION ALL
        SELECT 200804, 'Fagwalawa','Sub-District','Nigeria' UNION ALL
        SELECT 190605, 'Fai','Sub-District','Nigeria' UNION ALL
        SELECT 340303, 'Fajaldu','Sub-District','Nigeria' UNION ALL
        SELECT 203704, 'Fajewa','Sub-District','Nigeria' UNION ALL
        SELECT 361002, 'Fajiganari','Sub-District','Nigeria' UNION ALL
        SELECT 220904, 'Fakai\ Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 181903, 'Fake','Sub-District','Nigeria' UNION ALL
        SELECT 342306, 'Fakka','Sub-District','Nigeria' UNION ALL
        SELECT 341001, 'Fakku','Sub-District','Nigeria' UNION ALL
        SELECT 212001, 'Fakuwa /Kafin Dangi','Sub-District','Nigeria' UNION ALL
        SELECT 370604, 'Falale','Sub-District','Nigeria' UNION ALL
        SELECT 220203, 'Falde','Sub-District','Nigeria' UNION ALL
        SELECT 180504, 'Falgeri','Sub-District','Nigeria' UNION ALL
        SELECT 201104, 'Falgore (Doguwa)','Sub-District','Nigeria' UNION ALL
        SELECT 203402, 'Falgore (Rogo)','Sub-District','Nigeria' UNION ALL
        SELECT 361104, 'Falimaram','Sub-District','Nigeria' UNION ALL
        SELECT 202302, 'Fammar','Sub-District','Nigeria' UNION ALL
        SELECT 220804, 'Fana','Sub-District','Nigeria' UNION ALL
        SELECT 200205, 'Fanda','Sub-District','Nigeria' UNION ALL
        SELECT 181803, 'Fandum','Sub-District','Nigeria' UNION ALL
        SELECT 204202, 'Fanisau','Sub-District','Nigeria' UNION ALL
        SELECT 201504, 'Fankurun','Sub-District','Nigeria' UNION ALL
        SELECT 190403, 'Fanshanu','Sub-District','Nigeria' UNION ALL
        SELECT 182404, 'Fara Barije','Sub-District','Nigeria' UNION ALL
        SELECT 200206, 'Faragai','Sub-District','Nigeria' UNION ALL
        SELECT 213002, 'Fardami','Sub-District','Nigeria' UNION ALL
        SELECT 181104, 'Farin Dutse','Sub-District','Nigeria' UNION ALL
        SELECT 211603, 'Faru','Sub-District','Nigeria' UNION ALL
        SELECT 370903, 'Faru/Magami','Sub-District','Nigeria' UNION ALL
        SELECT 203705, 'Farun Ruwa','Sub-District','Nigeria' UNION ALL
        SELECT 203503, 'Faruruwa','Sub-District','Nigeria' UNION ALL
        SELECT 211302, 'Faskari (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 210404, 'Faski/Kagara','Sub-District','Nigeria' UNION ALL
        SELECT 202303, 'Fassi','Sub-District','Nigeria' UNION ALL
        SELECT 182103, 'Fataika','Sub-District','Nigeria' UNION ALL
        SELECT 430903, 'Felo','Sub-District','Nigeria' UNION ALL
        SELECT 220204, 'Feske','Sub-District','Nigeria' UNION ALL
        SELECT 432104, 'Fezzan','Sub-District','Nigeria' UNION ALL
        SELECT 360401, 'Fika Anze','Sub-District','Nigeria' UNION ALL
        SELECT 430403, 'Fikhayel','Sub-District','Nigeria' UNION ALL
        SELECT 220303, 'Filande','Sub-District','Nigeria' UNION ALL
        SELECT 181204, 'Firji','Sub-District','Nigeria' UNION ALL
        SELECT 430104, 'Foguwa','Sub-District','Nigeria' UNION ALL
        SELECT 431405, 'Foi','Sub-District','Nigeria' UNION ALL
        SELECT 360605, 'Fukurti','Sub-District','Nigeria' UNION ALL
        SELECT 182003, 'Fulata','Sub-District','Nigeria' UNION ALL
        SELECT 203403, 'Fulatan','Sub-District','Nigeria' UNION ALL
        SELECT 342003, 'Fura Girke','Sub-District','Nigeria' UNION ALL
        SELECT 370505, 'Furfuri/Kwakwa','Sub-District','Nigeria' UNION ALL
        SELECT 432004, 'Furram','Sub-District','Nigeria' UNION ALL
        SELECT 360606, 'Futchimiram','Sub-District','Nigeria' UNION ALL
        SELECT 420105, 'Futuk East','Sub-District','Nigeria' UNION ALL
        SELECT 420106, 'Futuk West','Sub-District','Nigeria' UNION ALL
        SELECT 432501, 'Fuye','Sub-District','Nigeria' UNION ALL
        SELECT 342104, 'G/Bubu','Sub-District','Nigeria' UNION ALL
        SELECT 342105, 'G/Hamidu','Sub-District','Nigeria' UNION ALL
        SELECT 360805, 'Gabai','Sub-District','Nigeria' UNION ALL
        SELECT 370803, 'Gabake','Sub-District','Nigeria' UNION ALL
        SELECT 421904, 'Gabanga A','Sub-District','Nigeria' UNION ALL
        SELECT 421905, 'Gabanga B','Sub-District','Nigeria' UNION ALL
        SELECT 420503, 'Gabarin East','Sub-District','Nigeria' UNION ALL
        SELECT 420504, 'Gabarin West','Sub-District','Nigeria' UNION ALL
        SELECT 212103, 'Gabas 1','Sub-District','Nigeria' UNION ALL
        SELECT 212104, 'Gabas 2','Sub-District','Nigeria' UNION ALL
        SELECT 212105, 'Gabas 3','Sub-District','Nigeria' UNION ALL
        SELECT 201301, 'Gabasawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420505, 'Gabchiyari','Sub-District','Nigeria' UNION ALL
        SELECT 212002, 'Gachi','Sub-District','Nigeria' UNION ALL
        SELECT 181705, 'Gada (Kazaure)','Sub-District','Nigeria' UNION ALL
        SELECT 340402, 'Gada (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370506, 'Gada/Karakkai','Sub-District','Nigeria' UNION ALL
        SELECT 422004, 'Gadai','Sub-District','Nigeria' UNION ALL
        SELECT 432604, 'Gadai Sub-District','Sub-District','Nigeria' UNION ALL
        SELECT 360402, 'Gadaka Shembire','Sub-District','Nigeria' UNION ALL
        SELECT 200303, 'Gadanya','Sub-District','Nigeria' UNION ALL
        SELECT 421007, 'Gadau','Sub-District','Nigeria' UNION ALL
        SELECT 420702, 'Gadiya','Sub-District','Nigeria' UNION ALL
        SELECT 200605, 'Gafan','Sub-District','Nigeria' UNION ALL
        SELECT 221502, 'Gafara','Sub-District','Nigeria' UNION ALL
        SELECT 200106, 'Gafasa','Sub-District','Nigeria' UNION ALL
        SELECT 181503, 'Gafaya','Sub-District','Nigeria' UNION ALL
        SELECT 211805, 'Gafiya','Sub-District','Nigeria' UNION ALL
        SELECT 200207, 'Gagarame','Sub-District','Nigeria' UNION ALL
        SELECT 180701, 'Gagarawa Gari','Sub-District','Nigeria' UNION ALL
        SELECT 180702, 'Gagarawa Tasha','Sub-District','Nigeria' UNION ALL
        SELECT 341701, 'Gagi A','Sub-District','Nigeria' UNION ALL
        SELECT 341702, 'Gagi B','Sub-District','Nigeria' UNION ALL
        SELECT 341703, 'Gagi C','Sub-District','Nigeria' UNION ALL
        SELECT 421610, 'Gagidiba','Sub-District','Nigeria' UNION ALL
        SELECT 181303, 'Gagulmari','Sub-District','Nigeria' UNION ALL
        SELECT 360806, 'Gagure','Sub-District','Nigeria' UNION ALL
        SELECT 210505, 'Gaiwa','Sub-District','Nigeria' UNION ALL
        SELECT 430804, 'Gajibo','Sub-District','Nigeria' UNION ALL
        SELECT 203903, 'Gajida','Sub-District','Nigeria' UNION ALL
        SELECT 432605, 'Gajiram','Sub-District','Nigeria' UNION ALL
        SELECT 203601, 'Gala','Sub-District','Nigeria' UNION ALL
        SELECT 201804, 'Galadanchi','Sub-District','Nigeria' UNION ALL
        SELECT 182004, 'Galadi (Maigatari)','Sub-District','Nigeria' UNION ALL
        SELECT 371103, 'Galadi (Shinkafi)','Sub-District','Nigeria' UNION ALL
        SELECT 220304, 'Galadima','Sub-District','Nigeria' UNION ALL
        SELECT 212003, 'Galadima ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 212004, 'Galadima ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 370804, 'Galadima Dan Galadima','Sub-District','Nigeria' UNION ALL
        SELECT 370104, 'Galadima-Ank','Sub-District','Nigeria' UNION ALL
        SELECT 370701, 'Galadima-Gus','Sub-District','Nigeria' UNION ALL
        SELECT 371201, 'Galadima-Tma','Sub-District','Nigeria' UNION ALL
        SELECT 190302, 'Galadimawa (Giwa)','Sub-District','Nigeria' UNION ALL
        SELECT 202408, 'Galadimawa (Kiru)','Sub-District','Nigeria' UNION ALL
        SELECT 180905, 'Galagamma','Sub-District','Nigeria' UNION ALL
        SELECT 420208, 'Galambi','Sub-District','Nigeria' UNION ALL
        SELECT 431406, 'Galangi','Sub-District','Nigeria' UNION ALL
        SELECT 430503, 'Galdimari (Biu)','Sub-District','Nigeria' UNION ALL
        SELECT 421104, 'Galdimari (Jama''Are)','Sub-District','Nigeria' UNION ALL
        SELECT 432005, 'Galiganna','Sub-District','Nigeria' UNION ALL
        SELECT 202803, 'Galinja','Sub-District','Nigeria' UNION ALL
        SELECT 212704, 'Gallu','Sub-District','Nigeria' UNION ALL
        SELECT 431304, 'Galtimari','Sub-District','Nigeria' UNION ALL
        SELECT 203102, 'Gama','Sub-District','Nigeria' UNION ALL
        SELECT 192102, 'Gama Gira','Sub-District','Nigeria' UNION ALL
        SELECT 201901, 'Gama''A','Sub-District','Nigeria' UNION ALL
        SELECT 430404, 'Gamadadi','Sub-District','Nigeria' UNION ALL
        SELECT 180105, 'Gamafoi','Sub-District','Nigeria' UNION ALL
        SELECT 201602, 'Gamarya','Sub-District','Nigeria' UNION ALL
        SELECT 420703, 'Gamawa North','Sub-District','Nigeria' UNION ALL
        SELECT 420704, 'Gamawa South','Sub-District','Nigeria' UNION ALL
        SELECT 430904, 'Gamawo','Sub-District','Nigeria' UNION ALL
        SELECT 421207, 'Gambaki','Sub-District','Nigeria' UNION ALL
        SELECT 420308, 'Gambar','Sub-District','Nigeria' UNION ALL
        SELECT 360304, 'Gambir / Moduri','Sub-District','Nigeria' UNION ALL
        SELECT 432105, 'Gamboru','Sub-District','Nigeria' UNION ALL
        SELECT 432502, 'Gamboru A','Sub-District','Nigeria' UNION ALL
        SELECT 432503, 'Gamboru B','Sub-District','Nigeria' UNION ALL
        SELECT 432504, 'Gamboru C','Sub-District','Nigeria' UNION ALL
        SELECT 213103, 'Gamji','Sub-District','Nigeria' UNION ALL
        SELECT 202003, 'Gamma','Sub-District','Nigeria' UNION ALL
        SELECT 370605, 'Gamo','Sub-District','Nigeria' UNION ALL
        SELECT 201603, 'Gamoji','Sub-District','Nigeria' UNION ALL
        SELECT 180106, 'Gamsarka','Sub-District','Nigeria' UNION ALL
        SELECT 211703, 'Gamzago','Sub-District','Nigeria' UNION ALL
        SELECT 212705, 'Gana Jigawa','Sub-District','Nigeria' UNION ALL
        SELECT 341501, 'Gande','Sub-District','Nigeria' UNION ALL
        SELECT 341201, 'Gandi I','Sub-District','Nigeria' UNION ALL
        SELECT 341202, 'Gandi Ii','Sub-District','Nigeria' UNION ALL
        SELECT 201005, 'Ganduje','Sub-District','Nigeria' UNION ALL
        SELECT 202103, 'Gandun Albasa','Sub-District','Nigeria' UNION ALL
        SELECT 341104, 'Gandun Modibbo','Sub-District','Nigeria' UNION ALL
        SELECT 203002, 'Gandurwawa','Sub-District','Nigeria' UNION ALL
        SELECT 421208, 'Gangai','Sub-District','Nigeria' UNION ALL
        SELECT 341402, 'Gangan','Sub-District','Nigeria' UNION ALL
        SELECT 190303, 'Gangara (Giwa)','Sub-District','Nigeria' UNION ALL
        SELECT 211604, 'Gangara (Jibia)','Sub-District','Nigeria' UNION ALL
        SELECT 341301, 'Gangara (Sabon Birni)','Sub-District','Nigeria' UNION ALL
        SELECT 181402, 'Gangawa','Sub-District','Nigeria' UNION ALL
        SELECT 203602, 'Gani','Sub-District','Nigeria' UNION ALL
        SELECT 420801, 'Ganjuwa A','Sub-District','Nigeria' UNION ALL
        SELECT 420802, 'Ganjuwa B','Sub-District','Nigeria' UNION ALL
        SELECT 200906, 'Gano','Sub-District','Nigeria' UNION ALL
        SELECT 180505, 'Gantsa','Sub-District','Nigeria' UNION ALL
        SELECT 210604, 'Ganuwa','Sub-District','Nigeria' UNION ALL
        SELECT 420107, 'Gar','Sub-District','Nigeria' UNION ALL
        SELECT 181004, 'Garbagar','Sub-District','Nigeria' UNION ALL
        SELECT 361306, 'Garbi','Sub-District','Nigeria' UNION ALL
        SELECT 182202, 'Garbo','Sub-District','Nigeria' UNION ALL
        SELECT 203603, 'Garfa','Sub-District','Nigeria' UNION ALL
        SELECT 200406, 'Gargai','Sub-District','Nigeria' UNION ALL
        SELECT 201006, 'Gargari','Sub-District','Nigeria' UNION ALL
        SELECT 420406, 'Gargawa','Sub-District','Nigeria' UNION ALL
        SELECT 201402, 'Garin Ali','Sub-District','Nigeria' UNION ALL
        SELECT 180703, 'Garin Chiroma','Sub-District','Nigeria' UNION ALL
        SELECT 204303, 'Garin Dau','Sub-District','Nigeria' UNION ALL
        SELECT 180906, 'Garin Gambo','Sub-District','Nigeria' UNION ALL
        SELECT 361003, 'Garin Gawo','Sub-District','Nigeria' UNION ALL
        SELECT 360807, 'Garintuwo','Sub-District','Nigeria' UNION ALL
        SELECT 222002, 'Garkar Sarki','Sub-District','Nigeria' UNION ALL
        SELECT 210405, 'Garki (Baure)','Sub-District','Nigeria' UNION ALL
        SELECT 180803, 'Garki (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 181904, 'Garko (Kiyawa)','Sub-District','Nigeria' UNION ALL
        SELECT 201403, 'Garko (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 213402, 'Garni','Sub-District','Nigeria' UNION ALL
        SELECT 202004, 'Garo','Sub-District','Nigeria' UNION ALL
        SELECT 180204, 'Garu (Babura)','Sub-District','Nigeria' UNION ALL
        SELECT 430601, 'Garu (Chibok)','Sub-District','Nigeria' UNION ALL
        SELECT 360403, 'Garu (Fika)','Sub-District','Nigeria' UNION ALL
        SELECT 340805, 'Garu (Illela)','Sub-District','Nigeria' UNION ALL
        SELECT 191602, 'Garu (Kudan)','Sub-District','Nigeria' UNION ALL
        SELECT 212903, 'Garu (Musawa)','Sub-District','Nigeria' UNION ALL
        SELECT 192103, 'Garu (Soba)','Sub-District','Nigeria' UNION ALL
        SELECT 191703, 'Garu/Mariri','Sub-District','Nigeria' UNION ALL
        SELECT 430504, 'Garubula','Sub-District','Nigeria' UNION ALL
        SELECT 201505, 'Garun Babba','Sub-District','Nigeria' UNION ALL
        SELECT 201302, 'Garun Danga','Sub-District','Nigeria' UNION ALL
        SELECT 182104, 'Garun Gabas','Sub-District','Nigeria' UNION ALL
        SELECT 201506, 'Garun Malam (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 202602, 'Garun Sheme','Sub-District','Nigeria' UNION ALL
        SELECT 420407, 'Garuza','Sub-District','Nigeria' UNION ALL
        SELECT 180205, 'Gasakoli','Sub-District','Nigeria' UNION ALL
        SELECT 432306, 'Gashigar','Sub-District','Nigeria' UNION ALL
        SELECT 432703, 'Gasi','Sub-District','Nigeria' UNION ALL
        SELECT 361004, 'Gasma','Sub-District','Nigeria' UNION ALL
        SELECT 180107, 'Gatafa','Sub-District','Nigeria' UNION ALL
        SELECT 430602, 'Gatamarwa','Sub-District','Nigeria' UNION ALL
        SELECT 341302, 'Gatawa','Sub-District','Nigeria' UNION ALL
        SELECT 341502, 'Gaukai','Sub-District','Nigeria' UNION ALL
        SELECT 181403, 'Gauza','Sub-District','Nigeria' UNION ALL
        SELECT 431105, 'Gavva Agapalwa','Sub-District','Nigeria' UNION ALL
        SELECT 431902, 'Gawa','Sub-District','Nigeria' UNION ALL
        SELECT 220603, 'Gawassu','Sub-District','Nigeria' UNION ALL
        SELECT 340103, 'Gawazai','Sub-District','Nigeria' UNION ALL
        SELECT 201702, 'Gawo','Sub-District','Nigeria' UNION ALL
        SELECT 203103, 'Gawuna','Sub-District','Nigeria' UNION ALL
        SELECT 201604, 'Gaya Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 201605, 'Gaya Kudu','Sub-District','Nigeria' UNION ALL
        SELECT 190103, 'Gayam','Sub-District','Nigeria' UNION ALL
        SELECT 370606, 'Gayari','Sub-District','Nigeria' UNION ALL
        SELECT 204203, 'Gayawa','Sub-District','Nigeria' UNION ALL
        SELECT 181804, 'Gayin','Sub-District','Nigeria' UNION ALL
        SELECT 430905, 'Gazaburi','Sub-District','Nigeria' UNION ALL
        SELECT 191803, 'Gazara','Sub-District','Nigeria' UNION ALL
        SELECT 213104, 'Gazari','Sub-District','Nigeria' UNION ALL
        SELECT 221703, 'Gebbe','Sub-District','Nigeria' UNION ALL
        SELECT 340902, 'Gebe A','Sub-District','Nigeria' UNION ALL
        SELECT 340903, 'Gebe B','Sub-District','Nigeria' UNION ALL
        SELECT 203604, 'Gediya','Sub-District','Nigeria' UNION ALL
        SELECT 340304, 'Geere-Gajara','Sub-District','Nigeria' UNION ALL
        SELECT 221605, 'Gelwasa','Sub-District','Nigeria' UNION ALL
        SELECT 191405, 'Geshere','Sub-District','Nigeria' UNION ALL
        SELECT 201902, 'Getso','Sub-District','Nigeria' UNION ALL
        SELECT 220805, 'Geza','Sub-District','Nigeria' UNION ALL
        SELECT 201703, 'Gezawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221503, 'Gidan Baka','Sub-District','Nigeria' UNION ALL
        SELECT 370904, 'Gidan Goga','Sub-District','Nigeria' UNION ALL
        SELECT 340806, 'Gidan Hamma','Sub-District','Nigeria' UNION ALL
        SELECT 192201, 'Gidan Jatau','Sub-District','Nigeria' UNION ALL
        SELECT 342004, 'Gidan Kare','Sub-District','Nigeria' UNION ALL
        SELECT 340807, 'Gidan Katta','Sub-District','Nigeria' UNION ALL
        SELECT 340704, 'Gidan Kaya','Sub-District','Nigeria' UNION ALL
        SELECT 341901, 'Gidan Madi','Sub-District','Nigeria' UNION ALL
        SELECT 341105, 'Gidan Rugga/More','Sub-District','Nigeria' UNION ALL
        SELECT 190806, 'Gidan Tagwai','Sub-District','Nigeria' UNION ALL
        SELECT 190704, 'Gidan Waya','Sub-District','Nigeria' UNION ALL
        SELECT 420904, 'Gidea A','Sub-District','Nigeria' UNION ALL
        SELECT 420905, 'Gidea B','Sub-District','Nigeria' UNION ALL
        SELECT 221402, 'Gidiga','Sub-District','Nigeria' UNION ALL
        SELECT 340705, 'Gigane','Sub-District','Nigeria' UNION ALL
        SELECT 203104, 'Giginyu','Sub-District','Nigeria' UNION ALL
        SELECT 421008, 'Gijina','Sub-District','Nigeria' UNION ALL
        SELECT 340403, 'Gilbadi','Sub-District','Nigeria' UNION ALL
        SELECT 192104, 'Gimba','Sub-District','Nigeria' UNION ALL
        SELECT 191804, 'Gimi','Sub-District','Nigeria' UNION ALL
        SELECT 221104, 'Gindi/Kyarmi','Sub-District','Nigeria' UNION ALL
        SELECT 221807, 'Ginga','Sub-District','Nigeria' UNION ALL
        SELECT 212904, 'Gingin','Sub-District','Nigeria' UNION ALL
        SELECT 203904, 'Ginsawa','Sub-District','Nigeria' UNION ALL
        SELECT 181605, 'Girbobo','Sub-District','Nigeria' UNION ALL
        SELECT 210506, 'Giremawa','Sub-District','Nigeria' UNION ALL
        SELECT 360903, 'Girgir/ Bayam','Sub-District','Nigeria' UNION ALL
        SELECT 211806, 'Girka','Sub-District','Nigeria' UNION ALL
        SELECT 341002, 'Girkau','Sub-District','Nigeria' UNION ALL
        SELECT 221808, 'Giro','Sub-District','Nigeria' UNION ALL
        SELECT 190304, 'Giwa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221403, 'Giwatazo','Sub-District','Nigeria' UNION ALL
        SELECT 340503, 'Giyawa','Sub-District','Nigeria' UNION ALL
        SELECT 420309, 'Gobbiya','Sub-District','Nigeria' UNION ALL
        SELECT 200705, 'Gobirawa','Sub-District','Nigeria' UNION ALL
        SELECT 202005, 'Godiya','Sub-District','Nigeria' UNION ALL
        SELECT 190705, 'Godo-Godo','Sub-District','Nigeria' UNION ALL
        SELECT 360904, 'Gogaram','Sub-District','Nigeria' UNION ALL
        SELECT 204304, 'Gogel','Sub-District','Nigeria' UNION ALL
        SELECT 200304, 'Gogori','Sub-District','Nigeria' UNION ALL
        SELECT 420705, 'Gololo North','Sub-District','Nigeria' UNION ALL
        SELECT 420706, 'Gololo South','Sub-District','Nigeria' UNION ALL
        SELECT 431305, 'Gomari','Sub-District','Nigeria' UNION ALL
        SELECT 431306, 'Gongulong','Sub-District','Nigeria' UNION ALL
        SELECT 430307, 'Goniri (Bama)','Sub-District','Nigeria' UNION ALL
        SELECT 360704, 'Goniri (Gujba)','Sub-District','Nigeria' UNION ALL
        SELECT 192202, 'Gora  Sub-District','Sub-District','Nigeria' UNION ALL
        SELECT 370303, 'Gora (Birnin Magaji/Kiyaw)','Sub-District','Nigeria' UNION ALL
        SELECT 202804, 'Gora (Madobi)','Sub-District','Nigeria' UNION ALL
        SELECT 182405, 'Gora (Roni)','Sub-District','Nigeria' UNION ALL
        SELECT 432704, 'Gora (Shani)','Sub-District','Nigeria' UNION ALL
        SELECT 212504, 'Gora Dansaka','Sub-District','Nigeria' UNION ALL
        SELECT 370905, 'Gora/Namaye','Sub-District','Nigeria' UNION ALL
        SELECT 203504, 'Goron Du Tse','Sub-District','Nigeria' UNION ALL
        SELECT 201805, 'Goron Dutse','Sub-District','Nigeria' UNION ALL
        SELECT 200805, 'Goron Maje','Sub-District','Nigeria' UNION ALL
        SELECT 340504, 'Goronyo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 220205, 'Gorun Dikko','Sub-District','Nigeria' UNION ALL
        SELECT 431106, 'Goshe','Sub-District','Nigeria' UNION ALL
        SELECT 360705, 'Gotala Gotumba','Sub-District','Nigeria' UNION ALL
        SELECT 211405, 'Goya','Sub-District','Nigeria' UNION ALL
        SELECT 211704, 'Gozaki','Sub-District','Nigeria' UNION ALL
        SELECT 204003, 'Gozarki','Sub-District','Nigeria' UNION ALL
        SELECT 431202, 'Grim/Damch','Sub-District','Nigeria' UNION ALL
        SELECT 360204, 'Guba/Dapso','Sub-District','Nigeria' UNION ALL
        SELECT 430906, 'Gubio I','Sub-District','Nigeria' UNION ALL
        SELECT 430907, 'Gubio Ii','Sub-District','Nigeria' UNION ALL
        SELECT 191805, 'Gubuchi','Sub-District','Nigeria' UNION ALL
        SELECT 221404, 'Gubunkure','Sub-District','Nigeria' UNION ALL
        SELECT 421506, 'Guda','Sub-District','Nigeria' UNION ALL
        SELECT 202006, 'Gude','Sub-District','Nigeria' UNION ALL
        SELECT 360404, 'Gudi Dozi','Sub-District','Nigeria' UNION ALL
        SELECT 431107, 'Guduf A&B','Sub-District','Nigeria' UNION ALL
        SELECT 431002, 'Gudumbali E','Sub-District','Nigeria' UNION ALL
        SELECT 431003, 'Gudumbali W','Sub-District','Nigeria' UNION ALL
        SELECT 361503, 'Guduram','Sub-District','Nigeria' UNION ALL
        SELECT 210105, 'Guga','Sub-District','Nigeria' UNION ALL
        SELECT 421405, 'Gugulin','Sub-District','Nigeria' UNION ALL
        SELECT 360706, 'Gujba (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360205, 'Guji / Metalari','Sub-District','Nigeria' UNION ALL
        SELECT 182604, 'Gujungu','Sub-District','Nigeria' UNION ALL
        SELECT 360808, 'Gulani (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 220905, 'Gulbin Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 220305, 'Gulma','Sub-District','Nigeria' UNION ALL
        SELECT 221004, 'Gulmare','Sub-District','Nigeria' UNION ALL
        SELECT 203305, 'Gulu','Sub-District','Nigeria' UNION ALL
        SELECT 430308, 'Gulumba','Sub-District','Nigeria' UNION ALL
        SELECT 220604, 'Gulumbe','Sub-District','Nigeria' UNION ALL
        SELECT 422005, 'Gumai','Sub-District','Nigeria' UNION ALL
        SELECT 342106, 'Gumbi','Sub-District','Nigeria' UNION ALL
        SELECT 190807, 'Gumel (Kachia)','Sub-District','Nigeria' UNION ALL
        SELECT 432205, 'Gumna','Sub-District','Nigeria' UNION ALL
        SELECT 360607, 'Gumsa','Sub-District','Nigeria' UNION ALL
        SELECT 361702, 'Gumshi','Sub-District','Nigeria' UNION ALL
        SELECT 430706, 'Gumsuri','Sub-District','Nigeria' UNION ALL
        SELECT 220206, 'Gumunde /Rafin Tsaka','Sub-District','Nigeria' UNION ALL
        SELECT 430505, 'Gunda','Sub-District','Nigeria' UNION ALL
        SELECT 421406, 'Gundari','Sub-District','Nigeria' UNION ALL
        SELECT 211903, 'Gundawa','Sub-District','Nigeria' UNION ALL
        SELECT 202704, 'Gundutse','Sub-District','Nigeria' UNION ALL
        SELECT 420803, 'Gungura A','Sub-District','Nigeria' UNION ALL
        SELECT 420804, 'Gungura B','Sub-District','Nigeria' UNION ALL
        SELECT 181404, 'Gunka','Sub-District','Nigeria' UNION ALL
        SELECT 181205, 'Guntai','Sub-District','Nigeria' UNION ALL
        SELECT 430506, 'Gur','Sub-District','Nigeria' UNION ALL
        SELECT 211605, 'Gurbi (Jibia)','Sub-District','Nigeria' UNION ALL
        SELECT 211904, 'Gurbi (Kankara)','Sub-District','Nigeria' UNION ALL
        SELECT 200107, 'Gurduba','Sub-District','Nigeria' UNION ALL
        SELECT 191704, 'Gure/Kahugu','Sub-District','Nigeria' UNION ALL
        SELECT 181005, 'Guri (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420408, 'Guribana','Sub-District','Nigeria' UNION ALL
        SELECT 200606, 'Gurjiya (Bunkure)','Sub-District','Nigeria' UNION ALL
        SELECT 200907, 'Gurjiya (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
        SELECT 201404, 'Gurjiya (Garko)','Sub-District','Nigeria' UNION ALL
        SELECT 182704, 'Gurjiya (Yankwashi)','Sub-District','Nigeria' UNION ALL
        SELECT 204004, 'Gurun','Sub-District','Nigeria' UNION ALL
        SELECT 202505, 'Gurun Gawa','Sub-District','Nigeria' UNION ALL
        SELECT 370304, 'Gusami Gari','Sub-District','Nigeria' UNION ALL
        SELECT 370305, 'Gusami Hayi','Sub-District','Nigeria' UNION ALL
        SELECT 371202, 'Gusari/Garbadu','Sub-District','Nigeria' UNION ALL
        SELECT 180907, 'Gusau (Gumel)','Sub-District','Nigeria' UNION ALL
        SELECT 431802, 'Guwal','Sub-District','Nigeria' UNION ALL
        SELECT 431407, 'Guwo','Sub-District','Nigeria' UNION ALL
        SELECT 431004, 'Guworam','Sub-District','Nigeria' UNION ALL
        SELECT 361703, 'Guya','Sub-District','Nigeria' UNION ALL
        SELECT 421306, 'Guyaba','Sub-District','Nigeria' UNION ALL
        SELECT 431005, 'Guzamala E','Sub-District','Nigeria' UNION ALL
        SELECT 431006, 'Guzamala W','Sub-District','Nigeria' UNION ALL
        SELECT 340706, 'Gwadabawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 220605, 'Gwadangwaji','Sub-District','Nigeria' UNION ALL
        SELECT 220702, 'Gwade','Sub-District','Nigeria' UNION ALL
        SELECT 341203, 'Gwadodi/Gidan Buwai','Sub-District','Nigeria' UNION ALL
        SELECT 190202, 'Gwagwada','Sub-District','Nigeria' UNION ALL
        SELECT 203105, 'Gwagwarwa','Sub-District','Nigeria' UNION ALL
        SELECT 432705, 'Gwalasho','Sub-District','Nigeria' UNION ALL
        SELECT 201806, 'Gwale (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 342107, 'Gwamatse','Sub-District','Nigeria' UNION ALL
        SELECT 213403, 'Gwamba','Sub-District','Nigeria' UNION ALL
        SELECT 200607, 'Gwamma','Sub-District','Nigeria' UNION ALL
        SELECT 200706, 'Gwammaja','Sub-District','Nigeria' UNION ALL
        SELECT 420108, 'Gwana','Sub-District','Nigeria' UNION ALL
        SELECT 200806, 'Gwanda','Sub-District','Nigeria' UNION ALL
        SELECT 431803, 'Gwandi','Sub-District','Nigeria' UNION ALL
        SELECT 221005, 'Gwandu Dangaladima','Sub-District','Nigeria' UNION ALL
        SELECT 221006, 'Gwandu Marafa','Sub-District','Nigeria' UNION ALL
        SELECT 221905, 'Gwanfi/Kele','Sub-District','Nigeria' UNION ALL
        SELECT 432106, 'Gwange I','Sub-District','Nigeria' UNION ALL
        SELECT 432107, 'Gwange Ii','Sub-District','Nigeria' UNION ALL
        SELECT 432108, 'Gwange Iii','Sub-District','Nigeria' UNION ALL
        SELECT 203404, 'Gwangwan','Sub-District','Nigeria' UNION ALL
        SELECT 191806, 'Gwanki','Sub-District','Nigeria' UNION ALL
        SELECT 192005, 'Gwantu','Sub-District','Nigeria' UNION ALL
        SELECT 431203, 'Gwanzang','Sub-District','Nigeria' UNION ALL
        SELECT 200807, 'Gwarabtawa','Sub-District','Nigeria' UNION ALL
        SELECT 421009, 'Gwarai','Sub-District','Nigeria' UNION ALL
        SELECT 190404, 'Gwaraji','Sub-District','Nigeria' UNION ALL
        SELECT 421407, 'Gwaram (Misau)','Sub-District','Nigeria' UNION ALL
        SELECT 181105, 'Gwaram (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420109, 'Gwaram A','Sub-District','Nigeria' UNION ALL
        SELECT 420110, 'Gwaram B','Sub-District','Nigeria' UNION ALL
        SELECT 371203, 'Gwaram-Tma','Sub-District','Nigeria' UNION ALL
        SELECT 182203, 'Gwari','Sub-District','Nigeria' UNION ALL
        SELECT 212802, 'Gwarjo','Sub-District','Nigeria' UNION ALL
        SELECT 200407, 'Gwarmai (Bebeji)','Sub-District','Nigeria' UNION ALL
        SELECT 202603, 'Gwarmai (Kunchi)','Sub-District','Nigeria' UNION ALL
        SELECT 182705, 'Gwarta','Sub-District','Nigeria' UNION ALL
        SELECT 180804, 'Gwarzo (Garki)','Sub-District','Nigeria' UNION ALL
        SELECT 201903, 'Gwarzo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370403, 'Gwashi','Sub-District','Nigeria' UNION ALL
        SELECT 432706, 'Gwaskara','Sub-District','Nigeria' UNION ALL
        SELECT 420209, 'Gwaskwaram','Sub-District','Nigeria' UNION ALL
        SELECT 220306, 'Gwazange (Argungu)','Sub-District','Nigeria' UNION ALL
        SELECT 340605, 'Gwazange (Gudu)','Sub-District','Nigeria' UNION ALL
        SELECT 181206, 'Gwiwa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360103, 'Gwo Kura','Sub-District','Nigeria' UNION ALL
        SELECT 203804, 'Gyadi Gayadi Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 203805, 'Gyadi Gyadi Kudu','Sub-District','Nigeria' UNION ALL
        SELECT 370607, 'Gyalange','Sub-District','Nigeria' UNION ALL
        SELECT 420310, 'Gyara (Bogoro)','Sub-District','Nigeria' UNION ALL
        SELECT 421010, 'Gyara (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
        SELECT 201807, 'Gyaranya','Sub-District','Nigeria' UNION ALL
        SELECT 192303, 'Gyellesu','Sub-District','Nigeria' UNION ALL
        SELECT 432006, 'H/Chingua','Sub-District','Nigeria' UNION ALL
        SELECT 181606, 'Hadin','Sub-District','Nigeria' UNION ALL
        SELECT 431108, 'Hambagda L. Jaje','Sub-District','Nigeria' UNION ALL
        SELECT 212604, 'Hamcheta','Sub-District','Nigeria' UNION ALL
        SELECT 341106, 'Hamma''Ali','Sub-District','Nigeria' UNION ALL
        SELECT 180908, 'Hammado','Sub-District','Nigeria' UNION ALL
        SELECT 421105, 'Hanafari','Sub-District','Nigeria' UNION ALL
        SELECT 182204, 'Hantsu','Sub-District','Nigeria' UNION ALL
        SELECT 191905, 'Hanwa','Sub-District','Nigeria' UNION ALL
        SELECT 181405, 'Harbo Sabuwa','Sub-District','Nigeria' UNION ALL
        SELECT 181406, 'Harbo Tsohuwa','Sub-District','Nigeria' UNION ALL
        SELECT 421408, 'Hardawa','Sub-District','Nigeria' UNION ALL
        SELECT 420210, 'Hardo','Sub-District','Nigeria' UNION ALL
        SELECT 191504, 'Haskiya','Sub-District','Nigeria' UNION ALL
        SELECT 432109, 'Hausari (Maiduguri)','Sub-District','Nigeria' UNION ALL
        SELECT 361307, 'Hausari (Nguru)','Sub-District','Nigeria' UNION ALL
        SELECT 431109, 'Hausari Gaddamari','Sub-District','Nigeria' UNION ALL
        SELECT 360608, 'Hausari Sub-District','Sub-District','Nigeria' UNION ALL
        SELECT 430203, 'Hausari Z','Sub-District','Nigeria' UNION ALL
        SELECT 361407, 'Hausawa Asibiti','Sub-District','Nigeria' UNION ALL
        SELECT 202007, 'Hauwade','Sub-District','Nigeria' UNION ALL
        SELECT 190903, 'Hayin Banki','Sub-District','Nigeria' UNION ALL
        SELECT 221305, 'Herini/Madachi','Sub-District','Nigeria' UNION ALL
        SELECT 221105, 'Hirchin','Sub-District','Nigeria' UNION ALL
        SELECT 221204, 'Hirishi/Magarza','Sub-District','Nigeria' UNION ALL
        SELECT 431204, 'Hizhi/Bwala','Sub-District','Nigeria' UNION ALL
        SELECT 341403, 'Horo','Sub-District','Nigeria' UNION ALL
        SELECT 203806, 'Hotoro','Sub-District','Nigeria' UNION ALL
        SELECT 203106, 'Hotoro North','Sub-District','Nigeria' UNION ALL
        SELECT 203107, 'Hotoro South','Sub-District','Nigeria' UNION ALL
        SELECT 340707, 'Huchi','Sub-District','Nigeria' UNION ALL
        SELECT 210406, 'Hui','Sub-District','Nigeria' UNION ALL
        SELECT 200208, 'Hungu','Sub-District','Nigeria' UNION ALL
        SELECT 191603, 'Hunkuyi','Sub-District','Nigeria' UNION ALL
        SELECT 430204, 'Hussara/T','Sub-District','Nigeria' UNION ALL
        SELECT 181407, 'Idanduna','Sub-District','Nigeria' UNION ALL
        SELECT 190305, 'Idasu','Sub-District','Nigeria' UNION ALL
        SELECT 191102, 'Iddah','Sub-District','Nigeria' UNION ALL
        SELECT 191203, 'Idon','Sub-District','Nigeria' UNION ALL
        SELECT 190405, 'Igabi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 190502, 'Ikara (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 192203, 'Ikulu','Sub-District','Nigeria' UNION ALL
        SELECT 221306, 'Ilela/Sabon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 340808, 'Illela (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 220506, 'Illo/Sabon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 204305, 'Imawa','Sub-District','Nigeria' UNION ALL
        SELECT 211506, 'Ingawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 340104, 'Inname','Sub-District','Nigeria' UNION ALL
        SELECT 180206, 'Insharuwa','Sub-District','Nigeria' UNION ALL
        SELECT 340904, 'Isa North','Sub-District','Nigeria' UNION ALL
        SELECT 340905, 'Isa South','Sub-District','Nigeria' UNION ALL
        SELECT 420906, 'Isawa','Sub-District','Nigeria' UNION ALL
        SELECT 222104, 'Isgo Dago','Sub-District','Nigeria' UNION ALL
        SELECT 421011, 'Itas','Sub-District','Nigeria' UNION ALL
        SELECT 213003, 'Iyatawa','Sub-District','Nigeria' UNION ALL
        SELECT 360905, 'Jaba (Jakusko)','Sub-District','Nigeria' UNION ALL
        SELECT 181408, 'Jabarna','Sub-District','Nigeria' UNION ALL
        SELECT 181504, 'Jabbo','Sub-District','Nigeria' UNION ALL
        SELECT 341806, 'Jabo /Kagara','Sub-District','Nigeria' UNION ALL
        SELECT 430105, 'Jabullam','Sub-District','Nigeria' UNION ALL
        SELECT 221307, 'Jaddadi','Sub-District','Nigeria' UNION ALL
        SELECT 420707, 'Jadori','Sub-District','Nigeria' UNION ALL
        SELECT 181607, 'Jae','Sub-District','Nigeria' UNION ALL
        SELECT 190706, 'Jagindi','Sub-District','Nigeria' UNION ALL
        SELECT 181409, 'Jahun (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 203405, 'Jajaye','Sub-District','Nigeria' UNION ALL
        SELECT 360507, 'Jajere','Sub-District','Nigeria' UNION ALL
        SELECT 361005, 'Jajeri (Karasuwa)','Sub-District','Nigeria' UNION ALL
        SELECT 182005, 'Jajeri (Maigatari)','Sub-District','Nigeria' UNION ALL
        SELECT 361006, 'Jajimaji','Sub-District','Nigeria' UNION ALL
        SELECT 431604, 'Jakana','Sub-District','Nigeria' UNION ALL
        SELECT 202104, 'Jakara','Sub-District','Nigeria' UNION ALL
        SELECT 360906, 'Jakusko (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420409, 'Jalam','Sub-District','Nigeria' UNION ALL
        SELECT 201007, 'Jalli','Sub-District','Nigeria' UNION ALL
        SELECT 421801, 'Jama A','Sub-District','Nigeria' UNION ALL
        SELECT 191906, 'Jama''A','Sub-District','Nigeria' UNION ALL
        SELECT 421106, 'Jamaare A','Sub-District','Nigeria' UNION ALL
        SELECT 421107, 'Jamaare B','Sub-District','Nigeria' UNION ALL
        SELECT 421108, 'Jamaare C','Sub-District','Nigeria' UNION ALL
        SELECT 421109, 'Jamaare D','Sub-District','Nigeria' UNION ALL
        SELECT 340105, 'Jamali','Sub-District','Nigeria' UNION ALL
        SELECT 190503, 'Jampalan','Sub-District','Nigeria' UNION ALL
        SELECT 370906, 'Janbako','Sub-District','Nigeria' UNION ALL
        SELECT 221606, 'Janbirni','Sub-District','Nigeria' UNION ALL
        SELECT 420410, 'Janda','Sub-District','Nigeria' UNION ALL
        SELECT 204104, 'Jandutse','Sub-District','Nigeria' UNION ALL
        SELECT 221106, 'Jandutsi','Sub-District','Nigeria' UNION ALL
        SELECT 360405, 'Janga','Sub-District','Nigeria' UNION ALL
        SELECT 371204, 'Jangebe','Sub-District','Nigeria' UNION ALL
        SELECT 371104, 'Jangeru','Sub-District','Nigeria' UNION ALL
        SELECT 421507, 'Jangu','Sub-District','Nigeria' UNION ALL
        SELECT 203905, 'Janguza','Sub-District','Nigeria' UNION ALL
        SELECT 212605, 'Jani','Sub-District','Nigeria' UNION ALL
        SELECT 430405, 'Jara Dali','Sub-District','Nigeria' UNION ALL
        SELECT 430406, 'Jara Gol','Sub-District','Nigeria' UNION ALL
        SELECT 431502, 'Jarawa','Sub-District','Nigeria' UNION ALL
        SELECT 341404, 'Jaredi','Sub-District','Nigeria' UNION ALL
        SELECT 210106, 'Jargaba','Sub-District','Nigeria' UNION ALL
        SELECT 421409, 'Jarkasa','Sub-District','Nigeria' UNION ALL
        SELECT 203906, 'Jauben Kudu','Sub-District','Nigeria' UNION ALL
        SELECT 360206, 'Jawa Garun Dole','Sub-District','Nigeria' UNION ALL
        SELECT 360907, 'Jawur Katama','Sub-District','Nigeria' UNION ALL
        SELECT 361704, 'Jebuwa','Sub-District','Nigeria' UNION ALL
        SELECT 341503, 'Jekanadu','Sub-District','Nigeria' UNION ALL
        SELECT 182506, 'Jeke','Sub-District','Nigeria' UNION ALL
        SELECT 204306, 'Jemagu','Sub-District','Nigeria' UNION ALL
        SELECT 191103, 'Jere North','Sub-District','Nigeria' UNION ALL
        SELECT 191104, 'Jere South','Sub-District','Nigeria' UNION ALL
        SELECT 210904, 'Jiba','Sub-District','Nigeria' UNION ALL
        SELECT 210507, 'Jibawar Bade','Sub-District','Nigeria' UNION ALL
        SELECT 202903, 'Jibga','Sub-District','Nigeria' UNION ALL
        SELECT 211606, 'Jibia (A)','Sub-District','Nigeria' UNION ALL
        SELECT 211607, 'Jibia (B)','Sub-District','Nigeria' UNION ALL
        SELECT 200908, 'Jido','Sub-District','Nigeria' UNION ALL
        SELECT 220104, 'Jiga Birni','Sub-District','Nigeria' UNION ALL
        SELECT 220105, 'Jiga Makera','Sub-District','Nigeria' UNION ALL
        SELECT 432606, 'Jigalta','Sub-District','Nigeria' UNION ALL
        SELECT 180207, 'Jigawa (Babura)','Sub-District','Nigeria' UNION ALL
        SELECT 204307, 'Jigawa (Warawa)','Sub-District','Nigeria' UNION ALL
        SELECT 180605, 'Jigawar Tsada','Sub-District','Nigeria' UNION ALL
        SELECT 222003, 'Jijima','Sub-District','Nigeria' UNION ALL
        SELECT 212905, 'Jikamshi','Sub-District','Nigeria' UNION ALL
        SELECT 431503, 'Jilbe','Sub-District','Nigeria' UNION ALL
        SELECT 203306, 'Jili','Sub-District','Nigeria' UNION ALL
        SELECT 210207, 'Jino','Sub-District','Nigeria' UNION ALL
        SELECT 180805, 'Jirima','Sub-District','Nigeria' UNION ALL
        SELECT 204105, 'Jita','Sub-District','Nigeria' UNION ALL
        SELECT 201507, 'Jobawa','Sub-District','Nigeria' UNION ALL
        SELECT 201303, 'Joda','Sub-District','Nigeria' UNION ALL
        SELECT 201704, 'Jogana','Sub-District','Nigeria' UNION ALL
        SELECT 360609, 'Jororo','Sub-District','Nigeria' UNION ALL
        SELECT 420907, 'Jugudu','Sub-District','Nigeria' UNION ALL
        SELECT 360207, 'Juluri / Damnawa','Sub-District','Nigeria' UNION ALL
        SELECT 204308, 'Juma Galadima','Sub-District','Nigeria' UNION ALL
        SELECT 361504, 'Jumbam','Sub-District','Nigeria' UNION ALL
        SELECT 421110, 'Jurara','Sub-District','Nigeria' UNION ALL
        SELECT 191907, 'Jushi','Sub-District','Nigeria' UNION ALL
        SELECT 371305, 'K/Ganuwa','Sub-District','Nigeria' UNION ALL
        SELECT 204005, 'Kaba Giwa','Sub-District','Nigeria' UNION ALL
        SELECT 190904, 'Kabala','Sub-District','Nigeria' UNION ALL
        SELECT 341107, 'Kabanga','Sub-District','Nigeria' UNION ALL
        SELECT 202008, 'Kabo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 210107, 'Kabomo','Sub-District','Nigeria' UNION ALL
        SELECT 201808, 'Kabuga','Sub-District','Nigeria' UNION ALL
        SELECT 432206, 'Kabulawa','Sub-District','Nigeria' UNION ALL
        SELECT 200707, 'Kabuwaya','Sub-District','Nigeria' UNION ALL
        SELECT 203706, 'Kachako','Sub-District','Nigeria' UNION ALL
        SELECT 180406, 'Kachallari','Sub-District','Nigeria' UNION ALL
        SELECT 180606, 'Kachi','Sub-District','Nigeria' UNION ALL
        SELECT 190808, 'Kachia (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 340404, 'Kadadi','Sub-District','Nigeria' UNION ALL
        SELECT 203505, 'Kadamu','Sub-District','Nigeria' UNION ALL
        SELECT 202904, 'Kadan Dani','Sub-District','Nigeria' UNION ALL
        SELECT 213004, 'Kadandani','Sub-District','Nigeria' UNION ALL
        SELECT 191304, 'Kadarko','Sub-District','Nigeria' UNION ALL
        SELECT 340405, 'Kadassaka','Sub-District','Nigeria' UNION ALL
        SELECT 201508, 'Kadawa (Garun Malam)','Sub-District','Nigeria' UNION ALL
        SELECT 204204, 'Kadawa (Ungogo)','Sub-District','Nigeria' UNION ALL
        SELECT 340406, 'Kaddi','Sub-District','Nigeria' UNION ALL
        SELECT 201606, 'Kademi','Sub-District','Nigeria' UNION ALL
        SELECT 181006, 'Kadira','Sub-District','Nigeria' UNION ALL
        SELECT 430707, 'Kafa Mafi','Sub-District','Nigeria' UNION ALL
        SELECT 190707, 'Kafanchan A','Sub-District','Nigeria' UNION ALL
        SELECT 190708, 'Kafanchan A B','Sub-District','Nigeria' UNION ALL
        SELECT 212304, 'Kafarda','Sub-District','Nigeria' UNION ALL
        SELECT 340407, 'Kaffe','Sub-District','Nigeria' UNION ALL
        SELECT 422006, 'Kafin  Larabawa','Sub-District','Nigeria' UNION ALL
        SELECT 182303, 'Kafin Babushe','Sub-District','Nigeria' UNION ALL
        SELECT 202202, 'Kafin Dabga','Sub-District','Nigeria' UNION ALL
        SELECT 181505, 'Kafin Hausa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421307, 'Kafin Iya','Sub-District','Nigeria' UNION ALL
        SELECT 421209, 'Kafin Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 421508, 'Kafin Lemo','Sub-District','Nigeria' UNION ALL
        SELECT 420805, 'Kafin Madaki A','Sub-District','Nigeria' UNION ALL
        SELECT 420806, 'Kafin Madaki B','Sub-District','Nigeria' UNION ALL
        SELECT 201405, 'Kafin Malamai','Sub-District','Nigeria' UNION ALL
        SELECT 212005, 'Kafin Soli','Sub-District','Nigeria' UNION ALL
        SELECT 421410, 'Kafin Sule','Sub-District','Nigeria' UNION ALL
        SELECT 361605, 'Kafiya','Sub-District','Nigeria' UNION ALL
        SELECT 180108, 'Kafur (Auyo)','Sub-District','Nigeria' UNION ALL
        SELECT 211705, 'Kafur (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 340505, 'Kagara (Goronyo)','Sub-District','Nigeria' UNION ALL
        SELECT 370805, 'Kagara (Kaura Namoda)','Sub-District','Nigeria' UNION ALL
        SELECT 371205, 'Kagara-Tma','Sub-District','Nigeria' UNION ALL
        SELECT 213305, 'Kagare','Sub-District','Nigeria' UNION ALL
        SELECT 191105, 'Kagarko North','Sub-District','Nigeria' UNION ALL
        SELECT 191106, 'Kagarko South','Sub-District','Nigeria' UNION ALL
        SELECT 190709, 'Kagoma','Sub-District','Nigeria' UNION ALL
        SELECT 432402, 'Kaguram','Sub-District','Nigeria' UNION ALL
        SELECT 202304, 'Kahu','Sub-District','Nigeria' UNION ALL
        SELECT 210905, 'Kahuta A','Sub-District','Nigeria' UNION ALL
        SELECT 210906, 'Kahuta B','Sub-District','Nigeria' UNION ALL
        SELECT 212305, 'Kaikai','Sub-District','Nigeria' UNION ALL
        SELECT 211807, 'Kaita (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341405, 'Kajiji','Sub-District','Nigeria' UNION ALL
        SELECT 191204, 'Kajuru (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 190104, 'Kakangi (Birnin Gwari)','Sub-District','Nigeria' UNION ALL
        SELECT 190306, 'Kakangi (Giwa)','Sub-District','Nigeria' UNION ALL
        SELECT 190203, 'Kakau','Sub-District','Nigeria' UNION ALL
        SELECT 202805, 'Kakin Agur','Sub-District','Nigeria' UNION ALL
        SELECT 210108, 'Kakumi','Sub-District','Nigeria' UNION ALL
        SELECT 191003, 'Kakuri Gwari','Sub-District','Nigeria' UNION ALL
        SELECT 191004, 'Kakuri Hausa','Sub-District','Nigeria' UNION ALL
        SELECT 431504, 'Kala','Sub-District','Nigeria' UNION ALL
        SELECT 360305, 'Kalallawa / Gabai','Sub-District','Nigeria' UNION ALL
        SELECT 342108, 'Kalambaina','Sub-District','Nigeria' UNION ALL
        SELECT 341902, 'Kalanjeni','Sub-District','Nigeria' UNION ALL
        SELECT 181410, 'Kale','Sub-District','Nigeria' UNION ALL
        SELECT 341303, 'Kalgo (Sabon Birni)','Sub-District','Nigeria' UNION ALL
        SELECT 221205, 'Kalgo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360208, 'Kaliyari','Sub-District','Nigeria' UNION ALL
        SELECT 432007, 'Kalizorom','Sub-District','Nigeria' UNION ALL
        SELECT 191205, 'Kallah','Sub-District','Nigeria' UNION ALL
        SELECT 340809, 'Kalmalo','Sub-District','Nigeria' UNION ALL
        SELECT 361705, 'Kamaganam','Sub-District','Nigeria' UNION ALL
        SELECT 192204, 'Kamanton','Sub-District','Nigeria' UNION ALL
        SELECT 191406, 'Kamaru','Sub-District','Nigeria' UNION ALL
        SELECT 220806, 'Kamba Kamba','Sub-District','Nigeria' UNION ALL
        SELECT 341406, 'Kambama','Sub-District','Nigeria' UNION ALL
        SELECT 221007, 'Kambaza','Sub-District','Nigeria' UNION ALL
        SELECT 221504, 'Kambuwa','Sub-District','Nigeria' UNION ALL
        SELECT 210508, 'Kamri','Sub-District','Nigeria' UNION ALL
        SELECT 202105, 'Kan Karofi','Sub-District','Nigeria' UNION ALL
        SELECT 203605, 'Kanawa','Sub-District','Nigeria' UNION ALL
        SELECT 213404, 'Kanda','Sub-District','Nigeria' UNION ALL
        SELECT 210109, 'Kandarawa','Sub-District','Nigeria' UNION ALL
        SELECT 210305, 'Kandawa','Sub-District','Nigeria' UNION ALL
        SELECT 211507, 'Kandawa/Jobe','Sub-District','Nigeria' UNION ALL
        SELECT 420211, 'Kangere','Sub-District','Nigeria' UNION ALL
        SELECT 220906, 'Kangi','Sub-District','Nigeria' UNION ALL
        SELECT 180302, 'Kangire','Sub-District','Nigeria' UNION ALL
        SELECT 220207, 'Kangiwa','Sub-District','Nigeria' UNION ALL
        SELECT 190710, 'Kaninkon','Sub-District','Nigeria' UNION ALL
        SELECT 211905, 'Kankara (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 342109, 'Kanmata','Sub-District','Nigeria' UNION ALL
        SELECT 371006, 'Kanoma','Sub-District','Nigeria' UNION ALL
        SELECT 203003, 'Kantama','Sub-District','Nigeria' UNION ALL
        SELECT 181706, 'Kanti','Sub-District','Nigeria' UNION ALL
        SELECT 180303, 'Kantoga','Sub-District','Nigeria' UNION ALL
        SELECT 200708, 'Kantudu','Sub-District','Nigeria' UNION ALL
        SELECT 181411, 'Kanwa (Jahun)','Sub-District','Nigeria' UNION ALL
        SELECT 202009, 'Kanwa (Kabo)','Sub-District','Nigeria' UNION ALL
        SELECT 202806, 'Kanwa (Madobi)','Sub-District','Nigeria' UNION ALL
        SELECT 371404, 'Kanwa (Zurmi)','Sub-District','Nigeria' UNION ALL
        SELECT 180208, 'Kanya (Babura)','Sub-District','Nigeria' UNION ALL
        SELECT 180806, 'Kanya (Garki)','Sub-District','Nigeria' UNION ALL
        SELECT 221906, 'Kanya (Wasagu/Danko)','Sub-District','Nigeria' UNION ALL
        SELECT 220507, 'Kaoje/Gwamba','Sub-District','Nigeria' UNION ALL
        SELECT 201904, 'Kara','Sub-District','Nigeria' UNION ALL
        SELECT 212803, 'Karadua','Sub-District','Nigeria' UNION ALL
        SELECT 431408, 'Karagawaru','Sub-District','Nigeria' UNION ALL
        SELECT 180407, 'Karanga','Sub-District','Nigeria' UNION ALL
        SELECT 210306, 'Karare','Sub-District','Nigeria' UNION ALL
        SELECT 361007, 'Karasuwa G/Guna','Sub-District','Nigeria' UNION ALL
        SELECT 361008, 'Karasuwa Galu','Sub-District','Nigeria' UNION ALL
        SELECT 212706, 'Karau','Sub-District','Nigeria' UNION ALL
        SELECT 221405, 'Karaye (Maiyama)','Sub-District','Nigeria' UNION ALL
        SELECT 421707, 'Kardam A','Sub-District','Nigeria' UNION ALL
        SELECT 421708, 'Kardam B','Sub-District','Nigeria' UNION ALL
        SELECT 421709, 'Kardam C','Sub-District','Nigeria' UNION ALL
        SELECT 220606, 'Kardi','Sub-District','Nigeria' UNION ALL
        SELECT 204106, 'Karefa','Sub-District','Nigeria' UNION ALL
        SELECT 191505, 'Kareh','Sub-District','Nigeria' UNION ALL
        SELECT 432008, 'Kareram','Sub-District','Nigeria' UNION ALL
        SELECT 432307, 'Kareto','Sub-District','Nigeria' UNION ALL
        SELECT 340606, 'Karfen Chana','Sub-District','Nigeria' UNION ALL
        SELECT 340607, 'Karfensarki','Sub-District','Nigeria' UNION ALL
        SELECT 202705, 'Karfi (Kura)','Sub-District','Nigeria' UNION ALL
        SELECT 212505, 'Karfi (Malumfashi)','Sub-District','Nigeria' UNION ALL
        SELECT 203707, 'Karfi (Takai)','Sub-District','Nigeria' UNION ALL
        SELECT 191506, 'Kargi','Sub-District','Nigeria' UNION ALL
        SELECT 180807, 'Kargo','Sub-District','Nigeria' UNION ALL
        SELECT 213306, 'Karikarku','Sub-District','Nigeria' UNION ALL
        SELECT 420807, 'Kariya A','Sub-District','Nigeria' UNION ALL
        SELECT 420808, 'Kariya B','Sub-District','Nigeria' UNION ALL
        SELECT 182706, 'Karkarna','Sub-District','Nigeria' UNION ALL
        SELECT 201304, 'Karmami','Sub-District','Nigeria' UNION ALL
        SELECT 180607, 'Karnaya','Sub-District','Nigeria' UNION ALL
        SELECT 204205, 'Karo','Sub-District','Nigeria' UNION ALL
        SELECT 211205, 'Karofi A','Sub-District','Nigeria' UNION ALL
        SELECT 211206, 'Karofi B','Sub-District','Nigeria' UNION ALL
        SELECT 203307, 'Karofin Yashi','Sub-District','Nigeria' UNION ALL
        SELECT 182304, 'Karshi (Ringim)','Sub-District','Nigeria' UNION ALL
        SELECT 192006, 'Karshi (Sanga)','Sub-District','Nigeria' UNION ALL
        SELECT 220106, 'Kashin Zama','Sub-District','Nigeria' UNION ALL
        SELECT 421012, 'Kashuri','Sub-District','Nigeria' UNION ALL
        SELECT 430309, 'Kasugula','Sub-District','Nigeria' UNION ALL
        SELECT 191206, 'Kasuwan Magani','Sub-District','Nigeria' UNION ALL
        SELECT 421210, 'Kasuwar Kaji','Sub-District','Nigeria' UNION ALL
        SELECT 181304, 'Kasuwar Kofa','Sub-District','Nigeria' UNION ALL
        SELECT 181305, 'Kasuwar Kuda','Sub-District','Nigeria' UNION ALL
        SELECT 202604, 'Kasuwar Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 422007, 'Katagum (Zaki)','Sub-District','Nigeria' UNION ALL
        SELECT 341504, 'Katami North','Sub-District','Nigeria' UNION ALL
        SELECT 341505, 'Katami South','Sub-District','Nigeria' UNION ALL
        SELECT 221107, 'Katanga (Jega)','Sub-District','Nigeria' UNION ALL
        SELECT 181905, 'Katanga (Kiyawa)','Sub-District','Nigeria' UNION ALL
        SELECT 421906, 'Katanga (Warji)','Sub-District','Nigeria' UNION ALL
        SELECT 204309, 'Katar Kawa','Sub-District','Nigeria' UNION ALL
        SELECT 190809, 'Katari','Sub-District','Nigeria' UNION ALL
        SELECT 213307, 'Katsayal','Sub-District','Nigeria' UNION ALL
        SELECT 191107, 'Katugal','Sub-District','Nigeria' UNION ALL
        SELECT 181906, 'Katuka','Sub-District','Nigeria' UNION ALL
        SELECT 201406, 'Katumari','Sub-District','Nigeria' UNION ALL
        SELECT 371105, 'Katuru','Sub-District','Nigeria' UNION ALL
        SELECT 360104, 'Katuzu','Sub-District','Nigeria' UNION ALL
        SELECT 200504, 'Kau-Kau','Sub-District','Nigeria' UNION ALL
        SELECT 181608, 'Kaugama (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 191305, 'Kaura (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 342110, 'Kaura (Wamako)','Sub-District','Nigeria' UNION ALL
        SELECT 192304, 'Kaura (Zaria)','Sub-District','Nigeria' UNION ALL
        SELECT 203108, 'Kaura Goje','Sub-District','Nigeria' UNION ALL
        SELECT 202807, 'Kauran Mata','Sub-District','Nigeria' UNION ALL
        SELECT 191604, 'Kauran Wali North','Sub-District','Nigeria' UNION ALL
        SELECT 191605, 'Kauran Wali South','Sub-District','Nigeria' UNION ALL
        SELECT 340207, 'Kaurarmiyo/Mazangari/Jirga','Sub-District','Nigeria' UNION ALL
        SELECT 191407, 'Kauru East','Sub-District','Nigeria' UNION ALL
        SELECT 191408, 'Kauru West','Sub-District','Nigeria' UNION ALL
        SELECT 204405, 'Kausani','Sub-District','Nigeria' UNION ALL
        SELECT 430603, 'Kautakari','Sub-District','Nigeria' UNION ALL
        SELECT 431707, 'Kauwa','Sub-District','Nigeria' UNION ALL
        SELECT 203109, 'Kawaji','Sub-District','Nigeria' UNION ALL
        SELECT 221406, 'Kawara (Maiyama)','Sub-District','Nigeria' UNION ALL
        SELECT 221704, 'Kawara (Shanga)','Sub-District','Nigeria' UNION ALL
        SELECT 213405, 'Kawarin Kudi','Sub-District','Nigeria' UNION ALL
        SELECT 213406, 'Kawarin Malamai','Sub-District','Nigeria' UNION ALL
        SELECT 180506, 'Kawaya','Sub-District','Nigeria' UNION ALL
        SELECT 190905, 'Kawo','Sub-District','Nigeria' UNION ALL
        SELECT 431605, 'Kawuri','Sub-District','Nigeria' UNION ALL
        SELECT 370907, 'Kaya','Sub-District','Nigeria' UNION ALL
        SELECT 191705, 'Kayarda','Sub-District','Nigeria' UNION ALL
        SELECT 210208, 'Kayauki','Sub-District','Nigeria' UNION ALL
        SELECT 211104, 'Kayawa','Sub-District','Nigeria' UNION ALL
        SELECT 371206, 'Kayaye','Sub-District','Nigeria' UNION ALL
        SELECT 360508, 'Kayeri','Sub-District','Nigeria' UNION ALL
        SELECT 180408, 'Kazura','Sub-District','Nigeria' UNION ALL
        SELECT 201607, 'Kazurewa','Sub-District','Nigeria' UNION ALL
        SELECT 341003, 'Kebbe East','Sub-District','Nigeria' UNION ALL
        SELECT 341004, 'Kebbe West','Sub-District','Nigeria' UNION ALL
        SELECT 431708, 'Kekeno','Sub-District','Nigeria' UNION ALL
        SELECT 220508, 'Kende/Kurgu','Sub-District','Nigeria' UNION ALL
        SELECT 190406, 'Kerawa 1 (Igabi)','Sub-District','Nigeria' UNION ALL
        SELECT 190407, 'Kerawa 2 (Igabi)','Sub-District','Nigeria' UNION ALL
        SELECT 430106, 'Kessaa','Sub-District','Nigeria' UNION ALL
        SELECT 371306, 'Keta','Sub-District','Nigeria' UNION ALL
        SELECT 211906, 'Ketare','Sub-District','Nigeria' UNION ALL
        SELECT 201705, 'Ketawa','Sub-District','Nigeria' UNION ALL
        SELECT 431307, 'Khaddamari','Sub-District','Nigeria' UNION ALL
        SELECT 202305, 'Kibiya I','Sub-District','Nigeria' UNION ALL
        SELECT 202306, 'Kibiya Ii','Sub-District','Nigeria' UNION ALL
        SELECT 431205, 'Kida','Sub-District','Nigeria' UNION ALL
        SELECT 190307, 'Kidandan','Sub-District','Nigeria' UNION ALL
        SELECT 181106, 'Kila','Sub-District','Nigeria' UNION ALL
        SELECT 421611, 'Kilbori A','Sub-District','Nigeria' UNION ALL
        SELECT 421612, 'Kilbori B','Sub-District','Nigeria' UNION ALL
        SELECT 342307, 'Kilgori','Sub-District','Nigeria' UNION ALL
        SELECT 431505, 'Kilumaga','Sub-District','Nigeria' UNION ALL
        SELECT 221108, 'Kimba','Sub-District','Nigeria' UNION ALL
        SELECT 431007, 'Kingarwa','Sub-District','Nigeria' UNION ALL
        SELECT 430908, 'Kingowa','Sub-District','Nigeria' UNION ALL
        SELECT 192105, 'Kinkiba','Sub-District','Nigeria' UNION ALL
        SELECT 212906, 'Kira','Sub-District','Nigeria' UNION ALL
        SELECT 432207, 'Kirenowa','Sub-District','Nigeria' UNION ALL
        SELECT 421308, 'Kirfi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 340408, 'Kiri (Gada)','Sub-District','Nigeria' UNION ALL
        SELECT 182605, 'Kiri (Taura)','Sub-District','Nigeria' UNION ALL
        SELECT 181805, 'Kiri Kasamma (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 202409, 'Kiru (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 180304, 'Kiyako','Sub-District','Nigeria' UNION ALL
        SELECT 200305, 'Kiyawa (Bagwai)','Sub-District','Nigeria' UNION ALL
        SELECT 181907, 'Kiyawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431110, 'Kizawa Jimin','Sub-District','Nigeria' UNION ALL
        SELECT 210605, 'Koda','Sub-District','Nigeria' UNION ALL
        SELECT 200408, 'Kofa (Bebeji)','Sub-District','Nigeria' UNION ALL
        SELECT 212306, 'Kofa (Kusada)','Sub-District','Nigeria' UNION ALL
        SELECT 420708, 'Kofan Romi','Sub-District','Nigeria' UNION ALL
        SELECT 180909, 'Kofar Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 200709, 'Kofar Mazugal','Sub-District','Nigeria' UNION ALL
        SELECT 200710, 'Kofar Ruwa','Sub-District','Nigeria' UNION ALL
        SELECT 180910, 'Kofar Yamma','Sub-District','Nigeria' UNION ALL
        SELECT 212804, 'Kogari','Sub-District','Nigeria' UNION ALL
        SELECT 202410, 'Kogo','Sub-District','Nigeria' UNION ALL
        SELECT 202905, 'Koguna','Sub-District','Nigeria' UNION ALL
        SELECT 340506, 'Kojiyo','Sub-District','Nigeria' UNION ALL
        SELECT 221109, 'Kokani','Sub-District','Nigeria' UNION ALL
        SELECT 220307, 'Kokani North','Sub-District','Nigeria' UNION ALL
        SELECT 220308, 'Kokani South','Sub-District','Nigeria' UNION ALL
        SELECT 203506, 'Kokiya','Sub-District','Nigeria' UNION ALL
        SELECT 221308, 'Koko Firchin','Sub-District','Nigeria' UNION ALL
        SELECT 221309, 'Koko Magaji','Sub-District','Nigeria' UNION ALL
        SELECT 220607, 'Kola/Tarasa','Sub-District','Nigeria' UNION ALL
        SELECT 360509, 'Kolere/ Kafaje','Sub-District','Nigeria' UNION ALL
        SELECT 431506, 'Komakandi','Sub-District','Nigeria' UNION ALL
        SELECT 432707, 'Kombo','Sub-District','Nigeria' UNION ALL
        SELECT 431606, 'Konduga (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420506, 'Konkiyel','Sub-District','Nigeria' UNION ALL
        SELECT 361105, 'Konkomma','Sub-District','Nigeria' UNION ALL
        SELECT 181207, 'Korayel','Sub-District','Nigeria' UNION ALL
        SELECT 200808, 'Kore (Dambatta)','Sub-District','Nigeria' UNION ALL
        SELECT 420709, 'Kore (Gamawa)','Sub-District','Nigeria' UNION ALL
        SELECT 180808, 'Kore (Garki)','Sub-District','Nigeria' UNION ALL
        SELECT 180704, 'Kore Balatu','Sub-District','Nigeria' UNION ALL
        SELECT 361505, 'Koriyel','Sub-District','Nigeria' UNION ALL
        SELECT 430604, 'Korongilum','Sub-District','Nigeria' UNION ALL
        SELECT 202706, 'Kosawa','Sub-District','Nigeria' UNION ALL
        SELECT 431903, 'Koshebe','Sub-District','Nigeria' UNION ALL
        SELECT 370507, 'Kotorkoshi','Sub-District','Nigeria' UNION ALL
        SELECT 182205, 'Koya','Sub-District','Nigeria' UNION ALL
        SELECT 212404, 'Koza','Sub-District','Nigeria' UNION ALL
        SELECT 191306, 'Kpak','Sub-District','Nigeria' UNION ALL
        SELECT 202808, 'Kubaraci','Sub-District','Nigeria' UNION ALL
        SELECT 191507, 'Kubau (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420710, 'Kubdiya','Sub-District','Nigeria' UNION ALL
        SELECT 420809, 'Kubi A','Sub-District','Nigeria' UNION ALL
        SELECT 420810, 'Kubi B','Sub-District','Nigeria' UNION ALL
        SELECT 432708, 'Kubo','Sub-District','Nigeria' UNION ALL
        SELECT 341506, 'Kubodu','Sub-District','Nigeria' UNION ALL
        SELECT 431804, 'Kubuku','Sub-District','Nigeria' UNION ALL
        SELECT 430605, 'Kuburmbula','Sub-District','Nigeria' UNION ALL
        SELECT 341005, 'Kuchi','Sub-District','Nigeria' UNION ALL
        SELECT 432607, 'Kuda (Nganzai)','Sub-District','Nigeria' UNION ALL
        SELECT 182707, 'Kuda (Yankwashi)','Sub-District','Nigeria' UNION ALL
        SELECT 180608, 'Kudai','Sub-District','Nigeria' UNION ALL
        SELECT 191606, 'Kudan (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 191706, 'Kudaru','Sub-District','Nigeria' UNION ALL
        SELECT 430107, 'Kudo Kurgu','Sub-District','Nigeria' UNION ALL
        SELECT 212106, 'Kudu 1','Sub-District','Nigeria' UNION ALL
        SELECT 212107, 'Kudu 2','Sub-District','Nigeria' UNION ALL
        SELECT 212108, 'Kudu 3','Sub-District','Nigeria' UNION ALL
        SELECT 421509, 'Kudu Yamma','Sub-District','Nigeria' UNION ALL
        SELECT 191207, 'Kufana','Sub-District','Nigeria' UNION ALL
        SELECT 192305, 'Kufena','Sub-District','Nigeria' UNION ALL
        SELECT 190204, 'Kujama','Sub-District','Nigeria' UNION ALL
        SELECT 203708, 'Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 421411, 'Kukadi A','Sub-District','Nigeria' UNION ALL
        SELECT 421412, 'Kukadi B','Sub-District','Nigeria' UNION ALL
        SELECT 221206, 'Kukah','Sub-District','Nigeria' UNION ALL
        SELECT 360306, 'Kukareta /Warsala','Sub-District','Nigeria' UNION ALL
        SELECT 211907, 'Kukasheka','Sub-District','Nigeria' UNION ALL
        SELECT 431709, 'Kukawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361106, 'Kukayasku (Machina)','Sub-District','Nigeria' UNION ALL
        SELECT 182006, 'Kukayasku (Maigatari)','Sub-District','Nigeria' UNION ALL
        SELECT 200409, 'Kuki','Sub-District','Nigeria' UNION ALL
        SELECT 211207, 'Kuki A','Sub-District','Nigeria' UNION ALL
        SELECT 211208, 'Kuki B','Sub-District','Nigeria' UNION ALL
        SELECT 191307, 'Kukum','Sub-District','Nigeria' UNION ALL
        SELECT 180507, 'Kukuma','Sub-District','Nigeria' UNION ALL
        SELECT 361208, 'Kukuri / Chiromari','Sub-District','Nigeria' UNION ALL
        SELECT 191108, 'Kukuyi','Sub-District','Nigeria' UNION ALL
        SELECT 432208, 'Kulli','Sub-District','Nigeria' UNION ALL
        SELECT 200608, 'Kulluwa','Sub-District','Nigeria' UNION ALL
        SELECT 432403, 'Kumalia','Sub-District','Nigeria' UNION ALL
        SELECT 202506, 'Kumbotso (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 430310, 'Kumshe','Sub-District','Nigeria' UNION ALL
        SELECT 200609, 'Kumurya','Sub-District','Nigeria' UNION ALL
        SELECT 190205, 'Kunai','Sub-District','Nigeria' UNION ALL
        SELECT 202605, 'Kunchi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420212, 'Kundun Durum','Sub-District','Nigeria' UNION ALL
        SELECT 212006, 'Kunduru / Gyaza','Sub-District','Nigeria' UNION ALL
        SELECT 420111, 'Kungibar','Sub-District','Nigeria' UNION ALL
        SELECT 370806, 'Kungurki','Sub-District','Nigeria' UNION ALL
        SELECT 200108, 'Kunkun Rawa','Sub-District','Nigeria' UNION ALL
        SELECT 203004, 'Kunya','Sub-District','Nigeria' UNION ALL
        SELECT 432009, 'Kupti','Sub-District','Nigeria' UNION ALL
        SELECT 202707, 'Kura (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431111, 'Kurabasa Ngoshes','Sub-District','Nigeria' UNION ALL
        SELECT 210110, 'Kurami/Yankwani','Sub-District','Nigeria' UNION ALL
        SELECT 341304, 'Kurawa','Sub-District','Nigeria' UNION ALL
        SELECT 210606, 'Kuraye','Sub-District','Nigeria' UNION ALL
        SELECT 420908, 'Kurba','Sub-District','Nigeria' UNION ALL
        SELECT 431805, 'Kurbagayi','Sub-District','Nigeria' UNION ALL
        SELECT 340608, 'Kurdula','Sub-District','Nigeria' UNION ALL
        SELECT 202507, 'Kureken Sani','Sub-District','Nigeria' UNION ALL
        SELECT 370608, 'Kurfa','Sub-District','Nigeria' UNION ALL
        SELECT 211508, 'Kurfeji/Yankaura','Sub-District','Nigeria' UNION ALL
        SELECT 212203, 'Kurfi A','Sub-District','Nigeria' UNION ALL
        SELECT 212204, 'Kurfi B','Sub-District','Nigeria' UNION ALL
        SELECT 190206, 'Kuriga','Sub-District','Nigeria' UNION ALL
        SELECT 211706, 'Kuringafa','Sub-District','Nigeria' UNION ALL
        SELECT 212907, 'Kurkujan A','Sub-District','Nigeria' UNION ALL
        SELECT 212908, 'Kurkujan B','Sub-District','Nigeria' UNION ALL
        SELECT 421510, 'Kurmi','Sub-District','Nigeria' UNION ALL
        SELECT 190504, 'Kurmi Kogi','Sub-District','Nigeria' UNION ALL
        SELECT 191109, 'Kurmin Jibrin','Sub-District','Nigeria' UNION ALL
        SELECT 190810, 'Kurmin Musa','Sub-District','Nigeria' UNION ALL
        SELECT 360209, 'Kurnawa (Borsari)','Sub-District','Nigeria' UNION ALL
        SELECT 432608, 'Kurnawa (Nganzai)','Sub-District','Nigeria' UNION ALL
        SELECT 203005, 'Kuru','Sub-District','Nigeria' UNION ALL
        SELECT 202203, 'Kurugu','Sub-District','Nigeria' UNION ALL
        SELECT 202708, 'Kurun Sumau','Sub-District','Nigeria' UNION ALL
        SELECT 342005, 'Kuruwa','Sub-District','Nigeria' UNION ALL
        SELECT 370807, 'Kurya (Kaura Namoda)','Sub-District','Nigeria' UNION ALL
        SELECT 341204, 'Kurya (Rabah)','Sub-District','Nigeria' UNION ALL
        SELECT 371106, 'Kurya-Skf','Sub-District','Nigeria' UNION ALL
        SELECT 211608, 'Kusa','Sub-District','Nigeria' UNION ALL
        SELECT 212307, 'Kusada (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 191110, 'Kushe','Sub-District','Nigeria' UNION ALL
        SELECT 360809, 'Kushimaga','Sub-District','Nigeria' UNION ALL
        SELECT 211001, 'Kusugu','Sub-District','Nigeria' UNION ALL
        SELECT 360610, 'Kusur','Sub-District','Nigeria' UNION ALL
        SELECT 211209, 'Kutaina','Sub-District','Nigeria' UNION ALL
        SELECT 201905, 'Kutama','Sub-District','Nigeria' UNION ALL
        SELECT 190105, 'Kutemeshi','Sub-District','Nigeria' UNION ALL
        SELECT 190505, 'Kuya','Sub-District','Nigeria' UNION ALL
        SELECT 371007, 'Kuyanbana-Mrr','Sub-District','Nigeria' UNION ALL
        SELECT 190106, 'Kuyello','Sub-District','Nigeria' UNION ALL
        SELECT 180209, 'Kuzunzumi','Sub-District','Nigeria' UNION ALL
        SELECT 201008, 'Kwa','Sub-District','Nigeria' UNION ALL
        SELECT 341903, 'Kwacce Huro','Sub-District','Nigeria' UNION ALL
        SELECT 340208, 'Kwacciyar Lalle','Sub-District','Nigeria' UNION ALL
        SELECT 201206, 'Kwachiri','Sub-District','Nigeria' UNION ALL
        SELECT 421309, 'Kwagal','Sub-District','Nigeria' UNION ALL
        SELECT 220408, 'Kwaido','Sub-District','Nigeria' UNION ALL
        SELECT 221809, 'Kwaifa','Sub-District','Nigeria' UNION ALL
        SELECT 182406, 'Kwaita','Sub-District','Nigeria' UNION ALL
        SELECT 431206, 'Kwajaffa','Sub-District','Nigeria' UNION ALL
        SELECT 200306, 'Kwajali','Sub-District','Nigeria' UNION ALL
        SELECT 220807, 'Kwakkwaba','Sub-District','Nigeria' UNION ALL
        SELECT 221505, 'Kwakwara','Sub-District','Nigeria' UNION ALL
        SELECT 340507, 'Kwakwazo','Sub-District','Nigeria' UNION ALL
        SELECT 182606, 'Kwalam','Sub-District','Nigeria' UNION ALL
        SELECT 200505, 'Kwamarawa','Sub-District','Nigeria' UNION ALL
        SELECT 203907, 'Kwami','Sub-District','Nigeria' UNION ALL
        SELECT 202906, 'Kwanar Tabo','Sub-District','Nigeria' UNION ALL
        SELECT 181908, 'Kwanda','Sub-District','Nigeria' UNION ALL
        SELECT 180305, 'Kwangwara','Sub-District','Nigeria' UNION ALL
        SELECT 202809, 'Kwankwaso','Sub-District','Nigeria' UNION ALL
        SELECT 202204, 'Kwanyawa','Sub-District','Nigeria' UNION ALL
        SELECT 342006, 'Kwarare','Sub-District','Nigeria' UNION ALL
        SELECT 190408, 'Kwarau','Sub-District','Nigeria' UNION ALL
        SELECT 192306, 'Kwarbai  A','Sub-District','Nigeria' UNION ALL
        SELECT 192307, 'Kwarbai  B','Sub-District','Nigeria' UNION ALL
        SELECT 371107, 'Kware (Shinkafi)','Sub-District','Nigeria' UNION ALL
        SELECT 341108, 'Kware (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 342206, 'Kwargaba','Sub-District','Nigeria' UNION ALL
        SELECT 203006, 'Kwarkiya','Sub-District','Nigeria' UNION ALL
        SELECT 340409, 'Kwarma','Sub-District','Nigeria' UNION ALL
        SELECT 201407, 'Kwas','Sub-District','Nigeria' UNION ALL
        SELECT 192106, 'Kwasallo','Sub-District','Nigeria' UNION ALL
        SELECT 213308, 'Kwasarawa','Sub-District','Nigeria' UNION ALL
        SELECT 342207, 'Kwasare','Sub-District','Nigeria' UNION ALL
        SELECT 371405, 'Kwashebawa','Sub-District','Nigeria' UNION ALL
        SELECT 191409, 'Kwassam','Sub-District','Nigeria' UNION ALL
        SELECT 212606, 'Kwatta','Sub-District','Nigeria' UNION ALL
        SELECT 190811, 'Kwaturu','Sub-District','Nigeria' UNION ALL
        SELECT 431806, 'Kwaya Kusar (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431207, 'Kwaya/B','Sub-District','Nigeria' UNION ALL
        SELECT 181506, 'Kwazailewa','Sub-District','Nigeria' UNION ALL
        SELECT 181107, 'Kwondiko','Sub-District','Nigeria' UNION ALL
        SELECT 221907, 'Kyabu/Kandu','Sub-District','Nigeria' UNION ALL
        SELECT 340410, 'Kyadawa/Holai','Sub-District','Nigeria' UNION ALL
        SELECT 200506, 'Kyalli','Sub-District','Nigeria' UNION ALL
        SELECT 180210, 'Kyambo','Sub-District','Nigeria' UNION ALL
        SELECT 370808, 'Kyanbarawa','Sub-District','Nigeria' UNION ALL
        SELECT 220808, 'Kyangakwai','Sub-District','Nigeria' UNION ALL
        SELECT 370404, 'Kyaram','Sub-District','Nigeria' UNION ALL
        SELECT 182305, 'Kyarama','Sub-District','Nigeria' UNION ALL
        SELECT 421511, 'Kyata','Sub-District','Nigeria' UNION ALL
        SELECT 192308, 'L/Kona','Sub-District','Nigeria' UNION ALL
        SELECT 341507, 'Labani','Sub-District','Nigeria' UNION ALL
        SELECT 220509, 'Lafagu/Gante','Sub-District','Nigeria' UNION ALL
        SELECT 180306, 'Lafia','Sub-District','Nigeria' UNION ALL
        SELECT 360908, 'Lafia Loi Loi','Sub-District','Nigeria' UNION ALL
        SELECT 181007, 'Lafiya','Sub-District','Nigeria' UNION ALL
        SELECT 220608, 'Lagga/Randali','Sub-District','Nigeria' UNION ALL
        SELECT 420507, 'Lago','Sub-District','Nigeria' UNION ALL
        SELECT 342208, 'Lahodu','Sub-District','Nigeria' UNION ALL
        SELECT 220309, 'Lailaba','Sub-District','Nigeria' UNION ALL
        SELECT 204406, 'Lajawa','Sub-District','Nigeria' UNION ALL
        SELECT 431904, 'Laje','Sub-District','Nigeria' UNION ALL
        SELECT 341305, 'Lajinge','Sub-District','Nigeria' UNION ALL
        SELECT 432709, 'Lakundum','Sub-District','Nigeria' UNION ALL
        SELECT 201906, 'Lakwaya','Sub-District','Nigeria' UNION ALL
        SELECT 342007, 'Lambar Tureta','Sub-District','Nigeria' UNION ALL
        SELECT 341407, 'Lambara','Sub-District','Nigeria' UNION ALL
        SELECT 203908, 'Lambu','Sub-District','Nigeria' UNION ALL
        SELECT 421802, 'Lame','Sub-District','Nigeria' UNION ALL
        SELECT 361107, 'Lamisu','Sub-District','Nigeria' UNION ALL
        SELECT 432110, 'Lamisula','Sub-District','Nigeria' UNION ALL
        SELECT 203909, 'Langel','Sub-District','Nigeria' UNION ALL
        SELECT 221310, 'Lani/Shiba','Sub-District','Nigeria' UNION ALL
        SELECT 361506, 'Lantewa','Sub-District','Nigeria' UNION ALL
        SELECT 420508, 'Lanzai East','Sub-District','Nigeria' UNION ALL
        SELECT 420509, 'Lanzai West','Sub-District','Nigeria' UNION ALL
        SELECT 421310, 'Lariski','Sub-District','Nigeria' UNION ALL
        SELECT 421111, 'Lariye','Sub-District','Nigeria' UNION ALL
        SELECT 430205, 'Lassa','Sub-District','Nigeria' UNION ALL
        SELECT 203202, 'Lausu','Sub-District','Nigeria' UNION ALL
        SELECT 360105, 'Lawan Fernami','Sub-District','Nigeria' UNION ALL
        SELECT 360106, 'Lawan Musa','Sub-District','Nigeria' UNION ALL
        SELECT 432308, 'Layi','Sub-District','Nigeria' UNION ALL
        SELECT 191707, 'Lazuru/Tuddai','Sub-District','Nigeria' UNION ALL
        SELECT 180508, 'Lelenkudu','Sub-District','Nigeria' UNION ALL
        SELECT 220208, 'Lema/Jantulu','Sub-District','Nigeria' UNION ALL
        SELECT 203507, 'Leni','Sub-District','Nigeria' UNION ALL
        SELECT 191708, 'Lere (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421710, 'Lere North','Sub-District','Nigeria' UNION ALL
        SELECT 421711, 'Lere South','Sub-District','Nigeria' UNION ALL
        SELECT 221407, 'Liba','Sub-District','Nigeria' UNION ALL
        SELECT 221506, 'Libata','Sub-District','Nigeria' UNION ALL
        SELECT 430606, 'Likama','Sub-District','Nigeria' UNION ALL
        SELECT 191607, 'Likoro','Sub-District','Nigeria' UNION ALL
        SELECT 420112, 'Lim Kundak','Sub-District','Nigeria' UNION ALL
        SELECT 420213, 'Liman Katagun','Sub-District','Nigeria' UNION ALL
        SELECT 430407, 'Limanti (Bayo)','Sub-District','Nigeria' UNION ALL
        SELECT 431905, 'Limanti (Mafa)','Sub-District','Nigeria' UNION ALL
        SELECT 432111, 'Limanti (Maiduguri)','Sub-District','Nigeria' UNION ALL
        SELECT 180609, 'Limawa','Sub-District','Nigeria' UNION ALL
        SELECT 204407, 'Lndabo','Sub-District','Nigeria' UNION ALL
        SELECT 422008, 'Lodiyo','Sub-District','Nigeria' UNION ALL
        SELECT 342008, 'Lofa','Sub-District','Nigeria' UNION ALL
        SELECT 432505, 'Logumane','Sub-District','Nigeria' UNION ALL
        SELECT 220510, 'Lolo/Giris','Sub-District','Nigeria' UNION ALL
        SELECT 431906, 'Loskuri','Sub-District','Nigeria' UNION ALL
        SELECT 420610, 'Lukshi','Sub-District','Nigeria' UNION ALL
        SELECT 420311, 'Lusa','Sub-District','Nigeria' UNION ALL
        SELECT 430805, 'M. Kaza','Sub-District','Nigeria' UNION ALL
        SELECT 430806, 'M. Maja','Sub-District','Nigeria' UNION ALL
        SELECT 210804, 'M/Dansoda','Sub-District','Nigeria' UNION ALL
        SELECT 210805, 'M/Wando','Sub-District','Nigeria' UNION ALL
        SELECT 360611, 'Ma Anna','Sub-District','Nigeria' UNION ALL
        SELECT 431907, 'Maafa','Sub-District','Nigeria' UNION ALL
        SELECT 211908, 'Mabai','Sub-District','Nigeria' UNION ALL
        SELECT 212607, 'Machika (Mani)','Sub-District','Nigeria' UNION ALL
        SELECT 213105, 'Machika (Sabuwa)','Sub-District','Nigeria' UNION ALL
        SELECT 361108, 'Machina (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 180409, 'Machinamari','Sub-District','Nigeria' UNION ALL
        SELECT 370702, 'Mada (Gusau)','Sub-District','Nigeria' UNION ALL
        SELECT 431507, 'Mada (Kala/Balge)','Sub-District','Nigeria' UNION ALL
        SELECT 421211, 'Madachi (Katagum)','Sub-District','Nigeria' UNION ALL
        SELECT 181806, 'Madachi (Kiri Kasamma)','Sub-District','Nigeria' UNION ALL
        SELECT 203203, 'Madachi (Rano)','Sub-District','Nigeria' UNION ALL
        SELECT 201907, 'Madada','Sub-District','Nigeria' UNION ALL
        SELECT 180705, 'Madaka','Sub-District','Nigeria' UNION ALL
        SELECT 182007, 'Madana','Sub-District','Nigeria' UNION ALL
        SELECT 421212, 'Madangala','Sub-District','Nigeria' UNION ALL
        SELECT 421213, 'Madara','Sub-District','Nigeria' UNION ALL
        SELECT 204310, 'Madarin Mata','Sub-District','Nigeria' UNION ALL
        SELECT 370703, 'Madawaki','Sub-District','Nigeria' UNION ALL
        SELECT 192205, 'Madekiya','Sub-District','Nigeria' UNION ALL
        SELECT 200711, 'Madigawa','Sub-District','Nigeria' UNION ALL
        SELECT 180610, 'Madobi (Dutse)','Sub-District','Nigeria' UNION ALL
        SELECT 202810, 'Madobi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 211002, 'Madobi A','Sub-District','Nigeria' UNION ALL
        SELECT 211003, 'Madobi B','Sub-District','Nigeria' UNION ALL
        SELECT 210307, 'Madogara','Sub-District','Nigeria' UNION ALL
        SELECT 422009, 'Madufa','Sub-District','Nigeria' UNION ALL
        SELECT 431908, 'Mafa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361507, 'Mafa (Tarmua)','Sub-District','Nigeria' UNION ALL
        SELECT 432404, 'Mafio','Sub-District','Nigeria' UNION ALL
        SELECT 432112, 'Mafoni','Sub-District','Nigeria' UNION ALL
        SELECT 213005, 'Magabo/Kurabo','Sub-District','Nigeria' UNION ALL
        SELECT 221110, 'Magaji A','Sub-District','Nigeria' UNION ALL
        SELECT 221111, 'Magaji B','Sub-District','Nigeria' UNION ALL
        SELECT 370105, 'Magaji-Ank','Sub-District','Nigeria' UNION ALL
        SELECT 370609, 'Magaji-Gmm','Sub-District','Nigeria' UNION ALL
        SELECT 202205, 'Magajin Gari','Sub-District','Nigeria' UNION ALL
        SELECT 341601, 'Magajin Gari A','Sub-District','Nigeria' UNION ALL
        SELECT 341602, 'Magajin Gari B','Sub-District','Nigeria' UNION ALL
        SELECT 190107, 'Magajin Gari I','Sub-District','Nigeria' UNION ALL
        SELECT 190108, 'Magajin Gari Ii','Sub-District','Nigeria' UNION ALL
        SELECT 190109, 'Magajin Gari Iii','Sub-District','Nigeria' UNION ALL
        SELECT 341603, 'Magajin Rafi A','Sub-District','Nigeria' UNION ALL
        SELECT 341604, 'Magajin Rafi B','Sub-District','Nigeria' UNION ALL
        SELECT 212608, 'Magami (Mani)','Sub-District','Nigeria' UNION ALL
        SELECT 203606, 'Magami (Sumaila)','Sub-District','Nigeria' UNION ALL
        SELECT 370704, 'Magami-Gus','Sub-District','Nigeria' UNION ALL
        SELECT 430807, 'Magarta','Sub-District','Nigeria' UNION ALL
        SELECT 421013, 'Magarya (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
        SELECT 342209, 'Magarya (Wurno)','Sub-District','Nigeria' UNION ALL
        SELECT 432010, 'Magumeri (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421214, 'Magwanshi','Sub-District','Nigeria' UNION ALL
        SELECT 191508, 'Mah','Sub-District','Nigeria' UNION ALL
        SELECT 220907, 'Mahuta (Fakai)','Sub-District','Nigeria' UNION ALL
        SELECT 211707, 'Mahuta (Kafur)','Sub-District','Nigeria' UNION ALL
        SELECT 210806, 'Mahuta A','Sub-District','Nigeria' UNION ALL
        SELECT 210807, 'Mahuta B','Sub-District','Nigeria' UNION ALL
        SELECT 210808, 'Mahuta C','Sub-District','Nigeria' UNION ALL
        SELECT 180706, 'Mai Aduwa','Sub-District','Nigeria' UNION ALL
        SELECT 212405, 'Maiadua A','Sub-District','Nigeria' UNION ALL
        SELECT 212406, 'Maiadua B','Sub-District','Nigeria' UNION ALL
        SELECT 212407, 'Maiadua C','Sub-District','Nigeria' UNION ALL
        SELECT 213106, 'Maibakko','Sub-District','Nigeria' UNION ALL
        SELECT 210407, 'Maibara','Sub-District','Nigeria' UNION ALL
        SELECT 190906, 'Maiburiji','Sub-District','Nigeria' UNION ALL
        SELECT 210706, 'Maidabino A','Sub-District','Nigeria' UNION ALL
        SELECT 210707, 'Maidabino B','Sub-District','Nigeria' UNION ALL
        SELECT 220703, 'Maidahini','Sub-District','Nigeria' UNION ALL
        SELECT 211406, 'Maigamji','Sub-District','Nigeria' UNION ALL
        SELECT 192107, 'Maigana','Sub-District','Nigeria' UNION ALL
        SELECT 182008, 'Maigatari Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 182009, 'Maigatari Kudu','Sub-District','Nigeria' UNION ALL
        SELECT 190711, 'Maigizo','Sub-District','Nigeria' UNION ALL
        SELECT 211303, 'Maigora','Sub-District','Nigeria' UNION ALL
        SELECT 220809, 'Maigwaza','Sub-District','Nigeria' UNION ALL
        SELECT 220810, 'Maihausawa','Sub-District','Nigeria' UNION ALL
        SELECT 201608, 'Maikamawa','Sub-District','Nigeria' UNION ALL
        SELECT 422010, 'Maikawa','Sub-District','Nigeria' UNION ALL
        SELECT 220908, 'Maikende','Sub-District','Nigeria' UNION ALL
        SELECT 180707, 'Maikilili','Sub-District','Nigeria' UNION ALL
        SELECT 212408, 'Maikoni A','Sub-District','Nigeria' UNION ALL
        SELECT 212409, 'Maikoni B','Sub-District','Nigeria' UNION ALL
        SELECT 341205, 'Maikujera/Riji','Sub-District','Nigeria' UNION ALL
        SELECT 340106, 'Maikulki','Sub-District','Nigeria' UNION ALL
        SELECT 210809, 'Maikwama','Sub-District','Nigeria' UNION ALL
        SELECT 420113, 'Maimadi','Sub-District','Nigeria' UNION ALL
        SELECT 361706, 'Maimalari','Sub-District','Nigeria' UNION ALL
        SELECT 431308, 'Maimusari','Sub-District','Nigeria' UNION ALL
        SELECT 422011, 'Mainako North','Sub-District','Nigeria' UNION ALL
        SELECT 422012, 'Mainako South','Sub-District','Nigeria' UNION ALL
        SELECT 201908, 'Mainika','Sub-District','Nigeria' UNION ALL
        SELECT 431409, 'Mainok','Sub-District','Nigeria' UNION ALL
        SELECT 182105, 'Mairakumi','Sub-District','Nigeria' UNION ALL
        SELECT 431008, 'Mairari (Guzamala)','Sub-District','Nigeria' UNION ALL
        SELECT 361606, 'Mairari (Yunusari)','Sub-District','Nigeria' UNION ALL
        SELECT 431309, 'Mairi','Sub-District','Nigeria' UNION ALL
        SELECT 211304, 'Mairuwa','Sub-District','Nigeria' UNION ALL
        SELECT 432113, 'Maisandari','Sub-District','Nigeria' UNION ALL
        SELECT 360307, 'Maisandari /Waziri Ibrahim','Sub-District','Nigeria' UNION ALL
        SELECT 202907, 'Maitsida','Sub-District','Nigeria' UNION ALL
        SELECT 432609, 'Maiwa (Nganzai)','Sub-District','Nigeria' UNION ALL
        SELECT 422013, 'Maiwa (Zaki)','Sub-District','Nigeria' UNION ALL
        SELECT 221408, 'Maiyalo','Sub-District','Nigeria' UNION ALL
        SELECT 221409, 'Maiyama (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 371008, 'Maiyanchi','Sub-District','Nigeria' UNION ALL
        SELECT 361308, 'Maja Kura','Sub-District','Nigeria' UNION ALL
        SELECT 181507, 'Majawa','Sub-District','Nigeria' UNION ALL
        SELECT 181909, 'Maje (Kiyawa)','Sub-District','Nigeria' UNION ALL
        SELECT 341508, 'Maje (Silame)','Sub-District','Nigeria' UNION ALL
        SELECT 182607, 'Maje (Taura)','Sub-District','Nigeria' UNION ALL
        SELECT 213006, 'Maje/Karare','Sub-District','Nigeria' UNION ALL
        SELECT 181306, 'Majema','Sub-District','Nigeria' UNION ALL
        SELECT 210607, 'Majen Wayya','Sub-District','Nigeria' UNION ALL
        SELECT 182608, 'Majia','Sub-District','Nigeria' UNION ALL
        SELECT 212707, 'Majigiri','Sub-District','Nigeria' UNION ALL
        SELECT 420214, 'Makama A','Sub-District','Nigeria' UNION ALL
        SELECT 420215, 'Makama B','Sub-District','Nigeria' UNION ALL
        SELECT 191410, 'Makami','Sub-District','Nigeria' UNION ALL
        SELECT 191807, 'Makarfi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 212506, 'Makauraci','Sub-District','Nigeria' UNION ALL
        SELECT 221507, 'Makawa','Sub-District','Nigeria' UNION ALL
        SELECT 220609, 'Makera (Birnin Kebbi)','Sub-District','Nigeria' UNION ALL
        SELECT 211210, 'Makera (Dutsin Ma)','Sub-District','Nigeria' UNION ALL
        SELECT 211407, 'Makera (Funtua)','Sub-District','Nigeria' UNION ALL
        SELECT 371207, 'Makera/Take Tsaba','Sub-District','Nigeria' UNION ALL
        SELECT 202908, 'Makoda (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341306, 'Makuaana','Sub-District','Nigeria' UNION ALL
        SELECT 221607, 'Makuku','Sub-District','Nigeria' UNION ALL
        SELECT 213007, 'Makurda','Sub-District','Nigeria' UNION ALL
        SELECT 201509, 'Makwaro','Sub-District','Nigeria' UNION ALL
        SELECT 191308, 'Malagum','Sub-District','Nigeria' UNION ALL
        SELECT 360707, 'Malam Dunari','Sub-District','Nigeria' UNION ALL
        SELECT 182106, 'Malam Maduri (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431607, 'Malari','Sub-District','Nigeria' UNION ALL
        SELECT 221008, 'Malisa','Sub-District','Nigeria' UNION ALL
        SELECT 212507, 'Malumfashi A','Sub-District','Nigeria' UNION ALL
        SELECT 212508, 'Malumfashi B','Sub-District','Nigeria' UNION ALL
        SELECT 340708, 'Mamman Suka','Sub-District','Nigeria' UNION ALL
        SELECT 340709, 'Mammande','Sub-District','Nigeria' UNION ALL
        SELECT 361408, 'Mamudo','Sub-District','Nigeria' UNION ALL
        SELECT 211509, 'Manamawakafi','Sub-District','Nigeria' UNION ALL
        SELECT 210308, 'Manawa','Sub-District','Nigeria' UNION ALL
        SELECT 191309, 'Manchok','Sub-District','Nigeria' UNION ALL
        SELECT 180509, 'Mandabe','Sub-District','Nigeria' UNION ALL
        SELECT 361508, 'Mandadawa','Sub-District','Nigeria' UNION ALL
        SELECT 432405, 'Mandala','Sub-District','Nigeria' UNION ALL
        SELECT 430507, 'Mandaragirau','Sub-District','Nigeria' UNION ALL
        SELECT 201809, 'Mandawari','Sub-District','Nigeria' UNION ALL
        SELECT 341408, 'Mandera','Sub-District','Nigeria' UNION ALL
        SELECT 222105, 'Manga Ushe','Sub-District','Nigeria' UNION ALL
        SELECT 212609, 'Mani (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420114, 'Mansur','Sub-District','Nigeria' UNION ALL
        SELECT 421803, 'Mara','Sub-District','Nigeria' UNION ALL
        SELECT 210708, 'Mara A','Sub-District','Nigeria' UNION ALL
        SELECT 210709, 'Mara B','Sub-District','Nigeria' UNION ALL
        SELECT 181707, 'Maradawa','Sub-District','Nigeria' UNION ALL
        SELECT 370908, 'Maradun North','Sub-District','Nigeria' UNION ALL
        SELECT 370909, 'Maradun South','Sub-District','Nigeria' UNION ALL
        SELECT 220610, 'Marafa (Birnin Kebbi)','Sub-District','Nigeria' UNION ALL
        SELECT 220704, 'Marafa (Bunza)','Sub-District','Nigeria' UNION ALL
        SELECT 220909, 'Marafa (Fakai)','Sub-District','Nigeria' UNION ALL
        SELECT 341509, 'Marafa (Silame)','Sub-District','Nigeria' UNION ALL
        SELECT 342210, 'Marafa (Wurno)','Sub-District','Nigeria' UNION ALL
        SELECT 340609, 'Marake','Sub-District','Nigeria' UNION ALL
        SELECT 202411, 'Maraku','Sub-District','Nigeria' UNION ALL
        SELECT 431208, 'Marama/K','Sub-District','Nigeria' UNION ALL
        SELECT 420711, 'Marana','Sub-District','Nigeria' UNION ALL
        SELECT 181008, 'Margadu','Sub-District','Nigeria' UNION ALL
        SELECT 341006, 'Margai East','Sub-District','Nigeria' UNION ALL
        SELECT 341007, 'Margai West','Sub-District','Nigeria' UNION ALL
        SELECT 431410, 'Marguba','Sub-District','Nigeria' UNION ALL
        SELECT 360510, 'Marimarigudugurka','Sub-District','Nigeria' UNION ALL
        SELECT 202508, 'Mariri','Sub-District','Nigeria' UNION ALL
        SELECT 201009, 'Marke (Dawakin Tofa)','Sub-District','Nigeria' UNION ALL
        SELECT 181609, 'Marke (Kaugama)','Sub-District','Nigeria' UNION ALL
        SELECT 181807, 'Marma','Sub-District','Nigeria' UNION ALL
        SELECT 191208, 'Maro','Sub-District','Nigeria' UNION ALL
        SELECT 432209, 'Marte (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 371009, 'Maru (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221009, 'Maruda','Sub-District','Nigeria' UNION ALL
        SELECT 181108, 'Maruta','Sub-District','Nigeria' UNION ALL
        SELECT 360210, 'Masaba','Sub-District','Nigeria' UNION ALL
        SELECT 370405, 'Masama','Sub-District','Nigeria' UNION ALL
        SELECT 221010, 'Masama/Kwazgara','Sub-District','Nigeria' UNION ALL
        SELECT 202010, 'Masanawa','Sub-District','Nigeria' UNION ALL
        SELECT 211708, 'Masari','Sub-District','Nigeria' UNION ALL
        SELECT 431310, 'Mashamari','Sub-District','Nigeria' UNION ALL
        SELECT 421014, 'Mashema (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
        SELECT 371406, 'Mashema (Zurmi)','Sub-District','Nigeria' UNION ALL
        SELECT 212708, 'Mashi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360511, 'Mashio','Sub-District','Nigeria' UNION ALL
        SELECT 211408, 'Maska','Sub-District','Nigeria' UNION ALL
        SELECT 361109, 'Maskandare','Sub-District','Nigeria' UNION ALL
        SELECT 431909, 'Masu (Mafa)','Sub-District','Nigeria' UNION ALL
        SELECT 203607, 'Masu (Sumaila)','Sub-District','Nigeria' UNION ALL
        SELECT 180410, 'Matamu','Sub-District','Nigeria' UNION ALL
        SELECT 202606, 'Matan Fada','Sub-District','Nigeria' UNION ALL
        SELECT 181009, 'Matara Babba','Sub-District','Nigeria' UNION ALL
        SELECT 212805, 'Matazu A','Sub-District','Nigeria' UNION ALL
        SELECT 212806, 'Matazu B','Sub-District','Nigeria' UNION ALL
        SELECT 182010, 'Matoya','Sub-District','Nigeria' UNION ALL
        SELECT 211808, 'Matsai','Sub-District','Nigeria' UNION ALL
        SELECT 421215, 'Matsango','Sub-District','Nigeria' UNION ALL
        SELECT 181307, 'Matsaro','Sub-District','Nigeria' UNION ALL
        SELECT 370106, 'Matseri','Sub-District','Nigeria' UNION ALL
        SELECT 220511, 'Matsinkai/Geza','Sub-District','Nigeria' UNION ALL
        SELECT 220611, 'Maurida/Kariyo','Sub-District','Nigeria' UNION ALL
        SELECT 212308, 'Mawashi','Sub-District','Nigeria' UNION ALL
        SELECT 370705, 'Mayana','Sub-District','Nigeria' UNION ALL
        SELECT 371407, 'Mayasa/Kuturu','Sub-District','Nigeria' UNION ALL
        SELECT 361707, 'Mayori','Sub-District','Nigeria' UNION ALL
        SELECT 221608, 'Mazamaza','Sub-District','Nigeria' UNION ALL
        SELECT 211609, 'Mazanya','Sub-District','Nigeria' UNION ALL
        SELECT 211004, 'Mazoji A (Daura)','Sub-District','Nigeria' UNION ALL
        SELECT 212807, 'Mazoji A (Matazu)','Sub-District','Nigeria' UNION ALL
        SELECT 211005, 'Mazoji B (Daura)','Sub-District','Nigeria' UNION ALL
        SELECT 212808, 'Mazoji B (Matazu)','Sub-District','Nigeria' UNION ALL
        SELECT 430607, 'Mbalala','Sub-District','Nigeria' UNION ALL
        SELECT 421712, 'Mball','Sub-District','Nigeria' UNION ALL
        SELECT 430608, 'Mboakwa','Sub-District','Nigeria' UNION ALL
        SELECT 180708, 'Medu','Sub-District','Nigeria' UNION ALL
        SELECT 201305, 'Mekiya','Sub-District','Nigeria' UNION ALL
        SELECT 421015, 'Melandige','Sub-District','Nigeria' UNION ALL
        SELECT 201706, 'Mesar Tudu','Sub-District','Nigeria' UNION ALL
        SELECT 191808, 'Meyari','Sub-District','Nigeria' UNION ALL
        SELECT 181508, 'Mezan','Sub-District','Nigeria' UNION ALL
        SELECT 182206, 'Miga (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420411, 'Minchika','Sub-District','Nigeria' UNION ALL
        SELECT 203007, 'Minjibir (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 432406, 'Mintar','Sub-District','Nigeria' UNION ALL
        SELECT 420216, 'Miri','Sub-District','Nigeria' UNION ALL
        SELECT 430508, 'Miringa','Sub-District','Nigeria' UNION ALL
        SELECT 420811, 'Miya A','Sub-District','Nigeria' UNION ALL
        SELECT 420812, 'Miya B','Sub-District','Nigeria' UNION ALL
        SELECT 420813, 'Miya C','Sub-District','Nigeria' UNION ALL
        SELECT 432610, 'Miye','Sub-District','Nigeria' UNION ALL
        SELECT 182107, 'Mkandari','Sub-District','Nigeria' UNION ALL
        SELECT 370306, 'Modomawa East','Sub-District','Nigeria' UNION ALL
        SELECT 370307, 'Modomawa West','Sub-District','Nigeria' UNION ALL
        SELECT 431009, 'Moduri','Sub-District','Nigeria' UNION ALL
        SELECT 341904, 'Mogonho','Sub-District','Nigeria' UNION ALL
        SELECT 431508, 'Moholo','Sub-District','Nigeria' UNION ALL
        SELECT 432407, 'Monguno (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 371208, 'Morai','Sub-District','Nigeria' UNION ALL
        SELECT 371408, 'Moriki','Sub-District','Nigeria' UNION ALL
        SELECT 361607, 'Mosogun/Kujari','Sub-District','Nigeria' UNION ALL
        SELECT 360406, 'Mubi Fusami','Sub-District','Nigeria' UNION ALL
        SELECT 191908, 'Muchiya','Sub-District','Nigeria' UNION ALL
        SELECT 210408, 'Mudiri','Sub-District','Nigeria' UNION ALL
        SELECT 212610, 'Muduru','Sub-District','Nigeria' UNION ALL
        SELECT 360909, 'Muguram','Sub-District','Nigeria' UNION ALL
        SELECT 431910, 'Mujimne','Sub-District','Nigeria' UNION ALL
        SELECT 180809, 'Muku','Sub-District','Nigeria' UNION ALL
        SELECT 430708, 'Mulgoi Kobchi','Sub-District','Nigeria' UNION ALL
        SELECT 430808, 'Muliye','Sub-District','Nigeria' UNION ALL
        SELECT 420217, 'Mun-Munsal','Sub-District','Nigeria' UNION ALL
        SELECT 221410, 'Mungadi','Sub-District','Nigeria' UNION ALL
        SELECT 200507, 'Muntsira','Sub-District','Nigeria' UNION ALL
        SELECT 360308, 'Murfakalam','Sub-District','Nigeria' UNION ALL
        SELECT 422014, 'Murmur North','Sub-District','Nigeria' UNION ALL
        SELECT 422015, 'Murmur South','Sub-District','Nigeria' UNION ALL
        SELECT 181010, 'Musari','Sub-District','Nigeria' UNION ALL
        SELECT 212909, 'Musawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 430206, 'Mussa','Sub-District','Nigeria' UNION ALL
        SELECT 432210, 'Musune','Sub-District','Nigeria' UNION ALL
        SELECT 360708, 'Mutai','Sub-District','Nigeria' UNION ALL
        SELECT 221207, 'Mutubari','Sub-District','Nigeria' UNION ALL
        SELECT 432211, 'Muwalli','Sub-District','Nigeria' UNION ALL
        SELECT 420412, 'Muzuwa','Sub-District','Nigeria' UNION ALL
        SELECT 420312, 'Mwari','Sub-District','Nigeria' UNION ALL
        SELECT 191809, 'N/Doya','Sub-District','Nigeria' UNION ALL
        SELECT 212509, 'Na''Amma','Sub-District','Nigeria' UNION ALL
        SELECT 370508, 'Nahuche','Sub-District','Nigeria' UNION ALL
        SELECT 202509, 'Naibawa','Sub-District','Nigeria' UNION ALL
        SELECT 192007, 'Nandu','Sub-District','Nigeria' UNION ALL
        SELECT 361209, 'Nangere (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 190207, 'Narayi','Sub-District','Nigeria' UNION ALL
        SELECT 202307, 'Nariya','Sub-District','Nigeria' UNION ALL
        SELECT 341008, 'Nasagudu','Sub-District','Nigeria' UNION ALL
        SELECT 421216, 'Nasarawa A','Sub-District','Nigeria' UNION ALL
        SELECT 421217, 'Nasarawa B','Sub-District','Nigeria' UNION ALL
        SELECT 220612, 'Nasarawa I','Sub-District','Nigeria' UNION ALL
        SELECT 220613, 'Nasarawa Ii','Sub-District','Nigeria' UNION ALL
        SELECT 421512, 'Nasaru A','Sub-District','Nigeria' UNION ALL
        SELECT 421513, 'Nasaru B','Sub-District','Nigeria' UNION ALL
        SELECT 190208, 'Nassarawa (Chikun)','Sub-District','Nigeria' UNION ALL
        SELECT 211409, 'Nassarawa (Funtua)','Sub-District','Nigeria' UNION ALL
        SELECT 420814, 'Nassarawa A','Sub-District','Nigeria' UNION ALL
        SELECT 420815, 'Nassarawa B','Sub-District','Nigeria' UNION ALL
        SELECT 370308, 'Nassarawa Godel East','Sub-District','Nigeria' UNION ALL
        SELECT 370309, 'Nassarawa Godel West','Sub-District','Nigeria' UNION ALL
        SELECT 370310, 'Nassarawa Mailayi','Sub-District','Nigeria' UNION ALL
        SELECT 370406, 'Nassarawa-Bkm','Sub-District','Nigeria' UNION ALL
        SELECT 370207, 'Nassarawa/Bka','Sub-District','Nigeria' UNION ALL
        SELECT 204107, 'Nata/Ala','Sub-District','Nigeria' UNION ALL
        SELECT 212410, 'Natselle','Sub-District','Nigeria' UNION ALL
        SELECT 221208, 'Nayelwa','Sub-District','Nigeria' UNION ALL
        SELECT 360309, 'Nayinawa','Sub-District','Nigeria' UNION ALL
        SELECT 432506, 'Ndufu','Sub-District','Nigeria' UNION ALL
        SELECT 190606, 'Nduya','Sub-District','Nigeria' UNION ALL
        SELECT 430207, 'Ng/Kopa','Sub-District','Nigeria' UNION ALL
        SELECT 432507, 'Ngala (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360407, 'Ngalda Dumbulwa','Sub-District','Nigeria' UNION ALL
        SELECT 431411, 'Ngamdu','Sub-District','Nigeria' UNION ALL
        SELECT 432011, 'Ngamma','Sub-District','Nigeria' UNION ALL
        SELECT 221508, 'Ngaski (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360512, 'Ngelzarma A.','Sub-District','Nigeria' UNION ALL
        SELECT 360513, 'Ngelzarma B.','Sub-District','Nigeria' UNION ALL
        SELECT 430909, 'Ngetra','Sub-District','Nigeria' UNION ALL
        SELECT 430208, 'Ngohi','Sub-District','Nigeria' UNION ALL
        SELECT 361409, 'Ngojin Alaraba','Sub-District','Nigeria' UNION ALL
        SELECT 432012, 'Ngubala B','Sub-District','Nigeria' UNION ALL
        SELECT 430809, 'Ngudoram','Sub-District','Nigeria' UNION ALL
        SELECT 430209, 'Ngulde','Sub-District','Nigeria' UNION ALL
        SELECT 360709, 'Ngurbuwa','Sub-District','Nigeria' UNION ALL
        SELECT 432408, 'Ngurno','Sub-District','Nigeria' UNION ALL
        SELECT 180411, 'Nguwa','Sub-District','Nigeria' UNION ALL
        SELECT 421514, 'Ningi East','Sub-District','Nigeria' UNION ALL
        SELECT 421515, 'Ningi West','Sub-District','Nigeria' UNION ALL
        SELECT 192008, 'Ninzo North','Sub-District','Nigeria' UNION ALL
        SELECT 192009, 'Ninzo South','Sub-District','Nigeria' UNION ALL
        SELECT 192010, 'Ninzo West','Sub-District','Nigeria' UNION ALL
        SELECT 360810, 'Njibilwa','Sub-District','Nigeria' UNION ALL
        SELECT 432212, 'Njine','Sub-District','Nigeria' UNION ALL
        SELECT 360310, 'Njiwaji / Gwange','Sub-District','Nigeria' UNION ALL
        SELECT 190607, 'Nok','Sub-District','Nigeria' UNION ALL
        SELECT 430709, 'Nzuda Wuyaram','Sub-District','Nigeria' UNION ALL
        SELECT 431311, 'Old Maiduguri','Sub-District','Nigeria' UNION ALL
        SELECT 190506, 'Paki','Sub-District','Nigeria' UNION ALL
        SELECT 190507, 'Pala','Sub-District','Nigeria' UNION ALL
        SELECT 421804, 'Palama','Sub-District','Nigeria' UNION ALL
        SELECT 420115, 'Pali East','Sub-District','Nigeria' UNION ALL
        SELECT 420116, 'Pali West','Sub-District','Nigeria' UNION ALL
        SELECT 431209, 'Pama/Waitam','Sub-District','Nigeria' UNION ALL
        SELECT 191509, 'Pambegua','Sub-District','Nigeria' UNION ALL
        SELECT 190308, 'Panhauya','Sub-District','Nigeria' UNION ALL
        SELECT 202510, 'Panshekara','Sub-District','Nigeria' UNION ALL
        SELECT 420510, 'Papa North','Sub-District','Nigeria' UNION ALL
        SELECT 420511, 'Papa South','Sub-District','Nigeria' UNION ALL
        SELECT 191411, 'Pari','Sub-District','Nigeria' UNION ALL
        SELECT 430609, 'Pemi','Sub-District','Nigeria' UNION ALL
        SELECT 220910, 'Peni Peni','Sub-District','Nigeria' UNION ALL
        SELECT 431807, 'Peta','Sub-District','Nigeria' UNION ALL
        SELECT 420611, 'Polchi','Sub-District','Nigeria' UNION ALL
        SELECT 420313, 'Project','Sub-District','Nigeria' UNION ALL
        SELECT 431210, 'Puba/Vidau','Sub-District','Nigeria' UNION ALL
        SELECT 431112, 'Pulka Bokko','Sub-District','Nigeria' UNION ALL
        SELECT 211105, 'R/Kaya A','Sub-District','Nigeria' UNION ALL
        SELECT 211106, 'R/Kaya B','Sub-District','Nigeria' UNION ALL
        SELECT 201408, 'Raba','Sub-District','Nigeria' UNION ALL
        SELECT 341206, 'Rabah (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 210608, 'Radda','Sub-District','Nigeria' UNION ALL
        SELECT 213309, 'Rade ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213310, 'Rade ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 370610, 'Rafi','Sub-District','Nigeria' UNION ALL
        SELECT 220107, 'Rafin Bauna','Sub-District','Nigeria' UNION ALL
        SELECT 213107, 'Rafin Iwa','Sub-District','Nigeria' UNION ALL
        SELECT 180810, 'Rafin Marke','Sub-District','Nigeria' UNION ALL
        SELECT 222106, 'Rafin Zuru','Sub-District','Nigeria' UNION ALL
        SELECT 420712, 'Raga','Sub-District','Nigeria' UNION ALL
        SELECT 421218, 'Ragwam','Sub-District','Nigeria' UNION ALL
        SELECT 220705, 'Raha/Mailseri','Sub-District','Nigeria' UNION ALL
        SELECT 200410, 'Rahama (Bebeji)','Sub-District','Nigeria' UNION ALL
        SELECT 192108, 'Rahama (Soba)','Sub-District','Nigeria' UNION ALL
        SELECT 421805, 'Rahama (Toro)','Sub-District','Nigeria' UNION ALL
        SELECT 341905, 'Raka','Sub-District','Nigeria' UNION ALL
        SELECT 191709, 'Raminkura','Sub-District','Nigeria' UNION ALL
        SELECT 190110, 'Randagi','Sub-District','Nigeria' UNION ALL
        SELECT 421907, 'Ranga A','Sub-District','Nigeria' UNION ALL
        SELECT 421908, 'Ranga B','Sub-District','Nigeria' UNION ALL
        SELECT 204206, 'Rangaza','Sub-District','Nigeria' UNION ALL
        SELECT 200411, 'Ranka','Sub-District','Nigeria' UNION ALL
        SELECT 431509, 'Rann','Sub-District','Nigeria' UNION ALL
        SELECT 203204, 'Rano (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 200412, 'Rantan','Sub-District','Nigeria' UNION ALL
        SELECT 341207, 'Rara','Sub-District','Nigeria' UNION ALL
        SELECT 421806, 'Rauta/Geji','Sub-District','Nigeria' UNION ALL
        SELECT 212205, 'Rawayau A','Sub-District','Nigeria' UNION ALL
        SELECT 212206, 'Rawayau B','Sub-District','Nigeria' UNION ALL
        SELECT 221908, 'Ribah/Machika','Sub-District','Nigeria' UNION ALL
        SELECT 421807, 'Ribina East','Sub-District','Nigeria' UNION ALL
        SELECT 421808, 'Ribina West','Sub-District','Nigeria' UNION ALL
        SELECT 192109, 'Richifa','Sub-District','Nigeria' UNION ALL
        SELECT 202607, 'Ridawa','Sub-District','Nigeria' UNION ALL
        SELECT 190209, 'Rido','Sub-District','Nigeria' UNION ALL
        SELECT 190409, 'Rigachikun','Sub-District','Nigeria' UNION ALL
        SELECT 202709, 'Rigar Duka','Sub-District','Nigeria' UNION ALL
        SELECT 190410, 'Rigasa','Sub-District','Nigeria' UNION ALL
        SELECT 370706, 'Rijiya','Sub-District','Nigeria' UNION ALL
        SELECT 341704, 'Rijiya  A','Sub-District','Nigeria' UNION ALL
        SELECT 341705, 'Rijiya  B','Sub-District','Nigeria' UNION ALL
        SELECT 221705, 'Rijiyar Kirya','Sub-District','Nigeria' UNION ALL
        SELECT 201207, 'Rijiyar Lemo','Sub-District','Nigeria' UNION ALL
        SELECT 204207, 'Rijiyar Zaki','Sub-District','Nigeria' UNION ALL
        SELECT 202811, 'Rikadawa','Sub-District','Nigeria' UNION ALL
        SELECT 340305, 'Rikina','Sub-District','Nigeria' UNION ALL
        SELECT 211610, 'Riko','Sub-District','Nigeria' UNION ALL
        SELECT 222107, 'Rikoto','Sub-District','Nigeria' UNION ALL
        SELECT 191209, 'Rimau','Sub-District','Nigeria' UNION ALL
        SELECT 340508, 'Rimawa','Sub-District','Nigeria' UNION ALL
        SELECT 212007, 'Rimaye','Sub-District','Nigeria' UNION ALL
        SELECT 213008, 'Rimi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 203608, 'Rimi (Sumaila)','Sub-District','Nigeria' UNION ALL
        SELECT 200307, 'Rimin Dako','Sub-District','Nigeria' UNION ALL
        SELECT 203308, 'Rimin Gado (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 182306, 'Ringim (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 182708, 'Ringim (Yankwashi)','Sub-District','Nigeria' UNION ALL
        SELECT 370208, 'Rini','Sub-District','Nigeria' UNION ALL
        SELECT 212809, 'Rinjin Idi','Sub-District','Nigeria' UNION ALL
        SELECT 201105, 'Ririwai','Sub-District','Nigeria' UNION ALL
        SELECT 421809, 'Rishi','Sub-District','Nigeria' UNION ALL
        SELECT 203406, 'Rogo Ruma','Sub-District','Nigeria' UNION ALL
        SELECT 203407, 'Rogo Sabon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 213407, 'Rogogo Cidari','Sub-District','Nigeria' UNION ALL
        SELECT 200308, 'Romo','Sub-District','Nigeria' UNION ALL
        SELECT 341807, 'Romon Sarki','Sub-District','Nigeria' UNION ALL
        SELECT 182407, 'Roni (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 181208, 'Rorau','Sub-District','Nigeria' UNION ALL
        SELECT 181509, 'Ruba','Sub-District','Nigeria' UNION ALL
        SELECT 340306, 'Rugar Amanawa','Sub-District','Nigeria' UNION ALL
        SELECT 340810, 'Rugar Gatti','Sub-District','Nigeria' UNION ALL
        SELECT 340307, 'Rugar Gidado','Sub-District','Nigeria' UNION ALL
        SELECT 211709, 'Rugoji','Sub-District','Nigeria' UNION ALL
        SELECT 360811, 'Ruhu','Sub-District','Nigeria' UNION ALL
        SELECT 371409, 'Rukudawa','Sub-District','Nigeria' UNION ALL
        SELECT 210309, 'Rumah','Sub-District','Nigeria' UNION ALL
        SELECT 181308, 'Rumfa','Sub-District','Nigeria' UNION ALL
        SELECT 190508, 'Rumi','Sub-District','Nigeria' UNION ALL
        SELECT 430210, 'Rumirgo C','Sub-District','Nigeria' UNION ALL
        SELECT 203609, 'Rumo','Sub-District','Nigeria' UNION ALL
        SELECT 213205, 'Runka ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213206, 'Runka ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 203205, 'Rurum - Tsohon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 203206, 'Rurum-Sabon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 341906, 'Ruwa Wuri','Sub-District','Nigeria' UNION ALL
        SELECT 370707, 'Ruwan B0Re-Gus','Sub-District','Nigeria' UNION ALL
        SELECT 203408, 'Ruwan Bago','Sub-District','Nigeria' UNION ALL
        SELECT 371209, 'Ruwan Bore/Mirkidi','Sub-District','Nigeria' UNION ALL
        SELECT 371010, 'Ruwan Duruwa','Sub-District','Nigeria' UNION ALL
        SELECT 371210, 'Ruwan Gizo','Sub-District','Nigeria' UNION ALL
        SELECT 211305, 'Ruwan Goda','Sub-District','Nigeria' UNION ALL
        SELECT 370407, 'Ruwan Jema','Sub-District','Nigeria' UNION ALL
        SELECT 212510, 'Ruwan Sanyi','Sub-District','Nigeria' UNION ALL
        SELECT 220108, 'S/Fada 1','Sub-District','Nigeria' UNION ALL
        SELECT 220109, 'S/Fada 11','Sub-District','Nigeria' UNION ALL
        SELECT 191005, 'S/Gari North','Sub-District','Nigeria' UNION ALL
        SELECT 191006, 'S/Gari South','Sub-District','Nigeria' UNION ALL
        SELECT 190608, 'Sab-Chem','Sub-District','Nigeria' UNION ALL
        SELECT 190609, 'Sab-Zuro','Sub-District','Nigeria' UNION ALL
        SELECT 201208, 'Saban Gari East','Sub-District','Nigeria' UNION ALL
        SELECT 181708, 'Sabaru','Sub-District','Nigeria' UNION ALL
        SELECT 220110, 'Sabiyal','Sub-District','Nigeria' UNION ALL
        SELECT 220706, 'Sabon Birni (Bunza)','Sub-District','Nigeria' UNION ALL
        SELECT 201909, 'Sabon Birni (Gwarzo)','Sub-District','Nigeria' UNION ALL
        SELECT 190411, 'Sabon Birni (Igabi)','Sub-District','Nigeria' UNION ALL
        SELECT 341109, 'Sabon Birni (Kware)','Sub-District','Nigeria' UNION ALL
        SELECT 341307, 'Sabon Birni (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 370107, 'Sabon Birni-Ank','Sub-District','Nigeria' UNION ALL
        SELECT 341808, 'Sabon Birni/Bakaya','Sub-District','Nigeria' UNION ALL
        SELECT 191710, 'Sabon Birnin/U/Bawa','Sub-District','Nigeria' UNION ALL
        SELECT 360107, 'Sabon Gari (Barde)','Sub-District','Nigeria' UNION ALL
        SELECT 190210, 'Sabon Gari (Chikun)','Sub-District','Nigeria' UNION ALL
        SELECT 211006, 'Sabon Gari (Daura)','Sub-District','Nigeria' UNION ALL
        SELECT 211410, 'Sabon Gari (Funtua)','Sub-District','Nigeria' UNION ALL
        SELECT 191608, 'Sabon Gari (Kudan)','Sub-District','Nigeria' UNION ALL
        SELECT 182207, 'Sabon Gari (Miga)','Sub-District','Nigeria' UNION ALL
        SELECT 204108, 'Sabon Gari (Tudun Wada)','Sub-District','Nigeria' UNION ALL
        SELECT 204408, 'Sabon Gari (Wudil)','Sub-District','Nigeria' UNION ALL
        SELECT 340509, 'Sabon Gari Dole','Sub-District','Nigeria' UNION ALL
        SELECT 361309, 'Sabon Gari Kanuri','Sub-District','Nigeria' UNION ALL
        SELECT 201209, 'Sabon Gari West','Sub-District','Nigeria' UNION ALL
        SELECT 370708, 'Sabon Gari-Gus','Sub-District','Nigeria' UNION ALL
        SELECT 181309, 'Sabon Garu','Sub-District','Nigeria' UNION ALL
        SELECT 420909, 'Sabon Sara A','Sub-District','Nigeria' UNION ALL
        SELECT 420910, 'Sabon Sara B','Sub-District','Nigeria' UNION ALL
        SELECT 190812, 'Sabon Sarki','Sub-District','Nigeria' UNION ALL
        SELECT 190211, 'Sabon Tasha','Sub-District','Nigeria' UNION ALL
        SELECT 213009, 'Sabongari','Sub-District','Nigeria' UNION ALL
        SELECT 191007, 'Sabongari West','Sub-District','Nigeria' UNION ALL
        SELECT 182609, 'Sabongari Yaya','Sub-District','Nigeria' UNION ALL
        SELECT 211306, 'Sabonlayi','Sub-District','Nigeria' UNION ALL
        SELECT 432611, 'Sabsabuwa','Sub-District','Nigeria' UNION ALL
        SELECT 213108, 'Sabuwa A','Sub-District','Nigeria' UNION ALL
        SELECT 213109, 'Sabuwa B','Sub-District','Nigeria' UNION ALL
        SELECT 211710, 'Sabuwar Kasa','Sub-District','Nigeria' UNION ALL
        SELECT 420512, 'Sade East','Sub-District','Nigeria' UNION ALL
        SELECT 420513, 'Sade West','Sub-District','Nigeria' UNION ALL
        SELECT 210609, 'Safana (Charanchi)','Sub-District','Nigeria' UNION ALL
        SELECT 213207, 'Safana (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421613, 'Safi','Sub-District','Nigeria' UNION ALL
        SELECT 341809, 'Saida /Goshe','Sub-District','Nigeria' UNION ALL
        SELECT 200809, 'Saidawa','Sub-District','Nigeria' UNION ALL
        SELECT 203207, 'Saji','Sub-District','Nigeria' UNION ALL
        SELECT 221609, 'Sakaba (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 221706, 'Sakace','Sub-District','Nigeria' UNION ALL
        SELECT 370809, 'Sakajiki','Sub-District','Nigeria' UNION ALL
        SELECT 203309, 'Sakara Tsa','Sub-District','Nigeria' UNION ALL
        SELECT 341907, 'Sakkai','Sub-District','Nigeria' UNION ALL
        SELECT 422016, 'Sakwa','Sub-District','Nigeria' UNION ALL
        SELECT 431211, 'Sakwa/Hema','Sub-District','Nigeria' UNION ALL
        SELECT 180611, 'Sakwaya','Sub-District','Nigeria' UNION ALL
        SELECT 340710, 'Salame','Sub-District','Nigeria' UNION ALL
        SELECT 181808, 'Saleri','Sub-District','Nigeria' UNION ALL
        SELECT 341908, 'Salewa','Sub-District','Nigeria' UNION ALL
        SELECT 220707, 'Salwai','Sub-District','Nigeria' UNION ALL
        SELECT 421516, 'Sama','Sub-District','Nigeria' UNION ALL
        SELECT 340107, 'Samama','Sub-District','Nigeria' UNION ALL
        SELECT 191909, 'Samaru','Sub-District','Nigeria' UNION ALL
        SELECT 370509, 'Samawa','Sub-District','Nigeria' UNION ALL
        SELECT 190610, 'Samban','Sub-District','Nigeria' UNION ALL
        SELECT 421614, 'Sambowal','Sub-District','Nigeria' UNION ALL
        SELECT 191711, 'Saminaka','Sub-District','Nigeria' UNION ALL
        SELECT 200810, 'San San','Sub-District','Nigeria' UNION ALL
        SELECT 182208, 'San Sani','Sub-District','Nigeria' UNION ALL
        SELECT 200610, 'Sanda','Sub-District','Nigeria' UNION ALL
        SELECT 213311, 'Sandamu (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341009, 'Sangi','Sub-District','Nigeria' UNION ALL
        SELECT 201810, 'Sani Mainagge','Sub-District','Nigeria' UNION ALL
        SELECT 370510, 'Sankalawa','Sub-District','Nigeria' UNION ALL
        SELECT 182307, 'Sankara','Sub-District','Nigeria' UNION ALL
        SELECT 182408, 'Sankau','Sub-District','Nigeria' UNION ALL
        SELECT 341810, 'Sanyinna','Sub-District','Nigeria' UNION ALL
        SELECT 341409, 'Sanyinnawal','Sub-District','Nigeria' UNION ALL
        SELECT 181109, 'Sara (Gwaram)','Sub-District','Nigeria' UNION ALL
        SELECT 213408, 'Sara (Zango)','Sub-District','Nigeria' UNION ALL
        SELECT 221411, 'Sarandosa','Sub-District','Nigeria' UNION ALL
        SELECT 201707, 'Sararin Gezawa','Sub-District','Nigeria' UNION ALL
        SELECT 203008, 'Sarbi','Sub-District','Nigeria' UNION ALL
        SELECT 190907, 'Sardauna','Sub-District','Nigeria' UNION ALL
        SELECT 200309, 'Sare-Sare','Sub-District','Nigeria' UNION ALL
        SELECT 201409, 'Sarina','Sub-District','Nigeria' UNION ALL
        SELECT 220209, 'Sarka','Sub-District','Nigeria' UNION ALL
        SELECT 341606, 'Sarkin Adar G/Igwai','Sub-District','Nigeria' UNION ALL
        SELECT 341605, 'Sarkin Adar Gandu','Sub-District','Nigeria' UNION ALL
        SELECT 360108, 'Sarkin Hausawa','Sub-District','Nigeria' UNION ALL
        SELECT 370810, 'Sarkin Mafara S/Baura','Sub-District','Nigeria' UNION ALL
        SELECT 341607, 'Sarkin Musulmi A','Sub-District','Nigeria' UNION ALL
        SELECT 341608, 'Sarkin Musulmi B','Sub-District','Nigeria' UNION ALL
        SELECT 211007, 'Sarkin Yara  A','Sub-District','Nigeria' UNION ALL
        SELECT 211008, 'Sarkin Yara  B','Sub-District','Nigeria' UNION ALL
        SELECT 421413, 'Sarma','Sub-District','Nigeria' UNION ALL
        SELECT 360311, 'Sasawa / Kabaru','Sub-District','Nigeria' UNION ALL
        SELECT 202909, 'Satame','Sub-District','Nigeria' UNION ALL
        SELECT 190509, 'Saulawa','Sub-District','Nigeria' UNION ALL
        SELECT 371211, 'Sauna Ruwan Gora','Sub-District','Nigeria' UNION ALL
        SELECT 220310, 'Sauwa','Sub-District','Nigeria' UNION ALL
        SELECT 221707, 'Sawashi','Sub-District','Nigeria' UNION ALL
        SELECT 190510, 'Saya Saya','Sub-District','Nigeria' UNION ALL
        SELECT 200209, 'Saya-Saya','Sub-District','Nigeria' UNION ALL
        SELECT 213110, 'Sayau','Sub-District','Nigeria' UNION ALL
        SELECT 212810, 'Sayaya','Sub-District','Nigeria' UNION ALL
        SELECT 200508, 'Saye','Sub-District','Nigeria' UNION ALL
        SELECT 180811, 'Sayori','Sub-District','Nigeria' UNION ALL
        SELECT 222108, 'Senchi','Sub-District','Nigeria' UNION ALL
        SELECT 190908, 'Shaba','Sub-District','Nigeria' UNION ALL
        SELECT 182507, 'Shabaru','Sub-District','Nigeria' UNION ALL
        SELECT 181209, 'Shafe','Sub-District','Nigeria' UNION ALL
        SELECT 431212, 'Shaffa','Sub-District','Nigeria' UNION ALL
        SELECT 341410, 'Shagari (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 201609, 'Shagogo','Sub-District','Nigeria' UNION ALL
        SELECT 202106, 'Shahuchi','Sub-District','Nigeria' UNION ALL
        SELECT 182108, 'Shaiya','Sub-District','Nigeria' UNION ALL
        SELECT 203508, 'Shakogi','Sub-District','Nigeria' UNION ALL
        SELECT 202608, 'Shamakawa','Sub-District','Nigeria' UNION ALL
        SELECT 371108, 'Shanawa','Sub-District','Nigeria' UNION ALL
        SELECT 221708, 'Shanga (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 432710, 'Shani (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 203509, 'Shanono (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 220512, 'Sharabi/Kinan Gulnai','Sub-District','Nigeria' UNION ALL
        SELECT 202107, 'Sharada','Sub-District','Nigeria' UNION ALL
        SELECT 430311, 'Shehuri (Bama)','Sub-District','Nigeria' UNION ALL
        SELECT 432508, 'Shehuri (Ngala)','Sub-District','Nigeria' UNION ALL
        SELECT 432114, 'Shehuri North','Sub-District','Nigeria' UNION ALL
        SELECT 432115, 'Shehuri South','Sub-District','Nigeria' UNION ALL
        SELECT 361509, 'Shekau','Sub-District','Nigeria' UNION ALL
        SELECT 211211, 'Shema','Sub-District','Nigeria' UNION ALL
        SELECT 221810, 'Shema/Daniya','Sub-District','Nigeria' UNION ALL
        SELECT 211307, 'Sheme','Sub-District','Nigeria' UNION ALL
        SELECT 201106, 'Shere','Sub-District','Nigeria' UNION ALL
        SELECT 202108, 'Sheshe','Sub-District','Nigeria' UNION ALL
        SELECT 431412, 'Shetimare','Sub-District','Nigeria' UNION ALL
        SELECT 210509, 'Shifdawa','Sub-District','Nigeria' UNION ALL
        SELECT 190309, 'Shika','Sub-District','Nigeria' UNION ALL
        SELECT 430610, 'Shikarkir','Sub-District','Nigeria' UNION ALL
        SELECT 340510, 'Shinaka','Sub-District','Nigeria' UNION ALL
        SELECT 212109, 'Shinkafi 1','Sub-District','Nigeria' UNION ALL
        SELECT 212110, 'Shinkafi 2','Sub-District','Nigeria' UNION ALL
        SELECT 371109, 'Shinkafi North','Sub-District','Nigeria' UNION ALL
        SELECT 371110, 'Shinkafi South','Sub-District','Nigeria' UNION ALL
        SELECT 421615, 'Shira (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341706, 'Shiyar Adar A','Sub-District','Nigeria' UNION ALL
        SELECT 341707, 'Shiyar Adar B','Sub-District','Nigeria' UNION ALL
        SELECT 341708, 'Shiyar Zamfara A','Sub-District','Nigeria' UNION ALL
        SELECT 341709, 'Shiyar Zamfara B','Sub-District','Nigeria' UNION ALL
        SELECT 421311, 'Shongo','Sub-District','Nigeria' UNION ALL
        SELECT 360408, 'Shoye Garin Abba','Sub-District','Nigeria' UNION ALL
        SELECT 340308, 'Shuni','Sub-District','Nigeria' UNION ALL
        SELECT 202609, 'Shuwaki (Kunchi)','Sub-District','Nigeria' UNION ALL
        SELECT 204109, 'Shuwaki (Tudun Wada)','Sub-District','Nigeria' UNION ALL
        SELECT 181910, 'Shuwarin','Sub-District','Nigeria' UNION ALL
        SELECT 340209, 'Sifawa/Lukuyawa','Sub-District','Nigeria' UNION ALL
        SELECT 431510, 'Sigal/Karche','Sub-District','Nigeria' UNION ALL
        SELECT 341510, 'Silame (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 430509, 'Silumthla','Sub-District','Nigeria' UNION ALL
        SELECT 182308, 'Sintilmawa','Sub-District','Nigeria' UNION ALL
        SELECT 211107, 'Sirika A','Sub-District','Nigeria' UNION ALL
        SELECT 211108, 'Sirika B','Sub-District','Nigeria' UNION ALL
        SELECT 421414, 'Sirko','Sub-District','Nigeria' UNION ALL
        SELECT 203610, 'Sitti','Sub-District','Nigeria' UNION ALL
        SELECT 192110, 'Soba (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 431608, 'Sojiri','Sub-District','Nigeria' UNION ALL
        SELECT 212709, 'Sonkaya','Sub-District','Nigeria' UNION ALL
        SELECT 340108, 'Soron Gabas','Sub-District','Nigeria' UNION ALL
        SELECT 340109, 'Soron Yamma','Sub-District','Nigeria' UNION ALL
        SELECT 430312, 'Soye','Sub-District','Nigeria' UNION ALL
        SELECT 360109, 'Sugum Tagali','Sub-District','Nigeria' UNION ALL
        SELECT 432612, 'Sugundure','Sub-District','Nigeria' UNION ALL
        SELECT 212008, 'Sukuntuni','Sub-District','Nigeria' UNION ALL
        SELECT 182508, 'Sule Tankarkar','Sub-District','Nigeria' UNION ALL
        SELECT 203611, 'Sumaila (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361708, 'Sumbar','Sub-District','Nigeria' UNION ALL
        SELECT 180307, 'Sundimina','Sub-District','Nigeria' UNION ALL
        SELECT 361510, 'Sungul Koka','Sub-District','Nigeria' UNION ALL
        SELECT 432409, 'Sure','Sub-District','Nigeria' UNION ALL
        SELECT 180308, 'Surko','Sub-District','Nigeria' UNION ALL
        SELECT 221811, 'Suru (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341909, 'Sutti/Kwaraga','Sub-District','Nigeria' UNION ALL
        SELECT 191008, 'T/Nupawa','Sub-District','Nigeria' UNION ALL
        SELECT 192309, 'T/Tukur','Sub-District','Nigeria' UNION ALL
        SELECT 191810, 'T/Wada (Makarfi)','Sub-District','Nigeria' UNION ALL
        SELECT 192310, 'T/Wada (Zaria)','Sub-District','Nigeria' UNION ALL
        SELECT 191009, 'T/Wada North','Sub-District','Nigeria' UNION ALL
        SELECT 191010, 'T/Wada South','Sub-District','Nigeria' UNION ALL
        SELECT 191609, 'Taba','Sub-District','Nigeria' UNION ALL
        SELECT 190111, 'Tabani','Sub-District','Nigeria' UNION ALL
        SELECT 212910, 'Tabanni/Yarraddau','Sub-District','Nigeria' UNION ALL
        SELECT 222109, 'Tadurga','Sub-District','Nigeria' UNION ALL
        SELECT 212009, 'Tafashiya / Nasarawa','Sub-District','Nigeria' UNION ALL
        SELECT 211308, 'Tafoki','Sub-District','Nigeria' UNION ALL
        SELECT 361110, 'Taganama','Sub-District','Nigeria' UNION ALL
        SELECT 182109, 'Tagoro','Sub-District','Nigeria' UNION ALL
        SELECT 201107, 'Tagwaye','Sub-District','Nigeria' UNION ALL
        SELECT 340210, 'Taka-Tuku','Sub-District','Nigeria' UNION ALL
        SELECT 203709, 'Takai (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 340511, 'Takakume','Sub-District','Nigeria' UNION ALL
        SELECT 341308, 'Takatsaba (Sabon Birni)','Sub-District','Nigeria' UNION ALL
        SELECT 182509, 'Takatsaba (Sule Tankakar)','Sub-District','Nigeria' UNION ALL
        SELECT 190712, 'Takau','Sub-District','Nigeria' UNION ALL
        SELECT 221311, 'Takware (Koko/Besse)','Sub-District','Nigeria' UNION ALL
        SELECT 221709, 'Takware (Shanga)','Sub-District','Nigeria' UNION ALL
        SELECT 180211, 'Takwasa','Sub-District','Nigeria' UNION ALL
        SELECT 421810, 'Tama','Sub-District','Nigeria' UNION ALL
        SELECT 210510, 'Tama/Daye','Sub-District','Nigeria' UNION ALL
        SELECT 203310, 'Tamawa','Sub-District','Nigeria' UNION ALL
        SELECT 340711, 'Tambakarka','Sub-District','Nigeria' UNION ALL
        SELECT 341811, 'Tambawal/Shinfiri','Sub-District','Nigeria' UNION ALL
        SELECT 204311, 'Tamburawan Gabas','Sub-District','Nigeria' UNION ALL
        SELECT 212710, 'Tamilo  A','Sub-District','Nigeria' UNION ALL
        SELECT 212711, 'Tamilo  B','Sub-District','Nigeria' UNION ALL
        SELECT 431911, 'Tamsum-Gamdua','Sub-District','Nigeria' UNION ALL
        SELECT 204312, 'Tanagar','Sub-District','Nigeria' UNION ALL
        SELECT 202710, 'Tanawa','Sub-District','Nigeria' UNION ALL
        SELECT 200909, 'Tanburawa','Sub-District','Nigeria' UNION ALL
        SELECT 210907, 'Tandama','Sub-District','Nigeria' UNION ALL
        SELECT 202910, 'Tangaji','Sub-District','Nigeria' UNION ALL
        SELECT 341910, 'Tangaza (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 191210, 'Tantatu','Sub-District','Nigeria' UNION ALL
        SELECT 421713, 'Tapshin','Sub-District','Nigeria' UNION ALL
        SELECT 341309, 'Tara','Sub-District','Nigeria' UNION ALL
        SELECT 202308, 'Tarai','Sub-District','Nigeria' UNION ALL
        SELECT 210409, 'Taramnawa/Bare','Sub-District','Nigeria' UNION ALL
        SELECT 420713, 'Taranka','Sub-District','Nigeria' UNION ALL
        SELECT 201306, 'Tarauni (Gabasawa)','Sub-District','Nigeria' UNION ALL
        SELECT 203807, 'Tarauni (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 422017, 'Tarbuwa','Sub-District','Nigeria' UNION ALL
        SELECT 200413, 'Tariwa','Sub-District','Nigeria' UNION ALL
        SELECT 420714, 'Tarmasuwa','Sub-District','Nigeria' UNION ALL
        SELECT 181809, 'Tasheguwa','Sub-District','Nigeria' UNION ALL
        SELECT 182110, 'Tashena (Malam Maduri)','Sub-District','Nigeria' UNION ALL
        SELECT 422018, 'Tashena (Zaki)','Sub-District','Nigeria' UNION ALL
        SELECT 204006, 'Tatsa','Sub-District','Nigeria' UNION ALL
        SELECT 201010, 'Tattarawa','Sub-District','Nigeria' UNION ALL
        SELECT 182610, 'Taura (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 420514, 'Tauya East','Sub-District','Nigeria' UNION ALL
        SELECT 420515, 'Tauya West','Sub-District','Nigeria' UNION ALL
        SELECT 191011, 'Television','Sub-District','Nigeria' UNION ALL
        SELECT 430408, 'Teli','Sub-District','Nigeria' UNION ALL
        SELECT 360812, 'Teteba','Sub-District','Nigeria' UNION ALL
        SELECT 340906, 'Tidi Bale','Sub-District','Nigeria' UNION ALL
        SELECT 421517, 'Tiffi','Sub-District','Nigeria' UNION ALL
        SELECT 220409, 'Tiggi','Sub-District','Nigeria' UNION ALL
        SELECT 361210, 'Tikau','Sub-District','Nigeria' UNION ALL
        SELECT 421811, 'Tilde','Sub-District','Nigeria' UNION ALL
        SELECT 220708, 'Tilli/Helama','Sub-District','Nigeria' UNION ALL
        SELECT 420218, 'Tirwun','Sub-District','Nigeria' UNION ALL
        SELECT 432013, 'Titiwa','Sub-District','Nigeria' UNION ALL
        SELECT 421909, 'Tiyin A','Sub-District','Nigeria' UNION ALL
        SELECT 421910, 'Tiyin B','Sub-District','Nigeria' UNION ALL
        SELECT 431413, 'Tobolo','Sub-District','Nigeria' UNION ALL
        SELECT 341208, 'Tofa (Rabah)','Sub-District','Nigeria' UNION ALL
        SELECT 182309, 'Tofa (Ringim)','Sub-District','Nigeria' UNION ALL
        SELECT 203910, 'Tofa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 421415, 'Tofu','Sub-District','Nigeria' UNION ALL
        SELECT 222004, 'Tondi','Sub-District','Nigeria' UNION ALL
        SELECT 182111, 'Toni Kutara','Sub-District','Nigeria' UNION ALL
        SELECT 342308, 'Torankawa','Sub-District','Nigeria' UNION ALL
        SELECT 200109, 'Toranke','Sub-District','Nigeria' UNION ALL
        SELECT 421812, 'Toro (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361608, 'Toshia','Sub-District','Nigeria' UNION ALL
        SELECT 340811, 'Tozai (Illela)','Sub-District','Nigeria' UNION ALL
        SELECT 340907, 'Tozai (Isa)','Sub-District','Nigeria' UNION ALL
        --SELECT 212001, 'Tsa/Magam','Sub-District','Nigeria' UNION ALL
        SELECT 340908, 'Tsabre','Sub-District','Nigeria' UNION ALL
        SELECT 340309, 'Tsafanade','Sub-District','Nigeria' UNION ALL
        SELECT 371307, 'Tsafe Central','Sub-District','Nigeria' UNION ALL
        SELECT 421616, 'Tsafi','Sub-District','Nigeria' UNION ALL
        SELECT 212611, 'Tsagem/Takusheyi','Sub-District','Nigeria' UNION ALL
        SELECT 213010, 'Tsagero','Sub-District','Nigeria' UNION ALL
        SELECT 210610, 'Tsakatsa','Sub-District','Nigeria' UNION ALL
        SELECT 341110, 'Tsaki/Walakae','Sub-District','Nigeria' UNION ALL
        SELECT 203009, 'Tsakiya','Sub-District','Nigeria' UNION ALL
        SELECT 200910, 'Tsakuwa (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
        SELECT 421219, 'Tsakuwa (Katagum)','Sub-District','Nigeria' UNION ALL
        SELECT 203010, 'Tsakuwa (Minjibir)','Sub-District','Nigeria' UNION ALL
        SELECT 182209, 'Tsakuwawa','Sub-District','Nigeria' UNION ALL
        SELECT 341310, 'Tsamaye','Sub-District','Nigeria' UNION ALL
        SELECT 341209, 'Tsamiya (Rabah)','Sub-District','Nigeria' UNION ALL
        SELECT 342009, 'Tsamiya (Tureta)','Sub-District','Nigeria' UNION ALL
        SELECT 201708, 'Tsamiya Babba','Sub-District','Nigeria' UNION ALL
        SELECT 210908, 'Tsangamawa','Sub-District','Nigeria' UNION ALL
        SELECT 181110, 'Tsangarwa','Sub-District','Nigeria' UNION ALL
        SELECT 200210, 'Tsangaya','Sub-District','Nigeria' UNION ALL
        SELECT 210209, 'Tsanni','Sub-District','Nigeria' UNION ALL
        SELECT 204007, 'Tsanyawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 181510, 'Tsarawa','Sub-District','Nigeria' UNION ALL
        SELECT 213208, 'Tsaskiya','Sub-District','Nigeria' UNION ALL
        SELECT 202412, 'Tsaudawa','Sub-District','Nigeria' UNION ALL
        SELECT 203510, 'Tsaure','Sub-District','Nigeria' UNION ALL
        SELECT 212207, 'Tsauri A','Sub-District','Nigeria' UNION ALL
        SELECT 212208, 'Tsauri B','Sub-District','Nigeria' UNION ALL
        SELECT 370910, 'Tsibiri','Sub-District','Nigeria' UNION ALL
        SELECT 180109, 'Tsidar','Sub-District','Nigeria' UNION ALL
        SELECT 210111, 'Tsiga/Makurdi','Sub-District','Nigeria' UNION ALL
        SELECT 181911, 'Tsirma','Sub-District','Nigeria' UNION ALL
        SELECT 340411, 'Tsitse','Sub-District','Nigeria' UNION ALL
        SELECT 361310, 'Tsohon  Nguru','Sub-District','Nigeria' UNION ALL
        SELECT 204110, 'Tsohon Gari','Sub-District','Nigeria' UNION ALL
        SELECT 431312, 'Tuba','Sub-District','Nigeria' UNION ALL
        SELECT 421312, 'Tubule','Sub-District','Nigeria' UNION ALL
        SELECT 204208, 'Tudun Fulani','Sub-District','Nigeria' UNION ALL
        SELECT 211411, 'Tudun Iya','Sub-District','Nigeria' UNION ALL
        SELECT 202206, 'Tudun Kaya','Sub-District','Nigeria' UNION ALL
        SELECT 340110, 'Tudun Kose','Sub-District','Nigeria' UNION ALL
        SELECT 221610, 'Tudun Kuka','Sub-District','Nigeria' UNION ALL
        SELECT 203110, 'Tudun Murtala','Sub-District','Nigeria' UNION ALL
        SELECT 202109, 'Tudun Nufawa','Sub-District','Nigeria' UNION ALL
        SELECT 341710, 'Tudun Wada  A','Sub-District','Nigeria' UNION ALL
        SELECT 341711, 'Tudun Wada  B','Sub-District','Nigeria' UNION ALL
        SELECT 211009, 'Tudun Wada (Daura)','Sub-District','Nigeria' UNION ALL
        SELECT 370709, 'Tudun Wada (Gusau)','Sub-District','Nigeria' UNION ALL
        SELECT 203111, 'Tudun Wada (Nassarawa)','Sub-District','Nigeria' UNION ALL
        SELECT 421911, 'Tudun Wada (Warji)','Sub-District','Nigeria' UNION ALL
        SELECT 212911, 'Tuge','Sub-District','Nigeria' UNION ALL
        SELECT 421813, 'Tulai','Sub-District','Nigeria' UNION ALL
        SELECT 340211, 'Tulluwa/Kulafasa','Sub-District','Nigeria' UNION ALL
        SELECT 361709, 'Tulotulo','Sub-District','Nigeria' UNION ALL
        SELECT 340610, 'Tulun Doya','Sub-District','Nigeria' UNION ALL
        SELECT 201709, 'Tumbau','Sub-District','Nigeria' UNION ALL
        SELECT 420715, 'Tumbi','Sub-District','Nigeria' UNION ALL
        SELECT 210810, 'Tumburkai A','Sub-District','Nigeria' UNION ALL
        SELECT 210811, 'Tumburkai B','Sub-District','Nigeria' UNION ALL
        SELECT 201011, 'Tumfafi (Dawakin Tofa)','Sub-District','Nigeria' UNION ALL
        SELECT 421617, 'Tumfafi (Shira)','Sub-District','Nigeria' UNION ALL
        SELECT 182409, 'Tunas','Sub-District','Nigeria' UNION ALL
        SELECT 220709, 'Tunga (Bunza)','Sub-District','Nigeria' UNION ALL
        SELECT 342211, 'Tunga (Wurno)','Sub-District','Nigeria' UNION ALL
        SELECT 341111, 'Tungar Mallamawa','Sub-District','Nigeria' UNION ALL
        SELECT 340310, 'Tuntubetsefe','Sub-District','Nigeria' UNION ALL
        SELECT 181810, 'Turabu','Sub-District','Nigeria' UNION ALL
        SELECT 202207, 'Turawa (Karaye)','Sub-District','Nigeria' UNION ALL
        SELECT 192111, 'Turawa (Soba)','Sub-District','Nigeria' UNION ALL
        SELECT 340909, 'Turba','Sub-District','Nigeria' UNION ALL
        SELECT 182011, 'Turbus','Sub-District','Nigeria' UNION ALL
        SELECT 342010, 'Tureta (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 360409, 'Turmi Malluri','Sub-District','Nigeria' UNION ALL
        SELECT 341210, 'Tursa','Sub-District','Nigeria' UNION ALL
        SELECT 190412, 'Turunku','Sub-District','Nigeria' UNION ALL
        SELECT 430211, 'Uba','Sub-District','Nigeria' UNION ALL
        SELECT 370611, 'Uban Dawaki','Sub-District','Nigeria' UNION ALL
        SELECT 211010, 'Ubandawaki A','Sub-District','Nigeria' UNION ALL
        SELECT 211011, 'Ubandawaki B','Sub-District','Nigeria' UNION ALL
        SELECT 420716, 'Udubo Central','Sub-District','Nigeria' UNION ALL
        SELECT 420717, 'Udubo Norht East','Sub-District','Nigeria' UNION ALL
        SELECT 430810, 'Ufaye','Sub-District','Nigeria' UNION ALL
        SELECT 220614, 'Ujariyo','Sub-District','Nigeria' UNION ALL
        SELECT 203808, 'Ung Uku Cikin Gari','Sub-District','Nigeria' UNION ALL
        SELECT 203809, 'Ung Uku Kauyen Alu','Sub-District','Nigeria' UNION ALL
        SELECT 192311, 'Ung. Fatika','Sub-District','Nigeria' UNION ALL
        SELECT 191910, 'Ung. Gabas','Sub-District','Nigeria' UNION ALL
        SELECT 181610, 'Ung. Jibrin','Sub-District','Nigeria' UNION ALL
        SELECT 192312, 'Ung. Juma','Sub-District','Nigeria' UNION ALL
        SELECT 191012, 'Ung. Sanusi','Sub-District','Nigeria' UNION ALL
        SELECT 210410, 'Ung.Rai','Sub-District','Nigeria' UNION ALL
        SELECT 204209, 'Ungogo (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 341010, 'Ungushi','Sub-District','Nigeria' UNION ALL
        SELECT 200110, 'Unguwar Bai','Sub-District','Nigeria' UNION ALL
        SELECT 190909, 'Unguwar Dosa','Sub-District','Nigeria' UNION ALL
        SELECT 200911, 'Unguwar Duniya','Sub-District','Nigeria' UNION ALL
        SELECT 202309, 'Unguwar Gai','Sub-District','Nigeria' UNION ALL
        SELECT 203810, 'Unguwar Gano','Sub-District','Nigeria' UNION ALL
        SELECT 202208, 'Unguwar Hajji','Sub-District','Nigeria' UNION ALL
        SELECT 341311, 'Unguwar Lalle','Sub-District','Nigeria' UNION ALL
        SELECT 190910, 'Unguwar Rimi (Kaduna North)','Sub-District','Nigeria' UNION ALL
        SELECT 202511, 'Unguwar Rimi (Kumbotso)','Sub-District','Nigeria' UNION ALL
        SELECT 203911, 'Unguwar Rimi (Tofa)','Sub-District','Nigeria' UNION ALL
        SELECT 190911, 'Unguwar Sarki','Sub-District','Nigeria' UNION ALL
        SELECT 190912, 'Unguwar Shanu','Sub-District','Nigeria' UNION ALL
        SELECT 201108, 'Unguwar Tsohuwa','Sub-District','Nigeria' UNION ALL
        SELECT 201910, 'Unguwar Tudu','Sub-District','Nigeria' UNION ALL
        SELECT 180309, 'Unguwar Ya','Sub-District','Nigeria' UNION ALL
        SELECT 181709, 'Ungwar Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 181710, 'Ungwar Gabas','Sub-District','Nigeria' UNION ALL
        SELECT 192206, 'Ungwar Gaiya','Sub-District','Nigeria' UNION ALL
        SELECT 192207, 'Ungwar Rimi','Sub-District','Nigeria' UNION ALL
        SELECT 181711, 'Ungwar Yamma','Sub-District','Nigeria' UNION ALL
        SELECT 180110, 'Unik','Sub-District','Nigeria' UNION ALL
        SELECT 204409, 'Utai','Sub-District','Nigeria' UNION ALL
        SELECT 221509, 'Utono','Sub-District','Nigeria' UNION ALL
        SELECT 430212, 'Uvu Uda','Sub-District','Nigeria' UNION ALL
        SELECT 420911, 'Uzum','Sub-District','Nigeria' UNION ALL
        SELECT 340311, 'Wababe/Salau','Sub-District','Nigeria' UNION ALL
        SELECT 361009, 'Wachakal','Sub-District','Nigeria' UNION ALL
        SELECT 431808, 'Wada','Sub-District','Nigeria' UNION ALL
        SELECT 210310, 'Wagini','Sub-District','Nigeria' UNION ALL
        SELECT 360710, 'Wagir','Sub-District','Nigeria' UNION ALL
        SELECT 420516, 'Wahu','Sub-District','Nigeria' UNION ALL
        SELECT 421714, 'Wai A','Sub-District','Nigeria' UNION ALL
        SELECT 421715, 'Wai B','Sub-District','Nigeria' UNION ALL
        SELECT 202911, 'Wailare','Sub-District','Nigeria' UNION ALL
        SELECT 200509, 'Waire','Sub-District','Nigeria' UNION ALL
        SELECT 221909, 'Waje','Sub-District','Nigeria' UNION ALL
        SELECT 431414, 'Wajiro','Sub-District','Nigeria' UNION ALL
        SELECT 200414, 'Wak','Sub-District','Nigeria' UNION ALL
        SELECT 431113, 'Wala Warare','Sub-District','Nigeria' UNION ALL
        SELECT 432711, 'Walama','Sub-District','Nigeria' UNION ALL
        SELECT 342111, 'Wamakko','Sub-District','Nigeria' UNION ALL
        SELECT 430213, 'Wamdeeo G','Sub-District','Nigeria' UNION ALL
        SELECT 431010, 'Wamiri','Sub-District','Nigeria' UNION ALL
        SELECT 420612, 'Wandi','Sub-District','Nigeria' UNION ALL
        SELECT 421912, 'Wando','Sub-District','Nigeria' UNION ALL
        SELECT 201710, 'Wangara (Gezawa)','Sub-District','Nigeria' UNION ALL
        SELECT 203912, 'Wangara (Tofa)','Sub-District','Nigeria' UNION ALL
        SELECT 421313, 'Wanka','Sub-District','Nigeria' UNION ALL
        SELECT 370710, 'Wanke','Sub-District','Nigeria' UNION ALL
        SELECT 221510, 'Wara','Sub-District','Nigeria' UNION ALL
        SELECT 370108, 'Waramu','Sub-District','Nigeria' UNION ALL
        SELECT 204313, 'Warawa (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361010, 'Waro','Sub-District','Nigeria' UNION ALL
        SELECT 432509, 'Warshele','Sub-District','Nigeria' UNION ALL
        SELECT 192011, 'Wasa','Sub-District','Nigeria' UNION ALL
        SELECT 221910, 'Wasagu','Sub-District','Nigeria' UNION ALL
        SELECT 203011, 'Wasai','Sub-District','Nigeria' UNION ALL
        SELECT 431415, 'Wasaram','Sub-District','Nigeria' UNION ALL
        SELECT 361211, 'Watinane','Sub-District','Nigeria' UNION ALL
        SELECT 431809, 'Wawa','Sub-District','Nigeria' UNION ALL
        SELECT 430710, 'Wawa Korede','Sub-District','Nigeria' UNION ALL
        SELECT 190310, 'Wazata','Sub-District','Nigeria' UNION ALL
        SELECT 341609, 'Waziri A','Sub-District','Nigeria' UNION ALL
        SELECT 341610, 'Waziri B','Sub-District','Nigeria' UNION ALL
        SELECT 341611, 'Waziri C','Sub-District','Nigeria' UNION ALL
        SELECT 430611, 'Whuntaku','Sub-District','Nigeria' UNION ALL
        SELECT 370711, 'Wonaka','Sub-District','Nigeria' UNION ALL
        SELECT 421814, 'Wonu North','Sub-District','Nigeria' UNION ALL
        SELECT 421815, 'Wonu South','Sub-District','Nigeria' UNION ALL
        SELECT 192313, 'Wuciciri','Sub-District','Nigeria' UNION ALL
        SELECT 204410, 'Wudil (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 201610, 'Wudilawa','Sub-District','Nigeria' UNION ALL
        SELECT 432510, 'Wulgo','Sub-District','Nigeria' UNION ALL
        SELECT 432410, 'Wulo','Sub-District','Nigeria' UNION ALL
        SELECT 432511, 'Wurge','Sub-District','Nigeria' UNION ALL
        SELECT 212209, 'Wurma A','Sub-District','Nigeria' UNION ALL
        SELECT 212210, 'Wurma B','Sub-District','Nigeria' UNION ALL
        SELECT 180310, 'Wurno (Birnin Kudu)','Sub-District','Nigeria' UNION ALL
        SELECT 200310, 'Wuro Bagga','Sub-District','Nigeria' UNION ALL
        SELECT 221209, 'Wuro/Gauri','Sub-District','Nigeria' UNION ALL
        SELECT 370109, 'Wuya','Sub-District','Nigeria' UNION ALL
        SELECT 430409, 'Wuyo','Sub-District','Nigeria' UNION ALL
        SELECT 212511, 'Yaba','Sub-District','Nigeria' UNION ALL
        SELECT 431609, 'Yabal','Sub-District','Nigeria' UNION ALL
        SELECT 430313, 'Yabari','Sub-District','Nigeria' UNION ALL
        SELECT 342309, 'Yabo A','Sub-District','Nigeria' UNION ALL
        SELECT 342310, 'Yabo B','Sub-District','Nigeria' UNION ALL
        SELECT 204210, 'Yada Kunya','Sub-District','Nigeria' UNION ALL
        SELECT 201510, 'Yada Kwari','Sub-District','Nigeria' UNION ALL
        SELECT 431610, 'Yajiwa','Sub-District','Nigeria' UNION ALL
        SELECT 210909, 'Yakaji A','Sub-District','Nigeria' UNION ALL
        SELECT 210910, 'Yakaji B','Sub-District','Nigeria' UNION ALL
        SELECT 202110, 'Yakasai','Sub-District','Nigeria' UNION ALL
        SELECT 190311, 'Yakawada','Sub-District','Nigeria' UNION ALL
        SELECT 202413, 'Yako','Sub-District','Nigeria' UNION ALL
        SELECT 202812, 'Yakun','Sub-District','Nigeria' UNION ALL
        SELECT 200712, 'Yalawa (Dala)','Sub-District','Nigeria' UNION ALL
        SELECT 180709, 'Yalawa (Gagarawa)','Sub-District','Nigeria' UNION ALL
        SELECT 431611, 'Yale','Sub-District','Nigeria' UNION ALL
        SELECT 420816, 'Yali','Sub-District','Nigeria' UNION ALL
        SELECT 221911, 'Yalmo/Shindi/Wari','Sub-District','Nigeria' UNION ALL
        SELECT 181611, 'Yalo','Sub-District','Nigeria' UNION ALL
        SELECT 420117, 'Yalo 1','Sub-District','Nigeria' UNION ALL
        SELECT 420118, 'Yalo 2','Sub-District','Nigeria' UNION ALL
        SELECT 202414, 'Yalwa (Kiru)','Sub-District','Nigeria' UNION ALL
        SELECT 203208, 'Yalwa (Rano)','Sub-District','Nigeria' UNION ALL
        SELECT 203913, 'Yalwa Karama','Sub-District','Nigeria' UNION ALL
        SELECT 180311, 'Yalwan Damai','Sub-District','Nigeria' UNION ALL
        SELECT 203311, 'Yalwan Danziyal','Sub-District','Nigeria' UNION ALL
        SELECT 420413, 'Yame','Sub-District','Nigeria' UNION ALL
        SELECT 211109, 'Yamel A','Sub-District','Nigeria' UNION ALL
        SELECT 211110, 'Yamel B','Sub-District','Nigeria' UNION ALL
        SELECT 212111, 'Yamma 1','Sub-District','Nigeria' UNION ALL
        SELECT 212112, 'Yamma 2','Sub-District','Nigeria' UNION ALL
        SELECT 212512, 'Yammama','Sub-District','Nigeria' UNION ALL
        SELECT 201210, 'Yammata','Sub-District','Nigeria' UNION ALL
        SELECT 202209, 'Yammedi','Sub-District','Nigeria' UNION ALL
        SELECT 420219, 'Yamrat','Sub-District','Nigeria' UNION ALL
        SELECT 200912, 'Yan Barau','Sub-District','Nigeria' UNION ALL
        SELECT 204008, 'Yan Kamaye','Sub-District','Nigeria' UNION ALL
        SELECT 211309, 'Yan Kara','Sub-District','Nigeria' UNION ALL
        SELECT 421618, 'Yana','Sub-District','Nigeria' UNION ALL
        SELECT 371410, 'Yanbuki/Dutsi','Sub-District','Nigeria' UNION ALL
        SELECT 420414, 'Yanda','Sub-District','Nigeria' UNION ALL
        SELECT 202610, 'Yandadi','Sub-District','Nigeria' UNION ALL
        SELECT 211809, 'Yandaki','Sub-District','Nigeria' UNION ALL
        SELECT 204314, 'Yandalla','Sub-District','Nigeria' UNION ALL
        SELECT 182510, 'Yandamo','Sub-District','Nigeria' UNION ALL
        SELECT 211510, 'Yandoma','Sub-District','Nigeria' UNION ALL
        SELECT 182210, 'Yandona','Sub-District','Nigeria' UNION ALL
        SELECT 371308, 'Yandoton Daji','Sub-District','Nigeria' UNION ALL
        SELECT 210411, 'Yanduna','Sub-District','Nigeria' UNION ALL
        SELECT 182310, 'Yandutse','Sub-District','Nigeria' UNION ALL
        SELECT 340910, 'Yanfako','Sub-District','Nigeria' UNION ALL
        SELECT 211611, 'Yangaiya','Sub-District','Nigeria' UNION ALL
        SELECT 421112, 'Yangamai','Sub-District','Nigeria' UNION ALL
        SELECT 204009, 'Yanganau','Sub-District','Nigeria' UNION ALL
        SELECT 204315, 'Yangizo','Sub-District','Nigeria' UNION ALL
        SELECT 210511, 'Yangora','Sub-District','Nigeria' UNION ALL
        SELECT 211810, 'Yanhoho','Sub-District','Nigeria' UNION ALL
        SELECT 370811, 'Yankaba','Sub-District','Nigeria' UNION ALL
        SELECT 200913, 'Yankatsari','Sub-District','Nigeria' UNION ALL
        SELECT 181310, 'Yankoli','Sub-District','Nigeria' UNION ALL
        SELECT 371309, 'Yankuzo A','Sub-District','Nigeria' UNION ALL
        SELECT 371310, 'Yankuzo B','Sub-District','Nigeria' UNION ALL
        SELECT 182709, 'Yankwashi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 200510, 'Yanlami','Sub-District','Nigeria' UNION ALL
        SELECT 210412, 'Yanmaulu','Sub-District','Nigeria' UNION ALL
        SELECT 203914, 'Yanoko','Sub-District','Nigeria' UNION ALL
        SELECT 210710, 'Yantumaki A','Sub-District','Nigeria' UNION ALL
        SELECT 210711, 'Yantumaki B','Sub-District','Nigeria' UNION ALL
        SELECT 371311, 'Yanware','Sub-District','Nigeria' UNION ALL
        SELECT 182410, 'Yanzaki','Sub-District','Nigeria' UNION ALL
        SELECT 213409, 'Yar Daje','Sub-District','Nigeria' UNION ALL
        SELECT 221710, 'Yarbesse','Sub-District','Nigeria' UNION ALL
        SELECT 210210, 'Yargamji','Sub-District','Nigeria' UNION ALL
        SELECT 200914, 'Yargaya','Sub-District','Nigeria' UNION ALL
        SELECT 370209, 'Yargeda','Sub-District','Nigeria' UNION ALL
        SELECT 211909, 'Yargoje','Sub-District','Nigeria' UNION ALL
        SELECT 203915, 'Yarimawa','Sub-District','Nigeria' UNION ALL
        SELECT 370210, 'Yarkofoji','Sub-District','Nigeria' UNION ALL
        SELECT 211310, 'Yarmalamai','Sub-District','Nigeria' UNION ALL
        SELECT 370110, 'Yarsabaya','Sub-District','Nigeria' UNION ALL
        SELECT 341211, 'Yartsakkuwa','Sub-District','Nigeria' UNION ALL
        SELECT 211910, 'Yartsamiya','Sub-District','Nigeria' UNION ALL
        SELECT 204111, 'Yaryasa','Sub-District','Nigeria' UNION ALL
        SELECT 212309, 'Yashe  A','Sub-District','Nigeria' UNION ALL
        SELECT 212310, 'Yashe B','Sub-District','Nigeria' UNION ALL
        SELECT 370408, 'Yashi','Sub-District','Nigeria' UNION ALL
        SELECT 430108, 'Yau','Sub-District','Nigeria' UNION ALL
        SELECT 201307, 'Yautar Arewa','Sub-District','Nigeria' UNION ALL
        SELECT 201308, 'Yautar Kudu','Sub-District','Nigeria' UNION ALL
        SELECT 420517, 'Yautare','Sub-District','Nigeria' UNION ALL
        SELECT 210311, 'Yauyau/Malamawa','Sub-District','Nigeria' UNION ALL
        SELECT 430109, 'Yawa','Sub-District','Nigeria' UNION ALL
        SELECT 430510, 'Yawi','Sub-District','Nigeria' UNION ALL
        SELECT 211511, 'Yaya/Bidore','Sub-District','Nigeria' UNION ALL
        SELECT 420415, 'Yayari (Damban)','Sub-District','Nigeria' UNION ALL
        SELECT 181311, 'Yayari (Hadejia)','Sub-District','Nigeria' UNION ALL
        SELECT 180510, 'Yayari Tukur','Sub-District','Nigeria' UNION ALL
        SELECT 421220, 'Yayu','Sub-District','Nigeria' UNION ALL
        SELECT 220210, 'Yeldu','Sub-District','Nigeria' UNION ALL
        SELECT 432411, 'Yele','Sub-District','Nigeria' UNION ALL
        SELECT 190212, 'Yelwa','Sub-District','Nigeria' UNION ALL
        SELECT 222005, 'Yelwa Central','Sub-District','Nigeria' UNION ALL
        SELECT 222006, 'Yelwa East','Sub-District','Nigeria' UNION ALL
        SELECT 222007, 'Yelwa North','Sub-District','Nigeria' UNION ALL
        SELECT 222008, 'Yelwa South','Sub-District','Nigeria' UNION ALL
        SELECT 222009, 'Yelwa West','Sub-District','Nigeria' UNION ALL
        SELECT 361410, 'Yerimaram','Sub-District','Nigeria' UNION ALL
        SELECT 431810, 'Yimirdalong','Sub-District','Nigeria' UNION ALL
        SELECT 430110, 'Yituwa','Sub-District','Nigeria' UNION ALL
        SELECT 220410, 'Yola (Augie)','Sub-District','Nigeria' UNION ALL
        SELECT 181210, 'Yola (Gwiwa)','Sub-District','Nigeria' UNION ALL
        SELECT 421113, 'Yola (Jama''Are)','Sub-District','Nigeria' UNION ALL
        SELECT 202210, 'Yola (Karaye)','Sub-District','Nigeria' UNION ALL
        SELECT 431710, 'Yoyo','Sub-District','Nigeria' UNION ALL
        SELECT 420119, 'Yuli','Sub-District','Nigeria' UNION ALL
        SELECT 201309, 'Yumbu','Sub-District','Nigeria' UNION ALL
        SELECT 361609, 'Yunusari (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 361710, 'Yusufarri','Sub-District','Nigeria' UNION ALL
        SELECT 421518, 'Yuwa','Sub-District','Nigeria' UNION ALL
        SELECT 432309, 'Z. Umorti','Sub-District','Nigeria' UNION ALL
        SELECT 420912, 'Zabi (Giade)','Sub-District','Nigeria' UNION ALL
        SELECT 191510, 'Zabi (Kubau)','Sub-District','Nigeria' UNION ALL
        SELECT 191610, 'Zabi (Kudan)','Sub-District','Nigeria' UNION ALL
        SELECT 191911, 'Zabi (Sabon Gari)','Sub-District','Nigeria' UNION ALL
        SELECT 360910, 'Zabudum/ Dachia','Sub-District','Nigeria' UNION ALL
        SELECT 421416, 'Zadawa','Sub-District','Nigeria' UNION ALL
        SELECT 432213, 'Zaga','Sub-District','Nigeria' UNION ALL
        SELECT 220513, 'Zagga/Kwasara','Sub-District','Nigeria' UNION ALL
        SELECT 201109, 'Zainabi','Sub-District','Nigeria' UNION ALL
        SELECT 202111, 'Zaitawa','Sub-District','Nigeria' UNION ALL
        SELECT 361610, 'Zajibiriri/Dumbol','Sub-District','Nigeria' UNION ALL
        SELECT 201410, 'Zakarawa','Sub-District','Nigeria' UNION ALL
        SELECT 201310, 'Zakirai','Sub-District','Nigeria' UNION ALL
        SELECT 213209, 'Zakka ''A''','Sub-District','Nigeria' UNION ALL
        SELECT 213210, 'Zakka ''B''','Sub-District','Nigeria' UNION ALL
        SELECT 421816, 'Zalau','Sub-District','Nigeria' UNION ALL
        SELECT 192208, 'Zaman Dabo','Sub-District','Nigeria' UNION ALL
        SELECT 222010, 'Zamare','Sub-District','Nigeria' UNION ALL
        SELECT 360410, 'Zamba Mazawun','Sub-District','Nigeria' UNION ALL
        SELECT 181111, 'Zandam Nagogo','Sub-District','Nigeria' UNION ALL
        SELECT 430314, 'Zangeri','Sub-District','Nigeria' UNION ALL
        SELECT 201711, 'Zango (Gezawa)','Sub-District','Nigeria' UNION ALL
        SELECT 180911, 'Zango (Gumel)','Sub-District','Nigeria' UNION ALL
        SELECT 211911, 'Zango (Kankara)','Sub-District','Nigeria' UNION ALL
        SELECT 202112, 'Zango (Kano Municipal)','Sub-District','Nigeria' UNION ALL
        SELECT 213410, 'Zango (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 204211, 'Zango (Ungogo)','Sub-District','Nigeria' UNION ALL
        SELECT 181511, 'Zango Kura','Sub-District','Nigeria' UNION ALL
        SELECT 192209, 'Zango Urban','Sub-District','Nigeria' UNION ALL
        SELECT 190413, 'Zangon Aya','Sub-District','Nigeria' UNION ALL
        SELECT 203312, 'Zangon Dan Abdu','Sub-District','Nigeria' UNION ALL
        SELECT 191310, 'Zankan','Sub-District','Nigeria' UNION ALL
        SELECT 430410, 'Zara','Sub-District','Nigeria' UNION ALL
        SELECT 180710, 'Zarada','Sub-District','Nigeria' UNION ALL
        SELECT 421817, 'Zaranda','Sub-District','Nigeria' UNION ALL
        SELECT 430511, 'Zarawuyaki','Sub-District','Nigeria' UNION ALL
        SELECT 182211, 'Zareku','Sub-District','Nigeria' UNION ALL
        SELECT 203409, 'Zarewa','Sub-District','Nigeria' UNION ALL
        SELECT 432310, 'Zari','Sub-District','Nigeria' UNION ALL
        SELECT 221312, 'Zaria/Amiru','Sub-District','Nigeria' UNION ALL
        SELECT 204010, 'Zarogi','Sub-District','Nigeria' UNION ALL
        SELECT 370409, 'Zarummai','Sub-District','Nigeria' UNION ALL
        SELECT 370410, 'Zauma (Bukkuyum)','Sub-District','Nigeria' UNION ALL
        SELECT 181211, 'Zauma (Gwiwa)','Sub-District','Nigeria' UNION ALL
        SELECT 420416, 'Zaura','Sub-District','Nigeria' UNION ALL
        SELECT 220615, 'Zauru','Sub-District','Nigeria' UNION ALL
        SELECT 220311, 'Zazzagawa','Sub-District','Nigeria' UNION ALL
        SELECT 431912, 'Zengebe','Sub-District','Nigeria' UNION ALL
        SELECT 360110, 'Zengo','Sub-District','Nigeria' UNION ALL
        SELECT 420718, 'Zindiwa','Sub-District','Nigeria' UNION ALL
        SELECT 203209, 'Zinyau','Sub-District','Nigeria' UNION ALL
        SELECT 420913, 'Zirami','Sub-District','Nigeria' UNION ALL
        SELECT 222110, 'Zodi','Sub-District','Nigeria' UNION ALL
        SELECT 200915, 'Zogarawa','Sub-District','Nigeria' UNION ALL
        SELECT 220710, 'Zogirma','Sub-District','Nigeria' UNION ALL
        SELECT 192210, 'Zonkwa','Sub-District','Nigeria' UNION ALL
        SELECT 192211, 'Zonzon','Sub-District','Nigeria' UNION ALL
        SELECT 430910, 'Zowo','Sub-District','Nigeria' UNION ALL
        SELECT 203410, 'Zoza','Sub-District','Nigeria' UNION ALL
        SELECT 421016, 'Zubiki','Sub-District','Nigeria' UNION ALL
        SELECT 421619, 'Zubo','Sub-District','Nigeria' UNION ALL
        SELECT 203710, 'Zuga','Sub-District','Nigeria' UNION ALL
        SELECT 201311, 'Zugachi','Sub-District','Nigeria' UNION ALL
        SELECT 182411, 'Zugai','Sub-District','Nigeria' UNION ALL
        SELECT 221210, 'Zuguru','Sub-District','Nigeria' UNION ALL
        SELECT 432412, 'Zulum','Sub-District','Nigeria' UNION ALL
        SELECT 420613, 'Zumbul','Sub-District','Nigeria' UNION ALL
        SELECT 182710, 'Zungumba','Sub-District','Nigeria' UNION ALL
        SELECT 420220, 'Zungur','Sub-District','Nigeria' UNION ALL
        SELECT 191511, 'Zuntu','Sub-District','Nigeria' UNION ALL
        SELECT 203210, 'Zurgau','Sub-District','Nigeria' UNION ALL
        SELECT 421913, 'Zurgwai','Sub-District','Nigeria' UNION ALL
        SELECT 371411, 'Zurmi (Sub-District)','Sub-District','Nigeria' UNION ALL
        SELECT 202415, 'Zuwo','Sub-District','Nigeria';

        INSERT INTO region
        (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)
        SELECT
             tng.region_name
            ,tng.region_code
            ,tng.region_code
            ,o.id
            ,rt.id
            ,pr.id
            ,now()
        FROM _tmp_ng_regions tng
        INNER JOIN office o
            ON o.name = 'Nigeria'
        INNER JOIN region_type rt
            ON tng.region_type = rt.name
            AND tng.region_type = 'Province'
        INNER JOIN region pr
            ON pr.name = 'Nigeria';

        INSERT INTO region
        (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)
        SELECT
            tng.region_name
            ,tng.region_code
            ,tng.region_code
            ,o.id
            ,rt.id
            ,pr.id
            ,now()
        FROM _tmp_ng_regions tng
        INNER JOIN office o
            ON o.name = 'Nigeria'
        INNER JOIN region_type rt
            ON tng.region_type = rt.name
            AND tng.region_type = 'District'
        INNER JOIN region pr
            ON LEFT(CAST(tng.region_code AS VARCHAR),2) = CAST(pr.region_code AS VARCHAR);

        INSERT INTO region
        (name,region_code,slug,office_id,region_type_id,parent_region_id,created_at)
        SELECT
             tng.region_name
            ,tng.region_code
            ,tng.region_code
            ,o.id
            ,rt.id
            ,pr.id
            ,now()
        FROM _tmp_ng_regions tng
        INNER JOIN office o
            ON o.name = 'Nigeria'
        INNER JOIN region_type rt
            ON tng.region_type = rt.name
            AND tng.region_type = 'Sub-District'
        INNER JOIN region pr
            ON LEFT(CAST(tng.region_code AS VARCHAR),4) = CAST(pr.region_code AS VARCHAR);

	INSERT INTO source_object_map
	(source_object_code,master_object_id,content_type,mapped_by_id)

	SELECT region_code, id, 'region' ,1 FROM region;
    """)
    ]
