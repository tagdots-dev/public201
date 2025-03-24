import yaml


def update_nested_yaml(file_path, keys, value):
    """
    Updates a nested key in a YAML file.

    Args:
        file_path (str): The path to the YAML file.
        keys (list): A list of keys representing the path to the nested key.
        value: The new value for the nested key.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        # print(data)

    # for key in data['repos']:
    #     print(key['repo'])
    #     print(key['rev'])

    #     if 'python-jsonschema/check-jsonschema' in key['repo'] and '0.31.3' == key['rev']:
    #         key['rev'] = '1.1'

    # # # if 'repos' in data and 'rev' in data['repos'][0]:
    # # #     data['repos'][0]['rev'] = '1.1'

    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, indent=2, sort_keys=False)

    # https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order
    # with open(file_path, 'w', encoding='utf-8') as file:
    #     yaml.dump(data, file, default_flow_style=False, allow_unicode=True, indent=4, sort_keys=False)

    # # Access the nested key and update its value
    # nested_data = data
    # print(type(nested_data))
    # print(nested_data["repos"][0]["repo"])
    # for key in keys:
    #     # print(key)
    #     nested_data = nested_data["repos"][0]["repo"]
    #     print(nested_data)
    # nested_data[keys[-1]] = value

    # # Write the updated data back to the YAML file
    # with open(file_path, 'w') as file:
    #     yaml.dump(data, file, default_flow_style=False)


# Example usage:
file_path = 'pre-root.yaml'
# keys = ['["repos"][0]["repo"]', '["repos"][0]["rev"]']
keys = ['repo', 'rev']
new_rev = '1.1'

update_nested_yaml(file_path, keys, new_rev)


# {
#     'person': {
#         'name': 'Alice',
#         'age': 25
#     }
# }
