import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_loaded_entities


parameterize_creator = pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(
            e.application_1.get("colocated_db"),
            [
                {
                    "Name": "model1",
                    "Type": "DB Model",
                    "Backend": "model1_tf",
                    "Device": "model1_cpu",
                },
                {
                    "Name": "model2",
                    "Type": "DB Model",
                    "Backend": "model2_tf",
                    "Device": "model2_cpu",
                },
                {
                    "Name": "script1",
                    "Type": "DB Script",
                    "Backend": "script1_torch",
                    "Device": "script1_cpu",
                },
                {
                    "Name": "script2",
                    "Type": "DB Script",
                    "Backend": "script2_torch",
                    "Device": "script2_gpu",
                },
            ],
        ),
        pytest.param(
            e.application_2.get("colocated_db"),
            [
                {
                    "Name": "model1",
                    "Type": "DB Model",
                    "Backend": "model1_tf",
                    "Device": "model1_cpu",
                },
                {
                    "Name": "model2",
                    "Type": "DB Model",
                    "Backend": "model2_tf",
                    "Device": "model2_cpu",
                },
                {
                    "Name": "script1",
                    "Type": "DB Script",
                    "Backend": "script1_torch",
                    "Device": "script1_cpu",
                },
                {
                    "Name": "script2",
                    "Type": "DB Script",
                    "Backend": "script2_torch",
                    "Device": "script2_gpu",
                },
            ],
        ),
        pytest.param(
            e.orchestrator_1, {"Name": [], "Type": [], "Backend": [], "Device": []}
        ),
        pytest.param(
            e.no_db_scripts_or_models,
            {"Name": [], "Type": [], "Backend": [], "Device": []},
        ),
        pytest.param(
            e.application_3.get("colocated_db"),
            [
                {
                    "Name": "model1",
                    "Type": "DB Model",
                    "Backend": "model1_tf",
                    "Device": "model1_cpu",
                },
                {
                    "Name": "model2",
                    "Type": "DB Model",
                    "Backend": "model2_tf",
                    "Device": "model2_cpu",
                },
            ],
        ),
        pytest.param(
            e.application_4.get("colocated_db"),
            [
                {
                    "Name": "script1",
                    "Type": "DB Script",
                    "Backend": "script1_torch",
                    "Device": "script1_cpu",
                },
                {
                    "Name": "script2",
                    "Type": "DB Script",
                    "Backend": "script2_torch",
                    "Device": "script2_gpu",
                },
            ],
        ),
        pytest.param(None, {"Name": [], "Type": [], "Backend": [], "Device": []}),
    ],
)


@parameterize_creator
def test_get_loaded_entities(entity, expected_value):
    val = get_loaded_entities(entity)
    assert val == expected_value
