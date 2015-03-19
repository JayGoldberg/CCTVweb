var app = angular.module('myApp', ['ngRoute']);

app.controller('ImageFetch', function($scope, $http, $location, $log) {
    var arg = $location.url().substring(1).split(':')
    $log.debug($location.url().substring(1).split(':'))
    $log.debug('http://localhost:5000/events/range/' + arg[0] + '/' + arg[1] + '/')
    $http.get('http://localhost:5000/events/range/' + arg[0] + '/' + arg[1] + '/').
        success(function(data, status) {
		      $scope.images = [];
		      data.results.forEach(function(t) {
            // convert epoch to date here?
			      $scope.images.push(t);
		      });
        });
    });
    
/*
app.controller('TimeSelector', function($scope, $http) {
  });
*/
