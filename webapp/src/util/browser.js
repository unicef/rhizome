/* global window */

'use strict'

export default {
  isIE: function () {
    return ('ActiveXObject' in window)
  }
}
