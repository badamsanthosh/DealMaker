#!/usr/bin/env bash

export DJANGO_SETTINGS_MODULE="dealmaker.devel.settings"
export ENV='dev'
export AES_SECRET_KEY='w4G8Y2?:kF7jqgB#testEen9'

# Command Line for Code Coverage Execution

# --- Home Loans
coverage run --source='home_loans' --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini  manage.py test home_loans.test
# --- Meta
coverage run -a --source='meta' --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini  manage.py test meta.test
# --- Lending
coverage run -a --source='lending' --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini  manage.py test lending.test
# --- Third Party
coverage run -a --source='third_party' --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini  manage.py test third_party.test
# --- User Management
coverage run -a --source='user_mgmt' --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini  manage.py test user_mgmt.test

# Command Line for Code Coverage Html Report Generation
coverage html --rcfile /Users/santhoshbadam/Documents/development/dpx-backend-v2/dealmaker/code_coverage/config.ini

# RabbitMq
rabbitmq-server &

# Start Celery Workers
celery --app='dealmaker' worker --loglevel=INFO
