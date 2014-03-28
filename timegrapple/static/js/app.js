angular.module('timegrapple', ['ngRoute', 'ui.bootstrap'])

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

.controller('grapple', function($scope, $http, $location, $routeParams, $rootScope) {
  $scope.data = {};
  $scope.saving = false;
  $scope.saved = false;
  $scope.saveFailed = false;

  $rootScope.dateToString = function(d) {
    if (d instanceof Date) {
      return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    }
    else {
      return d;
    }
  }

  $rootScope.datesEqual = function(oldDate, newDate) {
    oldDate = $rootScope.dateToString(oldDate);
    newDate = $rootScope.dateToString(newDate);

    if (newDate == oldDate) {
      return true;
    }
    else {
      return false;
    }
  };

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

  $scope.$watch('data', function() {
    if ($scope.data.id !== undefined) {
      $rootScope.dataDate = new Date($scope.data.id + ' 17:00:00 GMT-0700')
    }
  });

  $rootScope.$watch('pickerDate', function(newDate, oldDate) {
    if (!$rootScope.datesEqual($rootScope.dataDate, newDate)) {
      $location.path('/for/' + $rootScope.dateToString(newDate));
    }
  });

  $scope.load($routeParams.dateId);

  $scope.save = function() {
    $scope.saved = false;
    $scope.saving = true;
    $scope.saveFailed = false;

    $http.post('/sheets/' + $scope.data.id, $scope.data).success(function() {
      $scope.saved = true;
      $scope.saving = false;
      $scope.saveFailed = false;
    }).error(function() {
      $scope.saved = false;
      $scope.saving = false;
      $scope.saveFailed = true;
    });
  }
})

.controller('weekmgr', function($scope, $http, $rootScope) {
  $rootScope.$watch('dataDate', function(newDate, oldDate) {
    if (newDate instanceof Date) {
      $scope.selectedDate = newDate;
    }
  });
  $scope.$watch('selectedDate', function(newDate, oldDate) {
    if (newDate != null) {
      $rootScope.pickerDate = $rootScope.dateToString(newDate);
    }
  });
});
