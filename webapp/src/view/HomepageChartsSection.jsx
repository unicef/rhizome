'use strict';

var React = require('react');
var HomepageCharts = require('dashboard/homepage/HomepageCharts.jsx');

var HomepageChartsSection = React.createClass({

    render: function () {
        console.log(this.props.data);


        var dashboard = React.createElement(HomepageCharts, this.props.data);
        var chartId = `${this.props.location.toLowerCase()}-chart`;

        return (
            <div>
                <div className="large-4 columns chart-container" id={chartId}>
                    <div className="chart">
                        <h5>{this.props.location}</h5>
                          {dashboard}
                        <div className="chart-button-group">
                            <div className="chart-button"><span>Country overview</span></div>
                            <div className="chart-button"><span>District summary</span></div>
                        </div>
                    </div>
                </div>

            </div>
        );
    }
});

module.exports = HomepageChartsSection;
