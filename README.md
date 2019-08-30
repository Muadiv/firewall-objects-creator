Small script with interface to create objects for firewalls (like hosts, groups, etc). The idea is to avoid loosing time when create hundred of objects, also avoid human errors. The script is checking if the list of IP is correct, and if there is any error, is showing wich ones are not correct. Also is showing duplicates.

The main idea behind this is this must be really friendly to use. I started this project because others that I saw take more time to learn to use it than create 1000 objects manually.

The initial script will create objects for Cisco and Fortigate devices:

Cisco:

    hosts
    networks
    add previous objects to a group

Fortigate (also NBF's)

    hosts
    networks
    add previous objects to a group

For next releases:

    add ranges
    who know?...
