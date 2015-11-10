/* global window */

'use strict'

module.exports = {
    isIE: function () {
        return ('ActiveXObject' in window)
    }

}
