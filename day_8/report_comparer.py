import json
import yaml
import xmltodict

def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return None

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading YAML: {e}")
        return None

def load_xml(file_path):
    try:
        with open(file_path, 'r') as f:
            xml_content = f.read()
            return xmltodict.parse(xml_content)
    except Exception as e:
        print(f"Error loading XML: {e}")
        return None

def compare_reports(json_dict, yaml_dict, xml_dict):
    if json_dict is None or yaml_dict is None or xml_dict is None:
        print("One or more files could not be loaded.")
        return False
    
    # Extract the inner dict from XML since it has a "scan_result" wrapper
    xml_inner = xml_dict.get("scan_result")
    
    if json_dict == yaml_dict == xml_inner:
        print("All reports match!")
        return True
    else:
        print("Reports do not match!")
        return False

if __name__ == "__main__": 
    json_file = 'raw_ping_reports/scan_results.json'
    yaml_file = 'raw_ping_reports/scan_results.yaml'
    xml_file = 'raw_ping_reports/scan_results.xml'
    
    json_dict = load_json(json_file)
    yaml_dict = load_yaml(yaml_file)
    xml_dict = load_xml(xml_file)
    
    compare_reports(json_dict, yaml_dict, xml_dict)