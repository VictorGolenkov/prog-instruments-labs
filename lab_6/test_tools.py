import json
from unittest.mock import mock_open, patch
import tools


class TestReadTxt:
    
    def test_read_txt_success(self):
        mock_content = "Hello, World!"
        with patch('builtins.open', mock_open(read_data=mock_content)):
            result = tools.read_txt("test.txt")
            assert result == mock_content
    
    def test_read_txt_file_not_found(self):
        with patch('builtins.open', side_effect=FileNotFoundError("File not found")):
            result = tools.read_txt("nonexistent.txt")
            assert result == ""


class TestSaveTxt:
    
    def test_save_txt_success(self):
        test_text = "Test content"
        mock_file = mock_open()
        with patch('builtins.open', mock_file):
            tools.save_txt("output.txt", test_text)
            
            mock_file.assert_called_once_with("output.txt", 'w', encoding="utf-8")
            
            handle = mock_file()
            handle.write.assert_called_once_with(test_text)


class TestReadJson:
    
    def test_read_json_success(self):
        json_data = {"key": "value", "number": 123}
        json_string = json.dumps(json_data, ensure_ascii=False)
        
        with patch('builtins.open', mock_open(read_data=json_string)):
            result = tools.read_json("test.json")
            assert result == json_data
    
    def test_read_json_invalid_json(self):
        invalid_json = "{key: value}"
        with patch('builtins.open', mock_open(read_data=invalid_json)):
            result = tools.read_json("invalid.json")
            assert result == {}


class TestSaveJson:
    
    def test_save_json_success(self):
        test_data = {"name": "Test", "value": 42}
        mock_file = mock_open()
        
        with patch('builtins.open', mock_file):
            tools.save_json("output.json", test_data)
            
            mock_file.assert_called_once_with("output.json", 'w', encoding='utf-8')
    
