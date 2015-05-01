var app = angular.module('cctv-player', ['ngRoute']);

app.controller('Player', function($scope, $http, $location, $log, $window) {
  var arg = [];
  arg = $location.url().split("/");
  $scope.images = [];
  
  $scope.init = function () {
    $http.get('http://<your_flask_backend>:5000/events/range/' + arg[1] + '/' + arg[2] + '/' + arg[3] + '/').
      success(function(data, status) {
        $scope.resultcount = data.resultcount;
        $scope.imgbase = data.imgbase;
          if (data.resultcount > 0) {
            $scope.est_size = data.est_size;
              data.result.forEach(function(t) {
                $scope.images.push($scope.imgbase + t.path);
              });
        };
        Sequencer.init($scope.images);
      });
      
  };
  
  $scope.eventDelete = function () {
    /*var dataObj = {
      cam_name: arg[1],
      start_time: arg[2],
      end_time: arg[3]
      }; */
    $http.delete('http://<your_flask_backend>:5000/events/range/' + arg[1] + '/' + arg[2] + '/' + arg[3] + '/').
      success(function(data, status) {
        $log.log("Deleted");
      });
      
  };
});

/*
app.directive('newPlayer', function () {
return {
    restrict: 'E',
    require: 'ngModel',
    link: function(scope, element, attr) {
      var scr = document.createElement('script');
      var text = document.createTextNode('Sequencer(' + scope.images + ')');
      scr.appendChild(text);
      element.appendChild(scr);
    }
  };
});
*/

/*
 * module.directive('exampleBindLeet', function () {
return {
        link: link
    };
});

function link($scope, $elem, attrs) {
    function updateProgress() {
        var percentValue = Math.round($scope.value / $scope.max * 100);
        $scope.percentValue = Math.min(Math.max(percentValue, 0), 100);
        $elem.children()[0].style.width = $scope.percentValue + '%';
    }
}*/

/*
app.run(function() {
    Sequencer.init({{ images }})
});
*/
