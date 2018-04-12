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
        scenario['duration'] = 0
        for step in scenario['steps']:
            # Get the scenario's duration by combining the step duration
            scenario['duration'] += step['result']['duration']
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


def get_slowest_scenario(cucumber_output):
    slowest_scenario = None
    slowest_scenario_duration = 0

    for feature in cucumber_output:
        scenarios = feature['elements']
        for scenario in scenarios:
            if scenario['duration'] > slowest_scenario_duration:
                slowest_scenario = scenario
                slowest_scenario_duration = scenario['duration']

    return slowest_scenario


def prepare_feature_data(cucumber_output):
    all_scenarios_failed = 0
    all_scenarios_passed = 0

    all_features_failed = 0
    all_features_passed = 0

    number_of_features = 0
    number_of_scenarios = 0

    for feature in cucumber_output:
        number_of_features += 1
        number_of_scenarios += len(feature["elements"])

        get_feature_totals(feature)

        all_scenarios_failed += feature["failed"]
        all_scenarios_passed += feature["passed"]

        if feature["failed"]:
            all_features_failed += 1
        else:
            all_features_passed += 1

    data = {
        "cucumber_output": cucumber_output,
        "number_of_features": number_of_features,
        "number_of_scenarios": number_of_scenarios,
        "all_scenarios_failed": all_scenarios_failed,
        "all_scenarios_passed": all_scenarios_passed,
        "all_features_failed": all_features_failed,
        "all_features_passed": all_features_passed,
        "slowest_scenario": get_slowest_scenario(cucumber_output),
    }

    return data
