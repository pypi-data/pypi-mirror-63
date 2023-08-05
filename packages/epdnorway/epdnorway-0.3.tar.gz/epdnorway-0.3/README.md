# epdnorway

Python module (pypi.org) to consume XML data from https://digi.epd-norge.no/ into any python project.

## Requirements

python v3.7
xmltodict (xmltodict-0.12.0)

## Usage

	pip install epdnorway

Example usage:

		from epdnorway import *
		import pprint as pp

query dataset and show a json list result

		res = epdnorway.list_query("limtre")
		pp.pprint(res)

get a specific dataset, e.g. first of results

		dataset = epdnorway.DataSet(res[0]["uuid"])

To get a list of available Exchange Flows:

		dataset.availableFlows()

Correspondingly, to get available Impact Assessments:

		dataset.availableImpactAssessments()

Data Points are now accessible as `dataset.impactAssessments` and `dataset.exchangeFlows`
Entire dataset is accessible in `dataset.data`

### Possible Datapoints

Handled Datapoints are to be found in the following constants:

		pp.pprint(epdnorway.EXCHANGE_FLOWS)
		pp.pprint(epdnorway.LIFE_CYCLE_METHODS)

Data Points are stored as keys, and values in secondary keys in `amounts`
List possible amounts for modules:

    pp.pprint(epdnorway.KNOWN_MODULES)

### Get specific datapoints

Example: get the numbers for Global warming potential

		>>> gwp = dataset.getImpact("GWP")
		>>> gwp.data
		{'id': '77e416eb-a363-4258-a04e-171d843a6460', 'name': 'Global warming potential', 'meanAmount': '0.0', 'unit': 'kg CO2-Äqv.', 'amounts': {'A1-A3': -679.0}}

get the reference flow of the dataset

		>>> dataset.referenceFlow.data
		{'id': '5ba9fce9-252d-457d-aea8-45d7d4c9a17d', 'name': 'Limtre', 'meanAmount': '1.0', 'resultingAmount': '1.0', 'version': '00.01.000'}

and the units for reference flow (if any):

		>>> dataset.referenceFlow.units
		[{'name': 'bulk density', 'desc': 'kilograms per cubic metre', 'unit': 'kg/m^3', 'value': '430.0'}]
