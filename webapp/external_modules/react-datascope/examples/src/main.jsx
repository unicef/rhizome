require('babel/polyfill');
require('./../styles/main.css');
require('./../styles/fixed-data-table.css');

var _ = require('lodash'),
    React = require('react/addons');

var {
    Datascope, LocalDatascope,
    InterfaceMixin,
    DataList,
    SimpleDataTable, SimpleDataTableColumn,
    ClearQueryLink,
    SearchBar,
    FilterPanel, FilterInputRadio, FilterInputCheckbox,
    FilterDateRange,
    Paginator
} = require('../../src');

var mockData = require('./mock-data3');

window.moment = require('moment');

var TestElement = React.createClass({
    mixins: [InterfaceMixin('Datascope', 'DatascopeSearch', 'DatascopeSort', 'DatascopeFilter')],
    componentDidMount() {
        console.log('mounted TestComponent', this.props)
    },
    render() {
        return <div>
            {this.props.data.map(d => {
                return _.map(this.props.schema.items.properties, (propSchema, key) => {
                    return <div><strong>{propSchema.title}: </strong>{d[key]}</div>
                }).concat(<hr/>);
            })}
        </div>
    }
});


var App = React.createClass({
    render() {
        return (
            <div>
                <LocalDatascope
                    data={mockData.data}
                    schema={mockData.schema}
                    fields={mockData.fields}
                    paginated={true}
                    pageSize={3}
                    >
                    <Datascope>

                        <ClearQueryLink>
                            <a href="#">Clear filters</a>
                        </ClearQueryLink>

                        <SearchBar
                            id="search-all"
                            placeholder="all fields"
                            />

                        <SearchBar
                            id="search-age"
                            fieldNames={['age']}
                            placeholder="age"
                            />

                        <FilterPanel>
                            <FilterDateRange name="date_joined" time={false} />
                            <FilterInputRadio name="is_superuser"/>
                        </FilterPanel>

                        <Paginator />

                        <DataList />

                        <SimpleDataTable>
                            <SimpleDataTableColumn name="first_name" />
                            <SimpleDataTableColumn name="last_name" />
                            <SimpleDataTableColumn name="username" />
                            <SimpleDataTableColumn name="edit_link" />
                        </SimpleDataTable>

                        <SimpleDataTable></SimpleDataTable>

                    </Datascope>
                </LocalDatascope>
            </div>
        );

    }
});

React.render(<App />, document.getElementById('container'));

module.exports = App;
