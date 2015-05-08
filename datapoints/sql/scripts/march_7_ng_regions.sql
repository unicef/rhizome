

-- source_region
-- region_map
-- region (master)

INSERT INTO source_data_document
(created_by_id,guid,doc_text,is_processed)

SELECT
	1
	, 'JD_INSERT_POLIO_412'
	, 'JD_INSERT_POLIO_412'
	, 't'
WHERE NOT EXISTS (
	SELECT 1 FROM source_data_document
	WHERE guid = 'JD_INSERT_POLIO_412'
);


/*
DROP TABLE IF EXISTS _sub_distr;
CREATE TEMP TABLE _sub_distr AS

SELECT
	x.*
	,sdd.id as document_id
	,CAST(NULL AS INT) as source_id
	,CAST(NULL AS INT) as master_id
FROM source_data_document sdd
INNER JOIN (
SELECT
	'Baro Ward' as region_name
	,'2701Barosub-district' as region_code
	,'Agaie' as parent_name
	,2701 as parent_id
	,'sub-district' as region_type

 UNION ALL

 SELECT 'Boku Ward','2701Bokusub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'DanDaudu ward','2718Dandaudusub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Dangunu  Ward','2718Dangunusub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Doko Ward','2713Dokosub-district','Lavun',2713,'sub-district' UNION ALL
 SELECT 'Ekossa Ward','2701Ekossasub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'EKOWUNA ward','2701Ekowunasub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'Etsugaie ward','2701Etsugaiesub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'Fogbe / Kusoyaba Ward','2701Fogbe/Kusoyabasub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'GADAI Ward','4526Gadaisub-district','Nganzai',4526,'sub-district' UNION ALL
 SELECT 'Gini ward','2718Ginisub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Gora  Ward','1922Gorasub-district','Zangon Kataf',1922,'sub-district' UNION ALL
 SELECT 'Guni Ward','2718Gunisub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Hausari Ward','3606Hausarisub-district','Geidam',3606,'sub-district' UNION ALL
 SELECT 'Kabulla Ward','2718Kabullasub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Kazai ward','2718Kazaisub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Kuchi Ward','2718Kuchisub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'Kutriko Ward','2701Kutrikosub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'Magaji Ward','2701Magajisub-district','Agaie',2701,'sub-district' UNION ALL
 SELECT 'Paiko Ward','2719Paikosub-district','Paikoro',2719,'sub-district' UNION ALL
 SELECT 'sarki Power Ward','2718SarkiPowersub-district','Munya',2718,'sub-district' UNION ALL
 SELECT 'BULABULIN','4511Bulabulin','Gwoza',4511,'sub-district' UNION ALL
 SELECT 'Kardam C','4217KardamC','Tafawa-Balewa',4217,'sub-district' UNION ALL
 SELECT 'Yangamai','4211Yangamai','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Jurara','4211Jurara','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Jamaare D','4211JamaareD','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Jamaare B','4211JamaareB','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Hanafari','4211Hanafari','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Galdimari','4211Galdimari','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Dogon  Jeji B','4211DogonJejiB','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Dogon  Jeji A','4211DogonJejiA','Jama''Are',4211,'sub-district' UNION ALL
 SELECT 'Bar','4203Bar','Bogoro',4203,'sub-district' UNION ALL
 SELECT 'Zungur','4202Zungur','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Makama B','4202MakamaB','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Makama A','4202MakamaA','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Kangere','4202Kangere','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Dawaki','4202Dawaki','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Dankade','4202Dankade','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Dan Amar B','4202DanAmarB','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'Dan Amar A','4202DanAmarA','Bauchi',4202,'sub-district' UNION ALL
 SELECT 'FARU/MAGAMI','3709Faru/Magami','Maradun',3709,'sub-district' UNION ALL
 SELECT 'BELA/RAWAYYA','3705Bela/Rawayya','Bungudu',3705,'sub-district' UNION ALL
 SELECT 'NASSARAWA MAILAYI','3703NassarawaMailayi','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'NASSARAWA GODEL EAST','3703NassarawaGodelEast','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'MODOMAWA WEST','3703ModomawaWest','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'MODOMAWA EAST','3703ModomawaEast','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'GUSAMI HAYI','3703GusamiHayi','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'GUSAMI GARI','3703GusamiGari','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'DAMFANI/S.BIRNI','3703Damfani/S.Birni','Birnin Magaji/Kiyaw',3703,'sub-district' UNION ALL
 SELECT 'SHEKAU','3615Shekau','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'MANDADAWA','3615Mandadawa','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'LANTEWA','3615Lantewa','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'KORIYEL','3615Koriyel','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'JUMBAM','3615Jumbam','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'GUDURAM','3615Guduram','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'BIRIRI','3615Biriri','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'BABANGIDA','3615Babangida','Tarmuwa',3615,'sub-district' UNION ALL
 SELECT 'Bare-Bari','3614Bare-Bari','Potiskum',3614,'sub-district' UNION ALL
 SELECT 'Fika Anze','3604FikaAnze','Fika',3604,'sub-district' UNION ALL
 SELECT 'Masaba','3602Masaba','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Kaliyari','3602Kaliyari','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Juluri / Damnawa','3602Juluri/Damnawa','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Jawa Garun Dole','3602JawaGarunDole','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Guji / Metalari','3602Guji/Metalari','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Guba/Dapso','3602Guba/Dapso','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Dapchi','3602Dapchi','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Bayamari','3602Bayamari','Bursari',3602,'sub-district' UNION ALL
 SELECT 'Sugum Tagali','3601SugumTagali','Bade',3601,'sub-district' UNION ALL
 SELECT 'Lawan Musa','3601LawanMusa','Bade',3601,'sub-district' UNION ALL
 SELECT 'Lawan Fernami','3601LawanFernami','Bade',3601,'sub-district' UNION ALL
 SELECT 'Gwo Kura','3601GwoKura','Bade',3601,'sub-district' UNION ALL
 SELECT 'Dawayo','3601Dawayo','Bade',3601,'sub-district' UNION ALL
 SELECT 'Dagona','3601Dagona','Bade',3601,'sub-district' UNION ALL
 SELECT 'Serti A','3504SertiA','Gashaka',3504,'sub-district' UNION ALL
 SELECT 'Wamakko','3421Wamakko','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Kalambaina','3421Kalambaina','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Gwamatse','3421Gwamatse','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Gumbi','3421Gumbi','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'G/Hamidu','3421G/Hamidu','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Dundaye','3421Dundaye','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Arkilla','3421Arkilla','Wamakko',3421,'sub-district' UNION ALL
 SELECT 'Sarkin Adar G/Igwai','3416SarkinAdarG/Igwai','Sokoto North',3416,'sub-district' UNION ALL
 SELECT 'Poeship','3216Poeship','Shendam',3216,'sub-district' UNION ALL
 SELECT 'Namu Central','3214NamuCentral','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Luukwu','3214Luukwu','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Kwang','3214Kwang','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Kwande Central','3214KwandeCentral','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Kurgwi East','3214KurgwiEast','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Koplong','3214Koplong','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Doka East','3214DokaEast','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Bwall','3214Bwall','Qua''An Pan',3214,'sub-district' UNION ALL
 SELECT 'Mabudi South','3210MabudiSouth','Langtang South',3210,'sub-district' UNION ALL
 SELECT 'Akari','2725Akari','Wushishi',2725,'sub-district' UNION ALL
 SELECT 'YAMMA II','2121YammaIi','Katsina',2121,'sub-district' UNION ALL
 SELECT 'YAMMA I','2121YammaI','Katsina',2121,'sub-district' UNION ALL
 SELECT 'GABAS II','2121GabasIi','Katsina',2121,'sub-district' UNION ALL
 SELECT 'GABAS I','2121GabasI','Katsina',2121,'sub-district' UNION ALL
 SELECT 'AREWA II','2121ArewaIi','Katsina',2121,'sub-district' UNION ALL
 SELECT 'AREWA I','2121ArewaI','Katsina',2121,'sub-district' UNION ALL
 SELECT 'Kausani','2044Kausani','Wudil',2044,'sub-district' UNION ALL
 SELECT 'Imawa','2043Imawa','Warawa',2043,'sub-district' UNION ALL
 SELECT 'Yada Kunya','2042YadaKunya','Ungogo',2042,'sub-district' UNION ALL
 SELECT 'Ungogo','2042Ungogo','Ungogo',2042,'sub-district' UNION ALL
 SELECT 'Bachirawa','2042Bachirawa','Ungogo',2042,'sub-district' UNION ALL
 SELECT 'Rurum - Tsohon Gari','2032Rurum-TsohonGari','Rano',2032,'sub-district' UNION ALL
 SELECT 'Zabi','1915Zabi','Kubau',1915,'sub-district' UNION ALL
 SELECT 'PAMBEGUA','1915Pambegua','Kubau',1915,'sub-district' UNION ALL
 SELECT 'MAH','1915Mah','Kubau',1915,'sub-district' UNION ALL
 SELECT 'KARGI','1915Kargi','Kubau',1915,'sub-district' UNION ALL
 SELECT 'KAREH','1915Kareh','Kubau',1915,'sub-district' UNION ALL
 SELECT 'HASKIYA','1915Haskiya','Kubau',1915,'sub-district' UNION ALL
 SELECT 'DUTSEN WAI','1915DutsenWai','Kubau',1915,'sub-district' UNION ALL
 SELECT 'ANCHAU','1915Anchau','Kubau',1915,'sub-district' UNION ALL
 SELECT 'UNG. SANUSI','1910Ung.Sanusi','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'TELEVISION','1910Television','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'T/NUPAWA','1910T/Nupawa','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'SabonGari West','1910SabongariWest','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'S/GARI NORTH','1910S/GariNorth','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'Kakuri Hausa','1910KakuriHausa','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'BARNAWA','1910Barnawa','Kaduna South',1910,'sub-district' UNION ALL
 SELECT 'Kurmin Musa','1908KurminMusa','Kachia',1908,'sub-district' UNION ALL
 SELECT 'MAIGIZO','1907Maigizo','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'KANINKON','1907Kaninkon','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'KAFANCHAN A B','1907KafanchanAB','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'KAFANCHAN A','1907KafanchanA','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'JAGINDI','1907Jagindi','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'GODO-GODO','1907Godo-Godo','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'GIDAN WAYA','1907GidanWaya','Jema''A',1907,'sub-district' UNION ALL
 SELECT 'Toni Kutara','1821ToniKutara','Malam Maduri',1821,'sub-district' UNION ALL
 SELECT 'Kwanda','1819Kwanda','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Kiyawa','1819Kiyawa','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Katuka','1819Katuka','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Katanga','1819Katanga','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Fake','1819Fake','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Balago','1819Balago','Kiyawa',1819,'sub-district' UNION ALL
 SELECT 'Andaza','1819Andaza','Kiyawa',1819,'sub-district'
)x
ON sdd.guid = 'JD_INSERT_POLIO_412';


UPDATE _sub_distr sd
SET source_id = sr.id
FROM source_region sr
WHERE sd.region_code = sr.region_code;

UPDATE _sub_distr sd
SET master_id = rm.master_id
FROM region_map rm
WHERE rm.source_id = sd.source_id

*/

