@echo off
echo "Building Python image..."
docker build -t ez-dash/python .\python
echo "Building MetricBeat image..."
docker build -t ez-dash/metricbeat .\metricbeat
echo "Done!"
