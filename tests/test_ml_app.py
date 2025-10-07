import importlib.util
import sys
from io import BytesIO
from pathlib import Path
import types
import pandas as pd


def load_module_from_path(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, str(file_path))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[module_name] = module
    spec.loader.exec_module(module)  # type: ignore[attr-defined]
    return module


def test_ml_index_renders(tmp_path, monkeypatch):
    # Ensure uploads go to a temp directory for the test
    monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path))
    ml_path = Path(__file__).resolve().parents[1] / "ML_based_detectionn" / "app.py"
    ml_module = load_module_from_path("ml_app_module", ml_path)

    app = ml_module.app
    client = app.test_client()

    res = client.get("/")
    assert res.status_code == 200


def test_ml_analyze_requires_file(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path))
    ml_path = Path(__file__).resolve().parents[1] / "ML_based_detectionn" / "app.py"
    ml_module = load_module_from_path("ml_app_module2", ml_path)

    app = ml_module.app
    client = app.test_client()

    res = client.post("/analyze", data={})
    assert res.status_code == 400
    assert b"No file uploaded" in res.data


def test_ml_analyze_rejects_unsupported_extension(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path))
    ml_path = Path(__file__).resolve().parents[1] / "ML_based_detectionn" / "app.py"
    ml_module = load_module_from_path("ml_app_module3", ml_path)

    app = ml_module.app
    client = app.test_client()

    data = {"file": (BytesIO(b"data"), "test.txt")}
    res = client.post("/analyze", data=data, content_type="multipart/form-data")
    assert res.status_code == 400
    assert b"Unsupported file type" in res.data


def test_ml_analyze_success_with_stubbed_model_and_features(tmp_path, monkeypatch):
    monkeypatch.setenv("UPLOAD_FOLDER", str(tmp_path))
    ml_path = Path(__file__).resolve().parents[1] / "ML_based_detectionn" / "app.py"

    # Create a stub feature_extraction module so the app imports it
    stub_mod = types.ModuleType("feature_extraction")

    def stub_extract_features(path: str):  # noqa: ARG001 - unused in stub
        # Return a single-row DataFrame; model will ignore contents
        return pd.DataFrame([{ "f": 1 }])

    stub_mod.extract_features = stub_extract_features  # type: ignore[attr-defined]
    sys.modules["feature_extraction"] = stub_mod

    ml_module = load_module_from_path("ml_app_module4", ml_path)

    class StubModel:
        def predict(self, X):  # noqa: N803 - sklearn-like API
            return [1]

    # Inject stub model so app does not require a real pickle
    ml_module.model = StubModel()

    app = ml_module.app
    client = app.test_client()

    data = {"file": (BytesIO(b"MZ\x00\x00fakepe"), "sample.exe")}
    res = client.post("/analyze", data=data, content_type="multipart/form-data")

    assert res.status_code == 200
    assert b"Malware" in res.data
