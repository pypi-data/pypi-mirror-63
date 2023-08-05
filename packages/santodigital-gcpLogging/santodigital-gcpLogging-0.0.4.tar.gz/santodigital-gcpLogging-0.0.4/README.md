# GCP LOGGING MANAGER

This is a simple gcp logging package where you can easily write logs to gcp stackdriver with custom parameters.

# Required library 
pip install --upgrade google-cloud-logging  

# Setting up authentication
1. In the Cloud Console, go to the Create service account key page.  
2. From the Service account list, select New service account.  
3. In the Service account name field, enter a name.  
4. From the Role list, select Project > Owner.  



# GCP Stackdriver matrics
param type: Resource type to filter in Stackdriver Logging (required)  
param service: Service name to filter in Stackdriver Logging (required)  
param log_name: Log Name to filter in Stackdriver Logging  
param region: GCP Service Region to filter in Stackdriver Logging (optional) default value region='us-east1'  

# Sample code 

```python
from  santodigital_gcpLogging import CloudRunLoggingClient

# Resouce must match with strackdriver resource.type (cloud_run_revision or bigquery_resource etc)
resource = 'cloud_run_revision'
name = 'santodigital-gcpLogging'
SERVICE = 'santodigital-gcpLogging'
logger = CloudRunLoggingClient(resource, SERVICE, name)

"""
:param struct: (Dict) Custom information for logging into Stackdriver Logging.
:param severity: Severity Level for the logging.
"""
def report(struct, severity='INFO'):
    logger.report(struct, severity)
    return True

if __name__ == '__main__':
    print(report({'info':'success'}, 'WARNING'))

```




