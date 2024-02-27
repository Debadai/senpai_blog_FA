import unittest
from main import query_all
from unittest.mock import patch, MagicMock

class TestBlogApp(unittest.TestCase):

    @patch('main.get_db_connection')
    def test_query_all(self, mock_db_conn):
        """
        Esta funcion de testing crea un cursor mock, lo configura para la conexion de la base de datos para que devuelva el cursor mock cuando se llama a execute.
        Luego llama a la funcion con un query de prueba y verifica el resultado.
        """

        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [{'id': 1, 'title': 'Test Post', 'content': 'Test content'}]

        mock_conn = mock_db_conn.return_value
        mock_conn.execute.return_value = mock_cursor

        result = query_all("SELECT * FROM posts")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['title'], 'Test Post')

        mock_db_conn.assert_called_once()
        mock_conn.execute.assert_called_with("SELECT * FROM posts")
        mock_conn.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