DROP TABLE IF EXISTS _sett;
CREATE TEMP TABLE _sett AS

 SELECT
	x.*
	,sdd.id as document_id
	,CAST(NULL AS INT) as source_id
	,CAST(NULL AS INT) as master_id
FROM source_data_document sdd
INNER JOIN (
SELECT
		'Alijiram' as region_name
		,'3606Hausarisub-district-Alijiram' as region_code
		,'Hausari Ward' as parent_name
		,'3606Hausarisub-district' as parent_code
		,'Settlement' as region_type
UNION ALL

SELECT 'ALKALI','2701Ekossasub-district-ALKALI','Ekossa Ward','2701Ekossasub-district','Settlement' UNION ALL
SELECT 'ANG DAN ASEBE','2718Dangunusub-district-ANG DAN ASEBE','Dangunu  Ward','2718Dangunusub-district','Settlement' UNION ALL
SELECT 'ANGWAN FULANI','2719Paikosub-district-ANGWAN FULANI','Paiko Ward','2719Paikosub-district','Settlement' UNION ALL
SELECT 'ANUZ HIBUYI','2718Dandaudusub-district-ANUZ HIBUYI','DanDaudu ward','2718Dandaudusub-district','Settlement' UNION ALL
SELECT 'ARFO','4526Gadaisub-district-ARFO','GADAI Ward','4526Gadaisub-district','Settlement' UNION ALL
SELECT 'BASAWAI','2718Dandaudusub-district-BASAWAI','DanDaudu ward','2718Dandaudusub-district','Settlement' UNION ALL
SELECT 'BAZAMA','2718Gunisub-district-BAZAMA','Guni Ward','2718Gunisub-district','Settlement' UNION ALL
SELECT 'BOROROKO I','2701Ekossasub-district-BOROROKO I','Ekossa Ward','2701Ekossasub-district','Settlement' UNION ALL
SELECT 'CHIBANI','2718Kazaisub-district-CHIBANI','Kazai ward','2718Kazaisub-district','Settlement' UNION ALL
SELECT 'DARACHITA','2701Bokusub-district-DARACHITA','Boku Ward','2701Bokusub-district','Settlement' UNION ALL
SELECT 'DOYA','4526Gadaisub-district-DOYA','GADAI Ward','4526Gadaisub-district','Settlement' UNION ALL
SELECT 'DUMI','2718SarkiPowersub-district-DUMI','sarki Power Ward','2718SarkiPowersub-district','Settlement' UNION ALL
SELECT 'EFU LIMAN MUSA','2701Kutrikosub-district-EFU LIMAN MUSA','Kutriko Ward','2701Kutrikosub-district','Settlement' UNION ALL
SELECT 'EGUNKPA','2701Fogbe/Kusoyabasub-district-EGUNKPA','Fogbe / Kusoyaba Ward','2701Fogbe/Kusoyabasub-district','Settlement' UNION ALL
SELECT 'EKOGI GIGAYAN','2701Fogbe/Kusoyabasub-district-EKOGI GIGAYAN','Fogbe / Kusoyaba Ward','2701Fogbe/Kusoyabasub-district','Settlement' UNION ALL
SELECT 'EMI WOROGI','2701Magajisub-district-EMI WOROGI','Magaji Ward','2701Magajisub-district','Settlement' UNION ALL
SELECT 'EMILAGBA TIFFIN','2713Dokosub-district-EMILAGBA TIFFIN','Doko Ward','2713Dokosub-district','Settlement' UNION ALL
SELECT 'ESUN','2701Barosub-district-ESUN','Baro Ward','2701Barosub-district','Settlement' UNION ALL
SELECT 'ETSU GAEI','2701Etsugaiesub-district-ETSU GAEI','Etsugaie ward','2701Etsugaiesub-district','Settlement' UNION ALL
SELECT 'EVONTAGI','2701Barosub-district-EVONTAGI','Baro Ward','2701Barosub-district','Settlement' UNION ALL
SELECT 'EWUGI SHESHI','2701Ekossasub-district-EWUGI SHESHI','Ekossa Ward','2701Ekossasub-district','Settlement' UNION ALL
SELECT 'GADE BEYI','2718Gunisub-district-GADE BEYI','Guni Ward','2718Gunisub-district','Settlement' UNION ALL
SELECT 'gadza','2701Etsugaiesub-district-gadza','Etsugaie ward','2701Etsugaiesub-district','Settlement' UNION ALL
SELECT 'Gamal Gamal','3606Hausarisub-district-Gamal Gamal','Hausari Ward','3606Hausarisub-district','Settlement' UNION ALL
SELECT 'gora gidan','1922Gorasub-district-gora gidan','Gora  Ward','1922Gorasub-district','Settlement' UNION ALL
SELECT 'GUNI GARI','2718Gunisub-district-GUNI GARI','Guni Ward','2718Gunisub-district','Settlement' UNION ALL
SELECT 'HAYIN DOGO','2718Kuchisub-district-HAYIN DOGO','Kuchi Ward','2718Kuchisub-district','Settlement' UNION ALL
SELECT 'INJITA','2718Ginisub-district-INJITA','Gini ward','2718Ginisub-district','Settlement' UNION ALL
SELECT 'JAIFULU','2718SarkiPowersub-district-JAIFULU','sarki Power Ward','2718SarkiPowersub-district','Settlement' UNION ALL
SELECT 'JIKPAGI','2701Kutrikosub-district-JIKPAGI','Kutriko Ward','2701Kutrikosub-district','Settlement' UNION ALL
SELECT 'JIPPO II','2701Bokusub-district-JIPPO II','Boku Ward','2701Bokusub-district','Settlement' UNION ALL
SELECT 'kakpi','2701Barosub-district-kakpi','Baro Ward','2701Barosub-district','Settlement' UNION ALL
SELECT 'KAMPANI','2718Kuchisub-district-KAMPANI','Kuchi Ward','2718Kuchisub-district','Settlement' UNION ALL
SELECT 'KONUFU','2713Dokosub-district-KONUFU','Doko Ward','2713Dokosub-district','Settlement' UNION ALL
SELECT 'KPANKPA','2701Magajisub-district-KPANKPA','Magaji Ward','2701Magajisub-district','Settlement' UNION ALL
SELECT 'KUBLET','2718Dandaudusub-district-KUBLET','DanDaudu ward','2718Dandaudusub-district','Settlement' UNION ALL
SELECT 'MAKON B.M','2701Fogbe/Kusoyabasub-district-MAKON B.M','Fogbe / Kusoyaba Ward','2701Fogbe/Kusoyabasub-district','Settlement' UNION ALL
SELECT 'MANBUHARI','2713Dokosub-district-MANBUHARI','Doko Ward','2713Dokosub-district','Settlement' UNION ALL
SELECT 'MASHINA','2701Bokusub-district-MASHINA','Boku Ward','2701Bokusub-district','Settlement' UNION ALL
SELECT 'MMANUM','4526Gadaisub-district-MMANUM','GADAI Ward','4526Gadaisub-district','Settlement' UNION ALL
SELECT 'MONSIDI','2701Ekowunasub-district-MONSIDI','EKOWUNA ward','2701Ekowunasub-district','Settlement' UNION ALL
SELECT 'OLD BANK','2701Ekowunasub-district-OLD BANK','EKOWUNA ward','2701Ekowunasub-district','Settlement' UNION ALL
SELECT 'OLD MAT','2719Paikosub-district-OLD MAT','Paiko Ward','2719Paikosub-district','Settlement' UNION ALL
SELECT 'R MOH''D','2719Paikosub-district-R MOH''D','Paiko Ward','2719Paikosub-district','Settlement' UNION ALL
SELECT 'SABON KABULSA','2718Kabullasub-district-SABON KABULSA','Kabulla Ward','2718Kabullasub-district','Settlement' UNION ALL
SELECT 'sawaza','1922Gorasub-district-sawaza','Gora  Ward','1922Gorasub-district','Settlement' UNION ALL
SELECT 'SHENGU','2718Ginisub-district-SHENGU','Gini ward','2718Ginisub-district','Settlement' UNION ALL
SELECT 'SHIGYIWE','2718Ginisub-district-SHIGYIWE','Gini ward','2718Ginisub-district','Settlement' UNION ALL
SELECT 'tsaduko','2701Etsugaiesub-district-tsaduko','Etsugaie ward','2701Etsugaiesub-district','Settlement' UNION ALL
SELECT 'tswachiko','2701Kutrikosub-district-tswachiko','Kutriko Ward','2701Kutrikosub-district','Settlement' UNION ALL
SELECT 'TSWATA','2701Ekowunasub-district-TSWATA','EKOWUNA ward','2701Ekowunasub-district','Settlement' UNION ALL
SELECT 'UNG GUDUGU','2718Kazaisub-district-UNG GUDUGU','Kazai ward','2718Kazaisub-district','Settlement' UNION ALL
SELECT 'UNG SIDI','2718Dangunusub-district-UNG SIDI','Dangunu  Ward','2718Dangunusub-district','Settlement' UNION ALL
SELECT 'UNG TATA','2718Kuchisub-district-UNG TATA','Kuchi Ward','2718Kuchisub-district','Settlement' UNION ALL
SELECT 'UNG YUSUF','2718Dangunusub-district-UNG YUSUF','Dangunu  Ward','2718Dangunusub-district','Settlement' UNION ALL
SELECT 'yagbak','1922Gorasub-district-yagbak','Gora  Ward','1922Gorasub-district','Settlement' UNION ALL
SELECT 'ZAZZAGA HAUAWA','2718Kabullasub-district-ZAZZAGA HAUAWA','Kabulla Ward','2718Kabullasub-district','Settlement' UNION ALL
SELECT 'ZAZZAGA UMANA','2718Kabullasub-district-ZAZZAGA UMANA','Kabulla Ward','2718Kabullasub-district','Settlement' UNION ALL
SELECT 'Low Cost','4511Bulabulin-Low Cost','BULABULIN','4511Bulabulin','Settlement' UNION ALL
SELECT 'Zari','4217KardamC-Zari','Kardam C','4217KardamC','Settlement' UNION ALL
SELECT 'JAURO DAIYABU','4211Yangamai-JAURO DAIYABU','Yangamai','4211Yangamai','Settlement' UNION ALL
SELECT 'JAURO MUSA','4211Yangamai-JAURO MUSA','Yangamai','4211Yangamai','Settlement' UNION ALL
SELECT 'UNG. ADADE','4211Yangamai-UNG. ADADE','Yangamai','4211Yangamai','Settlement' UNION ALL
SELECT 'K/FADA JURARA','4211Jurara-K/FADA JURARA','Jurara','4211Jurara','Settlement' UNION ALL
SELECT 'KESOWO','4211Jurara-KESOWO','Jurara','4211Jurara','Settlement' UNION ALL
SELECT 'RARUN KARI','4211Jurara-RARUN KARI','Jurara','4211Jurara','Settlement' UNION ALL
SELECT 'DUSHIN','4211JamaareD-DUSHIN','Jamaare D','4211JamaareD','Settlement' UNION ALL
SELECT 'NEPA AREWA','4211JamaareD-NEPA AREWA','Jamaare D','4211JamaareD','Settlement' UNION ALL
SELECT 'YAMMA DA TIKE','4211JamaareD-YAMMA DA TIKE','Jamaare D','4211JamaareD','Settlement' UNION ALL
SELECT 'GIDA DUBU','4211JamaareB-GIDA DUBU','Jamaare B','4211JamaareB','Settlement' UNION ALL
SELECT 'GINDIN DINYA','4211JamaareB-GINDIN DINYA','Jamaare B','4211JamaareB','Settlement' UNION ALL
SELECT 'K / ZANNA','4211JamaareB-K / ZANNA','Jamaare B','4211JamaareB','Settlement' UNION ALL
SELECT 'KARFAWA','4211Hanafari-KARFAWA','Hanafari','4211Hanafari','Settlement' UNION ALL
SELECT 'SOLAR','4211Hanafari-SOLAR','Hanafari','4211Hanafari','Settlement' UNION ALL
SELECT 'TAFIDA','4211Hanafari-TAFIDA','Hanafari','4211Hanafari','Settlement' UNION ALL
SELECT 'GANJILO','4211Galdimari-GANJILO','Galdimari','4211Galdimari','Settlement' UNION ALL
SELECT 'J BOREHOLE','4211Galdimari-J BOREHOLE','GALDIMARI','4211Galdimari','Settlement' UNION ALL
SELECT 'KOFAR GABAS GALDIMARI','4211Galdimari-KOFAR GABAS GALDIMARI','Galdimari','4211Galdimari','Settlement' UNION ALL
SELECT 'LOW COST','4211Galdimari-LOW COST','GALDIMARI','4211Galdimari','Settlement' UNION ALL
SELECT 'MUJABUR','4211Galdimari-MUJABUR','Galdimari','4211Galdimari','Settlement' UNION ALL
SELECT 'BANBASA','4211DogonJejiB-BANBASA','Dogon  Jeji B','4211DogonJejiB','Settlement' UNION ALL
SELECT 'GANJIYO','4211DogonJejiB-GANJIYO','Dogon  Jeji B','4211DogonJejiB','Settlement' UNION ALL
SELECT 'S/ MADAKI','4211DogonJejiB-S/ MADAKI','Dogon  Jeji B','4211DogonJejiB','Settlement' UNION ALL
SELECT 'KATTAKAI','4211DogonJejiA-KATTAKAI','Dogon  Jeji A','4211DogonJejiA','Settlement' UNION ALL
SELECT 'MUKADDAS','4211DogonJejiA-MUKADDAS','Dogon  Jeji A','4211DogonJejiA','Settlement' UNION ALL
SELECT 'KAMPANI','4203Bar-KAMPANI','Bar','4203Bar','Settlement' UNION ALL
SELECT 'Ang Galadima','4202Zungur-Ang Galadima','Zungur','4202Zungur','Settlement' UNION ALL
SELECT 'Ang sarkin kudu','4202Zungur-Ang sarkin kudu','Zungur','4202Zungur','Settlement' UNION ALL
SELECT 'Burum','4202Zungur-Burum','Zungur','4202Zungur','Settlement' UNION ALL
SELECT 'Kobi bayan primary','4202MakamaB-Kobi bayan primary','Makama B','4202MakamaB','Settlement' UNION ALL
SELECT 'Maikafi crescent','4202MakamaB-Maikafi crescent','Makama B','4202MakamaB','Settlement' UNION ALL
SELECT 'Rimin jahun','4202MakamaB-Rimin jahun','Makama B','4202MakamaB','Settlement' UNION ALL
SELECT 'Bala kariya street','4202MakamaA-Bala kariya street','Makama A','4202MakamaA','Settlement' UNION ALL
SELECT 'Commander House Area','4202MakamaA-Commander House Area','Makama A','4202MakamaA','Settlement' UNION ALL
SELECT 'Railway quarters north','4202MakamaA-Railway quarters north','Makama A','4202MakamaA','Settlement' UNION ALL
SELECT 'Bagali','4202Kangere-Bagali','Kangere','4202Kangere','Settlement' UNION ALL
SELECT 'Balanshi','4202Kangere-Balanshi','Kangere','4202Kangere','Settlement' UNION ALL
SELECT 'gidan anthony','4202Dawaki-gidan anthony','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'Janruwa','4202Dawaki-Janruwa','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'KWAGA','4202Dawaki-KWAGA','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'MAGUJI','4202Dawaki-MAGUJI','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'makan hanya ung mumumin','4202Dawaki-makan hanya ung mumumin','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'Mongoroji','4202Dawaki-Mongoroji','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'SAUNAWA','4202Dawaki-SAUNAWA','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'Shekal west','4202Dawaki-Shekal west','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'ung adamu','4202Dawaki-ung adamu','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'WUTAR KARA','4202Dawaki-WUTAR KARA','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'ZANBUWAWA','4202Dawaki-ZANBUWAWA','Dawaki','4202Dawaki','Settlement' UNION ALL
SELECT 'Igbo quarters','4202Dankade-Igbo quarters','Dankade','4202Dankade','Settlement' UNION ALL
SELECT 'Kangarke','4202Dankade-Kangarke','Dankade','4202Dankade','Settlement' UNION ALL
SELECT 'Malan goje','4202Dankade-Malan goje','Dankade','4202Dankade','Settlement' UNION ALL
SELECT 'Bayan vocational','4202DanAmarB-Bayan vocational','Dan Amar B','4202DanAmarB','Settlement' UNION ALL
SELECT 'Kandahar','4202DanAmarB-Kandahar','Dan Amar B','4202DanAmarB','Settlement' UNION ALL
SELECT 'Kofar wase A','4202DanAmarB-Kofar wase A','Dan Amar B','4202DanAmarB','Settlement' UNION ALL
SELECT 'Doya ta sakiya','4202DanAmarA-Doya ta sakiya','Dan Amar A','4202DanAmarA','Settlement' UNION ALL
SELECT 'Rafin albasa','4202DanAmarA-Rafin albasa','Dan Amar A','4202DanAmarA','Settlement' UNION ALL
SELECT 'Ung VIO','4202DanAmarA-Ung VIO','Dan Amar A','4202DanAmarA','Settlement' UNION ALL
SELECT 'dogon marke','3709Faru/Magami-dogon marke','FARU/MAGAMI','3709Faru/Magami','Settlement' UNION ALL
SELECT 'sakarawa','3705Bela/Rawayya-sakarawa','BELA/RAWAYYA','3705Bela/Rawayya','Settlement' UNION ALL
SELECT 'DABAWA A','3703NassarawaMailayi-DABAWA A','NASSARAWA MAILAYI','3703NassarawaMailayi','Settlement' UNION ALL
SELECT 'KARFASHI MARAFA','3703NassarawaMailayi-KARFASHI MARAFA','NASSARAWA MAILAYI','3703NassarawaMailayi','Settlement' UNION ALL
SELECT 'JARIRI','3703NassarawaGodelEast-JARIRI','NASSARAWA GODEL EAST','3703NassarawaGodelEast','Settlement' UNION ALL
SELECT 'SHIYAR S ASKI','3703NassarawaGodelEast-SHIYAR S ASKI','NASSARAWA GODEL EAST','3703NassarawaGodelEast','Settlement' UNION ALL
SELECT 'GARKA B','3703ModomawaWest-GARKA B','MODOMAWA WEST','3703ModomawaWest','Settlement' UNION ALL
SELECT 'GIDAN RABO','3703ModomawaWest-GIDAN RABO','MODOMAWA WEST','3703ModomawaWest','Settlement' UNION ALL
SELECT 'KISAWA','3703ModomawaWest-KISAWA','MODOMAWA WEST','3703ModomawaWest','Settlement' UNION ALL
SELECT 'BIRDIT','3703ModomawaEast-BIRDIT','MODOMAWA EAST','3703ModomawaEast','Settlement' UNION ALL
SELECT 'GIDAN HALIDU','3703ModomawaEast-GIDAN HALIDU','MODOMAWA EAST','3703ModomawaEast','Settlement' UNION ALL
SELECT 'SHATSI A','3703ModomawaEast-SHATSI A','MODOMAWA EAST','3703ModomawaEast','Settlement' UNION ALL
SELECT 'GIDAN BUGAJE','3703GusamiHayi-GIDAN BUGAJE','GUSAMI HAYI','3703GusamiHayi','Settlement' UNION ALL
SELECT 'GOBGAI','3703GusamiHayi-GOBGAI','GUSAMI HAYI','3703GusamiHayi','Settlement' UNION ALL
SELECT 'RUGAR BUGAJE','3703GusamiGari-RUGAR BUGAJE','GUSAMI GARI','3703GusamiGari','Settlement' UNION ALL
SELECT 'RUGAR FULANI','3703GusamiGari-RUGAR FULANI','GUSAMI GARI','3703GusamiGari','Settlement' UNION ALL
SELECT 'GALADIMA B','3703Damfani/S.Birni-GALADIMA B','DAMFANI/S.BIRNI','3703Damfani/S.Birni','Settlement' UNION ALL
SELECT 'MALLAMAWA','3703Damfani/S.Birni-MALLAMAWA','DAMFANI/S.BIRNI','3703Damfani/S.Birni','Settlement' UNION ALL
SELECT 'Ahmadu Guru','3615Shekau-Ahmadu Guru','SHEKAU','3615Shekau','Settlement' UNION ALL
SELECT 'Bulama Amsami','3615Shekau-Bulama Amsami','SHEKAU','3615Shekau','Settlement' UNION ALL
SELECT 'Bulama Umar','3615Shekau-Bulama Umar','SHEKAU','3615Shekau','Settlement' UNION ALL
SELECT 'kojolowa','3615Mandadawa-kojolowa','MANDADAWA','3615Mandadawa','Settlement' UNION ALL
SELECT 'koromari','3615Mandadawa-koromari','MANDADAWA','3615Mandadawa','Settlement' UNION ALL
SELECT 'Mandadawa','3615Mandadawa-Mandadawa','MANDADAWA','3615Mandadawa','Settlement' UNION ALL
SELECT 'Alhaji Musa','3615Lantewa-Alhaji Musa','LANTEWA','3615Lantewa','Settlement' UNION ALL
SELECT 'Bulama Dala','3615Lantewa-Bulama Dala','LANTEWA','3615Lantewa','Settlement' UNION ALL
SELECT 'Jama,ARE','3615Lantewa-Jama,ARE','LANTEWA','3615Lantewa','Settlement' UNION ALL
SELECT 'Anguwan Kanuri','3615Koriyel-Anguwan Kanuri','KORIYEL','3615Koriyel','Settlement' UNION ALL
SELECT 'Pawari','3615Koriyel-Pawari','KORIYEL','3615Koriyel','Settlement' UNION ALL
SELECT 'Bulama Audu','3615Jumbam-Bulama Audu','JUMBAM','3615Jumbam','Settlement' UNION ALL
SELECT 'Bulama Gaje','3615Jumbam-Bulama Gaje','JUMBAM','3615Jumbam','Settlement' UNION ALL
SELECT 'Bulama Kanumbu','3615Jumbam-Bulama Kanumbu','JUMBAM','3615Jumbam','Settlement' UNION ALL
SELECT 'Bulama Aisami','3615Guduram-Bulama Aisami','GUDURAM','3615Guduram','Settlement' UNION ALL
SELECT 'Kolori','3615Guduram-Kolori','GUDURAM','3615Guduram','Settlement' UNION ALL
SELECT 'Modu Kingimi','3615Guduram-Modu Kingimi','GUDURAM','3615Guduram','Settlement' UNION ALL
SELECT 'Bulama Jagalarima','3615Biriri-Bulama Jagalarima','BIRIRI','3615Biriri','Settlement' UNION ALL
SELECT 'Dogon Kuka','3615Biriri-Dogon Kuka','BIRIRI','3615Biriri','Settlement' UNION ALL
SELECT 'Bulama Jabtami','3615Babangida-Bulama Jabtami','BABANGIDA','3615Babangida','Settlement' UNION ALL
SELECT 'Bulama Modu Aji','3615Babangida-Bulama Modu Aji','BABANGIDA','3615Babangida','Settlement' UNION ALL
SELECT 'Tsamiya Uku','3615Babangida-Tsamiya Uku','BABANGIDA','3615Babangida','Settlement' UNION ALL
SELECT 'Kandahar','3614Bare-Bari-Kandahar','Bare-Bari','3614Bare-Bari','Settlement' UNION ALL
SELECT 'LOW COST','3604FikaAnze-LOW COST','Fika Anze','3604FikaAnze','Settlement' UNION ALL
SELECT 'BOKOLOJI','3602Masaba-BOKOLOJI','Masaba','3602Masaba','Settlement' UNION ALL
SELECT 'KORIJO','3602Masaba-KORIJO','Masaba','3602Masaba','Settlement' UNION ALL
SELECT 'LAMIDO ABDU','3602Masaba-LAMIDO ABDU','Masaba','3602Masaba','Settlement' UNION ALL
SELECT 'HARUNARI','3602Kaliyari-HARUNARI','Kaliyari','3602Kaliyari','Settlement' UNION ALL
SELECT 'NGELFASHI','3602Kaliyari-NGELFASHI','Kaliyari','3602Kaliyari','Settlement' UNION ALL
SELECT 'TUNGA GANGARE','3602Kaliyari-TUNGA GANGARE','Kaliyari','3602Kaliyari','Settlement' UNION ALL
SELECT 'GAMSAWA ALHAJI MUSA','3602Juluri/Damnawa-GAMSAWA ALHAJI MUSA','Juluri / Damnawa','3602Juluri/Damnawa','Settlement' UNION ALL
SELECT 'JULLURI KASHIMI','3602Juluri/Damnawa-JULLURI KASHIMI','Juluri / Damnawa','3602Juluri/Damnawa','Settlement' UNION ALL
SELECT 'KINNARI','3602Juluri/Damnawa-KINNARI','Juluri / Damnawa','3602Juluri/Damnawa','Settlement' UNION ALL
SELECT 'DOGON MARKE','3602JawaGarunDole-DOGON MARKE','Jawa Garun Dole','3602JawaGarunDole','Settlement' UNION ALL
SELECT 'JAWA ANGUWAN YAMMA','3602JawaGarunDole-JAWA ANGUWAN YAMMA','Jawa Garun Dole','3602JawaGarunDole','Settlement' UNION ALL
SELECT 'ZURGWAYA','3602JawaGarunDole-ZURGWAYA','Jawa Garun Dole','3602JawaGarunDole','Settlement' UNION ALL
SELECT 'AJIRI TSANGAYA','3602Guji/Metalari-AJIRI TSANGAYA','Guji / Metalari','3602Guji/Metalari','Settlement' UNION ALL
SELECT 'DAJIMI GONIRI','3602Guji/Metalari-DAJIMI GONIRI','Guji / Metalari','3602Guji/Metalari','Settlement' UNION ALL
SELECT 'DALARI MODU KAWURI','3602Guji/Metalari-DALARI MODU KAWURI','Guji / Metalari','3602Guji/Metalari','Settlement' UNION ALL
SELECT 'CHESKIRE','3602Guba/Dapso-CHESKIRE','Guba/Dapso','3602Guba/Dapso','Settlement' UNION ALL
SELECT 'HABUJA','3602Guba/Dapso-HABUJA','Guba/Dapso','3602Guba/Dapso','Settlement' UNION ALL
SELECT 'KWALJI','3602Guba/Dapso-KWALJI','Guba/Dapso','3602Guba/Dapso','Settlement' UNION ALL
SELECT 'AJAMARI','3602Dapchi-AJAMARI','Dapchi','3602Dapchi','Settlement' UNION ALL
SELECT 'BATALAWA','3602Dapchi-BATALAWA','Dapchi','3602Dapchi','Settlement' UNION ALL
SELECT 'LAMIDO GATA','3602Dapchi-LAMIDO GATA','Dapchi','3602Dapchi','Settlement' UNION ALL
SELECT 'BATAR BULAMA TURA','3602Bayamari-BATAR BULAMA TURA','Bayamari','3602Bayamari','Settlement' UNION ALL
SELECT 'MAI HAMIDU','3602Bayamari-MAI HAMIDU','Bayamari','3602Bayamari','Settlement' UNION ALL
SELECT 'MALAM BETI','3602Bayamari-MALAM BETI','Bayamari','3602Bayamari','Settlement' UNION ALL
SELECT 'CHALLARAM','3601SugumTagali-CHALLARAM','Sugum Tagali','3601SugumTagali','Settlement' UNION ALL
SELECT 'GABARWA GAYIN','3601SugumTagali-GABARWA GAYIN','Sugum Tagali','3601SugumTagali','Settlement' UNION ALL
SELECT 'GABARWA MALLUMA','3601SugumTagali-GABARWA MALLUMA','Sugum Tagali','3601SugumTagali','Settlement' UNION ALL
SELECT 'ALHAJI YELWA','3601LawanMusa-ALHAJI YELWA','Lawan Musa','3601LawanMusa','Settlement' UNION ALL
SELECT 'ANGUWAR LAWAN','3601LawanMusa-ANGUWAR LAWAN','Lawan Musa','3601LawanMusa','Settlement' UNION ALL
SELECT 'DAKISVI','3601LawanMusa-DAKISVI','Lawan Musa','3601LawanMusa','Settlement' UNION ALL
SELECT 'BABUJE','3601LawanFernami-BABUJE','Lawan Fernami','3601LawanFernami','Settlement' UNION ALL
SELECT 'BAHARU','3601LawanFernami-BAHARU','Lawan Fernami','3601LawanFernami','Settlement' UNION ALL
SELECT 'MALLAM BARTHEZ','3601LawanFernami-MALLAM BARTHEZ','Lawan Fernami','3601LawanFernami','Settlement' UNION ALL
SELECT 'FULKA','3601GwoKura-FULKA','Gwo Kura','3601GwoKura','Settlement' UNION ALL
SELECT 'GWIO KURA LAWANTI','3601GwoKura-GWIO KURA LAWANTI','Gwo Kura','3601GwoKura','Settlement' UNION ALL
SELECT 'KARKAFA AZBAK','3601Dawayo-KARKAFA AZBAK','Dawayo','3601Dawayo','Settlement' UNION ALL
SELECT 'USUR','3601Dawayo-USUR','Dawayo','3601Dawayo','Settlement' UNION ALL
SELECT 'BIZI','3601Dagona-BIZI','Dagona','3601Dagona','Settlement' UNION ALL
SELECT 'DAGONA MAKERA','3601Dagona-DAGONA MAKERA','Dagona','3601Dagona','Settlement' UNION ALL
SELECT 'DAGONA ZANGO COMPANY','3601Dagona-DAGONA ZANGO COMPANY','Dagona','3601Dagona','Settlement' UNION ALL
SELECT 'ANGWAN KASUWA','3504SertiA-ANGWAN KASUWA','Serti A','3504SertiA','Settlement' UNION ALL
SELECT 'GIDAN HODI','3421Wamakko-GIDAN HODI','Wamakko','3421Wamakko','Settlement' UNION ALL
SELECT 'MAJIYA KWACHAL AND TUDUN DAN JEKA','3421Wamakko-MAJIYA KWACHAL AND TUDUN DAN JEKA','Wamakko','3421Wamakko','Settlement' UNION ALL
SELECT 'BAKIN KUSU','3421Kalambaina-BAKIN KUSU','Kalambaina','3421Kalambaina','Settlement' UNION ALL
SELECT 'SHIYAR MARAFA','3421Kalambaina-SHIYAR MARAFA','Kalambaina','3421Kalambaina','Settlement' UNION ALL
SELECT 'HUCHI RUNJI','3421Gwamatse-HUCHI RUNJI','Gwamatse','3421Gwamatse','Settlement' UNION ALL
SELECT 'KURUNGUHU','3421Gwamatse-KURUNGUHU','Gwamatse','3421Gwamatse','Settlement' UNION ALL
SELECT 'LAGAU RUNJI','3421Gwamatse-LAGAU RUNJI','Gwamatse','3421Gwamatse','Settlement' UNION ALL
SELECT 'GIDAN MUMINI','3421Gumbi-GIDAN MUMINI','Gumbi','3421Gumbi','Settlement' UNION ALL
SELECT 'FIDAN YANFA','3421G/Hamidu-FIDAN YANFA','G/Hamidu','3421G/Hamidu','Settlement' UNION ALL
SELECT 'IDAN AYA','3421G/Hamidu-IDAN AYA','G/Hamidu','3421G/Hamidu','Settlement' UNION ALL
SELECT 'SAKARAWA','3421G/Hamidu-SAKARAWA','G/Hamidu','3421G/Hamidu','Settlement' UNION ALL
SELECT 'GIDAN SULE','3421Dundaye-GIDAN SULE','Dundaye','3421Dundaye','Settlement' UNION ALL
SELECT 'MAGINAWA','3421Dundaye-MAGINAWA','Dundaye','3421Dundaye','Settlement' UNION ALL
SELECT 'SHAMA','3421Dundaye-SHAMA','Dundaye','3421Dundaye','Settlement' UNION ALL
SELECT 'ARKILLA LIMAN','3421Arkilla-ARKILLA LIMAN','Arkilla','3421Arkilla','Settlement' UNION ALL
SELECT 'DUNGUZA','3421Arkilla-DUNGUZA','Arkilla','3421Arkilla','Settlement' UNION ALL
SELECT 'KANDAHAR','3416SarkinAdarG/Igwai-KANDAHAR','Sarkin Adar G/Igwai','3416SarkinAdarG/Igwai','Settlement' UNION ALL
SELECT 'ANGWAN MISSION','3216Poeship-ANGWAN MISSION','Poeship','3216Poeship','Settlement' UNION ALL
SELECT 'ANGWAN ALHERI','3214NamuCentral-ANGWAN ALHERI','Namu Central','3214NamuCentral','Settlement' UNION ALL
SELECT 'ANGWAN MISSION','3214NamuCentral-ANGWAN MISSION','Namu Central','3214NamuCentral','Settlement' UNION ALL
SELECT 'OLD GONGO','3214NamuCentral-OLD GONGO','Namu Central','3214NamuCentral','Settlement' UNION ALL
SELECT 'ANGWAN MISSION A','3214Luukwu-ANGWAN MISSION A','Luukwu','3214Luukwu','Settlement' UNION ALL
SELECT 'ANGWAN TOFA','3214Luukwu-ANGWAN TOFA','Luukwu','3214Luukwu','Settlement' UNION ALL
SELECT 'FE-GAMJI','3214Luukwu-FE-GAMJI','Luukwu','3214Luukwu','Settlement' UNION ALL
SELECT 'FUKWANG','3214Kwang-FUKWANG','Kwang','3214Kwang','Settlement' UNION ALL
SELECT 'KOPMOETOEGOER','3214Kwang-KOPMOETOEGOER','Kwang','3214Kwang','Settlement' UNION ALL
SELECT 'MANJI','3214Kwang-MANJI','Kwang','3214Kwang','Settlement' UNION ALL
SELECT 'ANGWAN FULANI','3214KwandeCentral-ANGWAN FULANI','Kwande Central','3214KwandeCentral','Settlement' UNION ALL
SELECT 'ANGWAN KASUWA','3214KwandeCentral-ANGWAN KASUWA','Kwande Central','3214KwandeCentral','Settlement' UNION ALL
SELECT 'ZAMLONG','3214KwandeCentral-ZAMLONG','Kwande Central','3214KwandeCentral','Settlement' UNION ALL
SELECT 'ANGWAN ABUJA','3214KurgwiEast-ANGWAN ABUJA','Kurgwi East','3214KurgwiEast','Settlement' UNION ALL
SELECT 'ANGWAN KWALLA','3214KurgwiEast-ANGWAN KWALLA','Kurgwi East','3214KurgwiEast','Settlement' UNION ALL
SELECT 'MUSKWANI','3214KurgwiEast-MUSKWANI','Kurgwi East','3214KurgwiEast','Settlement' UNION ALL
SELECT 'ANGWAN HALISAWA','3214Koplong-ANGWAN HALISAWA','Koplong','3214Koplong','Settlement' UNION ALL
SELECT 'KOPKLUK','3214Koplong-KOPKLUK','Koplong','3214Koplong','Settlement' UNION ALL
SELECT 'KOPMEOYLURI','3214Koplong-KOPMEOYLURI','Koplong','3214Koplong','Settlement' UNION ALL
SELECT 'ANGWAN ABUJA','3214DokaEast-ANGWAN ABUJA','Doka East','3214DokaEast','Settlement' UNION ALL
SELECT 'ANGWAN BORI','3214DokaEast-ANGWAN BORI','Doka East','3214DokaEast','Settlement' UNION ALL
SELECT 'ANGWAN SARKI AWE','3214DokaEast-ANGWAN SARKI AWE','Doka East','3214DokaEast','Settlement' UNION ALL
SELECT 'GOEPIA','3214Bwall-GOEPIA','Bwall','3214Bwall','Settlement' UNION ALL
SELECT 'SABON LANE B','3214Bwall-SABON LANE B','Bwall','3214Bwall','Settlement' UNION ALL
SELECT 'TANBA A','3214Bwall-TANBA A','Bwall','3214Bwall','Settlement' UNION ALL
SELECT 'ANGWAN MISSION','3210MabudiSouth-ANGWAN MISSION','Mabudi South','3210MabudiSouth','Settlement' UNION ALL
SELECT 'ALKALI','2725Akari-ALKALI','Akari','2725Akari','Settlement' UNION ALL
SELECT 'UNGUWA SARKIN FAWWA B2','2121YammaIi-UNGUWA SARKIN FAWWA B2','YAMMA II','2121YammaIi','Settlement' UNION ALL
SELECT 'KOFAR GUGA','2121YammaI-KOFAR GUGA','YAMMA I','2121YammaI','Settlement' UNION ALL
SELECT 'MAKUDAWA','2121YammaI-MAKUDAWA','YAMMA I','2121YammaI','Settlement' UNION ALL
SELECT 'SARARIN TSAKO','2121YammaI-SARARIN TSAKO','YAMMA I','2121YammaI','Settlement' UNION ALL
SELECT 'DUTSIN AMARE','2121GabasIi-DUTSIN AMARE','GABAS II','2121GabasIi','Settlement' UNION ALL
SELECT 'LAYOUT','2121GabasIi-LAYOUT','GABAS II','2121GabasIi','Settlement' UNION ALL
SELECT 'SABUWAR UNGUWAR D/AMARE','2121GabasIi-SABUWAR UNGUWAR D/AMARE','GABAS II','2121GabasIi','Settlement' UNION ALL
SELECT 'IYATANCHI 2','2121GabasI-IYATANCHI 2','GABAS I','2121GabasI','Settlement' UNION ALL
SELECT 'ZANGUNA C','2121GabasI-ZANGUNA C','GABAS I','2121GabasI','Settlement' UNION ALL
SELECT 'FARIN YARO','2121ArewaIi-FARIN YARO','AREWA II','2121ArewaIi','Settlement' UNION ALL
SELECT 'TUDUN YAN LIHIDDA A','2121ArewaIi-TUDUN YAN LIHIDDA A','AREWA II','2121ArewaIi','Settlement' UNION ALL
SELECT 'TUDUN YANLIHIDDA','2121ArewaIi-TUDUN YANLIHIDDA','AREWA II','2121ArewaIi','Settlement' UNION ALL
SELECT 'GAMBARAWA C','2121ArewaI-GAMBARAWA C','AREWA I','2121ArewaI','Settlement' UNION ALL
SELECT 'UNGUWAR MADAWAKI B','2121ArewaI-UNGUWAR MADAWAKI B','AREWA I','2121ArewaI','Settlement' UNION ALL
SELECT 'UNGUWAR YARI D','2121ArewaI-UNGUWAR YARI D','AREWA I','2121ArewaI','Settlement' UNION ALL
SELECT 'DILA','2044Kausani-DILA','Kausani','2044Kausani','Settlement' UNION ALL
SELECT 'KARABE','2043Imawa-KARABE','Imawa','2043Imawa','Settlement' UNION ALL
SELECT 'ADARAYE','2042YadaKunya-ADARAYE','Yada Kunya','2042YadaKunya','Settlement' UNION ALL
SELECT 'YUNUSAWA','2042YadaKunya-YUNUSAWA','Yada Kunya','2042YadaKunya','Settlement' UNION ALL
SELECT 'UNGOGGO MASASSAKA','2042Ungogo-UNGOGGO MASASSAKA','Ungogo','2042Ungogo','Settlement' UNION ALL
SELECT 'UNGUWAR MAI GARI','2042Ungogo-UNGUWAR MAI GARI','Ungogo','2042Ungogo','Settlement' UNION ALL
SELECT 'UNGUWAR MALAMAI','2042Ungogo-UNGUWAR MALAMAI','Ungogo','2042Ungogo','Settlement' UNION ALL
SELECT 'ASIBITIN TAFASA','2042Bachirawa-ASIBITIN TAFASA','Bachirawa','2042Bachirawa','Settlement' UNION ALL
SELECT 'I.ASIBITI','2042Bachirawa-I.ASIBITI','Bachirawa','2042Bachirawa','Settlement' UNION ALL
SELECT 'GIDAN RIMI','2032Rurum-TsohonGari-GIDAN RIMI','Rurum - Tsohon Gari','2032Rurum-TsohonGari','Settlement' UNION ALL
SELECT 'ang iro','1915Zabi-ang iro','Zabi','1915Zabi','Settlement' UNION ALL
SELECT 'ang jikanayi','1915Zabi-ang jikanayi','Zabi','1915Zabi','Settlement' UNION ALL
SELECT 'Kosso South','1915Zabi-Kosso South','ZABI','1915Zabi','Settlement' UNION ALL
SELECT 'Maisiddi East','1915Zabi-Maisiddi East','ZABI','1915Zabi','Settlement' UNION ALL
SELECT 'Nagunda South','1915Zabi-Nagunda South','ZABI','1915Zabi','Settlement' UNION ALL
SELECT 'ung dankyafi','1915Zabi-ung dankyafi','Zabi','1915Zabi','Settlement' UNION ALL
SELECT 'Makarahuta','1915Pambegua-Makarahuta','PAMBEGUA','1915Pambegua','Settlement' UNION ALL
SELECT 'Rugar Sa''idu','1915Pambegua-Rugar Sa''idu','PAMBEGUA','1915Pambegua','Settlement' UNION ALL
SELECT 'Gidan Guda','1915Mah-Gidan Guda','MAH','1915Mah','Settlement' UNION ALL
SELECT 'Hayin Soda','1915Mah-Hayin Soda','MAH','1915Mah','Settlement' UNION ALL
SELECT 'Karaba D.','1915Mah-Karaba D.','MAH','1915Mah','Settlement' UNION ALL
SELECT 'Gedege','1915Kargi-Gedege','KARGI','1915Kargi','Settlement' UNION ALL
SELECT 'Gidan Sule','1915Kargi-Gidan Sule','KARGI','1915Kargi','Settlement' UNION ALL
SELECT 'Goberawa','1915Kargi-Goberawa','KARGI','1915Kargi','Settlement' UNION ALL
SELECT 'Rugar Dogo','1915Kareh-Rugar Dogo','KAREH','1915Kareh','Settlement' UNION ALL
SELECT 'Rugar Idi','1915Kareh-Rugar Idi','KAREH','1915Kareh','Settlement' UNION ALL
SELECT 'Kwando','1915Haskiya-Kwando','HASKIYA','1915Haskiya','Settlement' UNION ALL
SELECT 'Ungwan Alaranma Harira','1915Haskiya-Ungwan Alaranma Harira','HASKIYA','1915Haskiya','Settlement' UNION ALL
SELECT 'Wawariya','1915Haskiya-Wawariya','HASKIYA','1915Haskiya','Settlement' UNION ALL
SELECT 'Bidabidi','1915DutsenWai-Bidabidi','DUTSEN WAI','1915DutsenWai','Settlement' UNION ALL
SELECT 'Rugar Goggo','1915DutsenWai-Rugar Goggo','DUTSEN WAI','1915DutsenWai','Settlement' UNION ALL
SELECT 'Ung. Alh. Dayyabu','1915DutsenWai-Ung. Alh. Dayyabu','DUTSEN WAI','1915DutsenWai','Settlement' UNION ALL
SELECT 'Gidan Mai Garu','1915Anchau-Gidan Mai Garu','ANCHAU','1915Anchau','Settlement' UNION ALL
SELECT 'Hawan Bala','1915Anchau-Hawan Bala','ANCHAU','1915Anchau','Settlement' UNION ALL
SELECT 'Layin Amu','1915Anchau-Layin Amu','ANCHAU','1915Anchau','Settlement' UNION ALL
SELECT 'dabba','1910Ung.Sanusi-dabba','UNG. SANUSI','1910Ung.Sanusi','Settlement' UNION ALL
SELECT 'danladi yunusa','1910Ung.Sanusi-danladi yunusa','UNG. SANUSI','1910Ung.Sanusi','Settlement' UNION ALL
SELECT 'kwarba','1910Ung.Sanusi-kwarba','UNG. SANUSI','1910Ung.Sanusi','Settlement' UNION ALL
SELECT 'abeylo close','1910Television-abeylo close','TELEVISION','1910Television','Settlement' UNION ALL
SELECT 'behind supermarket','1910Television-behind supermarket','TELEVISION','1910Television','Settlement' UNION ALL
SELECT 'shandem','1910Television-shandem','TELEVISION','1910Television','Settlement' UNION ALL
SELECT ' tudu ilu','1910T/Nupawa- tudu ilu','T/NUPAWA','1910T/Nupawa','Settlement' UNION ALL
SELECT 'police barrack','1910T/Nupawa-police barrack','T/NUPAWA','1910T/Nupawa','Settlement' UNION ALL
SELECT 'ribadu crescent','1910T/Nupawa-ribadu crescent','T/NUPAWA','1910T/Nupawa','Settlement' UNION ALL
SELECT 'layin mai turare','1910SabongariWest-layin mai turare','SabonGari West','1910SabongariWest','Settlement' UNION ALL
SELECT 'layin yar kare','1910SabongariWest-layin yar kare','SabonGari West','1910SabongariWest','Settlement' UNION ALL
SELECT 'sule gurgu','1910SabongariWest-sule gurgu','SabonGari West','1910SabongariWest','Settlement' UNION ALL
SELECT 'kwoi street','1910S/GariNorth-kwoi street','S/GARI NORTH','1910S/GariNorth','Settlement' UNION ALL
SELECT 'ruma road','1910S/GariNorth-ruma road','S/GARI NORTH','1910S/GariNorth','Settlement' UNION ALL
SELECT 'zango road','1910S/GariNorth-zango road','S/GARI NORTH','1910S/GariNorth','Settlement' UNION ALL
SELECT 'old artilery','1910KakuriHausa-old artilery','Kakuri Hausa','1910KakuriHausa','Settlement' UNION ALL
SELECT 'SNCO BY B2,C1,C2','1910KakuriHausa-SNCO BY B2,C1,C2','Kakuri Hausa','1910KakuriHausa','Settlement' UNION ALL
SELECT 'TABANI ROAD','1910KakuriHausa-TABANI ROAD','Kakuri Hausa','1910KakuriHausa','Settlement' UNION ALL
SELECT 'C B N QUARTER','1910Barnawa-C B N QUARTER','BARNAWA','1910Barnawa','Settlement' UNION ALL
SELECT 'INDIA STREET','1910Barnawa-INDIA STREET','BARNAWA','1910Barnawa','Settlement' UNION ALL
SELECT 'UNG YUSUF','1908KurminMusa-UNG YUSUF','Kurmin Musa','1908KurminMusa','Settlement' UNION ALL
SELECT 'FEDERATION','1907Maigizo-FEDERATION','MAIGIZO','1907Maigizo','Settlement' UNION ALL
SELECT 'MAYIKALI','1907Maigizo-MAYIKALI','MAIGIZO','1907Maigizo','Settlement' UNION ALL
SELECT 'ZIPAK','1907Maigizo-ZIPAK','MAIGIZO','1907Maigizo','Settlement' UNION ALL
SELECT 'goska','1907Kaninkon-goska','KANINKON','1907Kaninkon','Settlement' UNION ALL
SELECT 'misisi','1907Kaninkon-misisi','KANINKON','1907Kaninkon','Settlement' UNION ALL
SELECT 'ung tete','1907Kaninkon-ung tete','KANINKON','1907Kaninkon','Settlement' UNION ALL
SELECT 'hospital road','1907KafanchanAB-hospital road','KAFANCHAN A B','1907KafanchanAB','Settlement' UNION ALL
SELECT 'warri street','1907KafanchanAB-warri street','KAFANCHAN A B','1907KafanchanAB','Settlement' UNION ALL
SELECT 'FADA 2','1907KafanchanA-FADA 2','KAFANCHAN A','1907KafanchanA','Settlement' UNION ALL
SELECT 'UNG RIMI','1907KafanchanA-UNG RIMI','KAFANCHAN A','1907KafanchanA','Settlement' UNION ALL
SELECT 'UNG SA,A','1907KafanchanA-UNG SA,A','KAFANCHAN A','1907KafanchanA','Settlement' UNION ALL
SELECT 'kariyo','1907Jagindi-kariyo','JAGINDI','1907Jagindi','Settlement' UNION ALL
SELECT 'ARAK','1907Godo-Godo-ARAK','GODO-GODO','1907Godo-Godo','Settlement' UNION ALL
SELECT 'SABON GARI KIBON','1907Godo-Godo-SABON GARI KIBON','GODO-GODO','1907Godo-Godo','Settlement' UNION ALL
SELECT 'UNG GWANA','1907Godo-Godo-UNG GWANA','GODO-GODO','1907Godo-Godo','Settlement' UNION ALL
SELECT 'ANTANG','1907GidanWaya-ANTANG','GIDAN WAYA','1907GidanWaya','Settlement' UNION ALL
SELECT 'NASIMA B','1907GidanWaya-NASIMA B','GIDAN WAYA','1907GidanWaya','Settlement' UNION ALL
SELECT 'UNG MANGU','1907GidanWaya-UNG MANGU','GIDAN WAYA','1907GidanWaya','Settlement' UNION ALL
SELECT 'DOGON MARKE','1821ToniKutara-DOGON MARKE','Toni Kutara','1821ToniKutara','Settlement' UNION ALL
SELECT 'hamadaza','1819Kwanda-hamadaza','Kwanda','1819Kwanda','Settlement' UNION ALL
SELECT 'kwanda kudu','1819Kwanda-kwanda kudu','Kwanda','1819Kwanda','Settlement' UNION ALL
SELECT 'rusu','1819Kwanda-rusu','Kwanda','1819Kwanda','Settlement' UNION ALL
SELECT 'Ba''awa','1819Kiyawa-Ba''awa','Kiyawa','1819Kiyawa','Settlement' UNION ALL
SELECT 'gabari','1819Kiyawa-gabari','Kiyawa','1819Kiyawa','Settlement' UNION ALL
SELECT 'karabe','1819Kiyawa-karabe','Kiyawa','1819Kiyawa','Settlement' UNION ALL
SELECT 'Kauyen Adam','1819Kiyawa-Kauyen Adam','Kiyawa','1819Kiyawa','Settlement' UNION ALL
SELECT 'tsohuwar kanoke','1819Kiyawa-tsohuwar kanoke','Kiyawa','1819Kiyawa','Settlement' UNION ALL
SELECT 'badambo','1819Katuka-badambo','Katuka','1819Katuka','Settlement' UNION ALL
SELECT 'gidan tilo','1819Katuka-gidan tilo','Katuka','1819Katuka','Settlement' UNION ALL
SELECT 'Fagada Babba','1819Katanga-Fagada Babba','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'jigawa b','1819Katanga-jigawa b','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'Kambarawa','1819Katanga-Kambarawa','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'katanga kudu','1819Katanga-katanga kudu','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'kwallam','1819Katanga-kwallam','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'Sabon Gari Kudu','1819Katanga-Sabon Gari Kudu','Katanga','1819Katanga','Settlement' UNION ALL
SELECT 'fake a','1819Fake-fake a','Fake','1819Fake','Settlement' UNION ALL
SELECT 'maharba','1819Fake-maharba','Fake','1819Fake','Settlement' UNION ALL
SELECT 'babarin fulani','1819Balago-babarin fulani','Balago','1819Balago','Settlement' UNION ALL
SELECT 'debi a','1819Balago-debi a','Balago','1819Balago','Settlement' UNION ALL
SELECT 'andaza cikin gari','1819Andaza-andaza cikin gari','Andaza','1819Andaza','Settlement' UNION ALL
SELECT 'gidan rimi','1819Andaza-gidan rimi','Andaza','1819Andaza','Settlement'
)x
ON sdd.guid = 'JD_INSERT_POLIO_412';


