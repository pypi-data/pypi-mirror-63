import os
from sauceclient import SauceClient
from robot.libraries.BuiltIn import BuiltIn

username = 'solitea123'
access_key = '54ef43ce-9360-42b3-a2ac-592110227c01'

sauce_client = SauceClient(username, access_key)

def report_sauce_status(name, status):
    selenium = BuiltIn().get_library_instance('AppiumLibrary')
    job_id = selenium._current_application().session_id
    passed = status == 'PASS'
    sauce_client.jobs.update_job(job_id, passed = passed)
    print("SauceOnDemandSessionID=%s job-name=%s" % (job_id, name))