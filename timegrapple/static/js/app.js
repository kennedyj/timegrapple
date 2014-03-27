angular.module('timegrapple', ['ngRoute'])

.config(function($routeProvider) {
  $routeProvider
    .when('/', {
      controller: 'grapple',
      templateUrl: '/static/views/sheet.html'
    })
    .when('/for/:dateId', {
      controller: 'grapple',
      templateUrl: '/static/views/sheet.html'
    })
    .otherwise({
      redirectTo:'/'
    });
})

.controller('grapple', function($scope, $http, $routeParams) {
  $scope.data = {};

  $scope.load = function(when) {
    if (when === undefined) {
      $http.get('/sheets/').then(function (r) {
        $scope.data = r.data;
      });
    }
    else {
      $http.get('/sheets/' + when).then(function (r) {
        $scope.data = r.data;
      });
    }
  };

  $scope.load($routeParams.dateId);

  $scope.prev = function() {
  }

  $scope.next = function() {
  }

  $scope.save = function() {
    $http.post('/sheets/' + $scope.data.id, $scope.data).success(function() {
      console.log('woo');
    }).error(function() {
      console.log('boo');
    });
  }
});