-- Handle Dupe Region Names by adding parent --

UPDATE _sett s
SET region_name = x.region_name || '-' || s.parent_name
FROM (
	SELECT region_name,count(*) AS C FROM _sett
	GROUP BY region_name HAVING COUNT(1) > 1
)x
WHERE x.region_name = s.region_name;

INSERT INTO source_region
(region_code,parent_name,parent_code,region_type,document_id,source_guid,is_high_risk)

SELECT
	region_code
	,parent_name
	,parent_code
	,region_type
	,document_id
	,region_code || '-' || document_id
	,'t'
FROM _sett st
WHERE NOT EXISTS (
	SELECT 1 FROM source_region sr
	WHERE sr.region_code = st.region_code
);

UPDATE _sett s
SET source_id = sr.id
FROM source_region sr
WHERE s.region_code = sr.region_code;

INSERT INTO region
(office_id, slug, source_id, region_code, is_high_risk, name, parent_region_id, region_type_id,created_at)

SELECT
	o.id
	,LOWER(REPLACE(st.region_code,' ','-'))
	,src.id
	,st.region_code
	,'t'
	,st.region_name
	,rp.id
	,rt.id
	,now()
FROM _sett st
INNER JOIN (SELECT id FROM office WHERE name = 'Nigeria') o
	ON 1=1
INNER JOIN (SELECT id FROM source WHERE source_name = 'John_SQL') src
	ON 1=1
INNER JOIN region_type rt
	ON LOWER(st.region_type) = LOWER(rt.name)
INNER JOIN region rp
	ON st.parent_code = rp.region_code
WHERE st.source_id IS NOT NULL
AND NOT EXISTS (
	SELECT 1 FROM region r
	WHERE st.region_code = r.region_code
)
AND NOT EXISTS (
	SELECT 1 FROM region r
	WHERE st.region_name = r.name
);

INSERT INTO region_map
(source_id, master_id,mapped_by_id)

SELECT
	s.source_id
	,r.id
	,1
FROM _sett s
INNER JOIN region r
ON s.region_code = r.region_code
WHERE NOT EXISTS (
	SELECT 1 FROM region_map rm
	WHERE s.source_id = rm.source_id
);

UPDATE _sett
	SET master_id = rm.master_id
FROM region_map rm
WHERE _sett.source_id = rm.source_id
