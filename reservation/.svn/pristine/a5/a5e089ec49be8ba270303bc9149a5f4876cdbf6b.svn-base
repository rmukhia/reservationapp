'use strict';

angular.module('ModalModule')
.controller('ModalInstanceCtrl', ['$scope', '$uibModalInstance', 'data',
    'title', 'message', 'show_cancel', 'ok_text', 'cancel_text',
    function ($scope, $uibModalInstance, data, title, message, show_cancel, ok_text, cancel_text) {

    $scope.title = title;
    $scope.message = message;
    $scope.show_cancel = show_cancel;
    $scope.ok_text = ok_text;
    $scope.cancel_text = cancel_text;

    $scope.ok = function () {
        $uibModalInstance.close(data);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}]);
