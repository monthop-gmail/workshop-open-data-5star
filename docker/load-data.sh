#!/bin/bash
# Script to load RDF data into Fuseki SPARQL endpoint

FUSEKI_URL="http://fuseki:3030"
DATASET="energy"
DATA_FILE="/data/energy_stats_2566.ttl"

echo "==================================="
echo "Loading RDF data into Fuseki"
echo "==================================="

# Wait for Fuseki to be ready
echo "Waiting for Fuseki to start..."
until curl -s -f "$FUSEKI_URL/\$/ping" > /dev/null 2>&1; do
    echo "  Fuseki not ready yet, waiting..."
    sleep 5
done
echo "Fuseki is ready!"

# Check if dataset exists
echo "Checking if dataset '$DATASET' exists..."
DATASET_EXISTS=$(curl -s -o /dev/null -w "%{http_code}" "$FUSEKI_URL/$DATASET")

if [ "$DATASET_EXISTS" = "200" ]; then
    echo "Dataset '$DATASET' already exists"
else
    # Create dataset
    echo "Creating dataset '$DATASET'..."
    curl -s -X POST "$FUSEKI_URL/\$/datasets" \
        -u admin:admin123 \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "dbName=$DATASET&dbType=tdb2"

    if [ $? -eq 0 ]; then
        echo "Dataset created successfully!"
    else
        echo "Failed to create dataset"
        exit 1
    fi
fi

# Load data
echo "Loading data from $DATA_FILE..."
if [ -f "$DATA_FILE" ]; then
    curl -s -X POST "$FUSEKI_URL/$DATASET/data" \
        -u admin:admin123 \
        -H "Content-Type: text/turtle" \
        --data-binary "@$DATA_FILE"

    if [ $? -eq 0 ]; then
        echo "Data loaded successfully!"
    else
        echo "Failed to load data"
        exit 1
    fi
else
    echo "Data file not found: $DATA_FILE"
    exit 1
fi

# Verify data
echo ""
echo "Verifying data..."
QUERY="SELECT (COUNT(*) as ?count) WHERE { ?s ?p ?o }"
RESULT=$(curl -s -X POST "$FUSEKI_URL/$DATASET/sparql" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Accept: application/json" \
    -d "query=$QUERY")

echo "Query result: $RESULT"
echo ""
echo "==================================="
echo "Data loading complete!"
echo "SPARQL endpoint: $FUSEKI_URL/$DATASET/sparql"
echo "SPARQL UI: $FUSEKI_URL/#/dataset/$DATASET/query"
echo "==================================="
