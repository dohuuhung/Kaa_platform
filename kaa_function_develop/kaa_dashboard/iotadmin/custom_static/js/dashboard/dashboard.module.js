const route = {
	USERS: 'users',
	DEVICES: 'devices',
	DEVICE_TYPES: 'device_types',
	IP_CAMERAS: 'ip_cameras',
	KOA_GATEWAY: 'koa_gateway'
};

angular
	.module('app.dashboard', [		
	])
	.constant('app.dashboard.route', route)
	.config(config)
	.run(run);

config.$inject = []

function config() {
}

run.$inject = [];

function run() {
}
