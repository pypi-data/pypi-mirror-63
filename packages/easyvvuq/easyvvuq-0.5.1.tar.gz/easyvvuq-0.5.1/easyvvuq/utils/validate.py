def convert_params(param_desc, params):
    for key in param_desc:
        if param_desc[key]['type'] == 'float':
            params[key] = float(params[key])
        elif param_desc[key]['type'] == 'integer':
            params[key] = int(params[key])
        else:
            raise ValueError("This type is not supported", param_desc[key]['type'])
