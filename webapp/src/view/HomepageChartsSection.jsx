'use strict';

var React = require('react');
var HomepageCharts = require('dashboard/homepage/HomepageCharts.jsx');

var HomepageChartsSection = React.createClass({
    render: function () {
        var dashboard = React.createElement(HomepageCharts, this.props.data);
        var chartId = `${this.props.location.toLowerCase()}-chart`;

        var controls;
        if(this.props.location === 'Nigeria') {
            controls = <div className="chart-button-group">
                            <div className="chart-button"><span>Country overview</span></div>
                            <div className="chart-button"><span>District summary</span></div>
                            <div className="chart-button"><span>NGA Campaign Monitoring</span></div>
                        </div>
        } else {
            controls = <div className="chart-button-group">
                            <div className="chart-button"><span>Country overview</span></div>
                            <div className="chart-button"><span>District summary</span></div>
                        </div>
        }
        return (
            <div>
                <div className="large-4 columns chart-container" id={chartId}>
                    <div className="chart">
                        <h5>{this.props.location}</h5>
                        {dashboard}
                        {controls}
                    </div>
                </div>

            </div>
        );
    }
});

module.exports = HomepageChartsSection;
