(function(){
    var app = angular.module('article_link', ['ui.bootstrap']);

    app.controller("OptionsController", function($scope){
        console.log("OptionsController on");
        $scope.add_article = 0;
        $scope.browse_article = 0;
        $scope.filter_tag = {
            'tag1': {
                'name':'gand',

            },
            'tag2': {
                'name':'my_tag2',
            },
        };
        console.log($scope.filter_tag)


        $scope.selectBrowseArticle = function() {
            $scope.browse_article = 1;
            $scope.add_article = 0;
            console.log("selectBrowsearticle - browse_article is:", $scope.browse_article)
            console.log("selectAddarticle - add_article is:", $scope.add_article)
        };

        $scope.selectAddArticle = function() {
            $scope.add_article = 1;
            $scope.browse_article = 0;
            console.log("selectAddarticle - browse_article is:", $scope.browse_article)
            console.log("selectAddarticle - add_article is:", $scope.add_article)
        };

        $scope.isBrowseArticleSelected = function() {
            return $scope.browse_article === 1
        };

        $scope.isAddArticleSelected = function() {
            return $scope.add_article === 1
        };

        $scope.addFilterTag = function() {
            $scope.filter_tag.push()
        }

    });

    app.controller('FilterController', function($scope) {
        $scope.show_search_text_box = 0;

        $scope.SearchTextBoxSelected = function() {
            if ($scope.show_search_text_box===0) {
                $scope.show_search_text_box = 1;
            // }else {
            //     $scope.show_search_text_box = 1;
            // };
            };
        }

        $scope.isSearchTextBoxToggled = function() {
            return $scope.show_search_text_box === 1
        }

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

})();
