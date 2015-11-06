# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0006_cache_and_cleanup_metadata'),
    ]

    operations = [
    migrations.RunSQL('''


    DROP TABLE IF EXISTS _tmp_locations;
    CREATE TABLE _tmp_locations
    AS
    SELECT
            'Afghanistan'  as office
        	,'balkh-province' as location_slug
        	,'AF001036000000000000' as location_code
        	,'Balkh' as location_name
        	,'AF001000000000000000' as parent_location_code
        	,'province' as location_type UNION ALL
        SELECT 'Afghanistan','bamyan-province','AF001037000000000000','Bamyan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','farah-province','AF001039000000000000','Farah','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','ghazni-province','AF001041000000000000','Ghazni','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','kabul-province','AF001046000000000000','Kabul','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','kunduz-province','AF001051000000000000','Kunduz','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','sar-e-pul-province','AF001062000000000000','Sar-E-Pul','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','kandahar-province','AF001047000000000000','Kandahar (Province)','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','badakhshan','AF001033000000000000','Badakhshan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','badghis','AF001034000000000000','Badghis','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','baghlan','AF001035000000000000','Baghlan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','daykundi','AF001038000000000000','Daykundi','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','faryab','AF001040000000000000','Faryab','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','ghor','AF001042000000000000','Ghor','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','hilmand','AF001043000000000000','Hilmand','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','hirat','AF001044000000000000','Hirat','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','jawzjan','AF001045000000000000','Jawzjan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','kapisa','AF001048000000000000','Kapisa','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','khost','AF001049000000000000','Khost','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','kunar','AF001050000000000000','Kunar','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','laghman','AF001052000000000000','Laghman','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','logar','AF001053000000000000','Logar','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','nangarhar','AF001054000000000000','Nangarhar','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','nimroz','AF001055000000000000','Nimroz','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','nuristan','AF001056000000000000','Nuristan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','paktika','AF001057000000000000','Paktika','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','paktya','AF001058000000000000','Paktya','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','panjsher','AF001059000000000000','Panjsher','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','parwan','AF001060000000000000','Parwan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','samangan','AF001061000000000000','Samangan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','takhar','AF001063000000000000','Takhar','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','uruzgan','AF001064000000000000','Uruzgan','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','wardak','AF001065000000000000','Wardak','AF001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','zabul','AF001066000000000000','Zabul','AF001000000000000000','province' UNION ALL
        SELECT 'Pakistan','ajk','PK001001000000000000','Ajk','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','balochistan','PK001002000000000000','Balochistan','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','fata','PK001010000000000000','Fata','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','gilgit-baltistan','PK001003000000000000','Gilgit Baltistan','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','islamabad','PK001004000000000000','Islamabad','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','khyber-pakhtoon','PK001011000000000000','Khyber Pakhtoon','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','punjab','PK001006000000000000','Punjab','PK001000000000000000','province' UNION ALL
        SELECT 'Pakistan','sindh','PK001007000000000000','Sindh','PK001000000000000000','province' UNION ALL
        SELECT 'Afghanistan','arghandab-(zabul)','AF001066001000000000','Arghandab','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','kakar','AF001066004000000000','Kakar','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','tarnak-wa-jaldak','AF001066011000000000','Tarnak Wa Jaldak','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','shinkay','AF001066009000000000','Shinkay','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','shomulzay','AF001066010000000000','Shomulzay','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','nawbahar','AF001066006000000000','Nawbahar','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','mizan','AF001066005000000000','Mizan','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','qalat','AF001066007000000000','Qalat','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','daychopan','AF001066003000000000','Daychopan','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','atghar','AF001066002000000000','Atghar','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahjoy','AF001066008000000000','Shahjoy','AF001066000000000000','district' UNION ALL
        SELECT 'Afghanistan','jaghatu-(wardak)','AF001065004000000000','Jaghatu','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','jalrez','AF001065005000000000','Jalrez','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','chak','AF001065001000000000','Chak','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','nerkh','AF001065008000000000','Nerkh','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','maydanshahr','AF001065007000000000','Maydanshahr','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','markaz-e-behsud','AF001065006000000000','Markaz-E-Behsud','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','hesa-e--awal-e--behsud','AF001065003000000000','Hesa-E- Awal-E- Behsud','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','daymirdad','AF001065002000000000','Daymirdad','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','saydabad','AF001065009000000000','Saydabad','AF001065000000000000','district' UNION ALL
        SELECT 'Afghanistan','chora','AF001064001000000000','Chora','AF001064000000000000','district' UNION ALL
        SELECT 'Afghanistan','tirinkot','AF001064005000000000','Tirinkot','AF001064000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehrawud','AF001064002000000000','Dehrawud','AF001064000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahid-e-hassas','AF001064004000000000','Shahid-E-Hassas','AF001064000000000000','district' UNION ALL
        SELECT 'Afghanistan','khasuruzgan','AF001064003000000000','Khasuruzgan','AF001064000000000000','district' UNION ALL
        SELECT 'Afghanistan','kalafgan','AF001063010000000000','Kalafgan','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','taloqan','AF001063015000000000','Taloqan','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','warsaj','AF001063016000000000','Warsaj','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','farkhar','AF001063008000000000','Farkhar','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','bangi','AF001063002000000000','Bangi','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','chahab','AF001063003000000000','Chahab','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','eshkashem','AF001063007000000000','Eshkashem','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','namakab','AF001063013000000000','Namakab','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','baharak-(takhar)','AF001063001000000000','Baharak (Takhar)','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','chal','AF001063004000000000','Chal','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','yangi-qala','AF001063017000000000','Yangi Qala','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','rostaq','AF001063014000000000','Rostaq','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','hazarsumuch','AF001063009000000000','Hazarsumuch','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','dasht-e--qala','AF001063006000000000','Dasht-E- Qala','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','darqad','AF001063005000000000','Darqad','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajaghar','AF001063012000000000','Khwajaghar','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajabahawuddin','AF001063011000000000','Khwajabahawuddin','AF001063000000000000','district' UNION ALL
        SELECT 'Afghanistan','feroznakhchir','AF001061004000000000','Feroznakhchir','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','aybak','AF001061001000000000','Aybak','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','hazrat-e--sultan','AF001061005000000000','Hazrat-E- Sultan','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','ruy-e-duab','AF001061007000000000','Ruy-E-Duab','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','khuram-wa-sarbagh','AF001061006000000000','Khuram Wa Sarbagh','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','dara-e--suf-e--payin','AF001061002000000000','Dara-E- Suf-E- Payin','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','dara-e-suf-e-bala','AF001061003000000000','Dara-E Suf-E-Bala','AF001061000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghorband','AF001060003000000000','Ghorband','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','shinwari','AF001060009000000000','Shinwari','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','jabalussaraj','AF001060004000000000','Jabalussaraj','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','charikar','AF001060002000000000','Charikar','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','bagram','AF001060001000000000','Bagram','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','surkh-e--parsa','AF001060010000000000','Surkh-E- Parsa','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','salang','AF001060006000000000','Salang','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','koh-e--safi','AF001060005000000000','Koh-E- Safi','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','saydkhel','AF001060007000000000','Saydkhel','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','shekhali','AF001060008000000000','Shekhali','AF001060000000000000','district' UNION ALL
        SELECT 'Afghanistan','paryan','AF001059005000000000','Paryan','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','onaba(anawa)','AF001059004000000000','Onaba(Anawa)','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','shutul','AF001059007000000000','Shutul','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','rukha','AF001059006000000000','Rukha','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','bazarak','AF001059001000000000','Bazarak','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','khenj-(hes-e--awal)','AF001059003000000000','Khenj (Hes-E- Awal)','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','dara','AF001059002000000000','Dara','AF001059000000000000','district' UNION ALL
        SELECT 'Afghanistan','dand-wa-patan','AF001058004000000000','Dand Wa Patan','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','janikhel-(paktya)','AF001058006000000000','Janikhel (Paktya)','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','gardez','AF001058005000000000','Gardez','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','zadran','AF001058010000000000','Zadran','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','chamkani','AF001058003000000000','Chamkani','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','ahmadaba','AF001058001000000000','Ahmadaba','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','zurmat','AF001058011000000000','Zurmat','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','alikhel-(jaji)','AF001058002000000000','Alikhel (Jaji)','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','lija-ahmad-khel','AF001058007000000000','Lija Ahmad Khel','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','sayedkaram','AF001058008000000000','Sayedkaram','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','shawak','AF001058009000000000','Shawak','AF001058000000000000','district' UNION ALL
        SELECT 'Afghanistan','ziruk','AF001057019000000000','Ziruk','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','yosufkhel','AF001057017000000000','Yosufkhel','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','omna','AF001057008000000000','Omna','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','janikhel-(paktika)','AF001057005000000000','Janikhel (Paktika)','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','turwo-(tarwe)','AF001057012000000000','Turwo (Tarwe)','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','urgun','AF001057013000000000','Urgun','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','wazakhah','AF001057014000000000','Wazakhah','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','wormamay','AF001057015000000000','Wormamay','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','yahyakhel','AF001057016000000000','Yahyakhel','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','naka','AF001057007000000000','Naka','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','zarghunshahr','AF001057018000000000','Zarghunshahr','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','matakhan','AF001057006000000000','Matakhan','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','bermel','AF001057001000000000','Bermel','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','dila','AF001057002000000000','Dila','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','gyan','AF001057004000000000','Gyan','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','sarobi','AF001057009000000000','Sarobi','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','sarrawzah(sarhawzah)','AF001057010000000000','Sarrawzah(Sarhawzah)','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','sharan','AF001057011000000000','Sharan','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','gomal','AF001057003000000000','Gomal','AF001057000000000000','district' UNION ALL
        SELECT 'Afghanistan','kamdesh','AF001056003000000000','Kamdesh','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','barg-e--matal','AF001056001000000000','Barg-E- Matal','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','waygal','AF001056008000000000','Waygal','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','nurgeram','AF001056005000000000','Nurgeram','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','poruns','AF001056006000000000','Poruns','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','duab','AF001056002000000000','Duab','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','mandol','AF001056004000000000','Mandol','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','wama','AF001056007000000000','Wama','AF001056000000000000','district' UNION ALL
        SELECT 'Afghanistan','kang','AF001055003000000000','Kang','AF001055000000000000','district' UNION ALL
        SELECT 'Afghanistan','charburjak','AF001055002000000000','Charburjak','AF001055000000000000','district' UNION ALL
        SELECT 'Afghanistan','chakhansur','AF001055001000000000','Chakhansur','AF001055000000000000','district' UNION ALL
        SELECT 'Afghanistan','zaranj','AF001055005000000000','Zaranj','AF001055000000000000','district' UNION ALL
        SELECT 'Afghanistan','khashrod','AF001055004000000000','Khashrod','AF001055000000000000','district' UNION ALL
        SELECT 'Afghanistan','pachieragam','AF001054018000000000','Pachieragam','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','kama','AF001054011000000000','Kama','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','shinwar','AF001054021000000000','Shinwar','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','jalalabad','AF001054010000000000','Jalalabad','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','chaparhar','AF001054004000000000','Chaparhar','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','nazyan','AF001054017000000000','Nazyan','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','muhmand-dara','AF001054016000000000','Muhmand Dara','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','achin','AF001054001000000000','Achin','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','durbaba','AF001054007000000000','Durbaba','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','behsud','AF001054003000000000','Behsud','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehbala','AF001054006000000000','Dehbala','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','hesarak','AF001054009000000000','Hesarak','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','lalpur','AF001054015000000000','Lalpur','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','rodat','AF001054019000000000','Rodat','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','surkhrod','AF001054022000000000','Surkhrod','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','kuzkunar','AF001054014000000000','Kuzkunar','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','kot','AF001054013000000000','Kot','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','khogyani','AF001054012000000000','Khogyani','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','batikot','AF001054002000000000','Batikot','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','sherzad','AF001054020000000000','Sherzad','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','dara-e-nur','AF001054005000000000','Dara-E-Nur','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','goshta','AF001054008000000000','Goshta','AF001054000000000000','district' UNION ALL
        SELECT 'Afghanistan','barakibarak','AF001053002000000000','Barakibarak','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','charkh','AF001053003000000000','Charkh','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','pul-e--alam','AF001053007000000000','Pul-E- Alam','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','mohammadagha','AF001053006000000000','Mohammadagha','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','azra','AF001053001000000000','Azra','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','khoshi','AF001053005000000000','Khoshi','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','kharwar','AF001053004000000000','Kharwar','AF001053000000000000','district' UNION ALL
        SELECT 'Afghanistan','mehtarlam','AF001052004000000000','Mehtarlam','AF001052000000000000','district' UNION ALL
        SELECT 'Afghanistan','alishang','AF001052002000000000','Alishang','AF001052000000000000','district' UNION ALL
        SELECT 'Afghanistan','alingar','AF001052001000000000','Alingar','AF001052000000000000','district' UNION ALL
        SELECT 'Afghanistan','qarghayi','AF001052005000000000','Qarghayi','AF001052000000000000','district' UNION ALL
        SELECT 'Afghanistan','dawlatshah','AF001052003000000000','Dawlatshah','AF001052000000000000','district' UNION ALL
        SELECT 'Afghanistan','dangam','AF001050005000000000','Dangam','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghaziabad','AF001050007000000000','Ghaziabad','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','barkunar','AF001050002000000000','Barkunar','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','asadabad','AF001050001000000000','Asadabad','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','watapur','AF001050015000000000','Watapur','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','chawkay','AF001050004000000000','Chawkay','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','chapadara','AF001050003000000000','Chapadara','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','nurgal','AF001050012000000000','Nurgal','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','nari','AF001050011000000000','Nari','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','narang','AF001050010000000000','Narang','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','marawara','AF001050009000000000','Marawara','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','sarkani','AF001050013000000000','Sarkani','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','khaskunar','AF001050008000000000','Khaskunar','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','dara-e-pech','AF001050006000000000','Dara-E-Pech','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','shigal-wa-sheltan','AF001050014000000000','Shigal Wa Sheltan','AF001050000000000000','district' UNION ALL
        SELECT 'Afghanistan','tani','AF001049012000000000','Tani','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','jajimaydan','AF001049003000000000','Jajimaydan','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','terezayi','AF001049013000000000','Terezayi','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','musakhel-(khost)','AF001049006000000000','Musakhel (Khost)','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','bak','AF001049001000000000','Bak','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','nadirshahkot','AF001049007000000000','Nadirshahkot','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','qalandar','AF001049008000000000','Qalandar','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','mandozayi','AF001049005000000000','Mandozayi','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','spera','AF001049011000000000','Spera','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','sabari','AF001049009000000000','Sabari','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','gurbuz','AF001049002000000000','Gurbuz','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','khost(matun)','AF001049004000000000','Khost(Matun)','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','shamal','AF001049010000000000','Shamal','AF001049000000000000','district' UNION ALL
        SELECT 'Afghanistan','alasay','AF001048001000000000','Alasay','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','nejrab','AF001048006000000000','Nejrab','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','mahmud-e--raqi','AF001048005000000000','Mahmud-E- Raqi','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','hisa-e--duwum-e--kohestan','AF001048003000000000','Hisa-E- Duwum-E- Kohestan','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','hisa-e--awal-e--kohestan','AF001048002000000000','Hisa-E- Awal-E- Kohestan','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','kohband','AF001048004000000000','Kohband','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','tagab-(kapisa)','AF001048007000000000','Tagab (Kapisa)','AF001048000000000000','district' UNION ALL
        SELECT 'Afghanistan','fayzabad-(jawzjan)','AF001045003000000000','Fayzabad (Jawzjan)','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','mingajik','AF001045008000000000','Mingajik','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','aqcha','AF001045001000000000','Aqcha','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','mardyan','AF001045007000000000','Mardyan','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','qarqin','AF001045009000000000','Qarqin','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','qushtepa','AF001045010000000000','Qushtepa','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','darzab','AF001045002000000000','Darzab','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajadukoh','AF001045006000000000','Khwajadukoh','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','khanaqa','AF001045005000000000','Khanaqa','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','khamyab','AF001045004000000000','Khamyab','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','shiberghan','AF001045011000000000','Shiberghan','AF001045000000000000','district' UNION ALL
        SELECT 'Afghanistan','shindand','AF001044015000000000','Shindand','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghoryan','AF001044004000000000','Ghoryan','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','chisht-e-sharif','AF001044002000000000','Chisht-E-Sharif','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','farsi','AF001044003000000000','Farsi','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','injil','AF001044008000000000','Injil','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','obe','AF001044013000000000','Obe','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','pashtunzarghun','AF001044014000000000','Pashtunzarghun','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','adraskan','AF001044001000000000','Adraskan','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','zindajan','AF001044016000000000','Zindajan','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','herat','AF001044007000000000','Herat','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','kushk-e-kohna','AF001044012000000000','Kushk-E-Kohna','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','kushk','AF001044011000000000','Kushk','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','guzara','AF001044006000000000','Guzara','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','kohsan','AF001044010000000000','Kohsan','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','gulran','AF001044005000000000','Gulran','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','karukh','AF001044009000000000','Karukh','AF001044000000000000','district' UNION ALL
        SELECT 'Afghanistan','reg-(hilmand)','AF001043011000000000','Reg','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','marjah','AFGMarjah','Marjah','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','kajaki','AF001043004000000000','Kajaki','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','garmser','AF001043003000000000','Garmser','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','washer','AF001043013000000000','Washer','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','nawzad','AF001043010000000000','Nawzad','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','nawa-e-barakzaiy','AF001043009000000000','Nawa-E-Barakzaiy','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','nahr-e-saraj','AF001043008000000000','Nahr-E-Saraj','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','nad-e-ali','AF001043007000000000','Nad-E-Ali','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','musaqalah','AF001043006000000000','Musaqalah','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','baghran','AF001043001000000000','Baghran','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','lashkargah','AF001043005000000000','Lashkargah','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','deh-e-shu','AF001043002000000000','Deh-E-Shu','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','sangin','AF001043012000000000','Sangin','AF001043000000000000','district' UNION ALL
        SELECT 'Afghanistan','pasaband','AF001042006000000000','Pasaband','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','charsadra','AF001042002000000000','Charsadra','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','taywarah','AF001042009000000000','Taywarah','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','tolak','AF001042010000000000','Tolak','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','chaghcharan','AF001042001000000000','Chaghcharan','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','dolayna','AF001042004000000000','Dolayna','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','lal-wa-sarjangal','AF001042005000000000','Lal Wa Sarjangal','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','dawlatyar','AF001042003000000000','Dawlatyar','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','saghar','AF001042007000000000','Saghar','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahrak','AF001042008000000000','Shahrak','AF001042000000000000','district' UNION ALL
        SELECT 'Afghanistan','dawlatabad-(faryab)','AF001040004000000000','Dawlatabad','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','garziwan','AF001040005000000000','Garziwan','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','shirintagab','AF001040014000000000','Shirintagab','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','pashtunkot','AF001040010000000000','Pashtunkot','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','almar','AF001040001000000000','Almar','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','maymana','AF001040009000000000','Maymana','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','qaramqol','AF001040011000000000','Qaramqol','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','bilcheragh','AF001040003000000000','Bilcheragh','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','qaysar','AF001040012000000000','Qaysar','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','qorghan','AF001040013000000000','Qorghan','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','andkhoy','AF001040002000000000','Andkhoy','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','kohestan-(faryab)','AF001040008000000000','Kohestan (Faryab)','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajasabzposh','AF001040007000000000','Khwajasabzposh','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','khan-e-char-bagh','AF001040006000000000','Khan-E-Char Bagh','AF001040000000000000','district' UNION ALL
        SELECT 'Afghanistan','gizab','AF001038002000000000','Gizab','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','kajran','AF001038003000000000','Kajran','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','ashtarlay','AF001038001000000000','Ashtarlay','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','nili','AF001038007000000000','Nili','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','miramor','AF001038006000000000','Miramor','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','kiti','AF001038005000000000','Kiti','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','sang-e-takht','AF001038008000000000','Sang-E-Takht','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahrestan','AF001038009000000000','Shahrestan','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','khadir','AF001038004000000000','Khadir','AF001038000000000000','district' UNION ALL
        SELECT 'Afghanistan','andarab','AF001035001000000000','Andarab','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','tala-wa-barfak','AF001035015000000000','Tala Wa Barfak','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','dahana-e-ghori','AF001035004000000000','Dahana-E-Ghori','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','fereng-wa-gharu','AF001035007000000000','Fereng Wa Gharu','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','burka','AF001035003000000000','Burka','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','pul-e--khumri','AF001035013000000000','Pul-E- Khumri','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','pul-e-hesar','AF001035014000000000','Pul-E-Hesar','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','nahrin','AF001035012000000000','Nahrin','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','baghlan-e-jadid','AF001035002000000000','Baghlan-E-Jadid','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','doshi','AF001035006000000000','Doshi','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehsalah','AF001035005000000000','Dehsalah','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','guzargah-e--nur','AF001035008000000000','Guzargah-E- Nur','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajahejran','AF001035011000000000','Khwajahejran','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','khost-wa-fereng','AF001035010000000000','Khost Wa Fereng','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','khenjan','AF001035009000000000','Khenjan','AF001035000000000000','district' UNION ALL
        SELECT 'Afghanistan','muqur-(badghis)','AF001034005000000000','Muqur','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghormach','AF001034003000000000','Ghormach','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','jawand','AF001034004000000000','Jawand','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','balamurghab','AF001034002000000000','Balamurghab','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','qadis','AF001034006000000000','Qadis','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','qala-e-naw','AF001034007000000000','Qala-E-Naw','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','abkamari','AF001034001000000000','Abkamari','AF001034000000000000','district' UNION ALL
        SELECT 'Afghanistan','shighnan','AF001033019000000000','Shighnan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','jorm','AF001033009000000000','Jorm','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','teshkan','AF001033022000000000','Teshkan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','fayzabad-(badakhshan)','AF001033008000000000','Fayzabad (Badakhshan)','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','yaftal-e-sufla','AF001033025000000000','Yaftal-E-Sufla','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','eshkmesh','AF001033007000000000','Eshkmesh','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','argo','AF001033002000000000','Argo','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','arghanjkhwa','AF001033001000000000','Arghanjkhwa','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','baharak-(badakhshan)','AF001033003000000000','Baharak (Badakhshan)','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','zebak','AF001033028000000000','Zebak','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','yamgan','AF001033026000000000','Yamgan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','wakhan','AF001033023000000000','Wakhan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','raghestan','AF001033016000000000','Raghestan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','shuhada','AF001033020000000000','Shuhada','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','warduj','AF001033024000000000','Warduj','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','koran-wa-monjan','AF001033015000000000','Koran Wa Monjan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','kohestan-(badakhshan)','AF001033014000000000','Kohestan (Badakhshan)','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','kofab','AF001033013000000000','Kofab','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','darwaz-e-balla','AF001033006000000000','Darwaz-E-Balla','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','darwaz','AF001033005000000000','Darwaz','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwahan','AF001033012000000000','Khwahan','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahr-e-buzorg','AF001033017000000000','Shahr-E-Buzorg','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','shaki','AF001033018000000000','Shaki','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','khash','AF001033011000000000','Khash','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','keshem','AF001033010000000000','Keshem','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','darayem','AF001033004000000000','Darayem','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','tagab-(badakhshan)','AF001033021000000000','Tagab (Badakhshan)','AF001033000000000000','district' UNION ALL
        SELECT 'Afghanistan','yawan','AF001033027000000000','Yawan','AF001033000000000000','district' UNION ALL
        SELECT 'Pakistan','karachi','PAKKarachi','Karachi','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','hyderabad','PK001007004000000000','Hyderabad','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','jacobabad','PK001007005000000000','Jacobabad','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','jamshoro','PK001007006000000000','Jamshoro','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','shikarpur','PK001007034000000000','Shikarpur','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','kambar','PK001007007000000000','Kambar','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','kashmore','PK001007008000000000','Kashmore','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','khairpur','PK001007009000000000','Khairpur','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','sbenazirabad','PK001007033000000000','Sbenazirabad','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','sanghar','PK001007032000000000','Sanghar','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','tmkhan','PK001007039000000000','Tmkhan','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','thatta','PK001007038000000000','Thatta','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','tharparkar','PK001007037000000000','Tharparkar','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','larkana','PK001007028000000000','Larkana','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','ghotki','PK001007003000000000','Ghotki','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','matiari','PK001007029000000000','Matiari','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','mirpurkhas','PK001007030000000000','Mirpurkhas','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','nferoz','PK001007031000000000','Nferoz','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','badin','PK001007001000000000','Badin','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','t.allahyar','PK001007036000000000','T.Allahyar','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','umarkot','PK001007040000000000','Umarkot','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','sukkur','PK001007035000000000','Sukkur','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','dadu','PK001007002000000000','Dadu','PK001007000000000000','district' UNION ALL
        SELECT 'Pakistan','bahwlnagar','PK001006003000000000','Bahwlnagar','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','bhakkar','PK001006004000000000','Bhakkar','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','jhang','PK001006012000000000','Jhang','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','jhelum','PK001006013000000000','Jhelum','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','kasur','PK001006014000000000','Kasur','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','attock','PK001006001000000000','Attock','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','khanewal','PK001006015000000000','Khanewal','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','sheikupura','PK001006033000000000','Sheikupura','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','dgkhan','PK001006007000000000','Dgkhan','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','ttsingh','PK001006035000000000','Ttsingh','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','khushab','PK001006016000000000','Khushab','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','sargodha','PK001006032000000000','Sargodha','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','sahiwal','PK001006031000000000','Sahiwal','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','rykhan','PK001006030000000000','Rykhan','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','lahore','PK001006017000000000','Lahore','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','vehari','PK001006036000000000','Vehari','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','rawalpindi','PK001006029000000000','Rawalpindi','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','layyah','PK001006018000000000','Layyah','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','rajanpur','PK001006028000000000','Rajanpur','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','lodhran','PK001006019000000000','Lodhran','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','mbdin','PK001006020000000000','Mbdin','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','mianwali','PK001006021000000000','Mianwali','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','multan','PK001006022000000000','Multan','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','muzfargarh','PK001006023000000000','Muzfargarh','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','nankanasahib','PK001006024000000000','Nankanasahib','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','narowal','PK001006025000000000','Narowal','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','faisalabad','PK001006008000000000','Faisalabad','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','gujranwala','PK001006009000000000','Gujranwala','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','okara','PK001006026000000000','Okara','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','gujrat','PK001006010000000000','Gujrat','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','pakpatten','PK001006027000000000','Pakpatten','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','hafizabad','PK001006011000000000','Hafizabad','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','chakwal','PK001006005000000000','Chakwal','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','chiniot','PK001006006000000000','Chiniot','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','bahawalpur','PK001006002000000000','Bahawalpur','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','sialkot','PK001006034000000000','Sialkot','PK001006000000000000','district' UNION ALL
        SELECT 'Pakistan','abotabad','PK001011001000000000','Abotabad','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','karak','PK001011012000000000','Karak','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','shangla','PK001011021000000000','Shangla','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','dikhan','PK001011007000000000','Dikhan','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','torghar','PK001011025000000000','Torghar','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','dirlower','PK001011008000000000','Dirlower','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','kohat','PK001011013000000000','Kohat','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','kohistan','PK001011014000000000','Kohistan','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','dirupper','PK001011009000000000','Dirupper','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','lakkimrwt','PK001011015000000000','Lakkimrwt','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','bunir','PK001011004000000000','Bunir','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','bannu','PK001011002000000000','Bannu','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','tank','PK001011024000000000','Tank','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','malakand','PK001011016000000000','Malakand','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','mansehra','PK001011017000000000','Mansehra','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','mardan','PK001011018000000000','Mardan','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','peshawar','PK001011020000000000','Peshawar','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','nowshera','PK001011019000000000','Nowshera','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','swat','PK001011023000000000','Swat','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','swabi','PK001011022000000000','Swabi','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','hangu','PK001011010000000000','Hangu','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','charsada','PK001011005000000000','Charsada','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','haripur','PK001011011000000000','Haripur','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','chitral','PK001011006000000000','Chitral','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','batagram','PK001011003000000000','Batagram','PK001011000000000000','district' UNION ALL
        SELECT 'Pakistan','ict','PK001004002000000000','Ict','PK001004000000000000','district' UNION ALL
        SELECT 'Pakistan','cda','PK001004001000000000','Cda','PK001004000000000000','district' UNION ALL
        SELECT 'Pakistan','hunzanagar','PK001003008000000000','Hunzanagar','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','diamir','PK001003002000000000','Diamir','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','ghanche','PK001003003000000000','Ghanche','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','ghizer','PK001003004000000000','Ghizer','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','gilgit','PK001003007000000000','Gilgit','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','astore','PK001003001000000000','Astore','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','skardu','PK001003006000000000','Skardu','PK001003000000000000','district' UNION ALL
        SELECT 'Pakistan','subarea-2','PK001FATASubArea2','Subarea 2','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-bannu','PK001010002000000000','Fr Bannu','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','bajour','PK001010001000000000','Bajour','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-dikhan','PK001010003000000000','Fr Dikhan','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','khyber','PK001010008000000000','Khyber','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-kohat','PK001010004000000000','Fr Kohat','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-lakki','PK001010005000000000','Fr Lakki','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-peshawar','PK001010006000000000','Fr Peshawar','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','fr-tank','PK001010007000000000','Fr Tank','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','kurram','PK001010009000000000','Kurram','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','mohmand','PK001010010000000000','Mohmand','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','orakzai','PK001010011000000000','Orakzai','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','wazir-s','PK001010013000000000','Wazir-S','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','wazir-n','PK001010012000000000','Wazir-N','PK001010000000000000','district' UNION ALL
        SELECT 'Pakistan','jafarabad','PK001002008000000000','Jafarabad','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','jhalmagsi','PK001002009000000000','Jhalmagsi','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','kabdulah','PK001002010000000000','Kabdulah','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','dbugti','PK001002005000000000','Dbugti','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','kalat','PK001002011000000000','Kalat','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','kech','PK001002012000000000','Kech','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','kharan','PK001002013000000000','Kharan','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','sharani','PK001002026000000000','Sharani','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','ziarat','PK001002030000000000','Ziarat','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','khuzdar','PK001002014000000000','Khuzdar','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','kohlu','PK001002015000000000','Kohlu','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','ksaifulah','PK001002016000000000','Ksaifulah','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','bolan','PK001002003000000000','Bolan','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','zhob','PK001002029000000000','Zhob','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','lasbela','PK001002017000000000','Lasbela','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','awaran','PK001002001000000000','Awaran','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','loralai','PK001002018000000000','Loralai','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','quetta','PK001002025000000000','Quetta','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','mastung','PK001002019000000000','Mastung','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','musakhel-(balochistan)','PK001002020000000000','Musakhel (Balochistan)','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','barkhan','PK001002002000000000','Barkhan','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','noshki','PK001002021000000000','Noshki','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','pishin','PK001002024000000000','Pishin','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','nsirabad','PK001002022000000000','Nsirabad','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','panjgour','PK001002023000000000','Panjgour','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','chaghai','PK001002004000000000','Chaghai','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','gwadur','PK001002006000000000','Gwadur','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','harnai','PK001002007000000000','Harnai','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','washuk','PK001002028000000000','Washuk','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','sibi','PK001002027000000000','Sibi','PK001002000000000000','district' UNION ALL
        SELECT 'Pakistan','bhimber','PK001001002000000000','Bhimber','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','kotli','PK001001005000000000','Kotli','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','mirpur','PK001001006000000000','Mirpur','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','muzaffarabad','PK001001007000000000','Muzaffarabad','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','neelum','PK001001008000000000','Neelum','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','poonch','PK001001009000000000','Poonch','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','bagh','PK001001001000000000','Bagh','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','sudnuti','PK001001010000000000','Sudnuti','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','hattian','PK001001003000000000','Hattian','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','haveli','PK001001004000000000','Haveli','PK001001000000000000','district' UNION ALL
        SELECT 'Pakistan','PK001001004000000000Havaili','PK001001004000000000Havaili','Havaili','PK001001004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001004000000000Khurshidabad','PK001001004000000000Khurshidabad','Khurshidabad','PK001001004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006034000000000Pasrur','PK001006034000000000Pasrur','Pasrur','PK001006034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006034000000000Sambrial','PK001006034000000000Sambrial','Sambrial','PK001006034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006034000000000Daska','PK001006034000000000Daska','Daska','PK001006034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006034000000000Sialkot','PK001006034000000000Sialkot','Sialkot (Sialkot)','PK001006034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002027000000000Lehri','PK001002027000000000Lehri','Lehri','PK001002027000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002027000000000Sibi','PK001002027000000000Sibi','Sibi (Sibi)','PK001002027000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007002000000000Johi','PK001007002000000000Johi','Johi','PK001007002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007002000000000K.N.Shah','PK001007002000000000K.N.Shah','K.N.Shah','PK001007002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007002000000000Mehar','PK001007002000000000Mehar','Mehar','PK001007002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007002000000000Dadu','PK001007002000000000Dadu','Dadu (Dadu)','PK001007002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000Rondu','PK001003006000000000Rondu','Rondu','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000Shigar','PK001003006000000000Shigar','Shigar','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000GambaSkardu','PK001003006000000000GambaSkardu','Gamba ','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000Gultari','PK001003006000000000Gultari','Gultari','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000Kharmang','PK001003006000000000Kharmang','Kharmang','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003006000000000Skardu','PK001003006000000000Skardu','Skardu (Skardu)','PK001003006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011003000000000Allai','PK001011003000000000Allai','Allai','PK001011003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011003000000000Battagram','PK001011003000000000Battagram','Battagram','PK001011003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000AhmedpurEast','PK001006002000000000AhmedpurEast','Ahmedpur East','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000BwpCity','PK001006002000000000BwpCity','Bwp City','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000BwpSadar','PK001006002000000000BwpSadar','Bwp Sadar','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000Hasilpur','PK001006002000000000Hasilpur','Hasilpur','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000KhairpurTamewali','PK001006002000000000KhairpurTamewali','Khairpur Tamewali','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006002000000000Yazman','PK001006002000000000Yazman','Yazman','PK001006002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000Drosh','PK001011006000000000Drosh','Drosh','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000GaramChasma','PK001011006000000000GaramChasma','Garam Chasma','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000Mastuj','PK001011006000000000Mastuj','Mastuj','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000Mulkhow','PK001011006000000000Mulkhow','Mulkhow','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000Torkhow','PK001011006000000000Torkhow','Torkhow','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011006000000000Chitral','PK001011006000000000Chitral','Chitral (Chitral)','PK001011006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002028000000000Basima','PK001002028000000000Basima','Basima','PK001002028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002028000000000Mashkel','PK001002028000000000Mashkel','Mashkel','PK001002028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002028000000000Washuk','PK001002028000000000Washuk','Washuk (Washuk)','PK001002028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006006000000000Bhowana','PK001006006000000000Bhowana','Bhowana','PK001006006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006006000000000Lalian','PK001006006000000000Lalian','Lalian','PK001006006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006006000000000Chiniot','PK001006006000000000Chiniot','Chiniot (Chiniot)','PK001006006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001003000000000Chikar','PK001001003000000000Chikar','Chikar','PK001001003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001003000000000HattianBala','PK001001003000000000HattianBala',' Bala','PK001001003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001003000000000Leepa','PK001001003000000000Leepa','Leepa','PK001001003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002007000000000Shahrag','PK001002007000000000Shahrag','Shahrag','PK001002007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002007000000000Harnai','PK001002007000000000Harnai','Harnai (Harnai)','PK001002007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011011000000000Ghazi','PK001011011000000000Ghazi','Ghazi','PK001011011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011011000000000Haripur','PK001011011000000000Haripur','Haripur (Haripur)','PK001011011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001010000000000Baloch','PK001001010000000000Baloch','Baloch','PK001001010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001010000000000Pallandri','PK001001010000000000Pallandri','Pallandri','PK001001010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001010000000000Mang','PK001001010000000000Mang','Mang','PK001001010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001010000000000Tararkhel','PK001001010000000000Tararkhel','Tararkhel','PK001001010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007035000000000NewSukkur','PK001007035000000000NewSukkur','New ','PK001007035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007035000000000PanoAkil','PK001007035000000000PanoAkil','Pano Akil','PK001007035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007035000000000Rohri','PK001007035000000000Rohri','Rohri','PK001007035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007035000000000SalehPat','PK001007035000000000SalehPat','Saleh Pat','PK001007035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007035000000000SukkurCity','PK001007035000000000SukkurCity','Sukkur City (Sukkur)','PK001007035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011005000000000Shabqadar','PK001011005000000000Shabqadar','Shabqadar','PK001011005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011005000000000Charsadda','PK001011005000000000Charsadda','Charsadda','PK001011005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011005000000000Tangi','PK001011005000000000Tangi','Tangi','PK001011005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006005000000000ChoaSaidenShah','PK001006005000000000ChoaSaidenShah','Choa Saiden Shah','PK001006005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006005000000000KallarKahar','PK001006005000000000KallarKahar','Kallar Kahar','PK001006005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006005000000000Talagang','PK001006005000000000Talagang','Talagang','PK001006005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006005000000000Chakwal','PK001006005000000000Chakwal','Chakwal (Chakwal)','PK001006005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007040000000000Pithoro','PK001007040000000000Pithoro','Pithoro (Umerkot)','PK001007040000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007040000000000Samaro','PK001007040000000000Samaro','Samaro (Umerkot)','PK001007040000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007040000000000Kunri','PK001007040000000000Kunri','Kunri (Umerkot)','PK001007040000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007040000000000Umerkot','PK001007040000000000Umerkot','Umerkot (Umerkot)','PK001007040000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011010000000000Thall','PK001011010000000000Thall','Thall','PK001011010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011010000000000Hangu','PK001011010000000000Hangu','Hangu (Hangu)','PK001011010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006011000000000PindiBhattian','PK001006011000000000PindiBhattian','Pindi Bhattian','PK001006011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006011000000000Hafizabad','PK001006011000000000Hafizabad','Hafizabad (Hafizabad)','PK001006011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002006000000000Ormara','PK001002006000000000Ormara','Ormara','PK001002006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002006000000000Pasni','PK001002006000000000Pasni','Pasni','PK001002006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002006000000000Jiwani','PK001002006000000000Jiwani','Jiwani','PK001002006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002006000000000Gwadur','PK001002006000000000Gwadur','Gwadur (Gwadur)','PK001002006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010013000000000Sararogha','PK001010013000000000Sararogha','Sararogha','PK001010013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010013000000000Sarwakai','PK001010013000000000Sarwakai','Sarwakai','PK001010013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010013000000000Wana','PK001010013000000000Wana','Wana','PK001010013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002004000000000Nokundi','PK001002004000000000Nokundi','Nokundi','PK001002004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002004000000000Chagai','PK001002004000000000Chagai','Chagai','PK001002004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002004000000000Dalbandin','PK001002004000000000Dalbandin','Dalbandin','PK001002004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011022000000000Razar','PK001011022000000000Razar','Razar','PK001011022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011022000000000Topi','PK001011022000000000Topi','Topi','PK001011022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011022000000000Lahore','PK001011022000000000Lahore','Lahore (Swabi)','PK001011022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011022000000000Swabi','PK001011022000000000Swabi','Swabi (Swabi)','PK001011022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Babozi','PK001011023000000000Babozi','Babozi','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Bahrain','PK001011023000000000Bahrain','Bahrain','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Barikot','PK001011023000000000Barikot','Barikot','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Charbagh','PK001011023000000000Charbagh','Charbagh','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Kabal','PK001011023000000000Kabal','Kabal','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Kalam','PK001011023000000000Kalam','Kalam','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000KhwazaKhela','PK001011023000000000KhwazaKhela','Khwaza Khela','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011023000000000Matta','PK001011023000000000Matta','Matta','PK001011023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007036000000000Chambar','PK001007036000000000Chambar','Chambar','PK001007036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007036000000000JhandoMari','PK001007036000000000JhandoMari','Jhando Mari','PK001007036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007036000000000TalukaTandoA.Yar','PK001007036000000000TalukaTandoA.Yar','Taluka Tando A. Yar','PK001007036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001001000000000DhirKot','PK001001001000000000DhirKot','Dhir Kot','PK001001001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001001000000000HarriGhal','PK001001001000000000HarriGhal','Harri Ghal','PK001001001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001001000000000Bagh','PK001001001000000000Bagh','Bagh (Bagh)','PK001001001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003001000000000Honter','PK001003001000000000Honter','Honter','PK001003001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003001000000000Astore','PK001003001000000000Astore','Astore (Astore)','PK001003001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002023000000000Panjgur','PK001002023000000000Panjgur','Panjgur','PK001002023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002023000000000Gwargo','PK001002023000000000Gwargo','Gwargo','PK001002023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006027000000000Arifwala','PK001006027000000000Arifwala','Arifwala','PK001006027000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006027000000000Pakpatten','PK001006027000000000Pakpatten','Pakpatten (Pakpatten)','PK001006027000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006010000000000SaraiAlamgir','PK001006010000000000SaraiAlamgir','Sarai Alamgir','PK001006010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006010000000000Kharian','PK001006010000000000Kharian','Kharian','PK001006010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006010000000000Gujrat','PK001006010000000000Gujrat','Gujrat (Gujrat)','PK001006010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010011000000000IsmailZai','PK001010011000000000IsmailZai','Ismail Zai','PK001010011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010011000000000CentralOrakzai','PK001010011000000000CentralOrakzai','Central Orakzai (Orakzai)','PK001010011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010011000000000LowerOrakzai','PK001010011000000000LowerOrakzai','Lower Orakzai (Orakzai)','PK001010011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010011000000000UpperOrakzai','PK001010011000000000UpperOrakzai','Upper Orakzai (Orakzai)','PK001010011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006026000000000RenalaKhurd','PK001006026000000000RenalaKhurd','Renala Khurd','PK001006026000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006026000000000Depalpur','PK001006026000000000Depalpur','Depalpur','PK001006026000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006026000000000Okara','PK001006026000000000Okara','Okara (Okara)','PK001006026000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002022000000000Chatter','PK001002022000000000Chatter','Chatter','PK001002022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002022000000000DmJamali','PK001002022000000000DmJamali','Dm Jamali','PK001002022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002022000000000Tamboo','PK001002022000000000Tamboo','Tamboo','PK001002022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011019000000000Camps','PK001011019000000000Camps','Camps','PK001011019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011019000000000Nowshera','PK001011019000000000Nowshera','Nowshera (Nowshera)','PK001011019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000AroopTown','PK001006009000000000AroopTown','Aroop Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000Q.DSingTown','PK001006009000000000Q.DSingTown','Q.D Sing Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000K.SPurTown','PK001006009000000000K.SPurTown','K.S Pur Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000KamokeTown','PK001006009000000000KamokeTown','Kamoke Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000N.VirkanTown','PK001006009000000000N.VirkanTown','N.Virkan Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000NandipurTown','PK001006009000000000NandipurTown','Nandipur Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006009000000000WazirabadTown','PK001006009000000000WazirabadTown','Wazirabad Town','PK001006009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000Samundri','PK001006008000000000Samundri','Samundri','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000ChakJhumera','PK001006008000000000ChakJhumera','Chak Jhumera','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000FsdCity','PK001006008000000000FsdCity','Fsd City','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000FsdSadar','PK001006008000000000FsdSadar','Fsd Sadar','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000Jaranwala','PK001006008000000000Jaranwala','Jaranwala','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006008000000000Tandlianwala','PK001006008000000000Tandlianwala','Tandlianwala','PK001006008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011020000000000Peshawar','PK001011020000000000Peshawar','Peshawar (Peshawar)','PK001011020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002024000000000Barshore','PK001002024000000000Barshore','Barshore','PK001002024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002024000000000Karezat','PK001002024000000000Karezat','Karezat','PK001002024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002024000000000Pishin','PK001002024000000000Pishin','Pishin (Pishin)','PK001002024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001009000000000Abbaspur','PK001001009000000000Abbaspur','Abbaspur','PK001001009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001009000000000Rawalakot','PK001001009000000000Rawalakot','Rawalakot','PK001001009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001009000000000Hajira','PK001001009000000000Hajira','Hajira','PK001001009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001009000000000Thorar','PK001001009000000000Thorar','Thorar','PK001001009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007001000000000Golarchi','PK001007001000000000Golarchi','Golarchi','PK001007001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007001000000000Matli','PK001007001000000000Matli','Matli','PK001007001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007001000000000Talhar','PK001007001000000000Talhar','Talhar','PK001007001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007001000000000TandoBago','PK001007001000000000TandoBago','Tando Bago','PK001007001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007001000000000Badin','PK001007001000000000Badin','Badin (Badin)','PK001007001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002021000000000Noshki','PK001002021000000000Noshki','Noshki (Noshki)','PK001002021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002002000000000Rakhni','PK001002002000000000Rakhni','Rakhni','PK001002002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002002000000000Barkhan','PK001002002000000000Barkhan','Barkhan (Barkhan)','PK001002002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002020000000000Musakhel','PK001002020000000000Musakhel','Musakhel (Musakhel)','PK001002020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007031000000000Bhiria','PK001007031000000000Bhiria','Bhiria','PK001007031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007031000000000NausheroFeroz','PK001007031000000000NausheroFeroz','Naushero Feroz','PK001007031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007031000000000Kandiaro','PK001007031000000000Kandiaro','Kandiaro','PK001007031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007031000000000Mehrabpur','PK001007031000000000Mehrabpur','Mehrabpur','PK001007031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007031000000000Moro','PK001007031000000000Moro','Moro (Nferoz)','PK001007031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001008000000000Authmuqam','PK001001008000000000Authmuqam','Authmuqam','PK001001008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001008000000000Sharda','PK001001008000000000Sharda','Sharda','PK001001008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006025000000000Shakargarh','PK001006025000000000Shakargarh','Shakargarh','PK001006025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006025000000000Narowal','PK001006025000000000Narowal','Narowal (Narowal)','PK001006025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006024000000000SanglaHill','PK001006024000000000SanglaHill','Sangla Hill','PK001006024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006024000000000Shahkot','PK001006024000000000Shahkot','Shahkot','PK001006024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006024000000000NankanaSahib','PK001006024000000000NankanaSahib','Nankana Sahib','PK001006024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006023000000000Alipur','PK001006023000000000Alipur','Alipur','PK001006023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006023000000000Jatoi','PK001006023000000000Jatoi','Jatoi','PK001006023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006023000000000KotAdu','PK001006023000000000KotAdu','Kot Adu','PK001006023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006023000000000Muzaffargarh','PK001006023000000000Muzaffargarh','Muzaffargarh','PK001006023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001007000000000Nasirabad(Pattika)','PK001001007000000000Nasirabad(Pattika)','Nasirabad (Pattika)','PK001001007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001007000000000Muzaffarabad','PK001001007000000000Muzaffarabad','Muzaffarabad (Muzaffarabad)','PK001001007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006022000000000Shujabad','PK001006022000000000Shujabad','Shujabad','PK001006022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006022000000000JalalpurPirwala','PK001006022000000000JalalpurPirwala','Jalalpur Pirwala','PK001006022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006022000000000MultanUrban','PK001006022000000000MultanUrban',' Urban','PK001006022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006022000000000MultanRural','PK001006022000000000MultanRural','Multan Rural (Multan)','PK001006022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000Ambar','PK001010010000000000Ambar','Ambar','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000Pandiali','PK001010010000000000Pandiali','Pandiali','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000ParangGhaar','PK001010010000000000ParangGhaar','Parang Ghaar','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000SafiLakaro','PK001010010000000000SafiLakaro','Safi Lakaro','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000Ekkaghund','PK001010010000000000Ekkaghund','Ekkaghund','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000Haleemzai','PK001010010000000000Haleemzai','Haleemzai','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010010000000000Khawezai/Baizai','PK001010010000000000Khawezai/Baizai','Khawezai/Baizai','PK001010010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000Digri','PK001007030000000000Digri','Digri','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000H.BMari','PK001007030000000000H.BMari','H.B Mari','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000Jhudo','PK001007030000000000Jhudo','Jhudo','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000KotGhulamMohd.','PK001007030000000000KotGhulamMohd.','Kot Ghulam Mohd.','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000Sindri','PK001007030000000000Sindri','Sindri','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007030000000000Mirpurkhas','PK001007030000000000Mirpurkhas','Mirpurkhas (Mirpurkhas)','PK001007030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001006000000000Dudyal','PK001001006000000000Dudyal','Dudyal','PK001001006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001006000000000Mirpur','PK001001006000000000Mirpur','Mirpur (Mirpur)','PK001001006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006021000000000Piplan','PK001006021000000000Piplan','Piplan','PK001006021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006021000000000Eisakhail','PK001006021000000000Eisakhail','Eisakhail','PK001006021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006021000000000Mainwali','PK001006021000000000Mainwali','Mainwali','PK001006021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006020000000000Phalia','PK001006020000000000Phalia','Phalia','PK001006020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006020000000000M.BDin','PK001006020000000000M.BDin','M.B Din','PK001006020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006020000000000Malakwal','PK001006020000000000Malakwal','Malakwal','PK001006020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007029000000000Saeedabad','PK001007029000000000Saeedabad','Saeedabad','PK001007029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007029000000000Hala','PK001007029000000000Hala','Hala','PK001007029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007029000000000Matiari','PK001007029000000000Matiari','Matiari (Matiari)','PK001007029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011018000000000TakhtBahi','PK001011018000000000TakhtBahi','Takht Bahi','PK001011018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011018000000000Mardan','PK001011018000000000Mardan','Mardan (Mardan)','PK001011018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011017000000000Balakot','PK001011017000000000Balakot','Balakot','PK001011017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011017000000000Uggi','PK001011017000000000Uggi','Uggi','PK001011017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011017000000000Mansehra','PK001011017000000000Mansehra','Mansehra (Mansehra)','PK001011017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011016000000000Batkhela','PK001011016000000000Batkhela','Batkhela','PK001011016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011016000000000Dargai','PK001011016000000000Dargai','Dargai','PK001011016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003007000000000Gilgit','PK001003007000000000Gilgit','Gilgit (Gilgit)','PK001003007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002025000000000ChiltonTown','PK001002025000000000ChiltonTown','Chilton Town','PK001002025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002025000000000ZarghoonTown','PK001002025000000000ZarghoonTown','Zarghoon Town','PK001002025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002018000000000Bori','PK001002018000000000Bori','Bori','PK001002018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002018000000000Dukki','PK001002018000000000Dukki','Dukki','PK001002018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002001000000000CampJajoo','PK001002001000000000CampJajoo','Camp Jajoo','PK001002001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002001000000000Mashkey','PK001002001000000000Mashkey','Mashkey','PK001002001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002001000000000Awaran','PK001002001000000000Awaran','Awaran (Awaran)','PK001002001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007003000000000Daharki','PK001007003000000000Daharki','Daharki','PK001007003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007003000000000KhanGarh','PK001007003000000000KhanGarh','Khan Garh','PK001007003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007003000000000MirpurMathelo','PK001007003000000000MirpurMathelo','Mirpur Mathelo','PK001007003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007003000000000Ubauro','PK001007003000000000Ubauro','Ubauro','PK001007003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007003000000000Ghotki','PK001007003000000000Ghotki','Ghotki (Ghotki)','PK001007003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006019000000000DunyaPur','PK001006019000000000DunyaPur','Dunya Pur','PK001006019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006019000000000KahrorPakka','PK001006019000000000KahrorPakka','Kahror Pakka','PK001006019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006019000000000Lodhran','PK001006019000000000Lodhran','Lodhran (Lodhran)','PK001006019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006028000000000RajanPur','PK001006028000000000RajanPur','Rajan Pur','PK001006028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006028000000000Rojhan','PK001006028000000000Rojhan','Rojhan','PK001006028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006028000000000JamPur','PK001006028000000000JamPur','Jam Pur','PK001006028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001004001000000000Cda','PK001004001000000000Cda','Cda (Cda)','PK001004001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006018000000000Choubara','PK001006018000000000Choubara','Choubara','PK001006018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006018000000000KarorLalEsan','PK001006018000000000KarorLalEsan','Karor Lal Esan','PK001006018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006018000000000Layyah','PK001006018000000000Layyah','Layyah (Layyah)','PK001006018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000RwpCantt','PK001006029000000000RwpCantt','Rwp Cantt','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000RwpCity','PK001006029000000000RwpCity','Rwp City','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000RwpRural','PK001006029000000000RwpRural','Rwp Rural','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000GujarKhan','PK001006029000000000GujarKhan','Gujar Khan','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000Kahuta','PK001006029000000000Kahuta','Kahuta','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000KallarSyedan','PK001006029000000000KallarSyedan','Kallar Syedan','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000KotliSittian','PK001006029000000000KotliSittian','Kotli Sittian','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000Murree','PK001006029000000000Murree','Murree','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006029000000000Taxila','PK001006029000000000Taxila','Taxila','PK001006029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Bela','PK001002017000000000Bela','Bela','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Dureji','PK001002017000000000Dureji','Dureji','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Gaddani','PK001002017000000000Gaddani','Gaddani','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Hub','PK001002017000000000Hub','Hub','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Kanraj','PK001002017000000000Kanraj','Kanraj','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Lakhra','PK001002017000000000Lakhra','Lakhra','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Liari','PK001002017000000000Liari','Liari','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Sonmiani','PK001002017000000000Sonmiani','Sonmiani','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002017000000000Uthal','PK001002017000000000Uthal','Uthal','PK001002017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007028000000000Bakrani','PK001007028000000000Bakrani','Bakrani','PK001007028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007028000000000RatoDero','PK001007028000000000RatoDero','Rato Dero','PK001007028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007028000000000Dokri','PK001007028000000000Dokri','Dokri','PK001007028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007028000000000Larkana','PK001007028000000000Larkana','Larkana (Larkana)','PK001007028000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002029000000000KakarKhurasan','PK001002029000000000KakarKhurasan','Kakar Khurasan','PK001002029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002029000000000Zhob','PK001002029000000000Zhob','Zhob (Zhob)','PK001002029000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003004000000000Poniyal','PK001003004000000000Poniyal','Poniyal','PK001003004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003004000000000Gupis','PK001003004000000000Gupis','Gupis','PK001003004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003004000000000Ishkomen','PK001003004000000000Ishkomen','Ishkomen','PK001003004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003004000000000Yaseen','PK001003004000000000Yaseen','Yaseen','PK001003004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011024000000000Tank','PK001011024000000000Tank','Tank (Tank)','PK001011024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011002000000000Bannu','PK001011002000000000Bannu','Bannu (Bannu)','PK001011002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011004000000000Daggar','PK001011004000000000Daggar','Daggar (Buner)','PK001011004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011004000000000Gagra','PK001011004000000000Gagra','Gagra (Buner)','PK001011004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011004000000000Mandan','PK001011004000000000Mandan','Mandan (Buner)','PK001011004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011004000000000Totalai','PK001011004000000000Totalai','Totalai (Buner)','PK001011004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002003000000000Bhag','PK001002003000000000Bhag','Bhag','PK001002003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002003000000000Dhadar','PK001002003000000000Dhadar','Dhadar','PK001002003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002003000000000Mach','PK001002003000000000Mach','Mach','PK001002003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002003000000000Sunni','PK001002003000000000Sunni','Sunni','PK001002003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011015000000000SeraiNaurang','PK001011015000000000SeraiNaurang','Serai Naurang','PK001011015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011015000000000LakkiMarwat','PK001011015000000000LakkiMarwat','Lakki Marwat','PK001011015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003003000000000Daghoni','PK001003003000000000Daghoni','Daghoni','PK001003003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003003000000000Khapulu','PK001003003000000000Khapulu','Khapulu','PK001003003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003003000000000Mashabrum','PK001003003000000000Mashabrum','Mashabrum','PK001003003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006036000000000Burewala','PK001006036000000000Burewala','Burewala','PK001006036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006036000000000Mailsi','PK001006036000000000Mailsi','Mailsi','PK001006036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006036000000000Vehari','PK001006036000000000Vehari','Vehari (Vehari)','PK001006036000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000AllamaIqbalTown','PK001006017000000000AllamaIqbalTown','Allama Iqbal Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000AzizBhattiTown','PK001006017000000000AzizBhattiTown','Aziz Bhatti Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000NishterTown','PK001006017000000000NishterTown','Nishter Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000RaviTown','PK001006017000000000RaviTown','Ravi Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000SamanabadTown','PK001006017000000000SamanabadTown','Samanabad Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000ShalimarTown','PK001006017000000000ShalimarTown','Shalimar Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000Cantt.','PK001006017000000000Cantt.','Cantt.','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000DataGunjbuxTown','PK001006017000000000DataGunjbuxTown','Data Gunjbux Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000GulbergTown','PK001006017000000000GulbergTown','Gulberg Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006017000000000WahgaTown','PK001006017000000000WahgaTown','Wahga Town','PK001006017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010009000000000CentralKurram','PK001010009000000000CentralKurram','Central Kurram (Kurram)','PK001010009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010009000000000LowerKurram','PK001010009000000000LowerKurram','Lower Kurram (Kurram)','PK001010009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010009000000000UpperKurram','PK001010009000000000UpperKurram','Upper Kurram (Kurram)','PK001010009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002016000000000Ksaifullah','PK001002016000000000Ksaifullah','Ksaifullah','PK001002016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002016000000000MuslimBagh','PK001002016000000000MuslimBagh','Muslim Bagh','PK001002016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006030000000000RahimyarKhan','PK001006030000000000RahimyarKhan','Rahimyar Khan','PK001006030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006030000000000Sadiqabad','PK001006030000000000Sadiqabad','Sadiqabad','PK001006030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006030000000000Liaquaitpur','PK001006030000000000Liaquaitpur','Liaquaitpur','PK001006030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006030000000000Khanpur','PK001006030000000000Khanpur','Khanpur (Rykhan)','PK001006030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001005000000000Sehnsa','PK001001005000000000Sehnsa','Sehnsa','PK001001005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001005000000000Charohi','PK001001005000000000Charohi','Charohi','PK001001005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001005000000000FathehPur','PK001001005000000000FathehPur','Fatheh Pur','PK001001005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001005000000000Khuiratta','PK001001005000000000Khuiratta','Khuiratta','PK001001005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001005000000000Kotli','PK001001005000000000Kotli','Kotli (Kotli)','PK001001005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010007000000000FrTank','PK001010007000000000FrTank','Fr Tank (Fr Tank)','PK001010007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010006000000000FrPeshawar','PK001010006000000000FrPeshawar','Fr Peshawar (Fr Peshawar)','PK001010006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010005000000000FrLakki','PK001010005000000000FrLakki','Fr Lakki (Fr Lakki)','PK001010005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011009000000000Dir','PK001011009000000000Dir','Dir','PK001011009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011009000000000Wari','PK001011009000000000Wari','Wari','PK001011009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007037000000000Chachro','PK001007037000000000Chachro','Chachro','PK001007037000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007037000000000Diplo','PK001007037000000000Diplo','Diplo','PK001007037000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007037000000000Mithi','PK001007037000000000Mithi','Mithi','PK001007037000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007037000000000Nangarparkar','PK001007037000000000Nangarparkar','Nangarparkar','PK001007037000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002015000000000Kohlu','PK001002015000000000Kohlu','Kohlu (Kohlu)','PK001002015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006031000000000Chichawatni','PK001006031000000000Chichawatni','Chichawatni','PK001006031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006031000000000Sahiwal','PK001006031000000000Sahiwal','Sahiwal (Sahiwal)','PK001006031000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000ShahBunder','PK001007038000000000ShahBunder','Shah Bunder','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000GhoraBari','PK001007038000000000GhoraBari','Ghora Bari','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000Jati','PK001007038000000000Jati','Jati','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000KetiBunder','PK001007038000000000KetiBunder','Keti Bunder','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000KharoChhan','PK001007038000000000KharoChhan','Kharo Chhan','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000MirpurSakro','PK001007038000000000MirpurSakro','Mirpur Sakro','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000Mirpurbathoro','PK001007038000000000Mirpurbathoro','Mirpurbathoro','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000Sujawal','PK001007038000000000Sujawal','Sujawal','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007038000000000Thatta','PK001007038000000000Thatta','Thatta (Thatta)','PK001007038000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010004000000000FrKohat','PK001010004000000000FrKohat','Fr Kohat (Fr Kohat)','PK001010004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007039000000000BulriShahKarim','PK001007039000000000BulriShahKarim','Bulri Shah Karim','PK001007039000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007039000000000T.M.Khan','PK001007039000000000T.M.Khan','T. M. Khan','PK001007039000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007039000000000TandoGhulamHyder','PK001007039000000000TandoGhulamHyder','Tando Ghulam Hyder','PK001007039000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011014000000000Pattana','PK001011014000000000Pattana','Pattana','PK001011014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011014000000000Plalas','PK001011014000000000Plalas','Plalas','PK001011014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011014000000000Dassu','PK001011014000000000Dassu','Dassu','PK001011014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011013000000000Kohat','PK001011013000000000Kohat','Kohat (Kohat)','PK001011013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011008000000000SamarBagh','PK001011008000000000SamarBagh','Samar Bagh','PK001011008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011008000000000Timergara','PK001011008000000000Timergara','Timergara','PK001011008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010008000000000Bara','PK001010008000000000Bara','Bara','PK001010008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010008000000000Jamrud','PK001010008000000000Jamrud','Jamrud','PK001010008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010008000000000LandiKotal','PK001010008000000000LandiKotal','Landi Kotal','PK001010008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010008000000000Tirah','PK001010008000000000Tirah','Tirah','PK001010008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010003000000000FrDikhan','PK001010003000000000FrDikhan','Fr Dikhan (Fr Dikhan)','PK001010003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000ShahdadPur','PK001007032000000000ShahdadPur','Shahdad Pur','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000JamNawazAli','PK001007032000000000JamNawazAli','Jam Nawaz Ali','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000Khipro','PK001007032000000000Khipro','Khipro','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000Sinjhoro','PK001007032000000000Sinjhoro','Sinjhoro','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000TandoAdam','PK001007032000000000TandoAdam','Tando Adam','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007032000000000Sanghar','PK001007032000000000Sanghar','Sanghar (Sanghar)','PK001007032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002014000000000Karakh','PK001002014000000000Karakh','Karakh','PK001002014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002014000000000Nal','PK001002014000000000Nal','Nal','PK001002014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002014000000000Wadh','PK001002014000000000Wadh','Wadh','PK001002014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002014000000000Zehri','PK001002014000000000Zehri','Zehri','PK001002014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002014000000000Khuzdar','PK001002014000000000Khuzdar','Khuzdar (Khuzdar)','PK001002014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011025000000000Judbah','PK001011025000000000Judbah','Judbah','PK001011025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011025000000000Kandar','PK001011025000000000Kandar','Kandar','PK001011025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000Paroa','PK001011007000000000Paroa','Paroa','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000Pharpur','PK001011007000000000Pharpur','Pharpur','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000D.IKhan','PK001011007000000000D.IKhan','D.I Khan','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000DeraIsmailKhan','PK001011007000000000DeraIsmailKhan','Dera Ismail Khan','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000Draban','PK001011007000000000Draban','Draban','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011007000000000Kulachi','PK001011007000000000Kulachi','Kulachi','PK001011007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000Shahpur','PK001006032000000000Shahpur','Shahpur','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000Bhulwal','PK001006032000000000Bhulwal','Bhulwal','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000KotMomin','PK001006032000000000KotMomin','Kot Momin','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000Silanwali','PK001006032000000000Silanwali','Silanwali','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000Sahiwal','PK001006032000000000Sahiwal','Sahiwal (Sargodha)','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006032000000000Sargodha','PK001006032000000000Sargodha','Sargodha (Sargodha)','PK001006032000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006016000000000NoorpurThul','PK001006016000000000NoorpurThul','Noorpur Thul','PK001006016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006016000000000QuaidaAbad','PK001006016000000000QuaidaAbad','Quaida Abad','PK001006016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006016000000000Khushab','PK001006016000000000Khushab','Khushab (Khushab)','PK001006016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007033000000000Nawabshah','PK001007033000000000Nawabshah','Nawabshah','PK001007033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007033000000000Sakrand','PK001007033000000000Sakrand','Sakrand','PK001007033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007033000000000DaulatPur','PK001007033000000000DaulatPur','Daulat Pur','PK001007033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007033000000000Daur','PK001007033000000000Daur','Daur','PK001007033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003002000000000Chilas','PK001003002000000000Chilas','Chilas','PK001003002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003002000000000Darel','PK001003002000000000Darel','Darel','PK001003002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003002000000000Tangir','PK001003002000000000Tangir','Tangir','PK001003002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002030000000000Sinjavi','PK001002030000000000Sinjavi','Sinjavi','PK001002030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002030000000000Ziarat','PK001002030000000000Ziarat','Ziarat (Ziarat)','PK001002030000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Barang','PK001010001000000000Barang','Barang','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Nawagai','PK001010001000000000Nawagai','Nawagai','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Salarzai','PK001010001000000000Salarzai','Salarzai','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Chamarkand','PK001010001000000000Chamarkand','Chamarkand','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Khar','PK001010001000000000Khar','Khar','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000LoeMamound','PK001010001000000000LoeMamound','Loe Mamound','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000Utmankhel','PK001010001000000000Utmankhel','Utmankhel','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010001000000000WaraMamound','PK001010001000000000WaraMamound','Wara Mamound','PK001010001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011021000000000Alpuri','PK001011021000000000Alpuri','Alpuri','PK001011021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011021000000000Puran','PK001011021000000000Puran','Puran','PK001011021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006035000000000Gojra','PK001006035000000000Gojra','Gojra','PK001006035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006035000000000Kamalia','PK001006035000000000Kamalia','Kamalia','PK001006035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006035000000000TtSingh','PK001006035000000000TtSingh','Tt Singh','PK001006035000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006007000000000DgKhan','PK001006007000000000DgKhan','Dg Khan','PK001006007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006007000000000Taunsa','PK001006007000000000Taunsa','Taunsa','PK001006007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006007000000000Tribal','PK001006007000000000Tribal','Tribal','PK001006007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002026000000000Sharani','PK001002026000000000Sharani','Sharani (Sharani)','PK001002026000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002013000000000Kharan','PK001002013000000000Kharan','Kharan (Kharan)','PK001002013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006033000000000Safdarabad','PK001006033000000000Safdarabad','Safdarabad','PK001006033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006033000000000Sharaqpur','PK001006033000000000Sharaqpur','Sharaqpur','PK001006033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006033000000000Sheikhupura','PK001006033000000000Sheikhupura','Sheikhupura','PK001006033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006033000000000Ferozewala','PK001006033000000000Ferozewala','Ferozewala','PK001006033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006033000000000Muridke','PK001006033000000000Muridke','Muridke','PK001006033000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006015000000000Jahanian','PK001006015000000000Jahanian','Jahanian','PK001006015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006015000000000Kabirwala','PK001006015000000000Kabirwala','Kabirwala','PK001006015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006015000000000MianChanu','PK001006015000000000MianChanu','Mian Chanu','PK001006015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006015000000000Khanewal','PK001006015000000000Khanewal','Khanewal (Khanewal)','PK001006015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000PindiGheb','PK001006001000000000PindiGheb','Pindi Gheb','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000FatehJang','PK001006001000000000FatehJang','Fateh Jang','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000Hassanabdal','PK001006001000000000Hassanabdal','Hassanabdal','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000Hazro','PK001006001000000000Hazro','Hazro','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000Jand','PK001006001000000000Jand','Jand','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006001000000000Attock','PK001006001000000000Attock','Attock (Attock)','PK001006001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001010002000000000FrBannu','PK001010002000000000FrBannu','Fr Bannu (Fr Bannu)','PK001010002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000FaizGanj','PK001007009000000000FaizGanj','Faiz Ganj','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000Gambat','PK001007009000000000Gambat','Gambat','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000Kingri','PK001007009000000000Kingri','Kingri','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000KotDeji','PK001007009000000000KotDeji','Kot Deji','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000Nara','PK001007009000000000Nara','Nara','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000SobhoDero','PK001007009000000000SobhoDero','Sobho Dero','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000ThariMirWah','PK001007009000000000ThariMirWah','Thari Mir Wah','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007009000000000Khairpur','PK001007009000000000Khairpur','Khairpur (Khairpur)','PK001007009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002012000000000Bulida','PK001002012000000000Bulida','Bulida','PK001002012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002012000000000DashtKuddan','PK001002012000000000DashtKuddan','Dasht Kuddan','PK001002012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002012000000000Tump','PK001002012000000000Tump','Tump','PK001002012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002012000000000Turbat','PK001002012000000000Turbat','Turbat','PK001002012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006014000000000Pattoki','PK001006014000000000Pattoki','Pattoki','PK001006014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006014000000000Chunian','PK001006014000000000Chunian','Chunian','PK001006014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006014000000000Kasur','PK001006014000000000Kasur','Kasur (Kasur)','PK001006014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007008000000000KandhKot','PK001007008000000000KandhKot','Kandh Kot','PK001007008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007008000000000Tangwani','PK001007008000000000Tangwani','Tangwani','PK001007008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007008000000000Kashmore','PK001007008000000000Kashmore','Kashmore (Kashmore)','PK001007008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011012000000000B.D.Shah','PK001011012000000000B.D.Shah','B.D.Shah','PK001011012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011012000000000Takht-E-Nasrati','PK001011012000000000Takht-E-Nasrati','Takht-E-Nasrati','PK001011012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011012000000000Karak','PK001011012000000000Karak','Karak (Karak)','PK001011012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000NasirAbad','PK001007007000000000NasirAbad','Nasir Abad','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000QuboSaeedKhan','PK001007007000000000QuboSaeedKhan','Qubo Saeed Khan','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000Shahdadkot','PK001007007000000000Shahdadkot','Shahdadkot','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000MiroKhan','PK001007007000000000MiroKhan','Miro Khan','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000Sijawal','PK001007007000000000Sijawal','Sijawal','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000Warah','PK001007007000000000Warah','Warah','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007007000000000Kambar','PK001007007000000000Kambar','Kambar (Kambar)','PK001007007000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007034000000000GarhiYasin','PK001007034000000000GarhiYasin','Garhi Yasin','PK001007034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007034000000000Lakhi','PK001007034000000000Lakhi','Lakhi','PK001007034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007034000000000Shikarpur','PK001007034000000000Shikarpur','Shikarpur (Shikarpur)','PK001007034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007034000000000Khanpur','PK001007034000000000Khanpur','Khanpur (Shikarpur)','PK001007034000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002011000000000Surab','PK001002011000000000Surab','Surab','PK001002011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002011000000000Kalat','PK001002011000000000Kalat','Kalat (Kalat)','PK001002011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002005000000000Sui','PK001002005000000000Sui','Sui','PK001002005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002005000000000Dbugti','PK001002005000000000Dbugti','Dbugti (Dbugti)','PK001002005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002010000000000Chaman','PK001002010000000000Chaman','Chaman','PK001002010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002010000000000Dobandi','PK001002010000000000Dobandi','Dobandi','PK001002010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002010000000000Gulistan','PK001002010000000000Gulistan','Gulistan','PK001002010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002010000000000Kabdullah','PK001002010000000000Kabdullah','Kabdullah','PK001002010000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006013000000000PdKhan','PK001006013000000000PdKhan','Pd Khan','PK001006013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006013000000000Dina','PK001006013000000000Dina','Dina','PK001006013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006013000000000Sohawa','PK001006013000000000Sohawa','Sohawa','PK001006013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006013000000000Jhelum','PK001006013000000000Jhelum','Jhelum (Jhelum)','PK001006013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006012000000000ApSayal','PK001006012000000000ApSayal','Ap Sayal','PK001006012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006012000000000Shorkot','PK001006012000000000Shorkot','Shorkot','PK001006012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006012000000000Jhang','PK001006012000000000Jhang','Jhang (Jhang)','PK001006012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002009000000000Gandawah','PK001002009000000000Gandawah','Gandawah','PK001002009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002009000000000JhalMagsi','PK001002009000000000JhalMagsi','Jhal Magsi','PK001002009000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001002000000000Barnala','PK001001002000000000Barnala','Barnala','PK001001002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001002000000000Samahni','PK001001002000000000Samahni','Samahni','PK001001002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001001002000000000Bhimber','PK001001002000000000Bhimber','Bhimber (Bhimber)','PK001001002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007006000000000Sehwan','PK001007006000000000Sehwan','Sehwan','PK001007006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007006000000000Kotri','PK001007006000000000Kotri','Kotri','PK001007006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007006000000000Manjhand','PK001007006000000000Manjhand','Manjhand','PK001007006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007006000000000ThanoBulaKhan','PK001007006000000000ThanoBulaKhan','Thano Bula Khan','PK001007006000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006004000000000DaryaKhan','PK001006004000000000DaryaKhan','Darya Khan','PK001006004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006004000000000KaloorKot','PK001006004000000000KaloorKot','Kaloor Kot','PK001006004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006004000000000Mankera','PK001006004000000000Mankera','Mankera','PK001006004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006004000000000Bhakkar','PK001006004000000000Bhakkar','Bhakkar (Bhakkar)','PK001006004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002008000000000Gandakha','PK001002008000000000Gandakha','Gandakha','PK001002008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002008000000000JhatPat','PK001002008000000000JhatPat','Jhat Pat','PK001002008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002008000000000SohbatPur','PK001002008000000000SohbatPur','Sohbat Pur','PK001002008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001002008000000000UstaMuhammad','PK001002008000000000UstaMuhammad','Usta Muhammad','PK001002008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011001000000000Abbottabad','PK001011001000000000Abbottabad','Abbottabad','PK001011001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001011001000000000Hawallian','PK001011001000000000Hawallian','Hawallian','PK001011001000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006003000000000Bahawalnagar','PK001006003000000000Bahawalnagar','Bahawalnagar','PK001006003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006003000000000Chishtian','PK001006003000000000Chishtian','Chishtian','PK001006003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006003000000000Fortabbas','PK001006003000000000Fortabbas','Fortabbas','PK001006003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006003000000000Haroonabad','PK001006003000000000Haroonabad','Haroonabad','PK001006003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001006003000000000Minchanaba','PK001006003000000000Minchanaba','Minchanaba','PK001006003000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007005000000000GarhiKhairo','PK001007005000000000GarhiKhairo','Garhi Khairo','PK001007005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007005000000000Thull','PK001007005000000000Thull','Thull','PK001007005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007005000000000Jacobabad','PK001007005000000000Jacobabad','Jacobabad (Jacobabad)','PK001007005000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001004002000000000Ict','PK001004002000000000Ict','Ict (Ict)','PK001004002000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007004000000000Qasimabad','PK001007004000000000Qasimabad','Qasimabad','PK001007004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007004000000000Latifabad','PK001007004000000000Latifabad','Latifabad','PK001007004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007004000000000HyderabadCity','PK001007004000000000HyderabadCity','Hyderabad City (Hyderabad)','PK001007004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007004000000000HyderabadRural','PK001007004000000000HyderabadRural','Hyderabad Rural (Hyderabad)','PK001007004000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Gojal','PK001003008000000000Gojal','Gojal','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Hunza','PK001003008000000000Hunza','Hunza','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-1','PK001003008000000000Nagar-1','Nagar-1','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-2','PK001003008000000000Nagar-2','Nagar-2','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-3','PK001003008000000000Nagar-3','Nagar-3','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-4','PK001003008000000000Nagar-4','Nagar-4','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-5','PK001003008000000000Nagar-5','Nagar-5','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001003008000000000Nagar-6','PK001003008000000000Nagar-6','Nagar-6','PK001003008000000000','sub-district' UNION ALL
        SELECT 'Afghanistan','kandahar-(district)','AF001047005000000000','Kandahar District','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','panjwayi','AF001047011000000000','Panjwayi','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghorak','AF001047004000000000','Ghorak','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','daman','AF001047003000000000','Daman','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','nesh','AF001047010000000000','Nesh','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','arghestan','AF001047002000000000','Arghestan','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','arghandab-(kandahar)','AF001047001000000000','Arghandab (Kandahar)','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','miyanshin','AF001047009000000000','Miyanshin','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','maywand','AF001047008000000000','Maywand','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','maruf','AF001047007000000000','Maruf','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','zheray','AF001047016000000000','Zheray','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','shorabak','AF001047014000000000','Shorabak','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','reg-(kandahar)','AF001047012000000000','Reg (Kandahar)','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','spinboldak','AF001047015000000000','Spinboldak','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','shahwalikot','AF001047013000000000','Shahwalikot','AF001047000000000000','district' UNION ALL
        SELECT 'Afghanistan','khakrez','AF001047006000000000','Khakrez','AF001047000000000000','district' UNION ALL
        SELECT 'Pakistan','PK001007010000000000','PK001007010000000000','Khibaldia','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007011000000000','PK001007011000000000','Khibinqasim','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007012000000000','PK001007012000000000','Khigadap','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007013000000000','PK001007013000000000','Khigiqbal','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007014000000000','PK001007014000000000','Khigulberg','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007015000000000','PK001007015000000000','Khijamsheed','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007016000000000','PK001007016000000000','Khikamari','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007017000000000','PK001007017000000000','Khikorangi','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007018000000000','PK001007018000000000','Khilandhi','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007019000000000','PK001007019000000000','Khilayari','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007020000000000','PK001007020000000000','Khiliaqat','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007021000000000','PK001007021000000000','Khimalir','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007022000000000','PK001007022000000000','Khinnazim','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007023000000000','PK001007023000000000','Khinorth','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007024000000000','PK001007024000000000','Khiorangi','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007025000000000','PK001007025000000000','Khisaddar','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007026000000000','PK001007026000000000','Khishahfaisal','PAKKarachi','district' UNION ALL
        SELECT 'Pakistan','PK001007027000000000','PK001007027000000000','Khisite','PAKKarachi','district' UNION ALL
        SELECT 'Afghanistan','sar-e-pul-(district)','AF001062005000000000','Sar-E-Pul District','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','balkhab','AF001062001000000000','Balkhab','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','sozmaqala','AF001062007000000000','Sozmaqala','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','kohestanat','AF001062003000000000','Kohestanat','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','sancharak(sangchark)','AF001062004000000000','Sancharak(Sangchark)','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','sayad','AF001062006000000000','Sayad','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','gosfandi','AF001062002000000000','Gosfandi','AF001062000000000000','district' UNION ALL
        SELECT 'Afghanistan','kunduz-(district)','AF001051006000000000','Kunduz District','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','chardarah','AF001051002000000000','Chardarah','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','emamsaheb','AF001051004000000000','Emamsaheb','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','qala-e-zal','AF001051007000000000','Qala-E-Zal','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','aliabad','AF001051001000000000','Aliabad','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','dasht-e-archi','AF001051003000000000','Dasht-E-Archi','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','khanabad','AF001051005000000000','Khanabad','AF001051000000000000','district' UNION ALL
        SELECT 'Afghanistan','kabul-(district)','AF001046007000000000','Kabul District','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','paghman','AF001046012000000000','Paghman','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','kalakan','AF001046008000000000','Kalakan','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','farza','AF001046005000000000','Farza','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','chaharasyab','AF001046002000000000','Chaharasyab','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','estalef','AF001046004000000000','Estalef','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','musayi','AF001046011000000000','Musayi','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','bagrami','AF001046001000000000','Bagrami','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','mirbachakot','AF001046010000000000','Mirbachakot','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','qarabagh-(kabul)','AF001046013000000000','Qarabagh (Kabul)','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehsabz','AF001046003000000000','Dehsabz','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','surobi','AF001046015000000000','Surobi','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','shakardara','AF001046014000000000','Shakardara','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','khak-e--jabbar','AF001046009000000000','Khak-E- Jabbar','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','guldara','AF001046006000000000','Guldara','AF001046000000000000','district' UNION ALL
        SELECT 'Afghanistan','ghazni-(district)','AF001041006000000000','Ghazni District','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','giro','AF001041007000000000','Giro','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','andar','AF001041003000000000','Andar','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','gelan','AF001041005000000000','Gelan','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','jaghuri','AF001041009000000000','Jaghuri','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','jaghatu-(ghazni)','AF001041008000000000','Jaghatu (Ghazni)','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','nawur','AF001041014000000000','Nawur','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','nawa','AF001041013000000000','Nawa','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','zanakhan','AF001041019000000000','Zanakhan','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','muqur-(ghazni)','AF001041012000000000','Muqur (Ghazni)','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','qarabagh-(ghazni)','AF001041015000000000','Qarabagh (Ghazni)','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','malestan','AF001041011000000000','Malestan','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','waghaz','AF001041017000000000','Waghaz','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','walimuhammad-e--shahid','AF001041018000000000','Walimuhammad-E- Shahid','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehyak','AF001041004000000000','Dehyak','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','rashidan','AF001041016000000000','Rashidan','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','abband','AF001041001000000000','Abband','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','ajrestan','AF001041002000000000','Ajrestan','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','khwajaumari','AF001041010000000000','Khwajaumari','AF001041000000000000','district' UNION ALL
        SELECT 'Afghanistan','farah-(district)','AF001039004000000000','Farah District','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','anardara','AF001039001000000000','Anardara','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','balabuluk','AF001039003000000000','Balabuluk','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','bakwa','AF001039002000000000','Bakwa','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','purchaman','AF001039008000000000','Purchaman','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','pushtrod','AF001039009000000000','Pushtrod','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','qala-e-kah','AF001039010000000000','Qala-E-Kah','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','lash-e-juwayn','AF001039007000000000','Lash-E-Juwayn','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','khak-e-safed','AF001039006000000000','Khak-E-Safed','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','gulestan','AF001039005000000000','Gulestan','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','shibkoh','AF001039011000000000','Shibkoh','AF001039000000000000','district' UNION ALL
        SELECT 'Afghanistan','bamyan-(district)','AF001037001000000000','Bamyan District','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','panjab','AF001037003000000000','Panjab','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','kahmard','AF001037002000000000','Kahmard','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','yakawlang','AF001037007000000000','Yakawlang','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','waras','AF001037006000000000','Waras','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','sayghan','AF001037004000000000','Sayghan','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','shibar','AF001037005000000000','Shibar','AF001037000000000000','district' UNION ALL
        SELECT 'Afghanistan','balkh-(district)','AF001036001000000000','Balkh District','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','kaldar','AF001036007000000000','Kaldar','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','sholgareh','AF001036014000000000','Sholgareh','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','chemtal','AF001036004000000000','Chemtal','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','charkent','AF001036003000000000','Charkent','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','charbulak','AF001036002000000000','Charbulak','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','nahr-e--shahi','AF001036012000000000','Nahr-E- Shahi','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','zari','AF001036016000000000','Zari','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','mazar-e-sharif','AF001036011000000000','Mazar-E-Sharif','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','marmul','AF001036010000000000','Marmul','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','dehdadi','AF001036006000000000','Dehdadi','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','shortepa','AF001036015000000000','Shortepa','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','dawlatabad-(balkh)','AF001036005000000000','Dawlatabad (Balkh)','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','khulm','AF001036009000000000','Khulm','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','sharak-e-hayratan','AF001036013000000000','Sharak-E-Hayratan','AF001036000000000000','district' UNION ALL
        SELECT 'Afghanistan','keshendeh','AF001036008000000000','Keshendeh','AF001036000000000000','district' UNION ALL
        SELECT 'Pakistan','PK001007027000000000Site','PK001007027000000000Site','Site (Khisite)','PK001007027000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007026000000000Shahfaisal','PK001007026000000000Shahfaisal','Shahfaisal (Khishahfaisal)','PK001007026000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007025000000000Saddar','PK001007025000000000Saddar','Saddar (Khisaddar)','PK001007025000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007024000000000Orangi','PK001007024000000000Orangi','Orangi (Khiorangi)','PK001007024000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007023000000000North','PK001007023000000000North','North (Khinorth)','PK001007023000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007022000000000Nnazim','PK001007022000000000Nnazim','Nnazim (Khinnazim)','PK001007022000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007021000000000Malir','PK001007021000000000Malir','Malir (Khimalir)','PK001007021000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007020000000000Liaqat','PK001007020000000000Liaqat','Liaqat (Khiliaqat)','PK001007020000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007019000000000Layari','PK001007019000000000Layari','Layari (Khilayari)','PK001007019000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007018000000000Landhi','PK001007018000000000Landhi','Landhi (Khilandhi)','PK001007018000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007017000000000Korangi','PK001007017000000000Korangi','Korangi (Khikorangi)','PK001007017000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007016000000000Kamari','PK001007016000000000Kamari','Kamari (Khikamari)','PK001007016000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007015000000000Jamsheed','PK001007015000000000Jamsheed','Jamsheed (Khijamsheed)','PK001007015000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007014000000000Gulberg','PK001007014000000000Gulberg','Gulberg (Khigulberg)','PK001007014000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007013000000000Giqbal','PK001007013000000000Giqbal','Giqbal (Khigiqbal)','PK001007013000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007012000000000Gadap','PK001007012000000000Gadap','Gadap (Khigadap)','PK001007012000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007011000000000Binqasim','PK001007011000000000Binqasim','Binqasim (Khibinqasim)','PK001007011000000000','sub-district' UNION ALL
        SELECT 'Pakistan','PK001007010000000000Baldia','PK001007010000000000Baldia','Baldia (Khibaldia)','PK001007010000000000','sub-district';

        UPDATE _tmp_locations
        SET location_name = x.new_name
        FROM (
        	SELECT tr.location_name, tr.location_name || ' (' || tr_parent.location_name || ')' as new_name
        	FROM _tmp_locations tr
        	INNER JOIN _tmp_locations tr_parent
        	ON tr.parent_location_code = tr_parent.location_code
        	WHERE EXISTS (
        		SELECT 1 FROM location r
        		WHERE r.name = tr.location_name
        		AND r.office_id = 1
        	)
        )x
        WHERE _tmp_locations.location_name = x.location_name;

        -- PROVINCE --

        INSERT INTO location
        (name, location_code, slug, office_id, location_type_id,parent_location_id, created_at)
        SELECT
        	location_name
        	,tr.location_code
        	,tr.location_slug
        	,o.id as office_id
        	,rt.id as location_type_id
            ,r.id as parent_location_id
        	,now() as created_at
        from _tmp_locations tr
        INNER JOIN office o
        on o.name = tr.office
        INNER JOIN location_type rt
        ON tr.location_type = lower(rt.name)
        INNER JOIN location r
        ON tr.parent_location_code = r.location_code
        AND tr.location_type = 'province';

        -- DISTRICT --
        INSERT INTO location
        (name, location_code, slug, office_id, location_type_id,parent_location_id, created_at)
        SELECT
        	location_name
        	,tr.location_code
        	,tr.location_slug
        	,o.id as office_id
        	,rt.id as location_type_id
            ,r.id as parent_location_id
        	,now() as created_at
        from _tmp_locations tr
        INNER JOIN office o
        on o.name = tr.office
        INNER JOIN location_type rt
        ON tr.location_type = lower(rt.name)
        INNER JOIN location r
        ON tr.parent_location_code = r.location_code
        AND tr.location_type = 'district';

        -- SUB DISTRICT --
        INSERT INTO location
        (name, location_code, slug, office_id, location_type_id,parent_location_id, created_at)

        SELECT
        	location_name
        	,tr.location_code
        	,tr.location_slug
        	,o.id as office_id
        	,rt.id as location_type_id
            ,r.id as parent_location_id
        	,now() as created_at
        from _tmp_locations tr
        INNER JOIN office o
        on o.name = tr.office
        INNER JOIN location_type rt
        ON tr.location_type = lower(rt.name)
        INNER JOIN location r
        ON tr.parent_location_code = r.location_code
        AND tr.location_type = 'sub-district';

        -- INSERT MAPPINGS --
        INSERT INTO source_object_map
        (master_object_id, source_object_code, content_type, mapped_by_id)
        SELECT r.id, location_code, 'location', 1
        FROM location r
        WHERE NOT EXISTS (
        	SELECT 1 FROM source_object_map som
        	WHERE r.location_code = som.source_object_code
        	AND content_type = 'location'
        );
        ''')
    ]
