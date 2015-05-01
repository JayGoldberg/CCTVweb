var app = angular.module('myApp', ['ngRoute','ui.bootstrap']);

app.controller('EventGetter', function($scope, $http, $log) {
  
  $scope.today = function() {
    $scope.dt = new Date(); // set default date here? First day camera is active?
  };
  //$scope.today(); // unfortunately clears the scope every time something is triggered

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
  
  //$scope.starttime = $scope.dt;
  //$scope.endtime = $scope.dt;

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
/*
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
*/
  $scope.timechanged = function () {
    $log.log('Times changed to: ' + $scope.starttime + ' and ' + $scope.endtime);
    
    var dataObj = {
      group : $scope.group,
      dwell_time_secs : $scope.dwell_time_secs,
      sloppy_results : $scope.sloppy_results,
      cam_name: $scope.cam_name
      };

    $http.post('http://<your_flask_backend>:5000/events/range/' + $scope.cam_name + '/' + $scope.starttime.getTime() + '/' + $scope.endtime.getTime() + '/', dataObj).
      success(function(data, status) {
        $scope.resultcount = data.resultcount;
        
        if (data.resultcount > 0 && $scope.group) { // fill events table
          $scope.events = [];
          $scope.images = [];
          data.result.forEach(function(t) {
            $scope.events.push(t);
          });
        } else {
          if (data.resultcount == 0 && $scope.group) { // clear the events table
            $scope.events = []; 
          } else {
              if (data.resultcount > 0) { // fill the images table
                $scope.est_size = data.est_size;
                $scope.events = [];
                $scope.images = [];
                  data.result.forEach(function(t) {
                    $scope.images.push(t);
                  });
              } else { // clear the images table
                  $scope.images = [];
                }
            } 
          }
        });
  };
  
  $scope.datechanged = function () {
    $scope.starttime = $scope.dt;
    $log.log($scope.starttime.getTime());
    $scope.endtime = $scope.dt;
    $log.log($scope.endtime.getTime());
  };
  
  $scope.clear = function() {
    $scope.starttime = null;
    $scope.endtime = null;
  };
});
