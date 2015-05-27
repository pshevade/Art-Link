(function(){
    var app = angular.module('art_link', ['ui.bootstrap']);

    app.controller("OptionsController", function($scope){
        console.log("OptionsController on");
        $scope.add_art = 0;
        $scope.browse_art = 0;

        $scope.selectBrowseArt = function() {
            $scope.browse_art = 1;
            $scope.add_art = 0;
            console.log("selectBrowseArt - browse_art is:", $scope.browse_art)
            console.log("selectAddArt - add_art is:", $scope.add_art)
        };

        $scope.selectAddArt = function() {
            $scope.add_art = 1;
            $scope.browse_art = 0;
            console.log("selectAddArt - browse_art is:", $scope.browse_art)
            console.log("selectAddArt - add_art is:", $scope.add_art)
        };

        $scope.isBrowseArtSelected = function() {
            return $scope.browse_art === 1
        };

        $scope.isAddArtSelected = function() {
            return $scope.add_art === 1
        };

    });

    app.controller('DropdownCtrl', function ($scope, $log) {

        $scope.status = {
            genreisopen: false,
            artistisopen: false,

        };

        $scope.toggleDropdown = function($event) {
            $event.preventDefault();
            $event.stopPropagation();
            if ($scope.status.genreisopen) {
                $scope.status.genreisopen = !$scope.status.genreisopen;
            };
            if ($scope.status.artistisopen) {
                $scope.status.artistisopen = !$scope.status.artistisopen;
            };
        };
    });

})();
