"""
General.Conversion

This module contains functions for converting data types.

This module should not have any dependencies on any other Ignition modules.
"""
import re
import collections

LOGGER = system.util.getLogger("General.Conversion")

def convert_dataset_to_list(dataset):
	"""
	DESCRIPTION: This function converts a dataset to a list of dictionaries 
	PARAMETERS: dataset (REQ, dataset): The dataset to be converted to a list of dictionaries
	RETURNS: list (list): The list of dictionaries
	"""
	LOGGER.trace("convert_dataset_to_list(dataset=%s)" % (dataset))
	if dataset is None:
		return dataset
	if isinstance(dataset, collections.Iterable):
		return dataset
	if isinstance(dataset, (int, long)):
		return dataset
	if isinstance(dataset, str):
		return dataset

	column_names = dataset.getColumnNames()

	data = []
	
	for row in range(dataset.getRowCount()):
		row_data = {}
		for column in range(dataset.getColumnCount()):
			row_data[column_names[column]] = dataset.getValueAt(row, column)
		data.append(row_data)
	return data

def convert_list_to_dataset(list_var, titalize_headers=False, column_order=None, headers_list=None):
	"""
	DESCRIPTION: This function converts list of dictionaries to a dataset
	PARAMETERS: list_var (REQ, list): The list of dictionaries to be converted
				titalize_headers (OPT, bool): True in the case of the ability to get the names of the header in list_var
				column_order (OPT, list): The order of the columns in the dataset
				headers_list (OPT, list): The list of headers to be used in the dataset
	RETURNS: dataset (dataset): The dataset created from the list of dictionaries
	"""
	LOGGER.trace("convert_list_to_dataset(list_var=%s)" % (list_var))
	if not isinstance(list_var, collections.Iterable):
		return list_var

	if headers_list is not None:
		headers = column_names = headers_list
	elif column_order is not None:
		headers = column_names = column_order
	else:
		headers = column_names = list_var[0].keys()
			
	if titalize_headers:
		headers = [name.title() for name in column_names]
		
	
	data = []
	
	for row in list_var:
		row_data = []
		for column in column_names:
			# NOTE: Check to see if key value has a value with styling applied, and only return the value
			if hasattr(row[column], 'value') and hasattr(row[column], 'style'):
				value = str(row[column]['value']) if row[column]['value'] is not None else None
			else:
				value = str(row[column]) if row[column] is not None else None
			row_data.append(value)
		data.append(row_data)
	return system.dataset.toDataSet(headers, data)

def convert_properties_to_dictionary(obj):
	"""
	DESCRIPTION: Converts properties from the view into a dictionary, if possible
	PARAMETERS: obj (REQ, object): The properties to be converted
	RETURNS: dict (dict): The dictionary of the properties
	"""
	LOGGER.trace("convert_properties_to_dictionary(obj=%s)" % (obj))

	if obj is None:
		return None

	# NOTE: If this is a basic qualified value, and not a dictionary with the key 'value', 
	# then replace the object with its value
	if hasattr(obj, 'value') and not hasattr(obj, 'keys'):
		obj = obj.value

	# NOTE: Then check for any kind of dictionary or list
	if hasattr(obj, '__iter__'):
		if hasattr(obj, 'keys'):
			return dict((k, convert_properties_to_dictionary(obj[k])) for k in obj.keys())
		else:
			return list(convert_properties_to_dictionary(x) for x in obj)
	else:
		# anything else
		return obj
	
def convert_from_camel_case_to_caps(string):
	"""
	DESCRIPTION: Converts a string from camel case to all caps
	PARAMETERS: string (REQ, string): The string to be converted
	RETURNS: string (string): The converted string to all caps
	"""
	LOGGER.trace("convert_from_camel_case_to_caps(string=%s)" % (string))
	return re.sub("([a-z])([A-Z])", r"\g<1> \g<2>", string).capitalize()

def convert_snake_case_to_camel_case(string):	
	"""
	DESCRIPTION: Converts a string from snake case (standard within scripts) to camel case (standard within Ignition props)
	PARAMETERS: string (REQ, string): The string to be converted
	RETURNS: string (string): The converted string to camel case
	"""
	string = "".join(char.capitalize() for char in string.lower().split("_"))
	return string[0].lower() + string[1:]
	
def convert_list_to_dropdown(options):
	"""
	DESCRIPTION: Creates a list of dictionaries for each object to allow for a dropdown option
	PARAMETERS: options (REQ, list): The list of values possible for a drop down
	RETURNS: list (list): The list of dictionaries for the dropdown
	"""
	LOGGER.trace("convert_list_to_dropdown(options=%s)" % (options))
	dropdown_options = []
	for option in options:
		if isinstance(option, basestring):
			dropdown_options.append({"label": option, "value": option})
		elif isinstance(option, collections.Mapping):
			dropdown_options.append(option)
	return dropdown_options

def convert_dict_to_dropdown(options):
	"""
	DESCRIPTION: Creates a list of dictionaries for a dropdown from a dictionary
	PARAMETERS: options (REQ, dict): The dictionary to be converted (key is the label, value is the value)
	RETURNS: list (list): The list of dictionaries for the dropdown
	"""
	LOGGER.trace("convert_dict_to_dropdown(options=%s)" % (options))
	dropdown_options = []
	for key in options.keys():
		dropdown_options = [{"label": val, "value": key} for key, val in options.iteritems()]
	return sorted(dropdown_options, key=lambda opt: opt['value'])

def convert_seconds_to_str_format(seconds):
	"""
	DESCRIPTION: Converts seconds to a string in the format of HH:MM:SS
	PARAMETERS: seconds(str) - The number of seconds to convert
	RETURNS: A string in the format of HH:MM:SS
	"""
	LOGGER.trace("convert_str_to_seconds(seconds=%s)" % (seconds))
	seconds = seconds % (24 * 3600)
	hour = seconds // 3600
	seconds %= 3600
	minutes = seconds // 60
	seconds %= 60
	return "%d:%02d:%02d" % (hour, minutes, seconds)
