var app = angular.module('myApp', []);

app.controller('ImageCtrl', function($scope, $http) {
    $http.get('http://localhost:5000/events/range/2014-09-16/2014-9-17/').
        success(function(data, status) {
		      $scope.images = [];
		      data.results.forEach(function(t) {
            // convert epoch to date here?
			      $scope.images.push(t);
		      });
        });
    });
