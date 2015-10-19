'use strict';

module.exports = {
    Datascope: require('./Datascope'),
    LocalDatascope: require('./LocalDatascope'),

    InterfaceMixin: require('./InterfaceMixin'),

    DataList: require('./modules/DataList'),

    // fixed-data-table - deprecated for now
    //DataTable: require('./modules/DataTable'),

    SimpleDataTable: require('./modules/SimpleDataTable'),
    SimpleDataTableColumn: require('./modules/SimpleDataTableColumn'),

    ClearQueryLink: require('./modules/ClearQueryLink'),

    FilterPanel: require('./modules/FilterPanel'),
    FilterInputCheckbox: require('./modules/FilterInputCheckbox'),
    FilterInputRadio: require('./modules/FilterInputRadio'),
    FilterDateRange: require('./modules/FilterDateRange'),

    SearchBar: require('./modules/SearchBar'),

    Paginator: require('./modules/Paginator')
};
