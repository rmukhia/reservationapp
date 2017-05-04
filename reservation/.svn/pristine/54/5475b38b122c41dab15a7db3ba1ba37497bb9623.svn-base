angular.module('PreferenceModule')
.controller('PreferenceModalInstanceCtrl', ['$scope', '$uibModalInstance', 
    'title', 'message', 'show_cancel',
    function ($scope, $uibModalInstance, title, message, show_cancel) {

    $scope.title = title;
    $scope.message = message;
    $scope.show_cancel = show_cancel;

    $scope.ok = function () {
        $uibModalInstance.close(record_id);
    };

    $scope.cancel = function () {
        $uibModalInstance.dismiss('cancel');
    };
}]);
