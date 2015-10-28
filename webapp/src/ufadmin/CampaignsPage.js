var React = require('react');
var _ = require('lodash');
var DateRangePicker = require('component/DateTimePicker.jsx');
var api = require('../data/api');

var CampaignsPage = (function () {
  return {
    render: function (start_date_dom_id, end_date_dom_id) {
      var createControl = function (id) {
        var dateRangePickerProps = {};
        var input_dom = document.getElementById(id);
        input_dom.type = "hidden";

        var parent_dom = input_dom.parentNode;
        var input_dom = document.createElement("div");
        input_dom.id = id + "_date_picker";
        parent_dom.appendChild(input_dom);

        React.render(React.createElement(DateRangePicker, dateRangePickerProps), input_dom);
      };

      createControl(start_date_dom_id);
      createControl(end_date_dom_id);
    }
  };
})();

module.exports = CampaignsPage;