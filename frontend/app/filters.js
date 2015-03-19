var filters = angular.module('myAppFilters', []).filter('dateFilter', function() {
  return function(input) {
    return input ? '\u2713' : '\u2718';
  };
});
