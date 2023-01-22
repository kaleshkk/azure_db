# Databricks notebook source
# Python code to mount and access Azure Data Lake Storage Gen2 Account to Azure Databricks with Service Principal and OAuth
# Author: Dhyanendra Singh Rathore

# Define the variables used for creating connection strings
adlsAccountName = "dlakesnew"
adlsContainerName = "dlakes"
# adlsFolderName = "covid19-data"
mountPoint = "/mnt/dlakes"

# Application (Client) ID
applicationId = dbutils.secrets.get(scope="ADB_access",key="ClientId")

# Application (Client) Secret Key
authenticationKey = dbutils.secrets.get(scope="ADB_access",key="ClientSecretNew")

# Directory (Tenant) ID
tenandId = dbutils.secrets.get(scope="ADB_access",key="tenantID")

endpoint = "https://login.microsoftonline.com/" + tenandId + "/oauth2/token"
source = "abfss://" + adlsContainerName + "@" + adlsAccountName + ".dfs.core.windows.net/" 

# Connecting using Service Principal secrets and OAuth
configs = {"fs.azure.account.auth.type": "OAuth",
           "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
           "fs.azure.account.oauth2.client.id": applicationId,
           "fs.azure.account.oauth2.client.secret": authenticationKey,
           "fs.azure.account.oauth2.client.endpoint": endpoint}

# Mounting ADLS Storage to DBFS
# Mount only if the directory is not already mounted
if not any(mount.mountPoint == mountPoint for mount in dbutils.fs.mounts()):
  dbutils.fs.mount(
    source = source,
    mount_point = mountPoint,
    extra_configs = configs)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/dlakes

# COMMAND ----------

df = spark.read.option("header", "true").csv("/mnt/dlakes/source")
df.show()

# COMMAND ----------


