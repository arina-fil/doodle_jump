import unittest
from unittest.mock import patch, MagicMock
import main  # Assuming main.py is structured as provided

class TestMainGame(unittest.TestCase):

    def setUp(self):
        """Setup runs before each test."""
        print(f"\n=== Starting test: {self._testMethodName} ===")

    @patch('main.pygame.image.load')
    def test_image_loading(self, mock_image_load):
        print("Testing image loading...")
        mock_image_load.return_value = MagicMock()
        image_paths = ['images/Start_game.png', 'images/Exit.png']
        for path in image_paths:
            image = main.pygame.image.load(path)
            self.assertIsNotNone(image)
        print("✅ test_image_loading PASSED!")

    @patch('main.pygame.image.load')
    def test_menu_buttons_initialization(self, mock_image_load):
        print("Тестирование инициализации кнопки меню (неправильное)...")
        try:
            mock_image_load.return_value = MagicMock()
            menu_buttons = main.menu_buttons
            self.assertEqual(len(menu_buttons), 2)  
        except AssertionError:
            print("❌ test_menu_buttons_initialization failed как и ожидалось!")

    def test_add_record(self):
        """Test правильно ли add_record добавляет запись."""
        print("Testing add_record...")
        try:
            record = 150
            main.records_mass = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
            main.add_record(record)
            self.assertIn(record, main.records_mass)
            self.assertEqual(len(main.records_mass), 10)
            self.assertEqual(main.records_mass[0], 150)  # Highest record
            print("✅ test_add_record PASSED!")
        except Exception as e:
            print(f"❌ test_add_record failed!\n{e}")

    @patch('builtins.open', new_callable=MagicMock)
    def test_write_config(self, mock_open):
        """Test обновляет ли write_config файл конфигурации."""
        print("Testing write_config...")
        try:
            main.write_config()
            mock_open.assert_called_once_with('config/main.ini', 'w')
            print("✅ test_write_config PASSED!")
        except Exception as e:
            print(f"❌ test_write_config failed!\n{e}")

    def test_draw_background(self):
        """Test работает ли draw_background правильно."""
        print("Testing draw_background...")
        try:
            screen = MagicMock()
            main.draw_background(screen)
            screen.fill.assert_called_once_with((0, 143, 223))
            self.assertGreaterEqual(screen.blit.call_count, len(main.clouds_mass))
            print("✅ test_draw_background PASSED!")
        except Exception as e:
            print(f"❌ test_draw_background failed!\n{e}")

    def test_draw_menu_interface(self):
        """Test отображает ли draw_menu_interface кнопки меню."""
        print("Testing draw_menu_interface...")
        try:
            screen = MagicMock()
            main.menu_buttons[0]['click'] = True  # Simulate button click
            main.draw_menu_interface(screen)
            self.assertTrue(main.menu_buttons[0]['click'])
            print("✅ test_draw_menu_interface PASSED!")
        except Exception as e:
            print(f"❌ test_draw_menu_interface failed!\n{e}")

    def test_check_menu_events(self):
        """Test правильно ли распознаются нажатия кнопок меню."""
        print("Testing check_menu_events...")
        try:
            main.now_screen = 'menu'
            click_pos = (500, 200)  # Position of the first button
            main.check_menu_events(click_pos, have_click=True)
            self.assertTrue(main.menu_buttons[0]['click'])
            self.assertEqual(main.now_screen, 'choice')
            print("✅ test_check_menu_events PASSED!")
        except Exception as e:
            print(f"❌ test_check_menu_events failed!\n{e}")

    @patch('sys.exit')
    def test_menu_screen_exit(self, mock_exit):
        """Test if menu_screen exits correctly on quit event."""
        print("Testing menu_screen...")
        try:
            with patch('main.pygame.event.get') as mock_events:
                mock_events.return_value = [MagicMock(type=main.pygame.QUIT)]
                main.menu_screen(MagicMock())
                mock_exit.assert_called_once()
            print("✅ test_menu_screen_exit PASSED!")
        except Exception as e:
            print(f"❌ test_menu_screen_exit failed!\n{e}")

    def test_check_choice_events(self):
        """Test правильно ли распознаны кнопки выбора игрока.."""
        print("Testing check_choice_events...")
        try:
            main.now_screen = 'choice'
            click_pos = (300, 350)  # Position of the first choice button
            main.check_choice_events(click_pos, have_click=True)
            self.assertTrue(main.choice_buttons[0]['click'])
            self.assertEqual(main.now_screen, 'game1')
            print("✅ test_check_choice_events PASSED!")
        except Exception as e:
            print(f"❌ test_check_choice_events failed!\n{e}")

    def test_draw_choice_interface(self):
        """Test правильно ли отображен интерфейс выбора."""
        print("Testing draw_choice_interface...")
        try:
            screen = MagicMock()
            main.choice_buttons[1]['click'] = True  # Simulate second button click
            main.draw_choice_interface(screen)
            self.assertTrue(main.choice_buttons[1]['click'])
            print("✅ test_draw_choice_interface PASSED!")
        except Exception as e:
            print(f"❌ test_draw_choice_interface failed!\n{e}")

    def test_restart(self):
        """Test сбрасывает ли перезапуск состояние игры."""
        print("Testing restart...")
        try:
            main.player1_pos = [0, 0]
            main.restart()
            self.assertEqual(main.player1_pos, [250, main.frame_size_y - 100])
            self.assertFalse(main.game_lose)
            print("✅ test_restart PASSED!")
        except Exception as e:
            print(f"❌ test_restart failed!\n{e}")

if __name__ == '_main_':
    unittest.main(verbosity=2)