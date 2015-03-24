var app = angular.module('myApp', ['ngRoute','ui.bootstrap']);

app.controller('EventGetter', function($scope, $http, $location, $log) {
  var arg = $location.url().substring(1).split(':')
  
  $scope.today = function() {
  $scope.dt = new Date();
  };
  $scope.today();

  $scope.clear = function () {
    $scope.dt = null;
  };

  // Disable weekend selection
  $scope.disabled = function(date, mode) {
    return ( mode === 'day' && ( date.getDay() === 0 || date.getDay() === 6 ) );
  };
/*
  $scope.toggleMin = function() {
    // here we can limit selection to days where camera has data
    $scope.minDate = $scope.minDate ? null : new Date();
  };
  $scope.toggleMin();
*/
  $scope.open = function($event) {
    $event.preventDefault();
    $event.stopPropagation();

    $scope.opened = true;
  };

  $scope.dateOptions = {
    formatYear: 'yy',
    startingDay: 1,
    minDate: null
  };

  $scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
  $scope.format = $scope.formats[0];
  
  $scope.starttime = $scope.dt;
  $scope.endtime = $scope.dt;

  $scope.hstep = 1;
  $scope.mstep = 15;

  $scope.options = {
    hstep: [1, 2, 3],
    mstep: [1, 5, 10, 15, 25, 30]
  };

  $scope.ismeridian = true;
  $scope.toggleMode = function() {
    $scope.ismeridian = ! $scope.ismeridian;
  };

  $scope.update = function() {
    var sunrise = new Date();
    var sunset = new Date();
    sunrise.setHours( 7 );
    sunrise.setMinutes( 0 );
    sunset.setHours( 19 );
    sunset.setMinutes( 0 );
    $scope.starttime = sunrise;
    $scope.endtime = sunset;
  };

  $scope.timechanged = function () {
    $log.log('Times changed to: ' + $scope.starttime + ' and ' + $scope.endtime);
    $http.post('http://localhost:5000/events/range/' + $scope.starttime.getTime() + '/' + $scope.endtime.getTime() + '/').
      success(function(data, status) {
        $scope.images = [];
        data.results.forEach(function(t) {
          $scope.images.push(t);
        });
      });
  };
  
  $scope.datechanged = function () {
    $log.log($scope.dt.getFullYear());
    $scope.starttime.setFullYear($scope.dt.getFullYear());
    $scope.starttime.setMonth($scope.dt.getMonth());
    $scope.starttime.setDate($scope.dt.getDate());
    $scope.endtime.setFullYear($scope.dt.getFullYear());
    $scope.endtime.setMonth($scope.dt.getMonth());
    $scope.endtime.setDate($scope.dt.getDate());
    $log.log('Times changed to: ' + $scope.starttime + ' and ' + $scope.endtime);
  };
  
  $scope.clear = function() {
    $scope.starttime = null;
    $scope.endtime = null;
  };
});
