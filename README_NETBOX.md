# Netbox README

Netbox requires some passwords, which of course should not be anywhere near a
source code repository. Therefore, by whatever means, assign secrets to the
following environment variables:

- NETBOX_PSQL_PASSWORD, the Postgres password for the Netbox database

