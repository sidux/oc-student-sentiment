from opencensus.ext.azure.log_exporter import AzureLogHandler
import logging

logging.basicConfig(level=logging.DEBUG)

# Replace this with your actual connection string
CONNECTION_STRING = "InstrumentationKey=6a2b4e80-2fe3-4797-a04b-0d4bc7eb360a;IngestionEndpoint=https://westeurope-5.in.applicationinsights.azure.com/;LiveEndpoint=https://westeurope.livediagnostics.monitor.azure.com/;ApplicationId=dea423d0-5308-4147-b2ac-5545e9b895ef"

logger = logging.getLogger(__name__)
logger.addHandler(AzureLogHandler(connection_string=CONNECTION_STRING))
logger.setLevel(logging.INFO)

# Send a test log
logger.info("Test log from local app")

print("Log sent!")