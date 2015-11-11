var React = require('react')
var moment = require('moment')
var DatePicker = require('component/DatePicker.jsx')

var CampaignsPage = (function () {
  return {
    render: function (start_date_dom_id, end_date_dom_id) {
      var createControl = function (id) {
        var original_dom = document.getElementById(id)
        original_dom.type = 'hidden'

        var parent_dom = original_dom.parentNode
        var input_dom = document.createElement('div')
        input_dom.id = id + '_date_picker'
        parent_dom.appendChild(input_dom)
        input_dom.className = 'admin_campaigns_date_picker'

        var sendValue = function (date, dateStr) {
          original_dom.value = dateStr
        }

        var date_value = original_dom.value
        var set_date_value = null
        if (date_value !== null && date_value !== '') set_date_value = moment(date_value).toDate()

        var datePickerProps = {
          date: set_date_value,
          sendValue: sendValue
        }

        React.render(React.createElement(DatePicker, datePickerProps), input_dom)
      }

      createControl(start_date_dom_id)
      createControl(end_date_dom_id)
    }
  }
})()

module.exports = CampaignsPage
