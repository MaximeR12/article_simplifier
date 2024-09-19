#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo ".env file not found"
    exit 1
fi

# Function to check if logged in
check_login() {
    az account show > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "Not logged in. Please log in to Azure."
        az login
    else
        echo "Already logged in."
    fi
}

# Check login
check_login

# Check if resource group exists, create if it doesn't
if az group show --name $RG_NAME > /dev/null 2>&1; then
    echo "Resource group $RG_NAME already exists."
else
    echo "Creating resource group $RG_NAME..."
    az group create --name $RG_NAME --location $LOCATION
fi

# Check if PostgreSQL server exists
if az postgres flexible-server show --resource-group $RG_NAME --name $DB_SERVER > /dev/null 2>&1; then
    echo "PostgreSQL server $DB_SERVER already exists."
else
    echo "Creating PostgreSQL server..."
    az postgres flexible-server create --resource-group $RG_NAME --name $DB_SERVER --location $LOCATION --admin-user $DB_USER --admin-password $DB_PASSWORD \
                                       --sku-name Standard_B1ms --tier Burstable --storage-type PremiumV2_LRS --storage-size 32 --iops 3000 --throughput 125 --version 12
    
    echo "Waiting for the server to be fully provisioned..."
    sleep 60
fi

# Check if database exists
if az postgres flexible-server db show --resource-group $RG_NAME --server-name $DB_SERVER --database-name $DB_NAME > /dev/null 2>&1; then
    echo "Database $DB_NAME already exists."
else
    echo "Creating database $DB_NAME..."
    az postgres flexible-server db create --resource-group $RG_NAME --server-name $DB_SERVER --database-name $DB_NAME
fi

# Install required Python packages
pip install psycopg2-binary python-dotenv

# Run the Python script to create tables
echo "Running table creation script..."
python3 tables_creation.py

echo "Database and tables setup completed."

