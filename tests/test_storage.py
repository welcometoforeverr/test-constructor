from storage import load_data, save_data


def test_save_and_load_data(tmp_path) -> None:
    filename = tmp_path / "data.json"
    source = [{"id": 1, "name": "Кекс"}]
    save_data(str(filename), source)
    assert load_data(str(filename)) == source


def test_missing_file_returns_empty_list(tmp_path) -> None:
    filename = tmp_path / "missing.json"
    assert load_data(str(filename)) == []
