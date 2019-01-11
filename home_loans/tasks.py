from __future__ import absolute_import
from celery import shared_task
from django.conf import settings
import os
from third_party.lib import SalesForceHandler


@shared_task
def salesforce_sync(lead_info):
    print(">>>>>>>>>>>> SalesForce Sync: Start <<<<<<<<<<<<<<")
    env = os.environ.get('ENV') or ''
    domain = ''
    if env != 'prod':
        domain = 'test'
    sf_config_path = settings.BASE_DIR+"/third_party/config/"+env+"/salesforce.enc"
    email_cred_path = settings.BASE_DIR+"/third_party/config/"+env+"/email.enc"
    email_config_path = settings.BASE_DIR+"/third_party/config/"+env+"/email.yaml"
    sf_obj = SalesForceHandler(sf_config_path, email_cred_path, email_config_path, domain)
    exec_sync = sf_obj.trigger_sync(lead_info)
    print(">>>> Execution Status: %s" % exec_sync)
    print(">>>>>>>>>>>> SalesForce Sync: End <<<<<<<<<<<<<<")
