CREATE TYPE package_status AS ENUM (
	'created',
	'picked_up',
	'at_warehouse',
	'out_for_delivery',
	'delivered',
	'cancelled'
);