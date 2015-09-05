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
            (created_by_id,docfile,guid,doc_title,created_at)
            SELECT id,'initialize-db','init_ng_regions','init_ng_regions',NOW()
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

          SELECT 'NG001042000000000000', 'Bauchi (Province)','Province','Nigeria' UNION ALL
          SELECT 'NG001043000000000000', 'Borno','Province','Nigeria' UNION ALL
          SELECT 'NG001018000000000000', 'Jigawa (Province)','Province','Nigeria' UNION ALL
          SELECT 'NG001019000000000000', 'Kaduna','Province','Nigeria' UNION ALL
          SELECT 'NG001020000000000000', 'Kano','Province','Nigeria' UNION ALL
          SELECT 'NG001022000000000000', 'Kebbi','Province','Nigeria' UNION ALL
          SELECT 'NG001034000000000000', 'Sokoto','Province','Nigeria' UNION ALL
          SELECT 'NG001036000000000000', 'Yobe','Province','Nigeria' UNION ALL
          SELECT 'NG001037000000000000', 'Zamfara','Province','Nigeria' UNION ALL
          SELECT 'NG001021000000000000', 'Katsina','Province','Nigeria' UNION ALL
          SELECT 'NG001043010000000000', 'Abadam','District','Nigeria' UNION ALL
          SELECT 'NG001020010000000000', 'Ajingi (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020020000000000', 'Albasu (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001022010000000000', 'Aleiro','District','Nigeria' UNION ALL
          SELECT 'NG001042010000000000', 'Alkaleri','District','Nigeria' UNION ALL
          SELECT 'NG001037010000000000', 'Anka','District','Nigeria' UNION ALL
          SELECT 'NG001022020000000000', 'Arewa Dandi','District','Nigeria' UNION ALL
          SELECT 'NG001022030000000000', 'Argungu','District','Nigeria' UNION ALL
          SELECT 'NG001043020000000000', 'Askira/Uba','District','Nigeria' UNION ALL
          SELECT 'NG001022040000000000', 'Augie','District','Nigeria' UNION ALL
          SELECT 'NG001018010000000000', 'Auyo (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020040000000000', 'b (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018020000000000', 'Babura (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001022050000000000', 'Bagudo','District','Nigeria' UNION ALL
          SELECT 'NG001020030000000000', 'Bagwai (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001021010000000000', 'Bakori','District','Nigeria' UNION ALL
          SELECT 'NG001037020000000000', 'Bakura (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001043030000000000', 'Bama','District','Nigeria' UNION ALL
          SELECT 'NG001036010000000000', 'Barde (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001021020000000000', 'Batagarawa (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001021030000000000', 'Batsari (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001042020000000000', 'Bauchi (District)','District','Nigeria' UNION ALL
          SELECT 'NG001021040000000000', 'Baure (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001043040000000000', 'Bayo','District','Nigeria' UNION ALL
          SELECT 'NG001020050000000000', 'Bichi (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001021050000000000', 'Bindawa (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001034010000000000', 'Binji (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001019010000000000', 'Birnin Gwari','District','Nigeria' UNION ALL
          SELECT 'NG001022060000000000', 'Birnin Kebbi','District','Nigeria' UNION ALL
          SELECT 'NG001018030000000000', 'Birnin Kudu (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001037030000000000', 'Birnin Magaji/Kiyaw','District','Nigeria' UNION ALL
          SELECT 'NG001018040000000000', 'Birniwa (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001043050000000000', 'Biu','District','Nigeria' UNION ALL
          SELECT 'NG001034020000000000', 'Bodinga','District','Nigeria' UNION ALL
          SELECT 'NG001042030000000000', 'Bogoro (Bauchi)','District','Nigeria' UNION ALL
          SELECT 'NG001036020000000000', 'Borsari','District','Nigeria' UNION ALL
          SELECT 'NG001018050000000000', 'Buji (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001037040000000000', 'Bukkuyum (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001037050000000000', 'Bungudu (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001020060000000000', 'Bunkure (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001022070000000000', 'Bunza','District','Nigeria' UNION ALL
          SELECT 'NG001021060000000000', 'Charanchi (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001043060000000000', 'Chibok','District','Nigeria' UNION ALL
          SELECT 'NG001019020000000000', 'Chikun (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001020070000000000', 'Dala (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001036030000000000', 'Damaturu','District','Nigeria' UNION ALL
          SELECT 'NG001042040000000000', 'Damban','District','Nigeria' UNION ALL
          SELECT 'NG001020080000000000', 'Dambatta','District','Nigeria' UNION ALL
          SELECT 'NG001043070000000000', 'Damboa (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001021070000000000', 'Dan Musa','District','Nigeria' UNION ALL
          SELECT 'NG001022080000000000', 'Dandi (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001021080000000000', 'Dandume','District','Nigeria' UNION ALL
          SELECT 'NG001034030000000000', 'Dange-Shuni','District','Nigeria' UNION ALL
          SELECT 'NG001021090000000000', 'Danja','District','Nigeria' UNION ALL
          SELECT 'NG001042050000000000', 'Darazo','District','Nigeria' UNION ALL
          SELECT 'NG001042060000000000', 'Dass','District','Nigeria' UNION ALL
          SELECT 'NG001021100000000000', 'Daura (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001020090000000000', 'Dawakin Kudu','District','Nigeria' UNION ALL
          SELECT 'NG001020100000000000', 'Dawakin Tofa','District','Nigeria' UNION ALL
          SELECT 'NG001043080000000000', 'Dikwa (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001020110000000000', 'Doguwa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018060000000000', 'Dutse','District','Nigeria' UNION ALL
          SELECT 'NG001021110000000000', 'Dutsi','District','Nigeria' UNION ALL
          SELECT 'NG001021120000000000', 'Dutsin Ma','District','Nigeria' UNION ALL
          SELECT 'NG001020120000000000', 'Fagge','District','Nigeria' UNION ALL
          SELECT 'NG001022090000000000', 'Fakai','District','Nigeria' UNION ALL
          SELECT 'NG001021130000000000', 'Faskari (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001036040000000000', 'Fika','District','Nigeria' UNION ALL
          SELECT 'NG001036050000000000', 'Fune','District','Nigeria' UNION ALL
          SELECT 'NG001021140000000000', 'Funtua','District','Nigeria' UNION ALL
          SELECT 'NG001020130000000000', 'Gabasawa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001034040000000000', 'Gada (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001018070000000000', 'Gagarawa','District','Nigeria' UNION ALL
          SELECT 'NG001042070000000000', 'Gamawa','District','Nigeria' UNION ALL
          SELECT 'NG001042080000000000', 'Ganjuwa','District','Nigeria' UNION ALL
          SELECT 'NG001018080000000000', 'Garki (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020140000000000', 'Garko (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020150000000000', 'Garun Malam (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020160000000000', 'Gaya','District','Nigeria' UNION ALL
          SELECT 'NG001036060000000000', 'Geidam','District','Nigeria' UNION ALL
          SELECT 'NG001020170000000000', 'Gezawa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001042090000000000', 'Giade','District','Nigeria' UNION ALL
          SELECT 'NG001019030000000000', 'Giwa (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001034050000000000', 'Goronyo (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001043090000000000', 'Gubio','District','Nigeria' UNION ALL
          SELECT 'NG001034060000000000', 'Gudu','District','Nigeria' UNION ALL
          SELECT 'NG001036070000000000', 'Gujba (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001036080000000000', 'Gulani (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001018090000000000', 'Gumel (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001037060000000000', 'Gummi','District','Nigeria' UNION ALL
          SELECT 'NG001018100000000000', 'Guri (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001037070000000000', 'Gusau (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001043100000000000', 'Guzamala','District','Nigeria' UNION ALL
          SELECT 'NG001034070000000000', 'Gwadabawa (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001020180000000000', 'Gwale (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001022100000000000', 'Gwandu','District','Nigeria' UNION ALL
          SELECT 'NG001018110000000000', 'Gwaram (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020190000000000', 'Gwarzo (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018120000000000', 'Gwiwa (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001043110000000000', 'Gwoza','District','Nigeria' UNION ALL
          SELECT 'NG001018130000000000', 'Hadejia','District','Nigeria' UNION ALL
          SELECT 'NG001043120000000000', 'Hawul','District','Nigeria' UNION ALL
          SELECT 'NG001019040000000000', 'Igabi (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001019050000000000', 'Ikara (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001034080000000000', 'Illela (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001021150000000000', 'Ingawa (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001034090000000000', 'Isa','District','Nigeria' UNION ALL
          SELECT 'NG001042100000000000', 'Itas/Gadau','District','Nigeria' UNION ALL
          SELECT 'NG001019060000000000', 'Jaba (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001018140000000000', 'Jahun (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001036090000000000', 'Jakusko (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001042110000000000', 'Jama''Are','District','Nigeria' UNION ALL
          SELECT 'NG001022110000000000', 'Jega','District','Nigeria' UNION ALL
          SELECT 'NG001019070000000000', 'Jema''A','District','Nigeria' UNION ALL
          SELECT 'NG001043130000000000', 'Jere','District','Nigeria' UNION ALL
          SELECT 'NG001021160000000000', 'Jibia','District','Nigeria' UNION ALL
          SELECT 'NG001020200000000000', 'Kabo (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001019080000000000', 'Kachia (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001019090000000000', 'Kaduna North','District','Nigeria' UNION ALL
          SELECT 'NG001019100000000000', 'Kaduna South','District','Nigeria' UNION ALL
          SELECT 'NG001018150000000000', 'Kafin Hausa (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001021170000000000', 'Kafur (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001043140000000000', 'Kaga','District','Nigeria' UNION ALL
          SELECT 'NG001019110000000000', 'Kagarko','District','Nigeria' UNION ALL
          SELECT 'NG001021180000000000', 'Kaita (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001019120000000000', 'Kajuru (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001043150000000000', 'Kala/Balge','District','Nigeria' UNION ALL
          SELECT 'NG001022120000000000', 'Kalgo (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001021190000000000', 'Kankara (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001021200000000000', 'Kankia','District','Nigeria' UNION ALL
          SELECT 'NG001020210000000000', 'Kano Municipal','District','Nigeria' UNION ALL
          SELECT 'NG001036100000000000', 'Karasuwa','District','Nigeria' UNION ALL
          SELECT 'NG001020220000000000', 'Karaye (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001042120000000000', 'Katagum (Bauchi)','District','Nigeria' UNION ALL
          SELECT 'NG001021210000000000', 'Katsina (District)','District','Nigeria' UNION ALL
          SELECT 'NG001018160000000000', 'Kaugama (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001019130000000000', 'Kaura (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001037080000000000', 'Kaura Namoda','District','Nigeria' UNION ALL
          SELECT 'NG001019140000000000', 'Kauru','District','Nigeria' UNION ALL
          SELECT 'NG001018170000000000', 'Kazaure','District','Nigeria' UNION ALL
          SELECT 'NG001034100000000000', 'Kebbe','District','Nigeria' UNION ALL
          SELECT 'NG001020230000000000', 'Kibiya','District','Nigeria' UNION ALL
          SELECT 'NG001042130000000000', 'Kirfi (Bauchi)','District','Nigeria' UNION ALL
          SELECT 'NG001018180000000000', 'Kiri Kasamma (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020240000000000', 'Kiru (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018190000000000', 'Kiyawa (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001022130000000000', 'Koko/Besse','District','Nigeria' UNION ALL
          SELECT 'NG001043160000000000', 'Konduga (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001019150000000000', 'Kubau (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001019160000000000', 'Kudan (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001043170000000000', 'Kukawa (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001020250000000000', 'Kumbotso (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020260000000000', 'Kunchi (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020270000000000', 'Kura (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001021220000000000', 'Kurfi','District','Nigeria' UNION ALL
          SELECT 'NG001021230000000000', 'Kusada (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001034110000000000', 'Kware (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001043180000000000', 'Kwaya Kusar (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001019170000000000', 'Lere (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001036110000000000', 'Machina (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001020280000000000', 'Madobi (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001043190000000000', 'Mafa (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001043200000000000', 'Magumeri (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001021240000000000', 'Mai''Adua','District','Nigeria' UNION ALL
          SELECT 'NG001043210000000000', 'Maiduguri','District','Nigeria' UNION ALL
          SELECT 'NG001018200000000000', 'Maigatari','District','Nigeria' UNION ALL
          SELECT 'NG001022140000000000', 'Maiyama (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001019180000000000', 'Makarfi (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001020290000000000', 'Makoda (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018210000000000', 'Malam Maduri (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001021250000000000', 'Malumfashi','District','Nigeria' UNION ALL
          SELECT 'NG001021260000000000', 'Mani (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001037090000000000', 'Maradun','District','Nigeria' UNION ALL
          SELECT 'NG001043220000000000', 'Marte (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001037100000000000', 'Maru (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001021270000000000', 'Mashi (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001021280000000000', 'Matazu','District','Nigeria' UNION ALL
          SELECT 'NG001018220000000000', 'Miga (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020300000000000', 'Minjibir (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001042140000000000', 'Misau','District','Nigeria' UNION ALL
          SELECT 'NG001043230000000000', 'Mobbar','District','Nigeria' UNION ALL
          SELECT 'NG001043240000000000', 'Monguno (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001021290000000000', 'Musawa (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001036120000000000', 'Nangere (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001020310000000000', 'Nassarawa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001043250000000000', 'Ngala (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001043260000000000', 'Nganzai','District','Nigeria' UNION ALL
          SELECT 'NG001022150000000000', 'Ngaski (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001036130000000000', 'Nguru','District','Nigeria' UNION ALL
          SELECT 'NG001042150000000000', 'Ningi','District','Nigeria' UNION ALL
          SELECT 'NG001036140000000000', 'Potiskum','District','Nigeria' UNION ALL
          SELECT 'NG001034120000000000', 'Rabah (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001020320000000000', 'Rano (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001021300000000000', 'Rimi (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001020330000000000', 'Rimin Gado (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001018230000000000', 'Ringim (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020340000000000', 'Rogo','District','Nigeria' UNION ALL
          SELECT 'NG001018240000000000', 'Roni (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001034130000000000', 'Sabon Birni (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001019190000000000', 'Sabon Gari (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001021310000000000', 'Sabuwa','District','Nigeria' UNION ALL
          SELECT 'NG001021320000000000', 'Safana (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001022160000000000', 'Sakaba (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001021330000000000', 'Sandamu (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001019200000000000', 'Sanga','District','Nigeria' UNION ALL
          SELECT 'NG001034140000000000', 'Shagari (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001022170000000000', 'Shanga (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001043270000000000', 'Shani (Borno)','District','Nigeria' UNION ALL
          SELECT 'NG001020350000000000', 'Shanono (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001037110000000000', 'Shinkafi','District','Nigeria' UNION ALL
          SELECT 'NG001042160000000000', 'Shira (Bauchi)','District','Nigeria' UNION ALL
          SELECT 'NG001034150000000000', 'Silame (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001019210000000000', 'Soba (Kaduna)','District','Nigeria' UNION ALL
          SELECT 'NG001034160000000000', 'Sokoto North','District','Nigeria' UNION ALL
          SELECT 'NG001034170000000000', 'Sokoto South','District','Nigeria' UNION ALL
          SELECT 'NG001018250000000000', 'Sule Tankakar','District','Nigeria' UNION ALL
          SELECT 'NG001020360000000000', 'Sumaila (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001022180000000000', 'Suru (Kebbi)','District','Nigeria' UNION ALL
          SELECT 'NG001042170000000000', 'Tafawa-Balewa','District','Nigeria' UNION ALL
          SELECT 'NG001020370000000000', 'Takai (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001037120000000000', 'Talata Mafara','District','Nigeria' UNION ALL
          SELECT 'NG001034180000000000', 'Tambuwal','District','Nigeria' UNION ALL
          SELECT 'NG001034190000000000', 'Tangaza (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001020380000000000', 'Tarauni (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001036150000000000', 'Tarmua','District','Nigeria' UNION ALL
          SELECT 'NG001018260000000000', 'Taura (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001020390000000000', 'Tofa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001042180000000000', 'Toro (Bauchi)','District','Nigeria' UNION ALL
          SELECT 'NG001037130000000000', 'Tsafe','District','Nigeria' UNION ALL
          SELECT 'NG001020400000000000', 'Tsanyawa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001020410000000000', 'Tudun Wada (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001034200000000000', 'Tureta (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001020420000000000', 'Ungogo (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001034210000000000', 'Wamako','District','Nigeria' UNION ALL
          SELECT 'NG001020430000000000', 'Warawa (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001042190000000000', 'Warji','District','Nigeria' UNION ALL
          SELECT 'NG001022190000000000', 'Wasagu/Danko','District','Nigeria' UNION ALL
          SELECT 'NG001020440000000000', 'Wudil (Kano)','District','Nigeria' UNION ALL
          SELECT 'NG001034220000000000', 'Wurno (Sokoto)','District','Nigeria' UNION ALL
          SELECT 'NG001034230000000000', 'Yabo','District','Nigeria' UNION ALL
          SELECT 'NG001018270000000000', 'Yankwashi (Jigawa)','District','Nigeria' UNION ALL
          SELECT 'NG001022200000000000', 'Yauri','District','Nigeria' UNION ALL
          SELECT 'NG001036160000000000', 'Yunusari (Yobe)','District','Nigeria' UNION ALL
          SELECT 'NG001036170000000000', 'Yusufari','District','Nigeria' UNION ALL
          SELECT 'NG001042200000000000', 'Zaki','District','Nigeria' UNION ALL
          SELECT 'NG001021340000000000', 'Zango (Katsina)','District','Nigeria' UNION ALL
          SELECT 'NG001019220000000000', 'Zangon Kataf','District','Nigeria' UNION ALL
          SELECT 'NG001019230000000000', 'Zaria','District','Nigeria' UNION ALL
          SELECT 'NG001037140000000000', 'Zurmi (Zamfara)','District','Nigeria' UNION ALL
          SELECT 'NG001022210000000000', 'Zuru','District','Nigeria' UNION ALL


            SELECT 'NG001019170100000000', 'Abadawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030100000000', 'Abadua/Kagara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060100000000', 'Abaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030100000000', 'Abbaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100100000000', 'Abdallawa (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180100000000', 'Abdallawa (Kaita)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200100000000', 'Aboro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300100000000', 'Abukur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100100000000', 'Abunabo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220100000000', 'Achida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440100000000', 'Achika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270100000000', 'Achilafiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040100000000', 'Adabka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160100000000', 'Adai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070100000000', 'Adakawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160100000000', 'Adamami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100200000000', 'Adiyani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100100000000', 'Aduwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040100000000', 'Afaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120100000000', 'Afogo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130100000000', 'Afunori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080100000000', 'Afuye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150100000000', 'Agayawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130100000000', 'Agban','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080100000000', 'Agunu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050100000000', 'Ahoto','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200100000000', 'Ai Yesku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260100000000', 'Ajaura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070100000000', 'Ajigin A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070200000000', 'Ajigin B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140100000000', 'Ajili','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010100000000', 'Ajingi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190100000000', 'Ajiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020100000000', 'Ajiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080100000000', 'Ajumawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140200000000', 'Akuyam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220100000000', 'Ala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220200000000', 'Ala-Lawanti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050100000000', 'Alagarno (Fune)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070100000000', 'Alagarno (Gamawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170100000000', 'Alagarno (Kukawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350100000000', 'Alajawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200100000000', 'Alangwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260100000000', 'Alarge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130100000000', 'Alau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020100000000', 'Albasu (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250100000000', 'Albasu (Sule Tankakar)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110100000000', 'Alelu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090100000000', 'Alhaji Barka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180100000000', 'Aljannare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010100000000', 'Alkaleri East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010200000000', 'Alkaleri West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220200000000', 'Alkammu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030100000000', 'Alwasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250200000000', 'Amanga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430100000000', 'Amarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200200000000', 'Amarmari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240100000000', 'Amaryawa 3','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060100000000', 'Ambursa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030200000000', 'Amchaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040100000000', 'Anadariya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150100000000', 'Anchau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030300000000', 'Andara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140100000000', 'Andarai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190100000000', 'Andaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160200000000', 'Andubun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140100000000', 'Ang. Ibrahim','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140200000000', 'Ang. Musa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080200000000', 'Ankwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080100000000', 'Araba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200200000000', 'Arak','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160100000000', 'Arbus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090100000000', 'Ardimini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200200000000', 'Ardoram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210100000000', 'Arewa 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210200000000', 'Arewa 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010100000000', 'Arge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150100000000', 'Ari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110100000000', 'Aribi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210100000000', 'Arki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210100000000', 'Arkilla','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230100000000', 'Asaga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070100000000', 'Asara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060100000000', 'Asheikiri  1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060200000000', 'Asheikiri  2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110100000000', 'Ashigashiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160200000000', 'Askandu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020100000000', 'Askira E','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070100000000', 'Asso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130100000000', 'Atafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100200000000', 'Atafowa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070200000000', 'Attakwanyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070200000000', 'Atuku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170100000000', 'Atuwo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050100000000', 'Auchan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040100000000', 'Augie North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040200000000', 'Augie South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140100000000', 'Aujara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160100000000', 'Auno','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010100000000', 'Auyakayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010200000000', 'Auyo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080300000000', 'Awon','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060100000000', 'Awulkiti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010300000000', 'Ayama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010400000000', 'Ayan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200300000000', 'Ayu (Sanga)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190100000000', 'Ayu (Wasagu/Danko)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070300000000', 'Azir Multe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300100000000', 'Azore','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040100000000', 'B/Mutum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180200000000', 'Ba''Awa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170100000000', 'Baauzini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240100000000', 'Baawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130100000000', 'Baba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320100000000', 'Baban Duhu ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320200000000', 'Baban Duhu ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150100000000', 'Babangida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170100000000', 'Babawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380100000000', 'Babban Giji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290100000000', 'Babbar Riga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020100000000', 'Babura (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410100000000', 'Baburi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020100000000', 'Bachaka (Arewa Dandi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060200000000', 'Bachaka (Gudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420100000000', 'Bachirawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240200000000', 'Badafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030100000000', 'Badagari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220300000000', 'Badairi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130200000000', 'Badara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090100000000', 'Badarawa (Kaduna North)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110100000000', 'Badarawa (Shinkafi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020100000000', 'Badau/Darhela','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100100000000', 'Badiko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210200000000', 'Bado','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260200000000', 'Badu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140100000000', 'Badurum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170200000000', 'Baga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120100000000', 'Bagagadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020200000000', 'Bagarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040300000000', 'Bagaye Meira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010100000000', 'Bagega','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060100000000', 'Bagel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180100000000', 'Bagida/Lukkingo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260100000000', 'Bagiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040200000000', 'Baguda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050100000000', 'Bagudo/Tuga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030100000000', 'Bagwai (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370100000000', 'Bagwaro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050200000000', 'Bahindi/Kaliel 1 (Bagudo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050300000000', 'Bahindi/Kaliel 2 (Bagudo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190100000000', 'Baima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090100000000', 'Bajida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230100000000', 'Bakale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120100000000', 'Bakin Kasuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070200000000', 'Bakin Ruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020200000000', 'Bakiyawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010100000000', 'Bakori A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010200000000', 'Bakori B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020100000000', 'Bakura (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180200000000', 'Bakuwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190200000000', 'Balago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160100000000', 'Balan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130200000000', 'Balanguwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200100000000', 'Balarabe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010200000000', 'Balare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060300000000', 'Balle (Geidam)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060300000000', 'Balle (Gudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150200000000', 'Balma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100300000000', 'Bambal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270100000000', 'Bamle','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180300000000', 'Bandan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080100000000', 'Banga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020300000000', 'Bangi/Dabaga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160300000000', 'Bangire','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090200000000', 'Bangu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050400000000', 'Bani/Tsamiya 1 (Bagudo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050500000000', 'Bani/Tsamiya 2 (Bagudo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080100000000', 'Banizumbu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110100000000', 'Bankanu/Rigakade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030400000000', 'Banki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010200000000', 'Banowa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060100000000', 'Banye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030200000000', 'Bar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080100000000', 'Bara (Gulani)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130300000000', 'Bara (Kirfi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240200000000', 'Baragumi 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170300000000', 'Barati','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020300000000', 'Barawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010200000000', 'Barayar Zaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060200000000', 'Baraza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180400000000', 'Barbarejo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040100000000', 'Barbaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070300000000', 'Barde (Jema''A)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010300000000', 'Barde/K/Kwaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060100000000', 'Bardoki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140100000000', 'Bare-Bari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090100000000', 'Bargaja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240300000000', 'Bargoni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270100000000', 'Bargu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180200000000', 'Barkeji/Nabaguda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220100000000', 'Barkiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060100000000', 'Barkum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100200000000', 'Barnawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110200000000', 'Basansan/Lemi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190100000000', 'Basawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150300000000', 'Bashe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180300000000', 'Bashire/Maikada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110100000000', 'Basirka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020400000000', 'Batagarawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020200000000', 'Bataiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020200000000', 'Batali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030200000000', 'Batsari (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040100000000', 'Batu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180100000000', 'Baturiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240400000000', 'Bauda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230100000000', 'Bauranya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320300000000', 'Baure ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320400000000', 'Baure ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040200000000', 'Baure 1 (Baure)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050100000000', 'Baure 2 (Bindawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020100000000', 'Bayamari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040400000000', 'Bayawa North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040500000000', 'Bayawa South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040300000000', 'Bebeji (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210100000000', 'Bedi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070400000000', 'Bego Karwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090200000000', 'Bekarya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050100000000', 'Bela/Rawayya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270200000000', 'Belas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340100000000', 'Beli (Rogo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160400000000', 'Beli (Shira)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190200000000', 'Bena','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230200000000', 'Bengaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130400000000', 'Beni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140100000000', 'Benisheikh','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150200000000', 'Beruruwa/Ruruma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130100000000', 'Besse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140300000000', 'Beti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050100000000', 'Bichi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120200000000', 'Bidir','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180100000000', 'Bilagusi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100100000000', 'Bilal Jawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130100000000', 'Bilbis','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120100000000', 'Bilingwi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100400000000', 'Bilkicheri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050200000000', 'Bindawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030100000000', 'Bindigari / Pawari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100100000000', 'Bindin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100200000000', 'Bingi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050200000000', 'Bingi North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050300000000', 'Bingi South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010100000000', 'Binji (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230300000000', 'Binjin Muza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220200000000', 'Birchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010300000000', 'Birin Gigyara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150200000000', 'Biriri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050100000000', 'Birjingo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030100000000', 'Birnin Kudu (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030100000000', 'Birnin Magaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060200000000', 'Birnin Magaji-Gmm','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230400000000', 'Birnin Ruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090300000000', 'Birnin Tudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040600000000', 'Birnin Tudu Gudale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020200000000', 'Birnin Tudu-Bka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060300000000', 'Birnin Tudu/Gmm','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150100000000', 'Birnin Yauri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040200000000', 'Birnin Yero (Igabi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110200000000', 'Birnin Yero (Shinkafi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040200000000', 'Birniwa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020100000000', 'Birshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080400000000', 'Bishini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110200000000', 'Bita Izge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140200000000', 'Bital','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060100000000', 'Bitaro/Dura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080200000000', 'Boboshe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030100000000', 'Bodai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020400000000', 'Bodinga/Tauma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110100000000', 'Bogo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030500000000', 'Bogomari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030300000000', 'Bogoro (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230200000000', 'Bogum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030400000000', 'Boi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200400000000', 'Bokana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230200000000', 'Boko (Kusada)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140100000000', 'Boko (Zurmi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140200000000', 'Bolewa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140300000000', 'Bolewa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210100000000', 'Bolori I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210200000000', 'Bolori Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190200000000', 'Bomo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130200000000', 'Bondong','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060200000000', 'Bono','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140200000000', 'Borgozo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250100000000', 'Borindawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060400000000', 'Borko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050200000000', 'Borno Kiji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200300000000', 'Borno Yesu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220400000000', 'Borsori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050200000000', 'Boyekai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040200000000', 'Briyel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040700000000', 'Bubuche','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120200000000', 'Buda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080100000000', 'Buduru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090100000000', 'Buduwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160100000000', 'Bugaje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030500000000', 'Bugun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260200000000', 'Bujawa/Gewayau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050200000000', 'Buji (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040200000000', 'Bukkuyum (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160500000000', 'Bukul','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110300000000', 'Bulabulin (Gwoza)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210300000000', 'Bulabulin (Maiduguri)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130300000000', 'Bulabulin (Nguru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170100000000', 'Bulangawo A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170200000000', 'Bulangawo B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150100000000', 'Bulangu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080200000000', 'Bularafa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170100000000', 'Bulatura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120300000000', 'Bulkachuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160100000000', 'Bultuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180200000000', 'Bulunchai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080200000000', 'Buma (Dandi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270200000000', 'Buma (Shani)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260100000000', 'Bumai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240100000000', 'Bumbum A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240200000000', 'Bumbum B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060300000000', 'Bundot','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170400000000', 'Bundur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050400000000', 'Bungudu (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070100000000', 'Buni Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070200000000', 'Buni Yadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010200000000', 'Bunkari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060300000000', 'Bunkure (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080300000000', 'Bunsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120100000000', 'Buntusu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170300000000', 'Bununu A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060400000000', 'Bununu Central','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060500000000', 'Bununu East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060600000000', 'Bununu South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060700000000', 'Bununu West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050100000000', 'Buratai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190100000000', 'Burdugau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280100000000', 'Burji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150400000000', 'Burra','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200300000000', 'Bursali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410200000000', 'Burun-Burun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120400000000', 'Buskuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010300000000', 'Busuna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330100000000', 'Butu-Butu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100500000000', 'Buzawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220300000000', 'Chacho/Marnona','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230100000000', 'Chaichai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250100000000', 'Challawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230300000000', 'Chamba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060200000000', 'Chamo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060200000000', 'Charanchi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100100000000', 'Cheberu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210100000000', 'Chedi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130200000000', 'Chediya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020200000000', 'Chibiku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190300000000', 'Chikaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110400000000', 'Chikide Jahode','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020100000000', 'Chikun (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120100000000', 'Chilariye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060400000000', 'Chillas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070300000000', 'Chimola','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120500000000', 'Chinade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090100000000', 'Chinkani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250200000000', 'Chiranchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050300000000', 'Chirbin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060400000000', 'Chirin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150100000000', 'Chiromawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060200000000', 'Chori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120200000000', 'Chukiriwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260200000000', 'Chukuto','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260300000000', 'Chukwikwiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010300000000', 'Chula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200100000000', 'Chulu/Gumbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280200000000', 'Cinkoso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010100000000', 'D/Galadima 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010200000000', 'D/Galadima 11','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130200000000', 'D/Meri D/Mereu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170200000000', 'Daba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090100000000', 'Dabai (Danja)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210200000000', 'Dabai (Zuru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210300000000', 'Dabai Seme','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020500000000', 'Dabaibayawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090100000000', 'Dabar Kwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120200000000', 'Dabawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170300000000', 'Dabaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120200000000', 'Dabi (Gwiwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230200000000', 'Dabi (Ringim)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010400000000', 'Dabin-Kanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090200000000', 'Dabira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130400000000', 'Dabule','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160300000000', 'Dabuwaran','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130300000000', 'Dada/Alelu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400100000000', 'Daddarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060300000000', 'Daddu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090200000000', 'Dadi Riba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110100000000', 'Dadin Kowa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070300000000', 'Dadingel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120600000000', 'Dagaro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040100000000', 'Dagauda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230500000000', 'Dagawa/Rugar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010100000000', 'Dagona','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190200000000', 'Dagu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440200000000', 'Dagumawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020300000000', 'Daho','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150100000000', 'Daima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170400000000', 'Dajin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160400000000', 'Dakaiyyawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150200000000', 'Dakasoye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310100000000', 'Dakata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180500000000', 'Dakin Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020300000000', 'Dakko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140100000000', 'Dal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130200000000', 'Dala (Jere)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070300000000', 'Dala (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410300000000', 'Dalawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100200000000', 'Dalijan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190300000000', 'Dallaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050300000000', 'Dallaji/Faru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270100000000', 'Dalli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160200000000', 'Dalori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160300000000', 'Dalwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090100000000', 'Damaga/Gamagiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050300000000', 'Damagum A.','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050400000000', 'Damagum B.','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110200000000', 'Damai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030200000000', 'Damakasu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140300000000', 'Damakasuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240100000000', 'Damakuli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260300000000', 'Damaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010100000000', 'Damari (Birnin Gwari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310100000000', 'Damari (Sabuwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230400000000', 'Damasau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030300000000', 'Damaturu Central','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040400000000', 'Damau (Bebeji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150200000000', 'Damau (Kubau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080200000000', 'Damba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130400000000', 'Damba/Bakoshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040200000000', 'Dambam A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040300000000', 'Dambam B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230100000000', 'Dambo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070500000000', 'Damboa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030200000000', 'Damfani/S.Birni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020400000000', 'Damri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010400000000', 'Dan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070100000000', 'Dan - Ali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210200000000', 'Dan Agundi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170200000000', 'Dan Alhaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090300000000', 'Dan Ama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020200000000', 'Dan Amar A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020300000000', 'Dan Amar B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110100000000', 'Dan Auani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020400000000', 'Dan Dango','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070200000000', 'Dan Dire A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070300000000', 'Dan Dire B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140300000000', 'Dan Dutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060200000000', 'Dan Galadima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100300000000', 'Dan Gulbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270200000000', 'Dan Hassan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080200000000', 'Dan Isa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020500000000', 'Dan Iya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100400000000', 'Dan Kurmi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070400000000', 'Dan Musa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070500000000', 'Dan Musa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100500000000', 'Dan Sadau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190300000000', 'Dan Umaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010300000000', 'Dan Warai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030300000000', 'Dan-Alhaji/Yangayya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020200000000', 'Danani / Lawanti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090200000000', 'Danbagina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250300000000', 'Danbare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080200000000', 'Danbatta 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080300000000', 'Danbatta 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020500000000', 'Danchadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140400000000', 'Danchuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180100000000', 'Dandago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020600000000', 'Dandagoro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180100000000', 'Dandamisa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180600000000', 'Dandane','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390100000000', 'Dandare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170400000000', 'Dandi (Kazaure)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140100000000', 'Dandin Mahe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080100000000', 'Dandume A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080200000000', 'Dandume B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330100000000', 'Daneji ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330200000000', 'Daneji ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030200000000', 'Dangada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010300000000', 'Dangaladima (Anka)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070100000000', 'Dangaladima (Bunza)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110200000000', 'Dangamaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290100000000', 'Dangani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030200000000', 'Dange','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160600000000', 'Dango','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120100000000', 'Dangoma/Gayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240500000000', 'Dangora','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100100000000', 'Danguguwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200100000000', 'Dangulbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180200000000', 'Danguzuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040300000000', 'Dangwaleri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250300000000', 'Dangwanki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220100000000', 'Dangyatun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090200000000', 'Danja A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090300000000', 'Danja B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290200000000', 'Danjanku/Karachi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130300000000', 'Danjibga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180300000000', 'Dankaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020600000000', 'Dankade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020500000000', 'Dankadu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180400000000', 'Dankama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440300000000', 'Dankaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190400000000', 'Danko/Maga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160200000000', 'Dankolo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040300000000', 'Dankum/Agala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200200000000', 'Dankumbo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250400000000', 'Danladi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430200000000', 'Danlasan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030100000000', 'Danmahawayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250400000000', 'Danmaliki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020600000000', 'Danmanau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190200000000', 'Danmurabu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250200000000', 'Dansarai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240600000000', 'Dansoshiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240300000000', 'Dansure 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080300000000', 'Dantakari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090400000000', 'Dantanoma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170100000000', 'Dantutture','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210100000000', 'Danwata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240300000000', 'Danyashe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050200000000', 'Danzabuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250500000000', 'Danzomo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020300000000', 'Dapchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150300000000', 'Dara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080300000000', 'Daran Sabon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050100000000', 'Darazo East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050200000000', 'Darazo West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340100000000', 'Dargage','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120300000000', 'Darin/ Langawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120300000000', 'Darina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030400000000', 'Darini/Magaji Abu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440400000000', 'Darki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380200000000', 'Darmanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080400000000', 'Darnar Tsolawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240700000000', 'Dashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130100000000', 'Daudawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130400000000', 'Dauki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150400000000', 'Daunaka/Bakinkori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220100000000', 'Daura (Karaye)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050500000000', 'Daura A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050600000000', 'Daura B.','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140200000000', 'Daura/B.Tsaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380300000000', 'Daurawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100300000000', 'Dawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020700000000', 'Dawaki (Bauchi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090300000000', 'Dawaki (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140400000000', 'Dawaki (Kauru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320100000000', 'Dawaki (Rano)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100200000000', 'Dawaki East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100300000000', 'Dawaki West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090400000000', 'Dawakiji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330200000000', 'Dawakin Gulu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270300000000', 'Dawan Gawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010400000000', 'Dawan Musa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100400000000', 'Dawanau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120400000000', 'Dawasa /G/Baba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010200000000', 'Dawayo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250300000000', 'Dayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030600000000', 'Dazara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120500000000', 'Dazigau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160200000000', 'Degeltura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120600000000', 'Degubi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160300000000', 'Dekwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130500000000', 'Dewu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100600000000', 'Diga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120200000000', 'Diggi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040400000000', 'Diginsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030200000000', 'Dikko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080300000000', 'Dikwa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160400000000', 'Dilala/Kalgi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020200000000', 'Dille/Huy','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220400000000', 'Dimbiso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220500000000', 'Dinawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110200000000', 'Dingaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150500000000', 'Dingis','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020600000000', 'Dingyadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030600000000', 'Dipchari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160700000000', 'Disina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180200000000', 'Diso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280100000000', 'Dissi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100300000000', 'Dodoru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190400000000', 'Dogarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140500000000', 'Dogo Nini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140600000000', 'Dogo Tebo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140300000000', 'Dogoma/ J','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110100000000', 'Dogon  Jeji A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110200000000', 'Dogon  Jeji B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010200000000', 'Dogon Dawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110300000000', 'Dogon Jeji C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110200000000', 'Dogon Kawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070400000000', 'Dogon Nama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180400000000', 'Dogondaji/Salah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170500000000', 'Dogoshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270200000000', 'Doguru A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270300000000', 'Doguru B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090200000000', 'Doguwa (Giade)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110300000000', 'Doguwa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060300000000', 'Doka (Charanchi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080500000000', 'Doka (Kachia)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160100000000', 'Doka (Kudan)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390200000000', 'Doka (Tofa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330300000000', 'Doka Dawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160300000000', 'Doka/Bere','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080200000000', 'Doko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080400000000', 'Dokshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140300000000', 'Dole','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110300000000', 'Dole  Machina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080300000000', 'Dolekaina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140400000000', 'Dongo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020300000000', 'Dorawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150300000000', 'Dorawar Sallau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180300000000', 'Dorayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050400000000', 'Doro (Bindawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170600000000', 'Doro (Kukawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090500000000', 'Dosan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090200000000', 'Dosara/Birni Kaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060800000000', 'Dott','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130200000000', 'Dubantu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120700000000', 'Duddaye / Pakarau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230300000000', 'Dudunni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200100000000', 'Dugabau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050200000000', 'Dugja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170200000000', 'Dugu Tsoho','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150500000000', 'Dugul','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330400000000', 'Dugurawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020400000000', 'Duja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230500000000', 'Duji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040100000000', 'Dukamaje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270300000000', 'Dukawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140400000000', 'Dukke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170500000000', 'Dull A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170600000000', 'Dull B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200200000000', 'Duma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150200000000', 'Dumadumi Toka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090200000000', 'Dumbari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110300000000', 'Dumbegu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130500000000', 'Dumsai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210200000000', 'Dunari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400200000000', 'Dunbulum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210300000000', 'Dundaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060300000000', 'Dundubus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010500000000', 'Dundun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310200000000', 'Dungum Muazu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140400000000', 'Dunkurmi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230100000000', 'Durba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110300000000', 'Durbawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370200000000', 'Durbunde','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290200000000', 'Durma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040500000000', 'Durmawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042060900000000', 'Durr','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060400000000', 'Duru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200200000000', 'Durun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130300000000', 'Dusuman','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030700000000', 'Dutsen  Lawan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230200000000', 'Dutsen Abba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350200000000', 'Dutsen Bakoshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170200000000', 'Dutsen Kura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150300000000', 'Dutsen Wai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110200000000', 'Dutsi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110300000000', 'Dutsi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120300000000', 'Dutsinma A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120400000000', 'Dutsinma B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260300000000', 'Duwan/Makau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120300000000', 'Etene','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370300000000', 'F Alali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060400000000', 'Fada (Jaba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130300000000', 'Fada (Kaura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160400000000', 'Fada (Sakaba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160200000000', 'Fafaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180500000000', 'Faga/Alasan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040400000000', 'Fagam (Damban)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110300000000', 'Fagam (Gwaram)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040500000000', 'Fagarau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120100000000', 'Fagge A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120200000000', 'Fagge B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120300000000', 'Fagge C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120400000000', 'Fagge D1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120500000000', 'Fagge D2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160800000000', 'Faggo A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042160900000000', 'Faggo B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040500000000', 'Fagi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330300000000', 'Fago ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330400000000', 'Fago ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050300000000', 'Fagolo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090300000000', 'Faguji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080400000000', 'Fagwalawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060500000000', 'Fai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030300000000', 'Fajaldu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370400000000', 'Fajewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100200000000', 'Fajiganari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090400000000', 'Fakai\ Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190300000000', 'Fake','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230600000000', 'Fakka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100100000000', 'Fakku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200100000000', 'Fakuwa /Kafin Dangi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060400000000', 'Falale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020300000000', 'Falde','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050400000000', 'Falgeri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110400000000', 'Falgore (Doguwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340200000000', 'Falgore (Rogo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110400000000', 'Falimaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230200000000', 'Fammar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080400000000', 'Fana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020500000000', 'Fanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180300000000', 'Fandum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420200000000', 'Fanisau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150400000000', 'Fankurun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040300000000', 'Fanshanu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240400000000', 'Fara Barije','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020600000000', 'Faragai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300200000000', 'Fardami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110400000000', 'Farin Dutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160300000000', 'Faru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090300000000', 'Faru/Magami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370500000000', 'Farun Ruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350300000000', 'Faruruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130200000000', 'Faskari (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040400000000', 'Faski/Kagara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230300000000', 'Fassi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210300000000', 'Fataika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090300000000', 'Felo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020400000000', 'Feske','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210400000000', 'Fezzan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040100000000', 'Fika Anze','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040300000000', 'Fikhayel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030300000000', 'Filande','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120400000000', 'Firji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010400000000', 'Foguwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140500000000', 'Foi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060500000000', 'Fukurti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200300000000', 'Fulata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340300000000', 'Fulatan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200300000000', 'Fura Girke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050500000000', 'Furfuri/Kwakwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200400000000', 'Furram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060600000000', 'Futchimiram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010500000000', 'Futuk East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010600000000', 'Futuk West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250100000000', 'Fuye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210400000000', 'G/Bubu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210500000000', 'G/Hamidu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080500000000', 'Gabai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080300000000', 'Gabake','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190400000000', 'Gabanga A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190500000000', 'Gabanga B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050300000000', 'Gabarin East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050400000000', 'Gabarin West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210300000000', 'Gabas 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210400000000', 'Gabas 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210500000000', 'Gabas 3','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130100000000', 'Gabasawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050500000000', 'Gabchiyari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200200000000', 'Gachi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170500000000', 'Gada (Kazaure)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040200000000', 'Gada (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050600000000', 'Gada/Karakkai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200400000000', 'Gadai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260400000000', 'Gadai Sub-District','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040200000000', 'Gadaka Shembire','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030300000000', 'Gadanya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100700000000', 'Gadau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070200000000', 'Gadiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060500000000', 'Gafan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150200000000', 'Gafara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010600000000', 'Gafasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150300000000', 'Gafaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180500000000', 'Gafiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020700000000', 'Gagarame','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070100000000', 'Gagarawa Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070200000000', 'Gagarawa Tasha','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170100000000', 'Gagi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170200000000', 'Gagi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170300000000', 'Gagi C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161000000000', 'Gagidiba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130300000000', 'Gagulmari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080600000000', 'Gagure','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050500000000', 'Gaiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080400000000', 'Gajibo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390300000000', 'Gajida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260500000000', 'Gajiram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360100000000', 'Gala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180400000000', 'Galadanchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200400000000', 'Galadi (Maigatari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110300000000', 'Galadi (Shinkafi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030400000000', 'Galadima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200300000000', 'Galadima ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200400000000', 'Galadima ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080400000000', 'Galadima Dan Galadima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010400000000', 'Galadima-Ank','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070100000000', 'Galadima-Gus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120100000000', 'Galadima-Tma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030200000000', 'Galadimawa (Giwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240800000000', 'Galadimawa (Kiru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090500000000', 'Galagamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020800000000', 'Galambi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140600000000', 'Galangi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050300000000', 'Galdimari (Biu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110400000000', 'Galdimari (Jama''Are)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200500000000', 'Galiganna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280300000000', 'Galinja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270400000000', 'Gallu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130400000000', 'Galtimari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310200000000', 'Gama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210200000000', 'Gama Gira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190100000000', 'Gama''A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040400000000', 'Gamadadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010500000000', 'Gamafoi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160200000000', 'Gamarya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070300000000', 'Gamawa North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070400000000', 'Gamawa South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090400000000', 'Gamawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120700000000', 'Gambaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030800000000', 'Gambar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030400000000', 'Gambir / Moduri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210500000000', 'Gamboru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250200000000', 'Gamboru A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250300000000', 'Gamboru B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250400000000', 'Gamboru C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310300000000', 'Gamji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200300000000', 'Gamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060500000000', 'Gamo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160300000000', 'Gamoji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010600000000', 'Gamsarka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170300000000', 'Gamzago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270500000000', 'Gana Jigawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150100000000', 'Gande','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120100000000', 'Gandi I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120200000000', 'Gandi Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100500000000', 'Ganduje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210300000000', 'Gandun Albasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110400000000', 'Gandun Modibbo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300200000000', 'Gandurwawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120800000000', 'Gangai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140200000000', 'Gangan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030300000000', 'Gangara (Giwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160400000000', 'Gangara (Jibia)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130100000000', 'Gangara (Sabon Birni)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140200000000', 'Gangawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360200000000', 'Gani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080100000000', 'Ganjuwa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080200000000', 'Ganjuwa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090600000000', 'Gano','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050500000000', 'Gantsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060400000000', 'Ganuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010700000000', 'Gar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100400000000', 'Garbagar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130600000000', 'Garbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220200000000', 'Garbo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360300000000', 'Garfa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040600000000', 'Gargai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100600000000', 'Gargari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040600000000', 'Gargawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140200000000', 'Garin Ali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070300000000', 'Garin Chiroma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430300000000', 'Garin Dau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090600000000', 'Garin Gambo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100300000000', 'Garin Gawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080700000000', 'Garintuwo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200200000000', 'Garkar Sarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040500000000', 'Garki (Baure)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080300000000', 'Garki (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190400000000', 'Garko (Kiyawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140300000000', 'Garko (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340200000000', 'Garni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200400000000', 'Garo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020400000000', 'Garu (Babura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060100000000', 'Garu (Chibok)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040300000000', 'Garu (Fika)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080500000000', 'Garu (Illela)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160200000000', 'Garu (Kudan)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290300000000', 'Garu (Musawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210300000000', 'Garu (Soba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170300000000', 'Garu/Mariri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050400000000', 'Garubula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150500000000', 'Garun Babba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130200000000', 'Garun Danga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210400000000', 'Garun Gabas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150600000000', 'Garun Malam (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260200000000', 'Garun Sheme','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040700000000', 'Garuza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020500000000', 'Gasakoli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230600000000', 'Gashigar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270300000000', 'Gasi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100400000000', 'Gasma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010700000000', 'Gatafa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060200000000', 'Gatamarwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130200000000', 'Gatawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150200000000', 'Gaukai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140300000000', 'Gauza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110500000000', 'Gavva Agapalwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190200000000', 'Gawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060300000000', 'Gawassu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010300000000', 'Gawazai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170200000000', 'Gawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310300000000', 'Gawuna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160400000000', 'Gaya Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160500000000', 'Gaya Kudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010300000000', 'Gayam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060600000000', 'Gayari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420300000000', 'Gayawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180400000000', 'Gayin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090500000000', 'Gazaburi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180300000000', 'Gazara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310400000000', 'Gazari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170300000000', 'Gebbe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090200000000', 'Gebe A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090300000000', 'Gebe B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360400000000', 'Gediya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030400000000', 'Geere-Gajara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160500000000', 'Gelwasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140500000000', 'Geshere','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190200000000', 'Getso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080500000000', 'Geza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170300000000', 'Gezawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150300000000', 'Gidan Baka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090400000000', 'Gidan Goga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080600000000', 'Gidan Hamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220100000000', 'Gidan Jatau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200400000000', 'Gidan Kare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080700000000', 'Gidan Katta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070400000000', 'Gidan Kaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190100000000', 'Gidan Madi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110500000000', 'Gidan Rugga/More','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080600000000', 'Gidan Tagwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070400000000', 'Gidan Waya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090400000000', 'Gidea A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090500000000', 'Gidea B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140200000000', 'Gidiga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070500000000', 'Gigane','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310400000000', 'Giginyu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100800000000', 'Gijina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040300000000', 'Gilbadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210400000000', 'Gimba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180400000000', 'Gimi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110400000000', 'Gindi/Kyarmi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180700000000', 'Ginga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290400000000', 'Gingin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390400000000', 'Ginsawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160500000000', 'Girbobo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050600000000', 'Giremawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090300000000', 'Girgir/ Bayam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180600000000', 'Girka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100200000000', 'Girkau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180800000000', 'Giro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030400000000', 'Giwa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140300000000', 'Giwatazo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050300000000', 'Giyawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042030900000000', 'Gobbiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070500000000', 'Gobirawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200500000000', 'Godiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070500000000', 'Godo-Godo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090400000000', 'Gogaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430400000000', 'Gogel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030400000000', 'Gogori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070500000000', 'Gololo North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070600000000', 'Gololo South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130500000000', 'Gomari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130600000000', 'Gongulong','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030700000000', 'Goniri (Bama)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070400000000', 'Goniri (Gujba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220200000000', 'Gora  Sub-District','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030300000000', 'Gora (Birnin Magaji/Kiyaw)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280400000000', 'Gora (Madobi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240500000000', 'Gora (Roni)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270400000000', 'Gora (Shani)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250400000000', 'Gora Dansaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090500000000', 'Gora/Namaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350400000000', 'Goron Du Tse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180500000000', 'Goron Dutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080500000000', 'Goron Maje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050400000000', 'Goronyo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020500000000', 'Gorun Dikko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110600000000', 'Goshe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070500000000', 'Gotala Gotumba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140500000000', 'Goya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170400000000', 'Gozaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400300000000', 'Gozarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120200000000', 'Grim/Damch','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020400000000', 'Guba/Dapso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090600000000', 'Gubio I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090700000000', 'Gubio Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180500000000', 'Gubuchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140400000000', 'Gubunkure','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150600000000', 'Guda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200600000000', 'Gude','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040400000000', 'Gudi Dozi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110700000000', 'Guduf A&B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100200000000', 'Gudumbali E','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100300000000', 'Gudumbali W','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150300000000', 'Guduram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010500000000', 'Guga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140500000000', 'Gugulin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070600000000', 'Gujba (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020500000000', 'Guji / Metalari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260400000000', 'Gujungu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080800000000', 'Gulani (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090500000000', 'Gulbin Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030500000000', 'Gulma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100400000000', 'Gulmare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330500000000', 'Gulu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030800000000', 'Gulumba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060400000000', 'Gulumbe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200500000000', 'Gumai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210600000000', 'Gumbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080700000000', 'Gumel (Kachia)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220500000000', 'Gumna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060700000000', 'Gumsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170200000000', 'Gumshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070600000000', 'Gumsuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020600000000', 'Gumunde /Rafin Tsaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050500000000', 'Gunda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140600000000', 'Gundari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190300000000', 'Gundawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270400000000', 'Gundutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080300000000', 'Gungura A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080400000000', 'Gungura B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140400000000', 'Gunka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120500000000', 'Guntai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050600000000', 'Gur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160500000000', 'Gurbi (Jibia)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190400000000', 'Gurbi (Kankara)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010700000000', 'Gurduba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170400000000', 'Gure/Kahugu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100500000000', 'Guri (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040800000000', 'Guribana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060600000000', 'Gurjiya (Bunkure)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090700000000', 'Gurjiya (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140400000000', 'Gurjiya (Garko)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270400000000', 'Gurjiya (Yankwashi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400400000000', 'Gurun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250500000000', 'Gurun Gawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030400000000', 'Gusami Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030500000000', 'Gusami Hayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120200000000', 'Gusari/Garbadu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090700000000', 'Gusau (Gumel)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180200000000', 'Guwal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140700000000', 'Guwo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100400000000', 'Guworam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170300000000', 'Guya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130600000000', 'Guyaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100500000000', 'Guzamala E','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100600000000', 'Guzamala W','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070600000000', 'Gwadabawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060500000000', 'Gwadangwaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070200000000', 'Gwade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120300000000', 'Gwadodi/Gidan Buwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020200000000', 'Gwagwada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310500000000', 'Gwagwarwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270500000000', 'Gwalasho','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180600000000', 'Gwale (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210700000000', 'Gwamatse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340300000000', 'Gwamba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060700000000', 'Gwamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070600000000', 'Gwammaja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010800000000', 'Gwana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080600000000', 'Gwanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180300000000', 'Gwandi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100500000000', 'Gwandu Dangaladima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100600000000', 'Gwandu Marafa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190500000000', 'Gwanfi/Kele','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210600000000', 'Gwange I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210700000000', 'Gwange Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210800000000', 'Gwange Iii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340400000000', 'Gwangwan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180600000000', 'Gwanki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200500000000', 'Gwantu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120300000000', 'Gwanzang','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080700000000', 'Gwarabtawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042100900000000', 'Gwarai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040400000000', 'Gwaraji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140700000000', 'Gwaram (Misau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110500000000', 'Gwaram (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042010900000000', 'Gwaram A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011000000000', 'Gwaram B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120300000000', 'Gwaram-Tma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220300000000', 'Gwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280200000000', 'Gwarjo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040700000000', 'Gwarmai (Bebeji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260300000000', 'Gwarmai (Kunchi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270500000000', 'Gwarta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080400000000', 'Gwarzo (Garki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190300000000', 'Gwarzo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040300000000', 'Gwashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270600000000', 'Gwaskara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042020900000000', 'Gwaskwaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030600000000', 'Gwazange (Argungu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060500000000', 'Gwazange (Gudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120600000000', 'Gwiwa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010300000000', 'Gwo Kura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380400000000', 'Gyadi Gayadi Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380500000000', 'Gyadi Gyadi Kudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060700000000', 'Gyalange','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042031000000000', 'Gyara (Bogoro)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101000000000', 'Gyara (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180700000000', 'Gyaranya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230300000000', 'Gyellesu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200600000000', 'H/Chingua','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160600000000', 'Hadin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110800000000', 'Hambagda L. Jaje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260400000000', 'Hamcheta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110600000000', 'Hamma''Ali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090800000000', 'Hammado','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110500000000', 'Hanafari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220400000000', 'Hantsu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190500000000', 'Hanwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140500000000', 'Harbo Sabuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140600000000', 'Harbo Tsohuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140800000000', 'Hardawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021000000000', 'Hardo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150400000000', 'Haskiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043210900000000', 'Hausari (Maiduguri)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130700000000', 'Hausari (Nguru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043110900000000', 'Hausari Gaddamari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060800000000', 'Hausari Sub-District','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020300000000', 'Hausari Z','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140700000000', 'Hausawa Asibiti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200700000000', 'Hauwade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090300000000', 'Hayin Banki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130500000000', 'Herini/Madachi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110500000000', 'Hirchin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120400000000', 'Hirishi/Magarza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120400000000', 'Hizhi/Bwala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140300000000', 'Horo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380600000000', 'Hotoro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310600000000', 'Hotoro North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310700000000', 'Hotoro South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070700000000', 'Huchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040600000000', 'Hui','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020800000000', 'Hungu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160300000000', 'Hunkuyi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020400000000', 'Hussara/T','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140700000000', 'Idanduna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030500000000', 'Idasu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110200000000', 'Iddah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120300000000', 'Idon','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040500000000', 'Igabi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050200000000', 'Ikara (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220300000000', 'Ikulu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130600000000', 'Ilela/Sabon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080800000000', 'Illela (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050600000000', 'Illo/Sabon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430500000000', 'Imawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150600000000', 'Ingawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010400000000', 'Inname','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020600000000', 'Insharuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090400000000', 'Isa North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090500000000', 'Isa South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090600000000', 'Isawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210400000000', 'Isgo Dago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101100000000', 'Itas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300300000000', 'Iyatawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090500000000', 'Jaba (Jakusko)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140800000000', 'Jabarna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150400000000', 'Jabbo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180600000000', 'Jabo /Kagara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010500000000', 'Jabullam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130700000000', 'Jaddadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070700000000', 'Jadori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160700000000', 'Jae','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070600000000', 'Jagindi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018140900000000', 'Jahun (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340500000000', 'Jajaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050700000000', 'Jajere','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100500000000', 'Jajeri (Karasuwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200500000000', 'Jajeri (Maigatari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100600000000', 'Jajimaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160400000000', 'Jakana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210400000000', 'Jakara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090600000000', 'Jakusko (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042040900000000', 'Jalam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100700000000', 'Jalli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180100000000', 'Jama A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190600000000', 'Jama''A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110600000000', 'Jamaare A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110700000000', 'Jamaare B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110800000000', 'Jamaare C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042110900000000', 'Jamaare D','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010500000000', 'Jamali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050300000000', 'Jampalan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090600000000', 'Janbako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160600000000', 'Janbirni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041000000000', 'Janda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410400000000', 'Jandutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110600000000', 'Jandutsi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040500000000', 'Janga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120400000000', 'Jangebe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110400000000', 'Jangeru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150700000000', 'Jangu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390500000000', 'Janguza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260500000000', 'Jani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040500000000', 'Jara Dali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040600000000', 'Jara Gol','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150200000000', 'Jarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140400000000', 'Jaredi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010600000000', 'Jargaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042140900000000', 'Jarkasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390600000000', 'Jauben Kudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020600000000', 'Jawa Garun Dole','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090700000000', 'Jawur Katama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170400000000', 'Jebuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150300000000', 'Jekanadu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250600000000', 'Jeke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430600000000', 'Jemagu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110300000000', 'Jere North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110400000000', 'Jere South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090400000000', 'Jiba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050700000000', 'Jibawar Bade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290300000000', 'Jibga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160600000000', 'Jibia (A)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160700000000', 'Jibia (B)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090800000000', 'Jido','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010400000000', 'Jiga Birni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010500000000', 'Jiga Makera','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260600000000', 'Jigalta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020700000000', 'Jigawa (Babura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430700000000', 'Jigawa (Warawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060500000000', 'Jigawar Tsada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200300000000', 'Jijima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290500000000', 'Jikamshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150300000000', 'Jilbe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330600000000', 'Jili','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020700000000', 'Jino','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080500000000', 'Jirima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410500000000', 'Jita','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150700000000', 'Jobawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130300000000', 'Joda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170400000000', 'Jogana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036060900000000', 'Jororo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090700000000', 'Jugudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020700000000', 'Juluri / Damnawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430800000000', 'Juma Galadima','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150400000000', 'Jumbam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042111000000000', 'Jurara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190700000000', 'Jushi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130500000000', 'K/Ganuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400500000000', 'Kaba Giwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090400000000', 'Kabala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110700000000', 'Kabanga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200800000000', 'Kabo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010700000000', 'Kabomo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180800000000', 'Kabuga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220600000000', 'Kabulawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070700000000', 'Kabuwaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370600000000', 'Kachako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040600000000', 'Kachallari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060600000000', 'Kachi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080800000000', 'Kachia (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040400000000', 'Kadadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350500000000', 'Kadamu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290400000000', 'Kadan Dani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300400000000', 'Kadandani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130400000000', 'Kadarko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040500000000', 'Kadassaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150800000000', 'Kadawa (Garun Malam)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420400000000', 'Kadawa (Ungogo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040600000000', 'Kaddi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160600000000', 'Kademi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100600000000', 'Kadira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070700000000', 'Kafa Mafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070700000000', 'Kafanchan A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070800000000', 'Kafanchan A B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230400000000', 'Kafarda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040700000000', 'Kaffe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200600000000', 'Kafin  Larabawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230300000000', 'Kafin Babushe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220200000000', 'Kafin Dabga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150500000000', 'Kafin Hausa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130700000000', 'Kafin Iya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042120900000000', 'Kafin Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150800000000', 'Kafin Lemo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080500000000', 'Kafin Madaki A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080600000000', 'Kafin Madaki B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140500000000', 'Kafin Malamai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200500000000', 'Kafin Soli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141000000000', 'Kafin Sule','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160500000000', 'Kafiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010800000000', 'Kafur (Auyo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170500000000', 'Kafur (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050500000000', 'Kagara (Goronyo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080500000000', 'Kagara (Kaura Namoda)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120500000000', 'Kagara-Tma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330500000000', 'Kagare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110500000000', 'Kagarko North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110600000000', 'Kagarko South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019070900000000', 'Kagoma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240200000000', 'Kaguram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230400000000', 'Kahu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090500000000', 'Kahuta A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090600000000', 'Kahuta B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230500000000', 'Kaikai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180700000000', 'Kaita (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140500000000', 'Kajiji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120400000000', 'Kajuru (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010400000000', 'Kakangi (Birnin Gwari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030600000000', 'Kakangi (Giwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020300000000', 'Kakau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280500000000', 'Kakin Agur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010800000000', 'Kakumi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100300000000', 'Kakuri Gwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100400000000', 'Kakuri Hausa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150400000000', 'Kala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030500000000', 'Kalallawa / Gabai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210800000000', 'Kalambaina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190200000000', 'Kalanjeni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018141000000000', 'Kale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130300000000', 'Kalgo (Sabon Birni)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120500000000', 'Kalgo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020800000000', 'Kaliyari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200700000000', 'Kalizorom','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120500000000', 'Kallah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034080900000000', 'Kalmalo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170500000000', 'Kamaganam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220400000000', 'Kamanton','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140600000000', 'Kamaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080600000000', 'Kamba Kamba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140600000000', 'Kambama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100700000000', 'Kambaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150400000000', 'Kambuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050800000000', 'Kamri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210500000000', 'Kan Karofi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360500000000', 'Kanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340400000000', 'Kanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021010900000000', 'Kandarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030500000000', 'Kandawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150700000000', 'Kandawa/Jobe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021100000000', 'Kangere','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090600000000', 'Kangi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030200000000', 'Kangire','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020700000000', 'Kangiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019071000000000', 'Kaninkon','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190500000000', 'Kankara (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034210900000000', 'Kanmata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100600000000', 'Kanoma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300300000000', 'Kantama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170600000000', 'Kanti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030300000000', 'Kantoga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070800000000', 'Kantudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018141100000000', 'Kanwa (Jahun)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020200900000000', 'Kanwa (Kabo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280600000000', 'Kanwa (Madobi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140400000000', 'Kanwa (Zurmi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020800000000', 'Kanya (Babura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080600000000', 'Kanya (Garki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190600000000', 'Kanya (Wasagu/Danko)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050700000000', 'Kaoje/Gwamba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190400000000', 'Kara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280300000000', 'Karadua','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140800000000', 'Karagawaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040700000000', 'Karanga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030600000000', 'Karare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100700000000', 'Karasuwa G/Guna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100800000000', 'Karasuwa Galu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270600000000', 'Karau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140500000000', 'Karaye (Maiyama)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170700000000', 'Kardam A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170800000000', 'Kardam B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042170900000000', 'Kardam C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060600000000', 'Kardi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410600000000', 'Karefa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150500000000', 'Kareh','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200800000000', 'Kareram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230700000000', 'Kareto','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060600000000', 'Karfen Chana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060700000000', 'Karfensarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270500000000', 'Karfi (Kura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250500000000', 'Karfi (Malumfashi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370700000000', 'Karfi (Takai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150600000000', 'Kargi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080700000000', 'Kargo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330600000000', 'Karikarku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080700000000', 'Kariya A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080800000000', 'Kariya B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270600000000', 'Karkarna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130400000000', 'Karmami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060700000000', 'Karnaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420500000000', 'Karo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120500000000', 'Karofi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120600000000', 'Karofi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330700000000', 'Karofin Yashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230400000000', 'Karshi (Ringim)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200600000000', 'Karshi (Sanga)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010600000000', 'Kashin Zama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101200000000', 'Kashuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043030900000000', 'Kasugula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120600000000', 'Kasuwan Magani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121000000000', 'Kasuwar Kaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130400000000', 'Kasuwar Kofa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130500000000', 'Kasuwar Kuda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260400000000', 'Kasuwar Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200700000000', 'Katagum (Zaki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150400000000', 'Katami North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150500000000', 'Katami South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110700000000', 'Katanga (Jega)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190500000000', 'Katanga (Kiyawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190600000000', 'Katanga (Warji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020430900000000', 'Katar Kawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019080900000000', 'Katari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330700000000', 'Katsayal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110700000000', 'Katugal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190600000000', 'Katuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140600000000', 'Katumari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110500000000', 'Katuru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010400000000', 'Katuzu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050400000000', 'Kau-Kau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160800000000', 'Kaugama (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130500000000', 'Kaura (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034211000000000', 'Kaura (Wamako)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230400000000', 'Kaura (Zaria)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310800000000', 'Kaura Goje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280700000000', 'Kauran Mata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160400000000', 'Kauran Wali North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160500000000', 'Kauran Wali South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020700000000', 'Kaurarmiyo/Mazangari/Jirga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140700000000', 'Kauru East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140800000000', 'Kauru West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440500000000', 'Kausani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060300000000', 'Kautakari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170700000000', 'Kauwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020310900000000', 'Kawaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140600000000', 'Kawara (Maiyama)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170400000000', 'Kawara (Shanga)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340500000000', 'Kawarin Kudi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340600000000', 'Kawarin Malamai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050600000000', 'Kawaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090500000000', 'Kawo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160500000000', 'Kawuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090700000000', 'Kaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170500000000', 'Kayarda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020800000000', 'Kayauki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110400000000', 'Kayawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120600000000', 'Kayaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050800000000', 'Kayeri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040800000000', 'Kazura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160700000000', 'Kazurewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100300000000', 'Kebbe East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100400000000', 'Kebbe West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170800000000', 'Kekeno','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050800000000', 'Kende/Kurgu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040600000000', 'Kerawa 1 (Igabi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040700000000', 'Kerawa 2 (Igabi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010600000000', 'Kessaa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130600000000', 'Keta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190600000000', 'Ketare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170500000000', 'Ketawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130700000000', 'Khaddamari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230500000000', 'Kibiya I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230600000000', 'Kibiya Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120500000000', 'Kida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030700000000', 'Kidandan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110600000000', 'Kila','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161100000000', 'Kilbori A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161200000000', 'Kilbori B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230700000000', 'Kilgori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150500000000', 'Kilumaga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110800000000', 'Kimba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100700000000', 'Kingarwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090800000000', 'Kingowa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210500000000', 'Kinkiba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290600000000', 'Kira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220700000000', 'Kirenowa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130800000000', 'Kirfi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040800000000', 'Kiri (Gada)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260500000000', 'Kiri (Taura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180500000000', 'Kiri Kasamma (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020240900000000', 'Kiru (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030400000000', 'Kiyako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030500000000', 'Kiyawa (Bagwai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190700000000', 'Kiyawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043111000000000', 'Kizawa Jimin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060500000000', 'Koda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040800000000', 'Kofa (Bebeji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230600000000', 'Kofa (Kusada)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070800000000', 'Kofan Romi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018090900000000', 'Kofar Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020070900000000', 'Kofar Mazugal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020071000000000', 'Kofar Ruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018091000000000', 'Kofar Yamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280400000000', 'Kogari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241000000000', 'Kogo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290500000000', 'Koguna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050600000000', 'Kojiyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022110900000000', 'Kokani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030700000000', 'Kokani North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030800000000', 'Kokani South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350600000000', 'Kokiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130800000000', 'Koko Firchin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022130900000000', 'Koko Magaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060700000000', 'Kola/Tarasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036050900000000', 'Kolere/ Kafaje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150600000000', 'Komakandi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270700000000', 'Kombo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160600000000', 'Konduga (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050600000000', 'Konkiyel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110500000000', 'Konkomma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120700000000', 'Korayel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080800000000', 'Kore (Dambatta)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042070900000000', 'Kore (Gamawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080800000000', 'Kore (Garki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070400000000', 'Kore Balatu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150500000000', 'Koriyel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060400000000', 'Korongilum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270600000000', 'Kosawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190300000000', 'Koshebe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050700000000', 'Kotorkoshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220500000000', 'Koya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240400000000', 'Koza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130600000000', 'Kpak','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280800000000', 'Kubaraci','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150700000000', 'Kubau (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071000000000', 'Kubdiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042080900000000', 'Kubi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081000000000', 'Kubi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270800000000', 'Kubo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150600000000', 'Kubodu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180400000000', 'Kubuku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060500000000', 'Kuburmbula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100500000000', 'Kuchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260700000000', 'Kuda (Nganzai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270700000000', 'Kuda (Yankwashi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060800000000', 'Kudai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160600000000', 'Kudan (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170600000000', 'Kudaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010700000000', 'Kudo Kurgu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210600000000', 'Kudu 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210700000000', 'Kudu 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210800000000', 'Kudu 3','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042150900000000', 'Kudu Yamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120700000000', 'Kufana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230500000000', 'Kufena','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020400000000', 'Kujama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370800000000', 'Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141100000000', 'Kukadi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141200000000', 'Kukadi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120600000000', 'Kukah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030600000000', 'Kukareta /Warsala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190700000000', 'Kukasheka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043170900000000', 'Kukawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110600000000', 'Kukayasku (Machina)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200600000000', 'Kukayasku (Maigatari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020040900000000', 'Kuki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120700000000', 'Kuki A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120800000000', 'Kuki B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130700000000', 'Kukum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050700000000', 'Kukuma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120800000000', 'Kukuri / Chiromari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110800000000', 'Kukuyi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220800000000', 'Kulli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060800000000', 'Kulluwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240300000000', 'Kumalia','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250600000000', 'Kumbotso (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043031000000000', 'Kumshe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020060900000000', 'Kumurya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020500000000', 'Kunai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260500000000', 'Kunchi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021200000000', 'Kundun Durum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200600000000', 'Kunduru / Gyaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011100000000', 'Kungibar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080600000000', 'Kungurki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010800000000', 'Kunkun Rawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300400000000', 'Kunya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043200900000000', 'Kupti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270700000000', 'Kura (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043111100000000', 'Kurabasa Ngoshes','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021011000000000', 'Kurami/Yankwani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130400000000', 'Kurawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060600000000', 'Kuraye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090800000000', 'Kurba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180500000000', 'Kurbagayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060800000000', 'Kurdula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250700000000', 'Kureken Sani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060800000000', 'Kurfa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150800000000', 'Kurfeji/Yankaura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220300000000', 'Kurfi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220400000000', 'Kurfi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020600000000', 'Kuriga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170600000000', 'Kuringafa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290700000000', 'Kurkujan A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290800000000', 'Kurkujan B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151000000000', 'Kurmi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050400000000', 'Kurmi Kogi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019110900000000', 'Kurmin Jibrin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019081000000000', 'Kurmin Musa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036020900000000', 'Kurnawa (Borsari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260800000000', 'Kurnawa (Nganzai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300500000000', 'Kuru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220300000000', 'Kurugu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270800000000', 'Kurun Sumau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200500000000', 'Kuruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080700000000', 'Kurya (Kaura Namoda)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120400000000', 'Kurya (Rabah)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110600000000', 'Kurya-Skf','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160800000000', 'Kusa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230700000000', 'Kusada (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019111000000000', 'Kushe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036080900000000', 'Kushimaga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100100000000', 'Kusugu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036061000000000', 'Kusur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021120900000000', 'Kutaina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190500000000', 'Kutama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010500000000', 'Kutemeshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050500000000', 'Kuya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100700000000', 'Kuyanbana-Mrr','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010600000000', 'Kuyello','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018020900000000', 'Kuzunzumi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100800000000', 'Kwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190300000000', 'Kwacce Huro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020800000000', 'Kwacciyar Lalle','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120600000000', 'Kwachiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042130900000000', 'Kwagal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040800000000', 'Kwaido','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022180900000000', 'Kwaifa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240600000000', 'Kwaita','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120600000000', 'Kwajaffa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030600000000', 'Kwajali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080700000000', 'Kwakkwaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150500000000', 'Kwakwara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050700000000', 'Kwakwazo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260600000000', 'Kwalam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050500000000', 'Kwamarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390700000000', 'Kwami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290600000000', 'Kwanar Tabo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190800000000', 'Kwanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030500000000', 'Kwangwara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020280900000000', 'Kwankwaso','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220400000000', 'Kwanyawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200600000000', 'Kwarare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040800000000', 'Kwarau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230600000000', 'Kwarbai  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230700000000', 'Kwarbai  B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110700000000', 'Kware (Shinkafi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110800000000', 'Kware (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220600000000', 'Kwargaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300600000000', 'Kwarkiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034040900000000', 'Kwarma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140700000000', 'Kwas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210600000000', 'Kwasallo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330800000000', 'Kwasarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220700000000', 'Kwasare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140500000000', 'Kwashebawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019140900000000', 'Kwassam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260600000000', 'Kwatta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019081100000000', 'Kwaturu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180600000000', 'Kwaya Kusar (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120700000000', 'Kwaya/B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150600000000', 'Kwazailewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110700000000', 'Kwondiko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190700000000', 'Kyabu/Kandu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034041000000000', 'Kyadawa/Holai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050600000000', 'Kyalli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018021000000000', 'Kyambo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080800000000', 'Kyanbarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080800000000', 'Kyangakwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040400000000', 'Kyaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230500000000', 'Kyarama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151100000000', 'Kyata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230800000000', 'L/Kona','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150700000000', 'Labani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022050900000000', 'Lafagu/Gante','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030600000000', 'Lafia','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090800000000', 'Lafia Loi Loi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100700000000', 'Lafiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060800000000', 'Lagga/Randali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050700000000', 'Lago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220800000000', 'Lahodu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022030900000000', 'Lailaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440600000000', 'Lajawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190400000000', 'Laje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130500000000', 'Lajinge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043270900000000', 'Lakundum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190600000000', 'Lakwaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200700000000', 'Lambar Tureta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140700000000', 'Lambara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390800000000', 'Lambu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180200000000', 'Lame','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110700000000', 'Lamisu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211000000000', 'Lamisula','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020390900000000', 'Langel','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022131000000000', 'Lani/Shiba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150600000000', 'Lantewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050800000000', 'Lanzai East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042050900000000', 'Lanzai West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042131000000000', 'Lariski','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042111100000000', 'Lariye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020500000000', 'Lassa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320200000000', 'Lausu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010500000000', 'Lawan Fernami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010600000000', 'Lawan Musa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230800000000', 'Layi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170700000000', 'Lazuru/Tuddai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050800000000', 'Lelenkudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020800000000', 'Lema/Jantulu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350700000000', 'Leni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170800000000', 'Lere (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171000000000', 'Lere North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171100000000', 'Lere South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140700000000', 'Liba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150600000000', 'Libata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060600000000', 'Likama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160700000000', 'Likoro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011200000000', 'Lim Kundak','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021300000000', 'Liman Katagun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040700000000', 'Limanti (Bayo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190500000000', 'Limanti (Mafa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211100000000', 'Limanti (Maiduguri)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018060900000000', 'Limawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440700000000', 'Lndabo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200800000000', 'Lodiyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200800000000', 'Lofa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250500000000', 'Logumane','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022051000000000', 'Lolo/Giris','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190600000000', 'Loskuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042061000000000', 'Lukshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042031100000000', 'Lusa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080500000000', 'M. Kaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080600000000', 'M. Maja','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080400000000', 'M/Dansoda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080500000000', 'M/Wando','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036061100000000', 'Ma Anna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190700000000', 'Maafa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190800000000', 'Mabai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260700000000', 'Machika (Mani)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310500000000', 'Machika (Sabuwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110800000000', 'Machina (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018040900000000', 'Machinamari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070200000000', 'Mada (Gusau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150700000000', 'Mada (Kala/Balge)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121100000000', 'Madachi (Katagum)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180600000000', 'Madachi (Kiri Kasamma)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320300000000', 'Madachi (Rano)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190700000000', 'Madada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070500000000', 'Madaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200700000000', 'Madana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121200000000', 'Madangala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121300000000', 'Madara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431000000000', 'Madarin Mata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070300000000', 'Madawaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220500000000', 'Madekiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020071100000000', 'Madigawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018061000000000', 'Madobi (Dutse)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020281000000000', 'Madobi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100200000000', 'Madobi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100300000000', 'Madobi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030700000000', 'Madogara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042200900000000', 'Madufa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190800000000', 'Mafa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150700000000', 'Mafa (Tarmua)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240400000000', 'Mafio','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211200000000', 'Mafoni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300500000000', 'Magabo/Kurabo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022111000000000', 'Magaji A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022111100000000', 'Magaji B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010500000000', 'Magaji-Ank','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037060900000000', 'Magaji-Gmm','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220500000000', 'Magajin Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160100000000', 'Magajin Gari A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160200000000', 'Magajin Gari B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010700000000', 'Magajin Gari I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010800000000', 'Magajin Gari Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019010900000000', 'Magajin Gari Iii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160300000000', 'Magajin Rafi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160400000000', 'Magajin Rafi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260800000000', 'Magami (Mani)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360600000000', 'Magami (Sumaila)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070400000000', 'Magami-Gus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080700000000', 'Magarta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101300000000', 'Magarya (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034220900000000', 'Magarya (Wurno)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043201000000000', 'Magumeri (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121400000000', 'Magwanshi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150800000000', 'Mah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090700000000', 'Mahuta (Fakai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170700000000', 'Mahuta (Kafur)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080600000000', 'Mahuta A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080700000000', 'Mahuta B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080800000000', 'Mahuta C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070600000000', 'Mai Aduwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240500000000', 'Maiadua A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240600000000', 'Maiadua B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240700000000', 'Maiadua C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310600000000', 'Maibakko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040700000000', 'Maibara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090600000000', 'Maiburiji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070600000000', 'Maidabino A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070700000000', 'Maidabino B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070300000000', 'Maidahini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140600000000', 'Maigamji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210700000000', 'Maigana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200800000000', 'Maigatari Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018200900000000', 'Maigatari Kudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019071100000000', 'Maigizo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130300000000', 'Maigora','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022080900000000', 'Maigwaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022081000000000', 'Maihausawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160800000000', 'Maikamawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201000000000', 'Maikawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090800000000', 'Maikende','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070700000000', 'Maikilili','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240800000000', 'Maikoni A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021240900000000', 'Maikoni B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120500000000', 'Maikujera/Riji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010600000000', 'Maikulki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021080900000000', 'Maikwama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011300000000', 'Maimadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170600000000', 'Maimalari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130800000000', 'Maimusari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201100000000', 'Mainako North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201200000000', 'Mainako South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190800000000', 'Mainika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043140900000000', 'Mainok','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210500000000', 'Mairakumi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100800000000', 'Mairari (Guzamala)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160600000000', 'Mairari (Yunusari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043130900000000', 'Mairi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130400000000', 'Mairuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211300000000', 'Maisandari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030700000000', 'Maisandari /Waziri Ibrahim','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290700000000', 'Maitsida','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043260900000000', 'Maiwa (Nganzai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201300000000', 'Maiwa (Zaki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140800000000', 'Maiyalo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022140900000000', 'Maiyama (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100800000000', 'Maiyanchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130800000000', 'Maja Kura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150700000000', 'Majawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018190900000000', 'Maje (Kiyawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150800000000', 'Maje (Silame)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260700000000', 'Maje (Taura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300600000000', 'Maje/Karare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130600000000', 'Majema','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060700000000', 'Majen Wayya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260800000000', 'Majia','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270700000000', 'Majigiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021400000000', 'Makama A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021500000000', 'Makama B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019141000000000', 'Makami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180700000000', 'Makarfi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250600000000', 'Makauraci','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150700000000', 'Makawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022060900000000', 'Makera (Birnin Kebbi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021121000000000', 'Makera (Dutsin Ma)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140700000000', 'Makera (Funtua)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120700000000', 'Makera/Take Tsaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290800000000', 'Makoda (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130600000000', 'Makuaana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160700000000', 'Makuku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300700000000', 'Makurda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020150900000000', 'Makwaro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130800000000', 'Malagum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070700000000', 'Malam Dunari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210600000000', 'Malam Maduri (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160700000000', 'Malari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100800000000', 'Malisa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250700000000', 'Malumfashi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250800000000', 'Malumfashi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070800000000', 'Mamman Suka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034070900000000', 'Mammande','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140800000000', 'Mamudo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021150900000000', 'Manamawakafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030800000000', 'Manawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019130900000000', 'Manchok','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018050900000000', 'Mandabe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150800000000', 'Mandadawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240500000000', 'Mandala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050700000000', 'Mandaragirau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020180900000000', 'Mandawari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140800000000', 'Mandera','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210500000000', 'Manga Ushe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021260900000000', 'Mani (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011400000000', 'Mansur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180300000000', 'Mara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070800000000', 'Mara A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021070900000000', 'Mara B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170700000000', 'Maradawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090800000000', 'Maradun North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037090900000000', 'Maradun South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061000000000', 'Marafa (Birnin Kebbi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070400000000', 'Marafa (Bunza)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022090900000000', 'Marafa (Fakai)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034150900000000', 'Marafa (Silame)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034221000000000', 'Marafa (Wurno)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034060900000000', 'Marake','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241100000000', 'Maraku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120800000000', 'Marama/K','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071100000000', 'Marana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100800000000', 'Margadu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100600000000', 'Margai East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100700000000', 'Margai West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141000000000', 'Marguba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036051000000000', 'Marimarigudugurka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250800000000', 'Mariri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020100900000000', 'Marke (Dawakin Tofa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018160900000000', 'Marke (Kaugama)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180700000000', 'Marma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120800000000', 'Maro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043220900000000', 'Marte (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037100900000000', 'Maru (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022100900000000', 'Maruda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110800000000', 'Maruta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036021000000000', 'Masaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040500000000', 'Masama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022101000000000', 'Masama/Kwazgara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020201000000000', 'Masanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170800000000', 'Masari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043131000000000', 'Mashamari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101400000000', 'Mashema (Itas/Gadau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140600000000', 'Mashema (Zurmi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270800000000', 'Mashi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036051100000000', 'Mashio','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140800000000', 'Maska','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036110900000000', 'Maskandare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043190900000000', 'Masu (Mafa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360700000000', 'Masu (Sumaila)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018041000000000', 'Matamu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260600000000', 'Matan Fada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018100900000000', 'Matara Babba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280500000000', 'Matazu A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280600000000', 'Matazu B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018201000000000', 'Matoya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180800000000', 'Matsai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121500000000', 'Matsango','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130700000000', 'Matsaro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010600000000', 'Matseri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022051100000000', 'Matsinkai/Geza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061100000000', 'Maurida/Kariyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230800000000', 'Mawashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070500000000', 'Mayana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140700000000', 'Mayasa/Kuturu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170700000000', 'Mayori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160800000000', 'Mazamaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021160900000000', 'Mazanya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100400000000', 'Mazoji A (Daura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280700000000', 'Mazoji A (Matazu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100500000000', 'Mazoji B (Daura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280800000000', 'Mazoji B (Matazu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060700000000', 'Mbalala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171200000000', 'Mball','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060800000000', 'Mboakwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070800000000', 'Medu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130500000000', 'Mekiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101500000000', 'Melandige','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170600000000', 'Mesar Tudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180800000000', 'Meyari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150800000000', 'Mezan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220600000000', 'Miga (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041100000000', 'Minchika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300700000000', 'Minjibir (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240600000000', 'Mintar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021600000000', 'Miri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050800000000', 'Miringa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081100000000', 'Miya A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081200000000', 'Miya B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081300000000', 'Miya C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043261000000000', 'Miye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210700000000', 'Mkandari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030600000000', 'Modomawa East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030700000000', 'Modomawa West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043100900000000', 'Moduri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190400000000', 'Mogonho','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150800000000', 'Moholo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240700000000', 'Monguno (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120800000000', 'Morai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140800000000', 'Moriki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160700000000', 'Mosogun/Kujari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040600000000', 'Mubi Fusami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190800000000', 'Muchiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040800000000', 'Mudiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021261000000000', 'Muduru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036090900000000', 'Muguram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043191000000000', 'Mujimne','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018080900000000', 'Muku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070800000000', 'Mulgoi Kobchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080800000000', 'Muliye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021700000000', 'Mun-Munsal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022141000000000', 'Mungadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050700000000', 'Muntsira','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030800000000', 'Murfakalam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201400000000', 'Murmur North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201500000000', 'Murmur South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018101000000000', 'Musari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021290900000000', 'Musawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020600000000', 'Mussa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043221000000000', 'Musune','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070800000000', 'Mutai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120700000000', 'Mutubari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043221100000000', 'Muwalli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041200000000', 'Muzuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042031200000000', 'Mwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019180900000000', 'N/Doya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021250900000000', 'Na''Amma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050800000000', 'Nahuche','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020250900000000', 'Naibawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200700000000', 'Nandu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036120900000000', 'Nangere (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020700000000', 'Narayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230700000000', 'Nariya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100800000000', 'Nasagudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121600000000', 'Nasarawa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121700000000', 'Nasarawa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061200000000', 'Nasarawa I','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061300000000', 'Nasarawa Ii','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151200000000', 'Nasaru A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151300000000', 'Nasaru B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020800000000', 'Nassarawa (Chikun)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021140900000000', 'Nassarawa (Funtua)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081400000000', 'Nassarawa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081500000000', 'Nassarawa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030800000000', 'Nassarawa Godel East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037030900000000', 'Nassarawa Godel West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037031000000000', 'Nassarawa Mailayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040600000000', 'Nassarawa-Bkm','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020700000000', 'Nassarawa/Bka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410700000000', 'Nata/Ala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021241000000000', 'Natselle','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120800000000', 'Nayelwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036030900000000', 'Nayinawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250600000000', 'Ndufu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060600000000', 'Nduya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020700000000', 'Ng/Kopa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250700000000', 'Ngala (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040700000000', 'Ngalda Dumbulwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141100000000', 'Ngamdu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043201100000000', 'Ngamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150800000000', 'Ngaski (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036051200000000', 'Ngelzarma A.','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036051300000000', 'Ngelzarma B.','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043090900000000', 'Ngetra','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020800000000', 'Ngohi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036140900000000', 'Ngojin Alaraba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043201200000000', 'Ngubala B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043080900000000', 'Ngudoram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043020900000000', 'Ngulde','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036070900000000', 'Ngurbuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240800000000', 'Ngurno','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018041100000000', 'Nguwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151400000000', 'Ningi East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151500000000', 'Ningi West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200800000000', 'Ninzo North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019200900000000', 'Ninzo South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019201000000000', 'Ninzo West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036081000000000', 'Njibilwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043221200000000', 'Njine','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036031000000000', 'Njiwaji / Gwange','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060700000000', 'Nok','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043070900000000', 'Nzuda Wuyaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043131100000000', 'Old Maiduguri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050600000000', 'Paki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050700000000', 'Pala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180400000000', 'Palama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011500000000', 'Pali East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011600000000', 'Pali West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043120900000000', 'Pama/Waitam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019150900000000', 'Pambegua','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030800000000', 'Panhauya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020251000000000', 'Panshekara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051000000000', 'Papa North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051100000000', 'Papa South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019141100000000', 'Pari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043060900000000', 'Pemi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022091000000000', 'Peni Peni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180700000000', 'Peta','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042061100000000', 'Polchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042031300000000', 'Project','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043121000000000', 'Puba/Vidau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043111200000000', 'Pulka Bokko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110500000000', 'R/Kaya A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110600000000', 'R/Kaya B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140800000000', 'Raba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120600000000', 'Rabah (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060800000000', 'Radda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021330900000000', 'Rade ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021331000000000', 'Rade ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037061000000000', 'Rafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010700000000', 'Rafin Bauna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310700000000', 'Rafin Iwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018081000000000', 'Rafin Marke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210600000000', 'Rafin Zuru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071200000000', 'Raga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121800000000', 'Ragwam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070500000000', 'Raha/Mailseri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020041000000000', 'Rahama (Bebeji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210800000000', 'Rahama (Soba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180500000000', 'Rahama (Toro)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190500000000', 'Raka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019170900000000', 'Raminkura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019011000000000', 'Randagi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190700000000', 'Ranga A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190800000000', 'Ranga B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420600000000', 'Rangaza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020041100000000', 'Ranka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043150900000000', 'Rann','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320400000000', 'Rano (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020041200000000', 'Rantan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120700000000', 'Rara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180600000000', 'Rauta/Geji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220500000000', 'Rawayau A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220600000000', 'Rawayau B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190800000000', 'Ribah/Machika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180700000000', 'Ribina East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180800000000', 'Ribina West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019210900000000', 'Richifa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260700000000', 'Ridawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019020900000000', 'Rido','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019040900000000', 'Rigachikun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020270900000000', 'Rigar Duka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019041000000000', 'Rigasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070600000000', 'Rijiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170400000000', 'Rijiya  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170500000000', 'Rijiya  B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170500000000', 'Rijiyar Kirya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120700000000', 'Rijiyar Lemo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420700000000', 'Rijiyar Zaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020281100000000', 'Rikadawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030500000000', 'Rikina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021161000000000', 'Riko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210700000000', 'Rikoto','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019120900000000', 'Rimau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050800000000', 'Rimawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200700000000', 'Rimaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300800000000', 'Rimi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360800000000', 'Rimi (Sumaila)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030700000000', 'Rimin Dako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330800000000', 'Rimin Gado (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230600000000', 'Ringim (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270800000000', 'Ringim (Yankwashi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020800000000', 'Rini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021280900000000', 'Rinjin Idi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110500000000', 'Ririwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042180900000000', 'Rishi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340600000000', 'Rogo Ruma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340700000000', 'Rogo Sabon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340700000000', 'Rogogo Cidari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030800000000', 'Romo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180700000000', 'Romon Sarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240700000000', 'Roni (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120800000000', 'Rorau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018150900000000', 'Ruba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030600000000', 'Rugar Amanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034081000000000', 'Rugar Gatti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030700000000', 'Rugar Gidado','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021170900000000', 'Rugoji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036081100000000', 'Ruhu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037140900000000', 'Rukudawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021030900000000', 'Rumah','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130800000000', 'Rumfa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050800000000', 'Rumi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043021000000000', 'Rumirgo C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020360900000000', 'Rumo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320500000000', 'Runka ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320600000000', 'Runka ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320500000000', 'Rurum - Tsohon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320600000000', 'Rurum-Sabon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190600000000', 'Ruwa Wuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070700000000', 'Ruwan B0Re-Gus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340800000000', 'Ruwan Bago','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037120900000000', 'Ruwan Bore/Mirkidi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037101000000000', 'Ruwan Duruwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037121000000000', 'Ruwan Gizo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130500000000', 'Ruwan Goda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040700000000', 'Ruwan Jema','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021251000000000', 'Ruwan Sanyi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010800000000', 'S/Fada 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022010900000000', 'S/Fada 11','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100500000000', 'S/Gari North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100600000000', 'S/Gari South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060800000000', 'Sab-Chem','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019060900000000', 'Sab-Zuro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120800000000', 'Saban Gari East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170800000000', 'Sabaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022011000000000', 'Sabiyal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070600000000', 'Sabon Birni (Bunza)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020190900000000', 'Sabon Birni (Gwarzo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019041100000000', 'Sabon Birni (Igabi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034110900000000', 'Sabon Birni (Kware)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130700000000', 'Sabon Birni (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010700000000', 'Sabon Birni-Ank','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180800000000', 'Sabon Birni/Bakaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019171000000000', 'Sabon Birnin/U/Bawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010700000000', 'Sabon Gari (Barde)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019021000000000', 'Sabon Gari (Chikun)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100600000000', 'Sabon Gari (Daura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021141000000000', 'Sabon Gari (Funtua)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160800000000', 'Sabon Gari (Kudan)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220700000000', 'Sabon Gari (Miga)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410800000000', 'Sabon Gari (Tudun Wada)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440800000000', 'Sabon Gari (Wudil)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034050900000000', 'Sabon Gari Dole','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036130900000000', 'Sabon Gari Kanuri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020120900000000', 'Sabon Gari West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070800000000', 'Sabon Gari-Gus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018130900000000', 'Sabon Garu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042090900000000', 'Sabon Sara A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042091000000000', 'Sabon Sara B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019081200000000', 'Sabon Sarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019021100000000', 'Sabon Tasha','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021300900000000', 'Sabongari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100700000000', 'Sabongari West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018260900000000', 'Sabongari Yaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130600000000', 'Sabonlayi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043261100000000', 'Sabsabuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310800000000', 'Sabuwa A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021310900000000', 'Sabuwa B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021171000000000', 'Sabuwar Kasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051200000000', 'Sade East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051300000000', 'Sade West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021060900000000', 'Safana (Charanchi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320700000000', 'Safana (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161300000000', 'Safi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034180900000000', 'Saida /Goshe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020080900000000', 'Saidawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320700000000', 'Saji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022160900000000', 'Sakaba (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170600000000', 'Sakace','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037080900000000', 'Sakajiki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020330900000000', 'Sakara Tsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190700000000', 'Sakkai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201600000000', 'Sakwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043121100000000', 'Sakwa/Hema','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018061100000000', 'Sakwaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034071000000000', 'Salame','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180800000000', 'Saleri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190800000000', 'Salewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070700000000', 'Salwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151600000000', 'Sama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010700000000', 'Samama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019190900000000', 'Samaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037050900000000', 'Samawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019061000000000', 'Samban','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161400000000', 'Sambowal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019171100000000', 'Saminaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020081000000000', 'San San','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220800000000', 'San Sani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020061000000000', 'Sanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021331100000000', 'Sandamu (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034100900000000', 'Sangi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020181000000000', 'Sani Mainagge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037051000000000', 'Sankalawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230700000000', 'Sankara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240800000000', 'Sankau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034181000000000', 'Sanyinna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034140900000000', 'Sanyinnawal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018110900000000', 'Sara (Gwaram)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340800000000', 'Sara (Zango)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022141100000000', 'Sarandosa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170700000000', 'Sararin Gezawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300800000000', 'Sarbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090700000000', 'Sardauna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020030900000000', 'Sare-Sare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020140900000000', 'Sarina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022020900000000', 'Sarka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160600000000', 'Sarkin Adar G/Igwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160500000000', 'Sarkin Adar Gandu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010800000000', 'Sarkin Hausawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037081000000000', 'Sarkin Mafara S/Baura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160700000000', 'Sarkin Musulmi A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160800000000', 'Sarkin Musulmi B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100700000000', 'Sarkin Yara  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100800000000', 'Sarkin Yara  B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141300000000', 'Sarma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036031100000000', 'Sasawa / Kabaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020290900000000', 'Satame','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019050900000000', 'Saulawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037121100000000', 'Sauna Ruwan Gora','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022031000000000', 'Sauwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170700000000', 'Sawashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019051000000000', 'Saya Saya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020020900000000', 'Saya-Saya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021311000000000', 'Sayau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021281000000000', 'Sayaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050800000000', 'Saye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018081100000000', 'Sayori','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210800000000', 'Senchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090800000000', 'Shaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250700000000', 'Shabaru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018120900000000', 'Shafe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043121200000000', 'Shaffa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034141000000000', 'Shagari (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020160900000000', 'Shagogo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210600000000', 'Shahuchi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210800000000', 'Shaiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350800000000', 'Shakogi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260800000000', 'Shamakawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110800000000', 'Shanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170800000000', 'Shanga (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043271000000000', 'Shani (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020350900000000', 'Shanono (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022051200000000', 'Sharabi/Kinan Gulnai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210700000000', 'Sharada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043031100000000', 'Shehuri (Bama)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250800000000', 'Shehuri (Ngala)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211400000000', 'Shehuri North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043211500000000', 'Shehuri South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036150900000000', 'Shekau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021121100000000', 'Shema','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022181000000000', 'Shema/Daniya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130700000000', 'Sheme','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110600000000', 'Shere','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210800000000', 'Sheshe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141200000000', 'Shetimare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021050900000000', 'Shifdawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019030900000000', 'Shika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043061000000000', 'Shikarkir','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034051000000000', 'Shinaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021210900000000', 'Shinkafi 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021211000000000', 'Shinkafi 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037110900000000', 'Shinkafi North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037111000000000', 'Shinkafi South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161500000000', 'Shira (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170600000000', 'Shiyar Adar A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170700000000', 'Shiyar Adar B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170800000000', 'Shiyar Zamfara A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034170900000000', 'Shiyar Zamfara B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042131100000000', 'Shongo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040800000000', 'Shoye Garin Abba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030800000000', 'Shuni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020260900000000', 'Shuwaki (Kunchi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020410900000000', 'Shuwaki (Tudun Wada)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018191000000000', 'Shuwarin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034020900000000', 'Sifawa/Lukuyawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043151000000000', 'Sigal/Karche','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034151000000000', 'Silame (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043050900000000', 'Silumthla','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230800000000', 'Sintilmawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110700000000', 'Sirika A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110800000000', 'Sirika B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141400000000', 'Sirko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020361000000000', 'Sitti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019211000000000', 'Soba (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160800000000', 'Sojiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021270900000000', 'Sonkaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010800000000', 'Soron Gabas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034010900000000', 'Soron Yamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043031200000000', 'Soye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036010900000000', 'Sugum Tagali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043261200000000', 'Sugundure','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200800000000', 'Sukuntuni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250800000000', 'Sule Tankarkar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020361100000000', 'Sumaila (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170800000000', 'Sumbar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030700000000', 'Sundimina','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036151000000000', 'Sungul Koka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043240900000000', 'Sure','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030800000000', 'Surko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022181100000000', 'Suru (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034190900000000', 'Sutti/Kwaraga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100800000000', 'T/Nupawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019230900000000', 'T/Tukur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019181000000000', 'T/Wada (Makarfi)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019231000000000', 'T/Wada (Zaria)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019100900000000', 'T/Wada North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019101000000000', 'T/Wada South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019160900000000', 'Taba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019011100000000', 'Tabani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021291000000000', 'Tabanni/Yarraddau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022210900000000', 'Tadurga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021200900000000', 'Tafashiya / Nasarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130800000000', 'Tafoki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036111000000000', 'Taganama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018210900000000', 'Tagoro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110700000000', 'Tagwaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034021000000000', 'Taka-Tuku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020370900000000', 'Takai (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034051100000000', 'Takakume','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130800000000', 'Takatsaba (Sabon Birni)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018250900000000', 'Takatsaba (Sule Tankakar)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019071200000000', 'Takau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022131100000000', 'Takware (Koko/Besse)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022170900000000', 'Takware (Shanga)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018021100000000', 'Takwasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181000000000', 'Tama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021051000000000', 'Tama/Daye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020331000000000', 'Tamawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034071100000000', 'Tambakarka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034181100000000', 'Tambawal/Shinfiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431100000000', 'Tamburawan Gabas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021271000000000', 'Tamilo  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021271100000000', 'Tamilo  B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043191100000000', 'Tamsum-Gamdua','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431200000000', 'Tanagar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020271000000000', 'Tanawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020090900000000', 'Tanburawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090700000000', 'Tandama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020291000000000', 'Tangaji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034191000000000', 'Tangaza (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019121000000000', 'Tantatu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171300000000', 'Tapshin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034130900000000', 'Tara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230800000000', 'Tarai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021040900000000', 'Taramnawa/Bare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071300000000', 'Taranka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130600000000', 'Tarauni (Gabasawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380700000000', 'Tarauni (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201700000000', 'Tarbuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020041300000000', 'Tariwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071400000000', 'Tarmasuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018180900000000', 'Tasheguwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018211000000000', 'Tashena (Malam Maduri)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042201800000000', 'Tashena (Zaki)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400600000000', 'Tatsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020101000000000', 'Tattarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018261000000000', 'Taura (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051400000000', 'Tauya East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051500000000', 'Tauya West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019101100000000', 'Television','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040800000000', 'Teli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036081200000000', 'Teteba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090600000000', 'Tidi Bale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151700000000', 'Tiffi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022040900000000', 'Tiggi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036121000000000', 'Tikau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181100000000', 'Tilde','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070800000000', 'Tilli/Helama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021800000000', 'Tirwun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043201300000000', 'Titiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042190900000000', 'Tiyin A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042191000000000', 'Tiyin B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141300000000', 'Tobolo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120800000000', 'Tofa (Rabah)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018230900000000', 'Tofa (Ringim)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391000000000', 'Tofa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141500000000', 'Tofu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200400000000', 'Tondi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018211100000000', 'Toni Kutara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230800000000', 'Torankawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020010900000000', 'Toranke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181200000000', 'Toro (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160800000000', 'Toshia','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034081100000000', 'Tozai (Illela)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090700000000', 'Tozai (Isa)','Sub-District','Nigeria' UNION ALL
            --SELECT 'NG001021200100000000', 'Tsa/Magam','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090800000000', 'Tsabre','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034030900000000', 'Tsafanade','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130700000000', 'Tsafe Central','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161600000000', 'Tsafi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021261100000000', 'Tsagem/Takusheyi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021301000000000', 'Tsagero','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021061000000000', 'Tsakatsa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034111000000000', 'Tsaki/Walakae','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020300900000000', 'Tsakiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091000000000', 'Tsakuwa (Dawakin Kudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042121900000000', 'Tsakuwa (Katagum)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020301000000000', 'Tsakuwa (Minjibir)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018220900000000', 'Tsakuwawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034131000000000', 'Tsamaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034120900000000', 'Tsamiya (Rabah)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034200900000000', 'Tsamiya (Tureta)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170800000000', 'Tsamiya Babba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090800000000', 'Tsangamawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018111000000000', 'Tsangarwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020021000000000', 'Tsangaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021020900000000', 'Tsanni','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400700000000', 'Tsanyawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018151000000000', 'Tsarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320800000000', 'Tsaskiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241200000000', 'Tsaudawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020351000000000', 'Tsaure','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220700000000', 'Tsauri A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220800000000', 'Tsauri B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037091000000000', 'Tsibiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018010900000000', 'Tsidar','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021011100000000', 'Tsiga/Makurdi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018191100000000', 'Tsirma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034041100000000', 'Tsitse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036131000000000', 'Tsohon  Nguru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020411000000000', 'Tsohon Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043131200000000', 'Tuba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042131200000000', 'Tubule','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420800000000', 'Tudun Fulani','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021141100000000', 'Tudun Iya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220600000000', 'Tudun Kaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034011000000000', 'Tudun Kose','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022161000000000', 'Tudun Kuka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020311000000000', 'Tudun Murtala','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020210900000000', 'Tudun Nufawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034171000000000', 'Tudun Wada  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034171100000000', 'Tudun Wada  B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021100900000000', 'Tudun Wada (Daura)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037070900000000', 'Tudun Wada (Gusau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020311100000000', 'Tudun Wada (Nassarawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042191100000000', 'Tudun Wada (Warji)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021291100000000', 'Tuge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181300000000', 'Tulai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034021100000000', 'Tulluwa/Kulafasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036170900000000', 'Tulotulo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034061000000000', 'Tulun Doya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020170900000000', 'Tumbau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071500000000', 'Tumbi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021081000000000', 'Tumburkai A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021081100000000', 'Tumburkai B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020101100000000', 'Tumfafi (Dawakin Tofa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161700000000', 'Tumfafi (Shira)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018240900000000', 'Tunas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022070900000000', 'Tunga (Bunza)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034221100000000', 'Tunga (Wurno)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034111100000000', 'Tungar Mallamawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034031000000000', 'Tuntubetsefe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018181000000000', 'Turabu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220700000000', 'Turawa (Karaye)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019211100000000', 'Turawa (Soba)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034090900000000', 'Turba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018201100000000', 'Turbus','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034201000000000', 'Tureta (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036040900000000', 'Turmi Malluri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034121000000000', 'Tursa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019041200000000', 'Turunku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043021100000000', 'Uba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037061100000000', 'Uban Dawaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021101000000000', 'Ubandawaki A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021101100000000', 'Ubandawaki B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071600000000', 'Udubo Central','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071700000000', 'Udubo Norht East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043081000000000', 'Ufaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061400000000', 'Ujariyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380800000000', 'Ung Uku Cikin Gari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020380900000000', 'Ung Uku Kauyen Alu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019231100000000', 'Ung. Fatika','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019191000000000', 'Ung. Gabas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018161000000000', 'Ung. Jibrin','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019231200000000', 'Ung. Juma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019101200000000', 'Ung. Sanusi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021041000000000', 'Ung.Rai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020420900000000', 'Ungogo (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034101000000000', 'Ungushi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020011000000000', 'Unguwar Bai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019090900000000', 'Unguwar Dosa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091100000000', 'Unguwar Duniya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020230900000000', 'Unguwar Gai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020381000000000', 'Unguwar Gano','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220800000000', 'Unguwar Hajji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034131100000000', 'Unguwar Lalle','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019091000000000', 'Unguwar Rimi (Kaduna North)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020251100000000', 'Unguwar Rimi (Kumbotso)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391100000000', 'Unguwar Rimi (Tofa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019091100000000', 'Unguwar Sarki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019091200000000', 'Unguwar Shanu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110800000000', 'Unguwar Tsohuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020191000000000', 'Unguwar Tudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018030900000000', 'Unguwar Ya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018170900000000', 'Ungwar Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018171000000000', 'Ungwar Gabas','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220600000000', 'Ungwar Gaiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220700000000', 'Ungwar Rimi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018171100000000', 'Ungwar Yamma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018011000000000', 'Unik','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020440900000000', 'Utai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022150900000000', 'Utono','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043021200000000', 'Uvu Uda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042091100000000', 'Uzum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034031100000000', 'Wababe/Salau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036100900000000', 'Wachakal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180800000000', 'Wada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021031000000000', 'Wagini','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036071000000000', 'Wagir','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051600000000', 'Wahu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171400000000', 'Wai A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042171500000000', 'Wai B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020291100000000', 'Wailare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020050900000000', 'Waire','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022190900000000', 'Waje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141400000000', 'Wajiro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020041400000000', 'Wak','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043111300000000', 'Wala Warare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043271100000000', 'Walama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034211100000000', 'Wamakko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043021300000000', 'Wamdeeo G','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043101000000000', 'Wamiri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042061200000000', 'Wandi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042191200000000', 'Wando','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020171000000000', 'Wangara (Gezawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391200000000', 'Wangara (Tofa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042131300000000', 'Wanka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037071000000000', 'Wanke','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022151000000000', 'Wara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010800000000', 'Waramu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431300000000', 'Warawa (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036101000000000', 'Waro','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043250900000000', 'Warshele','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019201100000000', 'Wasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022191000000000', 'Wasagu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020301100000000', 'Wasai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043141500000000', 'Wasaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036121100000000', 'Watinane','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043180900000000', 'Wawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043071000000000', 'Wawa Korede','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019031000000000', 'Wazata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034160900000000', 'Waziri A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034161000000000', 'Waziri B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034161100000000', 'Waziri C','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043061100000000', 'Whuntaku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037071100000000', 'Wonaka','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181400000000', 'Wonu North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181500000000', 'Wonu South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019231300000000', 'Wuciciri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020441000000000', 'Wudil (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020161000000000', 'Wudilawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043251000000000', 'Wulgo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043241000000000', 'Wulo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043251100000000', 'Wurge','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021220900000000', 'Wurma A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021221000000000', 'Wurma B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018031000000000', 'Wurno (Birnin Kudu)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020031000000000', 'Wuro Bagga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022120900000000', 'Wuro/Gauri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037010900000000', 'Wuya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043040900000000', 'Wuyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021251100000000', 'Yaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043160900000000', 'Yabal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043031300000000', 'Yabari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034230900000000', 'Yabo A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034231000000000', 'Yabo B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020421000000000', 'Yada Kunya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020151000000000', 'Yada Kwari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043161000000000', 'Yajiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021090900000000', 'Yakaji A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021091000000000', 'Yakaji B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020211000000000', 'Yakasai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019031100000000', 'Yakawada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241300000000', 'Yako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020281200000000', 'Yakun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020071200000000', 'Yalawa (Dala)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018070900000000', 'Yalawa (Gagarawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043161100000000', 'Yale','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042081600000000', 'Yali','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022191100000000', 'Yalmo/Shindi/Wari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018161100000000', 'Yalo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011700000000', 'Yalo 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011800000000', 'Yalo 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241400000000', 'Yalwa (Kiru)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320800000000', 'Yalwa (Rano)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391300000000', 'Yalwa Karama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018031100000000', 'Yalwan Damai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020331100000000', 'Yalwan Danziyal','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041300000000', 'Yame','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021110900000000', 'Yamel A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021111000000000', 'Yamel B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021211100000000', 'Yamma 1','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021211200000000', 'Yamma 2','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021251200000000', 'Yammama','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020121000000000', 'Yammata','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020220900000000', 'Yammedi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042021900000000', 'Yamrat','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091200000000', 'Yan Barau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400800000000', 'Yan Kamaye','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021130900000000', 'Yan Kara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161800000000', 'Yana','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037141000000000', 'Yanbuki/Dutsi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041400000000', 'Yanda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020261000000000', 'Yandadi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021180900000000', 'Yandaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431400000000', 'Yandalla','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018251000000000', 'Yandamo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021151000000000', 'Yandoma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018221000000000', 'Yandona','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130800000000', 'Yandoton Daji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021041100000000', 'Yanduna','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018231000000000', 'Yandutse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034091000000000', 'Yanfako','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021161100000000', 'Yangaiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042111200000000', 'Yangamai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020400900000000', 'Yanganau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020431500000000', 'Yangizo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021051100000000', 'Yangora','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021181000000000', 'Yanhoho','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037081100000000', 'Yankaba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091300000000', 'Yankatsari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018131000000000', 'Yankoli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037130900000000', 'Yankuzo A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037131000000000', 'Yankuzo B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018270900000000', 'Yankwashi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020051000000000', 'Yanlami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021041200000000', 'Yanmaulu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391400000000', 'Yanoko','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021071000000000', 'Yantumaki A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021071100000000', 'Yantumaki B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037131100000000', 'Yanware','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018241000000000', 'Yanzaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021340900000000', 'Yar Daje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022171000000000', 'Yarbesse','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021021000000000', 'Yargamji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091400000000', 'Yargaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037020900000000', 'Yargeda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021190900000000', 'Yargoje','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020391500000000', 'Yarimawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037021000000000', 'Yarkofoji','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021131000000000', 'Yarmalamai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037011000000000', 'Yarsabaya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001034121100000000', 'Yartsakkuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021191000000000', 'Yartsamiya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020411100000000', 'Yaryasa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021230900000000', 'Yashe  A','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021231000000000', 'Yashe B','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040800000000', 'Yashi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010800000000', 'Yau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130700000000', 'Yautar Arewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130800000000', 'Yautar Kudu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042051700000000', 'Yautare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021031100000000', 'Yauyau/Malamawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043010900000000', 'Yawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043051000000000', 'Yawi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021151100000000', 'Yaya/Bidore','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041500000000', 'Yayari (Damban)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018131100000000', 'Yayari (Hadejia)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018051000000000', 'Yayari Tukur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042122000000000', 'Yayu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022021000000000', 'Yeldu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043241100000000', 'Yele','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019021200000000', 'Yelwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200500000000', 'Yelwa Central','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200600000000', 'Yelwa East','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200700000000', 'Yelwa North','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200800000000', 'Yelwa South','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022200900000000', 'Yelwa West','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036141000000000', 'Yerimaram','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043181000000000', 'Yimirdalong','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043011000000000', 'Yituwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022041000000000', 'Yola (Augie)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018121000000000', 'Yola (Gwiwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042111300000000', 'Yola (Jama''Are)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020221000000000', 'Yola (Karaye)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043171000000000', 'Yoyo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042011900000000', 'Yuli','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020130900000000', 'Yumbu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036160900000000', 'Yunusari (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036171000000000', 'Yusufarri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042151800000000', 'Yuwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043230900000000', 'Z. Umorti','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042091200000000', 'Zabi (Giade)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019151000000000', 'Zabi (Kubau)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019161000000000', 'Zabi (Kudan)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019191100000000', 'Zabi (Sabon Gari)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036091000000000', 'Zabudum/ Dachia','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042141600000000', 'Zadawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043221300000000', 'Zaga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022051300000000', 'Zagga/Kwasara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020110900000000', 'Zainabi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020211100000000', 'Zaitawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036161000000000', 'Zajibiriri/Dumbol','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020141000000000', 'Zakarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020131000000000', 'Zakirai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021320900000000', 'Zakka ''A''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021321000000000', 'Zakka ''B''','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181600000000', 'Zalau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220800000000', 'Zaman Dabo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022201000000000', 'Zamare','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036041000000000', 'Zamba Mazawun','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018111100000000', 'Zandam Nagogo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043031400000000', 'Zangeri','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020171100000000', 'Zango (Gezawa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018091100000000', 'Zango (Gumel)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021191100000000', 'Zango (Kankara)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020211200000000', 'Zango (Kano Municipal)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001021341000000000', 'Zango (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020421100000000', 'Zango (Ungogo)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018151100000000', 'Zango Kura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019220900000000', 'Zango Urban','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019041300000000', 'Zangon Aya','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020331200000000', 'Zangon Dan Abdu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019131000000000', 'Zankan','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043041000000000', 'Zara','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018071000000000', 'Zarada','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042181700000000', 'Zaranda','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043051100000000', 'Zarawuyaki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018221100000000', 'Zareku','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020340900000000', 'Zarewa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043231000000000', 'Zari','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022131200000000', 'Zaria/Amiru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020401000000000', 'Zarogi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037040900000000', 'Zarummai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037041000000000', 'Zauma (Bukkuyum)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018121100000000', 'Zauma (Gwiwa)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042041600000000', 'Zaura','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022061500000000', 'Zauru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022031100000000', 'Zazzagawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043191200000000', 'Zengebe','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001036011000000000', 'Zengo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042071800000000', 'Zindiwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020320900000000', 'Zinyau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042091300000000', 'Zirami','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022211000000000', 'Zodi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020091500000000', 'Zogarawa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022071000000000', 'Zogirma','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019221000000000', 'Zonkwa','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019221100000000', 'Zonzon','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043091000000000', 'Zowo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020341000000000', 'Zoza','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042101600000000', 'Zubiki','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042161900000000', 'Zubo','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020371000000000', 'Zuga','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020131100000000', 'Zugachi','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018241100000000', 'Zugai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001022121000000000', 'Zuguru','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001043241200000000', 'Zulum','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042061300000000', 'Zumbul','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001018271000000000', 'Zungumba','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042022000000000', 'Zungur','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001019151100000000', 'Zuntu','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020321000000000', 'Zurgau','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001042191300000000', 'Zurgwai','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001037141100000000', 'Zurmi (Sub-District)','Sub-District','Nigeria' UNION ALL
            SELECT 'NG001020241500000000', 'Zuwo','Sub-District','Nigeria';

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

	SELECT region_code, r.id, 'region' ,x.id FROM region r
    INNER JOIN ( SELECT id FROM auth_user WHERE username = 'demo_user' ) x
    ON 1=1;

    INSERT INTO document_to_source_object_map
    (document_id,source_object_map_id)
    SELECT sd.id , som.id
    FROM source_data_document sd
    INNER JOIN source_object_map som
    ON som.content_type = 'region'
    AND sd.docfile = 'initialize-db';


    """)
    ]
