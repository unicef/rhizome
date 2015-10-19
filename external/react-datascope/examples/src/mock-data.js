// http://www.json-generator.com/
//[
//    '{{repeat(15, 20)}}',
//    {
//        id: '{{objectId()}}',
//        name: '{{firstName()}} {{surname()}}',
//        isActive: '{{bool()}}',
//        age: '{{integer(20, 40)}}',
//        gender: '{{gender()}}',
//        company: '{{company()}}',
//        email: '{{email()}}',
//        registered: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
//        latitude: '{{floating(-90.000001, 90)}}',
//        longitude: '{{floating(-180.000001, 180)}}'
//    }
//]

// takes a list of strings ['a','b','c'] and creates an object like {a:'a', b:'b', c:'c'}
function mirrorObj(list) { return _.object(list, list); }

var ValueTypes = mirrorObj([
    'string',
    'longstring', // ie. those which should be edited with a textarea?
    'number',
    'boolean',
    'datetime', // how to format... moment.js?
    'list', // list of objects or values?

    'string',
    'number',
    'integer',
    'boolean',
    'null',

]);
console.log(ValueTypes);

module.exports = {
    schema: {
        idKey: 'id',
        fields: [
            {
                name: 'id',
                title: "ID",
                type: ValueTypes.string,
                isVisible: false
            },
            {
                name: 'name',
                title: "Name",
                type: ValueTypes.string
            },
            {
                name: 'isActive',
                title: "Active?",
                type: ValueTypes.boolean
            },
            {
                name: 'age',
                title: "Age",
                type: ValueTypes.number
            },
            {
                name: 'gender',
                title: "Gender",
                type: ValueTypes.string
            },
            {
                name: 'company',
                title: "Company",
                type: ValueTypes.string
            },
            {
                name: 'email',
                title: "E-mail Address",
                type: ValueTypes.string,
            },
            {
                name: 'latitude',
                title: "Latitude",
                type: ValueTypes.number
            },
            {
                name: 'longitude',
                title: "Longitude",
                type: ValueTypes.number
            }
        ]
    },
    data: [
        {
            "id": "552429f9ecd9f0355bf876aa",
            "name": "May Baker",
            "isActive": true,
            "age": 29,
            "gender": "female",
            "company": "Bluegrain",
            "email": "maybaker@bluegrain.com",
            "registered": "2015-01-19T22:05:36 +05:00",
            "latitude": -14.306177,
            "longitude": -126.085883
        },
        {
            "id": "552429f9168277a5cef8211a",
            "name": "Marissa Sanders",
            "isActive": false,
            "age": 36,
            "gender": "female",
            "company": "Hivedom",
            "email": "marissasanders@hivedom.com",
            "registered": "2015-03-14T02:29:18 +04:00",
            "latitude": -42.599773,
            "longitude": 157.22632
        },
        {
            "id": "552429f97fafc5906951c208",
            "name": "Morris Burks",
            "isActive": true,
            "age": 23,
            "gender": "male",
            "company": "Cipromox",
            "email": "morrisburks@cipromox.com",
            "registered": "2014-12-05T20:15:58 +05:00",
            "latitude": 17.664601,
            "longitude": -9.810862
        },
        {
            "id": "552429f98dffd931d63a8d53",
            "name": "Anna Gay",
            "isActive": true,
            "age": 40,
            "gender": "female",
            "company": "Hatology",
            "email": "annagay@hatology.com",
            "registered": "2014-01-19T01:31:26 +05:00",
            "latitude": 30.150124,
            "longitude": 165.141861
        },
        {
            "id": "552429f9fe7402d53411c115",
            "name": "Julie Butler",
            "isActive": false,
            "age": 26,
            "gender": "female",
            "company": "Myopium",
            "email": "juliebutler@myopium.com",
            "registered": "2014-09-20T18:17:34 +04:00",
            "latitude": -56.931811,
            "longitude": -80.020407
        },
        {
            "id": "552429f9244d976e26dba038",
            "name": "Pugh Vincent",
            "isActive": false,
            "age": 32,
            "gender": "male",
            "company": "Katakana",
            "email": "pughvincent@katakana.com",
            "registered": "2014-11-13T14:11:33 +05:00",
            "latitude": -27.522091,
            "longitude": -89.426089
        },
        {
            "id": "552429f933a7525458de43ed",
            "name": "Dianne Marquez",
            "isActive": false,
            "age": 29,
            "gender": "female",
            "company": "Aquoavo",
            "email": "diannemarquez@aquoavo.com",
            "registered": "2015-02-23T10:07:52 +05:00",
            "latitude": 79.664372,
            "longitude": 76.636831
        },
        {
            "id": "552429f9627b271b4092f2ca",
            "name": "Dolly Hewitt",
            "isActive": true,
            "age": 23,
            "gender": "female",
            "company": "Kengen",
            "email": "dollyhewitt@kengen.com",
            "registered": "2014-02-19T18:39:24 +05:00",
            "latitude": -37.058702,
            "longitude": 140.374625
        },
        {
            "id": "552429f96c64aa7cb331dee1",
            "name": "Madden Atkinson",
            "isActive": false,
            "age": 34,
            "gender": "male",
            "company": "Gink",
            "email": "maddenatkinson@gink.com",
            "registered": "2014-05-07T15:54:59 +04:00",
            "latitude": 81.906734,
            "longitude": -68.865407
        },
        {
            "id": "552429f92ae12d1bd6dccfc9",
            "name": "Barker Cummings",
            "isActive": false,
            "age": 38,
            "gender": "male",
            "company": "Joviold",
            "email": "barkercummings@joviold.com",
            "registered": "2014-08-09T23:54:41 +04:00",
            "latitude": 73.225196,
            "longitude": 80.4118
        },
        {
            "id": "552429f96eebbad4bb6aafa7",
            "name": "Cassandra Greer",
            "isActive": true,
            "age": 31,
            "gender": "female",
            "company": "Updat",
            "email": "cassandragreer@updat.com",
            "registered": "2015-03-13T11:30:44 +04:00",
            "latitude": 37.696832,
            "longitude": 162.597054
        },
        {
            "id": "552429f95bf7c40563243e0a",
            "name": "Riggs Glover",
            "isActive": true,
            "age": 21,
            "gender": "male",
            "company": "Sunclipse",
            "email": "riggsglover@sunclipse.com",
            "registered": "2014-12-02T18:25:20 +05:00",
            "latitude": -26.894002,
            "longitude": -84.752323
        },
        {
            "id": "552429f959b67a868720f1de",
            "name": "Simmons Owen",
            "isActive": false,
            "age": 20,
            "gender": "male",
            "company": "Ginkogene",
            "email": "simmonsowen@ginkogene.com",
            "registered": "2014-02-17T21:07:03 +05:00",
            "latitude": 84.753196,
            "longitude": -78.513625
        },
        {
            "id": "552429f907dc32c2a0a677ea",
            "name": "Chandler Pickett",
            "isActive": true,
            "age": 21,
            "gender": "male",
            "company": "Idego",
            "email": "chandlerpickett@idego.com",
            "registered": "2014-03-09T23:57:09 +04:00",
            "latitude": -29.049122,
            "longitude": -129.988344
        },
        {
            "id": "552429f9b0e0322f11a76f34",
            "name": "Townsend Ellison",
            "isActive": false,
            "age": 34,
            "gender": "male",
            "company": "Infotrips",
            "email": "townsendellison@infotrips.com",
            "registered": "2015-02-26T07:52:55 +05:00",
            "latitude": 23.132955,
            "longitude": -79.996741
        },
        {
            "id": "552429f9a6f16a0eae837914",
            "name": "Norman Sandoval",
            "isActive": true,
            "age": 30,
            "gender": "male",
            "company": "Datacator",
            "email": "normansandoval@datacator.com",
            "registered": "2014-08-10T11:24:42 +04:00",
            "latitude": 1.647065,
            "longitude": 153.520958
        },
        {
            "id": "552429f9c228b312f08434da",
            "name": "Mcleod Marsh",
            "isActive": false,
            "age": 20,
            "gender": "male",
            "company": "Nspire",
            "email": "mcleodmarsh@nspire.com",
            "registered": "2014-01-23T23:04:34 +05:00",
            "latitude": 68.463413,
            "longitude": 19.537768
        },
        {
            "id": "552429f98f6a96c5f8c542cb",
            "name": "Sanford Joseph",
            "isActive": true,
            "age": 32,
            "gender": "male",
            "company": "Omnigog",
            "email": "sanfordjoseph@omnigog.com",
            "registered": "2014-01-20T20:24:53 +05:00",
            "latitude": -9.769939,
            "longitude": -126.280267
        },
        {
            "id": "552429f97572c8c812531fcb",
            "name": "Reilly Washington",
            "isActive": false,
            "age": 33,
            "gender": "male",
            "company": "Comtrail",
            "email": "reillywashington@comtrail.com",
            "registered": "2014-10-17T03:01:04 +04:00",
            "latitude": -83.474762,
            "longitude": 26.181351
        }
    ]
};