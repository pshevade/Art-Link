(function(){
    var app = angular.module('article_link', ['ui.bootstrap']);

    app.controller('FilterController', function($scope, FilterService) {
        $scope.show_search_text_box = 0;
        $scope.filter_new = '';
        $scope.filter_tags = [];
        console.log($scope.filter_tags)
        
        $scope.removeTag = function(tag){
            console.log("We want to remove this tag: ", tag)
            var index = $scope.filter_tags.indexOf(tag);
            $scope.filter_tags.splice(index,1)
        }

        $scope.setupFilter = function(){
            console.log("Inside get Articles");
            
            console.log("The new filter is: ", $scope.filter_new)
            console.log("The new filter is present in the current tags? ", $scope.filter_tags.indexOf($scope.filter_new))
            // Push the new filter tag into our array if the user has typed it, and if it doesn't already exist.
            if ($scope.filter_tags.indexOf($scope.filter_new) < 0){
                $scope.filter_tags.push($scope.filter_new)
            }
            $scope.filter_new = '';
            console.log("The filter tags are: ", $scope.filter_tags)
            // console.log("Here are the articles before any call: ", $scope.articles)
            // if ($scope.show_search_text_box ===1){
            //     $scope.SearchTextBoxSelected = 0;
            // }
            // console.log("Before calling service")
            // $scope.SearchTextBoxUnselected();
            $scope.getFilteredArticles();
            // console.log("Here are the articles we recieved: ", $scope.articles)
        };

        $scope.getFilteredArticles = function(){
            FilterService.getFilteredArticles($scope.filter_tags).then(function(dataResponse){
                // console.log("Inside the get function, dataresponse is: ", dataResponse)
                $scope.articles = dataResponse.data.article_display_content_json;
            });
        }

        $scope.SearchTextBoxSelected = function() {
            console.log("In search text box selected")
            if ($scope.show_search_text_box===0) {
                $scope.show_search_text_box = 1;
            // }else {
            //     $scope.show_search_text_box = 0;
            };

        };
    
        $scope.SearchTextBoxUnselected = function() {
            console.log("In search text box UNSelected")
            if ($scope.show_search_text_box ===1) {
                $scope.show_search_text_box = 0;
            };
        }

        $scope.isSearchTextBoxToggled = function() {
            console.log('Inside isSearchTextBoxToggled')
            return $scope.show_search_text_box === 1
        };

        $scope.articles = $scope.getFilteredArticles();

    });

    app.controller('DropdownCtrl', function ($scope, $log) {

        $scope.status = {
            genreisopen: false,
            articleistisopen: false,

        };

        $scope.toggleDropdown = function($event) {
            $event.preventDefault();
            $event.stopPropagation();
            if ($scope.status.genreisopen) {
                $scope.status.genreisopen = !$scope.status.genreisopen;
            };

        };
    });

    app.service("FilterService", function($http){
        console.log("FilterService on")

        this.getFilteredArticles = function(filter_tags){
            console.log("Inside FilterService - getFilteredArticles: filter tags are: ", filter_tags)
            article_url = '/articles/api/json';
            return $http({
                method  : 'GET',
                url     : article_url,
                headers : {'Content-Type': 'application/json'}, 
            });
        };
    });


})();
