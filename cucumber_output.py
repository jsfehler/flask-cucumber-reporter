def get_feature_totals(feature):
    """Scan an individual feature, looking for any failured steps.
    If none are found, assume the scenario passed.

    Returns:
        dict
    """
    scenarios_failed = 0
    scenarios_passed = 0

    scenarios = feature['elements']

    for scenario in scenarios:
        for step in scenario['steps']:
            if step['result']['status'] == 'failed':
                scenarios_failed += 1
                scenario['status'] = 'failed'
                break
        else:
            scenarios_passed += 1
            scenario['status'] = 'passed'

    feature['passed'] = scenarios_passed
    feature['failed'] = scenarios_failed
    if scenarios_failed == 0:
        feature['status'] = 'passed'
    else:
        feature['status'] = 'failed'

    feature["percentage_status"] = (scenarios_passed / len(scenarios)) * 100

    return feature


def prepare_feature_data(cucumber_output):
    all_scenarios_failed = 0
    all_scenarios_passed = 0

    all_features_failed = 0
    all_features_passed = 0

    for feature in cucumber_output:
        get_feature_totals(feature)
        all_scenarios_failed += feature["failed"]
        all_scenarios_passed += feature["passed"]
        if feature["failed"]:
            all_features_failed += 1
        else:
            all_features_passed += 1

    data = {
        "cucumber_output": cucumber_output,
        "all_scenarios_failed": all_scenarios_failed,
        "all_scenarios_passed": all_scenarios_passed,
        "all_features_failed": all_features_failed,
        "all_features_passed": all_features_passed
    }

    return data
