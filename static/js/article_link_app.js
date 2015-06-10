(function(){
    var app = angular.module('article_link', ['ui.bootstrap']);

    app.controller('FilterController', function($scope, FilterService) {
        $scope.show_search_text_box = 0;
        $scope.articles = {};
        $scope.filter_tag = {
            'tag1': {
                'name':'gand',

            },
            'tag2': {
                'name':'my_tag2',
            },
        };
        console.log($scope.filter_tag)
        
        $scope.getFilteredArticles = function(){
            console.log("Inside get Articles");
            $scope.SearchTextBoxSelected = 0;
            console.log("Before calling service")
            FilterService.getFilteredArticles($scope.filter_tag).then(function(dataResponse){
                console.log("Inside the get function, dataresponse is: ", dataResponse)
                $scope.articles = dataResponse.data.ArticlesList;
            });
            console.log("Here are the articles we recieved: ", $scope.articles)
        };

        $scope.SearchTextBoxSelected = function() {
            if ($scope.show_search_text_box===0) {
                $scope.show_search_text_box = 1;
            // }else {
            //     $scope.show_search_text_box = 0;
            };

        };
    


        $scope.isSearchTextBoxToggled = function() {
            console.log('Inside isSearchTextBoxToggled')
            return $scope.show_search_text_box === 1
        };

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
    // app.controller("OptionsController", function($scope){
    //     console.log("OptionsController on");
    //     $scope.add_article = 0;
    //     $scope.browse_article = 1;
        

    //     $scope.selectBrowseArticle = function() {
    //         $scope.browse_article = 1;
    //         $scope.add_article = 0;
    //         console.log("selectBrowsearticle - browse_article is:", $scope.browse_article)
    //         console.log("selectAddarticle - add_article is:", $scope.add_article)
    //     };

    //     $scope.selectAddArticle = function() {
    //         $scope.add_article = 1;
    //         $scope.browse_article = 0;
    //         console.log("selectAddarticle - browse_article is:", $scope.browse_article)
    //         console.log("selectAddarticle - add_article is:", $scope.add_article)
    //     };

    //     $scope.closeAddArticle = function() {
    //         $scope.add_article = 0;
    //         $scope.browse_article = 0;
    //         console.log("closeAddarticle - browse_article is:", $scope.browse_article)
    //         console.log("closeAddarticle - add_article is:", $scope.add_article)

    //     }

    //     $scope.isBrowseArticleSelected = function() {
    //         return $scope.browse_article === 1
    //     };

    //     $scope.isAddArticleSelected = function() {
    //         return $scope.add_article === 1
    //     };

    //     $scope.addFilterTag = function() {
    //         $scope.filter_tag.push()
    //     }

    // });

})();
