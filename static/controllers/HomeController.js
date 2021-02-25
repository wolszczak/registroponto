var app = angular.module('registro', []);
app.controller('HomeController', function ($scope, $http, $interval) {

    $interval(function () {
        $http.get("/api/list")
            .then(function (response) {
                $scope.lista = response.data;
                console.log($scope.lista)
            });
    }, 2000);


});