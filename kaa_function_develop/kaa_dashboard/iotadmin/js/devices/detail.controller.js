angular
	.module('app.devices.detail')
	.controller('DeviceDetailController', DeviceDetailController);

DeviceDetailController.$inject = [
	'app.devices.service',
	'$scope',
	'$routeParams'
];

function DeviceDetailController(deviceService, $scope, $routeParams) {
	
	$scope.deviceKeyHash = $routeParams.id;
	$scope.monitorData = {};

	$scope.init = function() {
		$scope.loadDataInterval = setInterval(() => {
			getDeviceDetail();
		}, 10000);
	}

	async function getDeviceDetail() {
		let id = $scope.deviceKeyHash;
		let device = await deviceService.showDevice(id);
		if (!device) throw new Error(`Device ID ${id} not found`);

		$scope.device = device;
		$scope.parametersMap = {};
		for (let param of device.parameters) {
			$scope.parametersMap[param.name] = param;
		}
		$scope.$apply();

		getDeviceMonitoringData(device);
	}

	function getDeviceMonitoringData(device) {
		for (let parameter of device.parameters) {
			getMonitoringDataByParam(device, parameter);
		}
	}

	async function getMonitoringDataByParam(device, parameter) {
		$scope.monitorData[parameter.name] = await deviceService.getMonitoringData(device.device_type_id,
				$scope.deviceKeyHash, parameter.name);
		$scope.$apply();


		drawChart(parameter, $scope.monitorData[parameter.name]);
	}

	$scope.init();

	$scope.capitalizeSpec = function(spec) {
		spec = spec.split('_').join(' ');
		return spec[0].toUpperCase() + spec.substr(1).toLowerCase();;
	}

	function drawChart(param, data) {
    try {
      //Team chart
      let id = 'team-chart-' + param.name;
      let ctx = document.getElementById(id);
      if (ctx) {
        ctx.height = 200;

        data = data.map(item => ({
        	x: new Date(item.timestamp.long),
        	y: item.value
        }));

        let myChart = new Chart(ctx, {
          type: 'line',
          data: {
            type: 'line',
            defaultFontFamily: 'Poppins',
            datasets: [{
              data: data,
              label: param.display_name,
              backgroundColor: 'rgba(0,103,255,.15)',
              borderColor: 'rgba(0,103,255,0.5)',
              borderWidth: 1.5,
              pointStyle: 'circle',
              pointRadius: 2,
              pointBorderColor: 'transparent',
              pointBackgroundColor: 'rgba(0,103,255,0.5)',
            },]
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
                  drawBorder: false
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
                  drawBorder: false
                },
                scaleLabel: {
                  display: true,
                  labelString: `Value (${param.unit})`,
                  fontFamily: "Poppins"
                },
                ticks: {
                  fontFamily: "Poppins"
                }
              }]
            },
            title: {
              display: true,
            }
          }
        });
      }

    } catch (error) {
      console.log(error);
    }
  }
}