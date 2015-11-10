module.exports = {
    'id'                : -5,
    'title'             : 'ODK Dashboard',
  'builtin': true,
    'default_office_id' : 1,
    'charts' : [{
        'title': 'Caregiver Awareness',
        'section': 'overview',
        'indicators': [276],
    'timeRange': 0
    },{
        'title': 'Non Compliance',
        'type'       : 'ChoroplethMap',
        'section': 'map',
        'indicators': [289],
    'timeRange': 0
    },
    {
        'title': 'Missed Children',
        'section': 'breakdown',
        'locations': 'sublocations',
        'timeRange': 0,
        'indicators': [267,268,251,264]
    },
]
}
