import unittest
import numpy as np
import tkinter as tk
from unittest.mock import MagicMock, patch

# Importando o módulo que contém a classe MeshInterfaceApp
# Assumindo que a classe está em um arquivo chamado mesh_interface.py
# Se estiver em outro arquivo, ajuste o import
import mesh_interface
from mesh_interface import MeshInterfaceApp, open_mesh_interface


class TestMeshInterfaceApp(unittest.TestCase):
    """Testes unitários para a classe MeshInterfaceApp."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        # Mock para a função create_3d_mesh
        self.mock_mesh_function = MagicMock()
        self.mock_mesh_function.return_value = np.zeros((8, 8, 3))
        
        # Mock para o callback on_mesh_created
        self.mock_callback = MagicMock()
        
        # Inicializar aplicação com mocks
        self.root = tk.Tk()
        self.app = MeshInterfaceApp(
            root=self.root,
            mesh_function=self.mock_mesh_function,
            on_mesh_created=self.mock_callback
        )
    
    def tearDown(self):
        """Limpeza após cada teste."""
        if hasattr(self, 'root') and self.root:
            self.root.destroy()
    
    def test_initialization(self):
        """Testa se a aplicação é inicializada corretamente com valores padrão."""
        # Verificar se as variáveis foram inicializadas com valores padrão
        self.assertEqual(self.app.nx_var.get(), 8)
        self.assertEqual(self.app.ny_var.get(), 8)
        self.assertEqual(self.app.nz_var.get(), 3)
        
        # Verificar se os intervalos padrão foram carregados
        default_intervals = self.app.get_default_intervals()
        self.assertEqual(self.app.active_intervals, default_intervals)
        
        # Verificar se a função de criação de malha foi armazenada
        self.assertEqual(self.app.create_3d_mesh, self.mock_mesh_function)
        
        # Verificar se o callback foi armazenado
        self.assertEqual(self.app.on_mesh_created, self.mock_callback)
    
    def test_get_default_intervals(self):
        """Testa se o método get_default_intervals retorna o formato esperado."""
        intervals = self.app.get_default_intervals()
        
        # Verificar se é um dicionário
        self.assertIsInstance(intervals, dict)
        
        # Verificar estrutura: {z: {x: [(y_start, y_end), ...]}}
        for z, x_dict in intervals.items():
            self.assertIsInstance(z, int)
            self.assertIsInstance(x_dict, dict)
            
            for x, y_intervals in x_dict.items():
                self.assertIsInstance(x, int)
                self.assertIsInstance(y_intervals, list)
                
                for interval in y_intervals:
                    self.assertIsInstance(interval, tuple)
                    self.assertEqual(len(interval), 2)
                    y_start, y_end = interval
                    self.assertIsInstance(y_start, int)
                    self.assertIsInstance(y_end, int)
                    self.assertLessEqual(y_start, y_end)
    
    def test_add_interval(self):
        """Testa a adição de um novo intervalo."""
        # Limpar intervalos existentes
        self.app.active_intervals = {}
        
        # Configurar um novo intervalo
        self.app.z_layer_var.set(1)
        self.app.x_line_var.set(2)
        self.app.y_start_var.set(3)
        self.app.y_end_var.set(5)
        
        # Adicionar o intervalo
        self.app.add_interval()
        
        # Verificar se o intervalo foi adicionado corretamente
        self.assertIn(1, self.app.active_intervals)
        self.assertIn(2, self.app.active_intervals[1])
        self.assertIn((3, 5), self.app.active_intervals[1][2])
    
    def test_add_invalid_interval(self):
        """Testa a adição de um intervalo inválido (y_start > y_end)."""
        # Limpar intervalos existentes
        self.app.active_intervals = {}
        
        # Configurar um intervalo inválido
        self.app.z_layer_var.set(1)
        self.app.x_line_var.set(2)
        self.app.y_start_var.set(5)  # Início maior que o fim
        self.app.y_end_var.set(3)
        
        # Tentar adicionar o intervalo (deve falhar)
        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.add_interval()
            # Verificar se a mensagem de erro foi exibida
            mock_showerror.assert_called_once()
        
        # Verificar que nenhum intervalo foi adicionado
        self.assertEqual(self.app.active_intervals, {})
    
    def test_add_duplicate_interval(self):
        """Testa a adição de um intervalo duplicado."""
        # Limpar intervalos existentes
        self.app.active_intervals = {1: {2: [(3, 5)]}}
        
        # Configurar o mesmo intervalo novamente
        self.app.z_layer_var.set(1)
        self.app.x_line_var.set(2)
        self.app.y_start_var.set(3)
        self.app.y_end_var.set(5)
        
        # Tentar adicionar o intervalo duplicado
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.add_interval()
            # Verificar se a mensagem de informação foi exibida
            mock_showinfo.assert_called_once()
    
    def test_clear_intervals(self):
        """Testa a limpeza de todos os intervalos."""
        # Garantir que há intervalos para limpar
        self.app.active_intervals = self.app.get_default_intervals()
        
        # Simular confirmação do usuário
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.clear_intervals()
        
        # Verificar se os intervalos foram limpos
        self.assertEqual(self.app.active_intervals, {})
    
    def test_restore_defaults(self):
        """Testa a restauração dos valores padrão."""
        # Modificar valores para algo diferente do padrão
        self.app.nx_var.set(10)
        self.app.ny_var.set(12)
        self.app.nz_var.set(5)
        self.app.active_intervals = {}
        
        # Simular confirmação do usuário
        with patch('tkinter.messagebox.askyesno', return_value=True):
            self.app.restore_defaults()
        
        # Verificar se os valores foram restaurados
        self.assertEqual(self.app.nx_var.get(), 8)
        self.assertEqual(self.app.ny_var.get(), 8)
        self.assertEqual(self.app.nz_var.get(), 3)
        self.assertEqual(self.app.active_intervals, self.app.get_default_intervals())
    
    def test_generate_mesh(self):
        """Testa a geração da malha."""
        # Configurar valores
        nx, ny, nz = 10, 12, 5
        self.app.nx_var.set(nx)
        self.app.ny_var.set(ny)
        self.app.nz_var.set(nz)
        
        # Configurar o retorno do mock da função de malha
        mock_mesh = np.ones((nx, ny, nz))
        self.mock_mesh_function.return_value = mock_mesh
        
        # Gerar a malha
        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.generate_mesh()
            mock_showinfo.assert_called_once()
        
        # Verificar se a função foi chamada com os parâmetros corretos
        self.mock_mesh_function.assert_called_with(
            nx=nx, 
            ny=ny, 
            nz=nz, 
            active_intervals=self.app.active_intervals
        )
        
        # Verificar se o callback foi chamado com a malha correta
        self.mock_callback.assert_called_with(mock_mesh)
    
    def test_generate_mesh_no_intervals(self):
        """Testa a geração da malha sem intervalos ativos."""
        # Limpar intervalos
        self.app.active_intervals = {}
        
        # Reset mock to ignore previous calls (e.g., from setup)
        self.mock_mesh_function.reset_mock()
        
        # Tentar gerar a malha
        with patch('tkinter.messagebox.showwarning') as mock_showwarning:
            self.app.generate_mesh()
            mock_showwarning.assert_called_once()
        
        # Verificar que a função de malha não foi chamada
        self.mock_mesh_function.assert_not_called()
        
        # Verificar que o callback não foi chamado
        self.mock_callback.assert_not_called()

    
    def test_update_spinbox_limits(self):
        """Testa a atualização dos limites dos spinboxes."""
        # Configurar novos valores
        self.app.nx_var.set(5)
        self.app.ny_var.set(6)
        self.app.nz_var.set(2)
        
        # Forçar chamada do método
        self.app.update_spinbox_limits()
        
        # Verificar se os limites foram atualizados corretamente
        self.assertEqual(self.app.z_spinbox.cget('to'), 1)  # nz-1
        self.assertEqual(self.app.x_spinbox.cget('to'), 4)  # nx-1
        self.assertEqual(self.app.y_start_spinbox.cget('to'), 5)  # ny-1
        self.assertEqual(self.app.y_end_spinbox.cget('to'), 5)  # ny-1
    
    def test_close_application(self):
        """Testa o fechamento da aplicação."""
        # Simular que uma malha foi gerada
        mock_mesh = np.ones((8, 8, 3))
        self.app.mesh = mock_mesh
        
        # Fechar a aplicação
        with patch.object(self.root, 'destroy') as mock_destroy:
            self.app.close_application()
            
            # Verificar se o callback foi chamado com a malha
            self.mock_callback.assert_called_with(mock_mesh)
            
            # Verificar se a janela foi destruída
            mock_destroy.assert_called_once()

class TestOpenMeshInterface(unittest.TestCase):
    """Testes para a função open_mesh_interface."""
    
    @patch('tkinter.Tk')
    @patch('mesh_interface.MeshInterfaceApp')
    def test_open_mesh_interface(self, mock_app_class, mock_tk_class):
        """Testa a função open_mesh_interface."""
        # Configurar mock para a janela Tk
        mock_root = mock_tk_class.return_value
        
        # Configurar mock para a classe MeshInterfaceApp
        mock_app = mock_app_class.return_value
        
        # Configurar o mainloop para capturar o argumento on_mesh_created
        def mock_mainloop():
            # Simular a criação de uma malha (chamar o callback)
            args, kwargs = mock_app_class.call_args
            captured_callback = kwargs['on_mesh_created']
            test_mesh = np.ones((5, 5, 2))
            captured_callback(test_mesh)
        
        mock_root.mainloop.side_effect = mock_mainloop
        
        # Chamar a função com uma função de malha de mock
        mock_mesh_func = MagicMock()
        result = open_mesh_interface(mesh_function=mock_mesh_func)
        
        # Verificar se a função retornou a malha correta
        self.assertIsNotNone(result)
        self.assertEqual(result.shape, (5, 5, 2))
        
        # Verificar se a classe MeshInterfaceApp foi inicializada corretamente
        mock_app_class.assert_called_once()
        args, kwargs = mock_app_class.call_args
        
        # Check positional arguments: root and mesh_function
        self.assertEqual(args[0], mock_root)  # root is first positional arg
        self.assertEqual(args[1], mock_mesh_func)  # mesh_function is second positional arg
        
        # Check on_mesh_created is in keyword arguments
        self.assertIn('on_mesh_created', kwargs)

if __name__ == '__main__':
    unittest.main()