angular
	.module('app.dashboard')
	.controller('DeviceDetailController', DeviceDetailController);

DeviceDetailController.$inject = [
	'$scope',
	'app.dashboard.route',
	'localStorage.service',
	'$location',
	'dashboard.service',
	'$routeParams',
	'modal.service',
	'$timeout',
	'utils.service'
];

function DeviceDetailController(
	$scope,
	route,
	localStorage,
	$location,
	dashboardService,
	$routeParams,
	modalService,
	$timeout,
	utils
) {

	$scope.device_key_hash = $routeParams.device_key_hash;

	const getDeviceOverview = async function() {
		try {
			$scope.failed = false;
			
			// TODO: uncomment
			// if (currentDevice.uuid != uuid) {
			// 	console.log('Current device not match', currentDevice, uuid);
			// 	return;
			// }
			
			let { data, headers, status } = await dashboardService.getDeviceOverviews(
				$scope.user.token, $scope.device_key_hash);
			
			$scope.deviceOverview = data;

			$scope.parametersMap = {};
			for (let param of $scope.deviceOverview.device_type.parameters) {
				$scope.parametersMap[param.name] = param;
			}
			
			$scope.$apply();
		} catch (err) {
			console.error(err)
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	};

	$scope.$on('$routeChangeSuccess',function(){
		getDeviceOverview();
	});

	$scope.currentTab = 'overviews';

	$scope.changeTab = function(tab) {
		$scope.currentTab = tab;
    clearInterval($scope.getDataInterval);

		if (tab == 'specifications') {
			$scope.getDeviceSpecs();
		} else if (tab == 'graphs') {
      $scope.getDeviceMonitoringData();
      $scope.getDataInterval = setInterval(() => {
        $scope.getDeviceMonitoringData();
      }, 10000);
		} else if (tab == 'lastest') {
      $scope.getDeviceLastestData();
      $scope.getDataInterval = setInterval(() => {
			  $scope.getDeviceLastestData();
      }, 10000);
		}
	};

	$scope.tabActive = function(tab) {
		return tab == $scope.currentTab ? 'active' : '';
	}

	$scope.getDeviceSpecs = async function() {
		try {
			$scope.failed = false;
			
			// TODO: uncomment
			// if (currentDevice.uuid != uuid) {
			// 	console.log('Current device not match', currentDevice, uuid);
			// 	return;
			// }
			
			let { data, headers, status } = await dashboardService.getDeviceSpecifications(
				$scope.user.token, $scope.device_key_hash);
			
			$scope.deviceSpecs = data;
			$scope.$apply();
		} catch (err) {
			console.error(err)
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	}

	$scope.monitorData = {};

	$scope.getDeviceLastestData = async function() {
		for (let parameter of $scope.deviceOverview.device_type.parameters) {
			getLastestMonitoringDataByParam(parameter);
		}
	}

	async function getLastestMonitoringDataByParam(parameter) {
		try {
			$scope.failed = false;

			let response = await dashboardService.getDeviceMonitorData(
					$scope.user.token, $scope.deviceOverview.device_type.device_type_token,
					$scope.device_key_hash, parameter.name, limit=1);

			$scope.monitorData[parameter.name] = response.data;

			$scope.$apply();
		} catch (err) {
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	}

	$scope.getDeviceMonitoringData = async function() {
		for (let parameter of $scope.deviceOverview.device_type.parameters) {
			getMonitoringDataByParam(parameter);
		}
	}

	async function getMonitoringDataByParam(parameter) {
		try {
			$scope.failed = false;

			let response = await dashboardService.getDeviceMonitorData(
					$scope.user.token, $scope.deviceOverview.device_type.device_type_token,
					$scope.device_key_hash, parameter.name, limit=10000);

			$scope.monitorData[parameter.name] = response.data;

			$scope.$apply();
			drawChart(parameter, $scope.monitorData[parameter.name]);

		} catch (err) {
			let { data, status } = err;
			$scope.failed = true;
			$scope.error = status + ' - ' + data.result;
      $scope.$apply();
		}
	}

	function drawChart(param, data) {
    try {
      //Team chart
      let id = '#line-chart-' + param.name;
	    let lineChartCanvas = $(id).get(0).getContext('2d');

	    data = data.map(item => ({
      	x: new Date(item.timestamp.long),
      	y: item.value
      }));

      let dataset = {
      	label: param.display_name,
      	data,
      	backgroundColor: 'rgba(0,103,255,.15)',
        borderColor: 'rgba(0,103,255,0.5)',
        borderWidth: 1.5,
        pointStyle: 'circle',
        pointRadius: 2,
        pointBorderColor: 'transparent',
        pointBackgroundColor: 'rgba(0,103,255,0.5)',
      };

	    let lineChart = new Chart(lineChartCanvas, {
	    	type: 'line',
	    	data: {
	    		datasets: [dataset]
	    	},
	    	options: {
          responsive: true,
          tooltips: {
            mode: 'index',
            titleFontSize: 12,
            titleFontColor: '#000',
            bodyFontColor: '#000',
            backgroundColor: '#fff',
            titleFontFamily: 'Poppins',
            bodyFontFamily: 'Poppins',
            cornerRadius: 3,
            intersect: false,
          },
          legend: {
            display: false,
            position: 'top',
            labels: {
              usePointStyle: true,
              fontFamily: 'Poppins',
            },


          },
          scales: {
            xAxes: [{
              display: true,
              gridLines: {
                display: false,
                drawBorder: true
              },
              scaleLabel: {
                display: false,
                // labelString: 'Month'
              },
              ticks: {
                fontFamily: "Poppins"
              },
              type: 'time',
              time: {
              	// unit: 'hour'
              }
            }],
            yAxes: [{
              display: true,
              gridLines: {
                display: false,
                drawBorder: true
              },
              scaleLabel: {
                display: true,
                labelString: `Value (${param.unit})`,
                fontFamily: "Poppins"
              },
              ticks: {
                fontFamily: "Poppins",
                suggestedMin: 0,
                suggestedMax: 100
              }
            }]
          },
          title: {
            display: true,
          }
        }
	    });

    } catch (error) {
      console.error(error);
    }
  }
}
