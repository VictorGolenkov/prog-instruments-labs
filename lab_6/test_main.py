# test_main.py
import pytest
import sys
import json
from unittest.mock import patch, mock_open, MagicMock
import main


class TestMainFunctions:
    
    def test_parser_for_program_default(self):
        test_args = ["program_name"]
        with patch.object(sys, 'argv', test_args):
            args = main.parser_for_program()
            assert args.settings_file == 'settings.json'
            assert args.mode is None
    
    def test_parser_for_program_custom_args(self):
        test_args = ["program_name", "--settings_file", "custom.json", "--mode", "task_1_enc"]
        with patch.object(sys, 'argv', test_args):
            args = main.parser_for_program()
            assert args.settings_file == 'custom.json'
            assert args.mode == 'task_1_enc'
    
    def test_parser_for_program_short_args(self):
        test_args = ["program_name", "-sf", "short.json", "-m", "task_1_dec"]
        with patch.object(sys, 'argv', test_args):
            args = main.parser_for_program()
            assert args.settings_file == 'short.json'
            assert args.mode == 'task_1_dec'


class TestMainFunction:
    
    @patch('main.tools.read_json')
    @patch('main.tools.read_txt')
    @patch('main.tools.save_txt')
    @patch('main.t1.caesar_encrypt')
    def test_main_encrypt_mode(self, mock_encrypt, mock_save_txt, mock_read_txt, mock_read_json):
        mock_read_json.return_value = {
            "original_t1": "input.txt",
            "encrypted_t1": "encrypted.txt",
            "key_path_t1": "key.txt",
            "key": 3,
            "alphabet": "abcdefghijklmnopqrstuvwxyz"
        }
        mock_read_txt.return_value = "hello world"
        mock_encrypt.return_value = "khoor zruog"
        
        test_args = ["program", "-m", "task_1_enc", "-sf", "settings.json"]
        with patch.object(sys, 'argv', test_args):
            main.main()
        
        mock_read_json.assert_called_once_with("settings.json")
        mock_read_txt.assert_called_once_with("input.txt")
        mock_encrypt.assert_called_once_with("hello world", 3, "abcdefghijklmnopqrstuvwxyz")
        
        assert mock_save_txt.call_count == 2
        mock_save_txt.assert_any_call("encrypted.txt", "khoor zruog")
        mock_save_txt.assert_any_call("key.txt", "3")
    
    @patch('main.tools.read_json')
    @patch('main.tools.read_txt')
    @patch('main.tools.save_txt')
    @patch('main.t1.ceasar_decrypt')
    def test_main_decrypt_mode(self, mock_decrypt, mock_save_txt, mock_read_txt, mock_read_json):
        mock_read_json.return_value = {
            "encrypted_t1": "encrypted.txt",
            "decrypted_t1": "decrypted.txt",
            "key_path_t1": "key.txt",
            "key": 3,
            "alphabet": "abcdefghijklmnopqrstuvwxyz"
        }
        mock_read_txt.return_value = "khoor zruog"
        mock_decrypt.return_value = "hello world"
        
        test_args = ["program", "-m", "task_1_dec", "-sf", "settings.json"]
        with patch.object(sys, 'argv', test_args):
            main.main()
        
        mock_read_json.assert_called_once_with("settings.json")
        mock_read_txt.assert_called_once_with("encrypted.txt")
        mock_decrypt.assert_called_once_with("khoor zruog", 3, "abcdefghijklmnopqrstuvwxyz")
        

        assert mock_save_txt.call_count == 2
        mock_save_txt.assert_any_call("decrypted.txt", "hello world")
        mock_save_txt.assert_any_call("key.txt", "3")
    
    @patch('builtins.print')
    @patch('main.tools.read_json')
    def test_main_invalid_mode(self, mock_read_json, mock_print):
        """Тест неверного режима работы"""
        mock_read_json.return_value = {}
        
        test_args = ["program", "-m", "invalid_mode"]
        with patch.object(sys, 'argv', test_args):
            main.main()
        
        mock_print.assert_called_once_with("Такого режима не существует")
    
    @patch('main.tools.read_json')
    @patch('builtins.print')
    def test_main_file_not_found(self, mock_print, mock_read_json):
        """Тест обработки отсутствия файла настроек"""
        mock_read_json.return_value = {}
        
        test_args = ["program", "-sf", "nonexistent.json"]
        with patch.object(sys, 'argv', test_args):
            main.main()
        
        assert True


@pytest.mark.parametrize("mode,settings_keys,read_txt_calls", [
    ("task_1_enc", ["original_t1", "encrypted_t1", "key_path_t1", "key", "alphabet"], 1),
    ("task_1_dec", ["encrypted_t1", "decrypted_t1", "key_path_t1", "key", "alphabet"], 1),
])
@patch('main.tools.save_txt')
@patch('main.t1.caesar_encrypt')
@patch('main.t1.ceasar_decrypt')
@patch('main.tools.read_txt')
@patch('main.tools.read_json')
def test_main_modes_parametrized(mock_read_json, mock_read_txt, mock_decrypt, 
                                 mock_encrypt, mock_save_txt, mode, 
                                 settings_keys, read_txt_calls):
    """Параметризованный тест различных режимов работы"""
    settings = {key: f"{key}.txt" for key in settings_keys}
    settings["key"] = 3
    settings["alphabet"] = "abc"
    mock_read_json.return_value = settings
    mock_read_txt.return_value = "test"
    mock_encrypt.return_value = "encrypted"
    mock_decrypt.return_value = "decrypted"
    
    test_args = ["program", "-m", mode]
    with patch.object(sys, 'argv', test_args):
        main.main()
    
    mock_read_json.assert_called_once()
    assert mock_read_txt.call_count == read_txt_calls
    
    if mode == "task_1_enc":
        mock_encrypt.assert_called_once()
    elif mode == "task_1_dec":
        mock_decrypt.assert_called_once()
    
    assert mock_save_txt.call_count == 2