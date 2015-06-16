module.exports = {
	'id'                : 3,
	'title'             : 'NGA Campaign Monitoring',
	'default_office_id' : 1,
	'charts' : [{
		'title': 'Inside',
		'section': 'overview',
		'indicators': [272]
	}, {
		'title': 'Outside',
		'section': 'overview',
		'indicators': [274]
	}, {
		'title': 'Caregiver Awareness',
		'section': 'overview',
		'indicators': [276]
	}, {
		'title': 'Influencers',
		'section': 'overview',
		'indicators': [287,288,289,290,291,292,293,294]
	}, {
		'title': 'Information Source',
		'section': 'overview',
		'indicators': [307,308,309,310,311,312,313,314,315,316,317]
	}, {
		'title': 'Reason for Missed',
		'section': 'overview',
		'indicators': [318,319,320,321]
	}, {
		'title': 'Reason for Absence',
		'section': 'overview',
		'indicators': [323,324,325,326,327]
	}, {
		'title': 'Reason for Non-Compliance',
		'section': 'overview',
		'indicators': [328,329,330,331,332,333,334,322]
	}, {
		'title': 'NC Resolved by',
		'section': 'overview',
		'indicators': [345,346,347,348]
	}, {
		'title': 'Inside Monitoring',
		'section': 'overview',
		'region': 'subregions',
		'indicators': [276, 272]
	}, {
		'title': 'Outside Monitoring',
		'section': 'overview',
		'region': 'subregions',
		'indicators': [276, 274]
	}, {
		'title': 'Missed Children',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [267,268,251,264]
	}, {
		'title': 'Missed Children (Inside vs Outside)',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [265,273]
	}, {
		'title': 'Absences',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [246,247,248,249,250]
	}, {
		'title': 'Non-Compliance',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [252,255,258,261,253,256,259,254,257,260,263,262,266]
	}, {
		'title': 'Non-Compliance Resolutions',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [340,341,342,343]
	}, {
		'title': 'Influencers',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [278,279,280,281,282,283,284,285]
	}, {
		'title': 'Sources of Information',
		'section': 'breakdown',
		'region': 'subregions',
		'indicators': [295,299,303,296,300,304,297,301,305,298,302]
	}]
};
