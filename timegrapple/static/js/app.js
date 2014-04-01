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

.factory('util', function() {
  return {
    dateToString: function(d) {
      if (d instanceof Date) {
        return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
      }
      else {
        return d;
      }
    },

    datesEqual: function(oldDate, newDate) {
      oldDate = this.dateToString(oldDate);
      newDate = this.dateToString(newDate);

      if (newDate == oldDate) {
        return true;
      }
      else {
        return false;
      }
    }
  };
})

.controller('grapple', function($scope, $http, $location, $routeParams, $rootScope, util) {
  $scope.data = {};
  $scope.saving = false;
  $scope.saved = false;
  $scope.saveFailed = false;

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
    if (!util.datesEqual($rootScope.dataDate, newDate)) {
      $location.path('/for/' + util.dateToString(newDate));
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
    }).error(function(data, status, headers, config) {
      $scope.saved = false;
      $scope.saving = false;
      $scope.saveFailed = true;
      console.log(status, data);
    });
  }
})

.controller('weekmgr', function($scope, $http, $rootScope, util) {
  $rootScope.$watch('dataDate', function(newDate, oldDate) {
    if (newDate instanceof Date) {
      $scope.selectedDate = newDate;
    }
  });
  $scope.$watch('selectedDate', function(newDate, oldDate) {
    if (newDate != null) {
      $rootScope.pickerDate = util.dateToString(newDate);
    }
  });
});
