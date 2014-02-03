(function (angular) {
    'use strict';
    
    var eric = angular.module('eric', []);
    
    eric.controller('CurrentInviteController', function ($scope, $element, $http) {
        var invite = JSON.parse($element.attr('data-invite'));
        var update_url = $element.attr('data-update-url');
        var csrf_token = $element.attr('data-csrf-token');
        
        $scope.invite = invite;
        $scope.invitees = invite.invitees;
        $scope.is_replying = false;
        $scope.start_replying = function () {
            $scope.is_replying = true;
        };
        $scope.stop_replying = function () {
            $scope.is_replying = false;
        };
        
        $scope.options = [
            {value: null, label: 'Undecided'},
            {value: true, label: "I'd love to come"},
            {value: false, label: "Can't make it"},
        ];
        
        $scope.update_invitee = function (invitee) {
            var post_data = angular.copy(invitee);
            try {
                post_data.is_attending = JSON.parse(post_data.is_attending);
            } catch (e) {
                post_data.is_attending = null;
            }
            
            $scope.is_saving = true;
            $http.defaults.headers.post["X-CSRFToken"] = csrf_token;
            $http.post(update_url, post_data).then(function (response) {
                $scope.is_saving = false;
                $scope.invite.is_complete = response.data.is_invite_complete;
            });
        };
    });
    
})(window.angular);