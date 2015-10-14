'use strict';

var Reflux = require('reflux');

module.exports = Reflux.createActions([
    "currentIndicatorPromise",
    "initialize",
    "baseFormSave",
    "addTagToIndicator",
    "removeTagFromIndicator",
    "addIndicatorCalc",
    "getTagTree",
    "initIndicatorToTag",
    "initIndicatorToCalc"
]);
