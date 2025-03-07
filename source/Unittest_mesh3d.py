import unittest
import numpy as np
from numpy.testing import assert_array_almost_equal
import matplotlib.pyplot as plt
from matplotlib import figure, axes
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D
from matplotlib.testing.compare import compare_images
import sys
import os
import io
import tempfile  # Import tempfile for temporary directory creation

# Import the mesh3d module
# Assuming the file is in the same directory as this test file
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mesh3d

class TestMesh3D(unittest.TestCase):
    """
    Test case for the mesh3d module, covering mesh creation and refinement.
    """
    def setUp(self):
        """
        Set up method to create a temporary directory for test files.
        """
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Tear down method to clean up the temporary directory after tests.
        """
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_create_3d_mesh_default(self):
        """Test create_3d_mesh with default parameters"""
        mesh = mesh3d.create_3d_mesh()
        
        # Check mesh dimensions
        self.assertEqual(mesh.shape, (8, 8, 3))
        
        # Check that mesh contains only 0s and 1s
        self.assertTrue(np.all((mesh == 0) | (mesh == 1)))
        
        # Check that there are active cells in the mesh
        self.assertTrue(np.any(mesh == 1))
        
        # Verify some specific expected active intervals from the default pattern
        # Layer 0, row 3 should have active cells from column 2 to 5
        self.assertTrue(np.all(mesh[3, 2:5, 0] == 1))
        
        # Layer 1, row 2 should have active cells from column 1 to 6
        self.assertTrue(np.all(mesh[2, 1:6, 1] == 1))
        
        # Layer 2, row 3 should have active cells from column 0 to 7
        self.assertTrue(np.all(mesh[3, 0:7, 2] == 1))

    def test_create_3d_mesh_custom(self):
        """Test create_3d_mesh with custom parameters"""
        custom_intervals = {
            0: {2: [(3, 4)], 3: [(2, 5)]},
            1: {1: [(2, 5)], 2: [(1, 6)]}
        }
        
        mesh = mesh3d.create_3d_mesh(nx=6, ny=6, nz=2, active_intervals=custom_intervals)
        
        # Check mesh dimensions
        self.assertEqual(mesh.shape, (6, 6, 2))
        
        # Check that mesh contains only 0s and 1s
        self.assertTrue(np.all((mesh == 0) | (mesh == 1)))
        
        # Verify the custom active intervals
        # Layer 0, row 2 should have active cell on column 3
        self.assertEqual(mesh[2, 3, 0], 1)
        self.assertEqual(mesh[2, 4, 0], 0)
        
        # Layer 0, row 3 should have active cells from column 2 to 4
        self.assertTrue(np.all(mesh[3, 2:5, 0] == 1))
        
        # Layer 1, row 1 should have active cells from column 2 to 4
        self.assertTrue(np.all(mesh[1, 2:5, 1] == 1))
        
        # Layer 1, row 2 should have active cells from column 1 to 5
        # But since mesh is 6x6, column 6 is out of bounds
        self.assertTrue(np.all(mesh[2, 1:6, 1] == 1))
        # Check that cells outside active intervals are inactive
        self.assertEqual(mesh[0, 0, 0], 0)
        self.assertEqual(mesh[5, 5, 1], 0)
        self.assertEqual(mesh[2,5,0],0)

    def test_refine_mesh(self):
        """Test refine_mesh function"""
        # Create a simple mesh
        mesh = np.zeros((5, 5, 3), dtype=int)
        mesh[1:4, 1:4, 0] = 1  # Active cells in layer 0
        mesh[2, 2, 1] = 1      # One active cell in layer 1
        
        # Define refinement regions
        refinement_regions = {
            0: {
                2: [(2, 3, 2, 2, 2)]
            },
            1: {
                2: [(2, 2, 3, 3, 3)]
            }
        }
        
        refined_mesh = mesh3d.refine_mesh(mesh, refinement_regions)

        # Test if the refinement was applied correctly
        self.assertEqual(refined_mesh[2,2,0],8)
        self.assertEqual(refined_mesh[2,3,0],8)
        self.assertEqual(refined_mesh[2, 2, 1], 27)
        self.assertEqual(refined_mesh[1,1,0],1)
        self.assertEqual(refined_mesh[0,0,0],0)
    
    def test_compute_weight_array(self):
        """Test compute_weight_array function"""
        # Create a simple 3D mesh
        mesh = np.zeros((3, 3, 4), dtype=int)
        
        # Set some values
        mesh[0, 0, 0] = 1
        mesh[0, 0, 1] = 2
        mesh[1, 1, 0] = 3
        mesh[1, 1, 1] = 4
        mesh[1, 1, 2] = 5
        mesh[2, 2, 3] = 6
        
        weights = mesh3d.compute_weight_array(mesh)
        
        # Check dimensions
        self.assertEqual(weights.shape, (3, 3))
        
        # Check specific weight values
        self.assertEqual(weights[0, 0], 3)  # 1 + 2 + 0 + 0
        self.assertEqual(weights[1, 1], 12)  # 3 + 4 + 5 + 0
        self.assertEqual(weights[2, 2], 6)  # 0 + 0 + 0 + 6
        self.assertEqual(weights[0, 1], 0)  # No active cells in this position

    def test_plot_weights_output(self):
        """Test if the function plot_weights generates a plot without errors."""
        weight_array = np.array([[1, 2], [3, 4]])
        mesh3d.plot_weights(weight_array)
        plt.close()  # Close the figure to release resources

    def test_plot_3d_mesh_with_weights_output(self):
        """Test if the function plot_3d_mesh_with_weights generates a plot without errors."""
        mesh = np.zeros((3, 3, 3), dtype=int)
        mesh[1, 1, 1] = 1
        mesh3d.plot_3d_mesh_with_weights(mesh)
        plt.close()

    def test_plot_both_mesh_views_output(self):
        """Test if the function plot_both_mesh_views generates a plot without errors."""
        mesh = np.zeros((3, 3, 3), dtype=int)
        mesh[1, 1, 1] = 1
        mesh3d.plot_both_mesh_views(mesh)
        plt.close()

    def test_inertia_matrix_calculation(self):
        """Test compute_inertia_matrix_from_grid function"""
        weight_matrix = np.array([
            [0, 1, 2],
            [4, 0, 1],
            [3, 5, 0]
        ])
        
        I, center_of_mass = mesh3d.compute_inertia_matrix_from_grid(weight_matrix)
        
        # Check if the inertia matrix is of the correct shape
        self.assertEqual(I.shape, (2, 2))
        
        # Perform some basic checks on the matrix elements
        self.assertAlmostEqual(I[0, 0], 9.4375)
        self.assertAlmostEqual(I[1, 1], 9.)
        self.assertAlmostEqual(I[0, 1], 3.75)
        self.assertAlmostEqual(I[1, 0], 3.75)

        # Check if the center of mass is calculated correctly
        self.assertAlmostEqual(center_of_mass[0], 1.3125)
        self.assertAlmostEqual(center_of_mass[1], 0.75)

    def test_calculate_principal_moments_diagonal(self):
        """Test calculate_principal_moments with a diagonal matrix."""
        diagonal_matrix = np.array([
            [2, 0],
            [0, 5]
        ])
        moments, axes = mesh3d.calculate_principal_moments(diagonal_matrix)
        expected_moments = np.array([2, 5])
        self.assertTrue(np.allclose(np.sort(moments), np.sort(expected_moments), atol=1e-10))

    def test_calculate_principal_moments_symmetric(self):
        """Test calculate_principal_moments with a symmetric matrix."""
        symmetric_matrix = np.array([
            [3, 1],
            [1, 2]
        ])
        moments, axes = mesh3d.calculate_principal_moments(symmetric_matrix)
        expected_moments = np.array([1.381966, 3.618033])  # Valores próprios da matriz [[3,1],[1,2]]

        self.assertTrue(np.allclose(np.sort(moments), np.sort(expected_moments), atol=1e-10))

    def test_calculate_principal_moments_3d(self):
        """Test calculate_principal_moments with a 3D matrix."""
        matrix_3d = np.array([
            [3, 1, 0.5],
            [1, 4, -0.2],
            [0.5, -0.2, 2]
        ])
        moments, axes = mesh3d.calculate_principal_moments(matrix_3d)
        self.assertEqual(len(moments), 3)
        self.assertEqual(axes.shape, (3, 3))

    def test_calculate_principal_moments_asymmetric(self):
        """Test if a ValueError is raised for a non-symmetric matrix."""
        asymmetric_matrix = np.array([
            [3, 1],
            [2, 4]
        ])
        with self.assertRaises(ValueError):
            mesh3d.calculate_principal_moments(asymmetric_matrix)
            
    def test_visualize_inertia_deformation_output(self):
        """Test if visualize_inertia_deformation generates a plot without errors."""
        symmetric_matrix = np.array([[3, 1], [1, 2]])
        moments, axes = mesh3d.calculate_principal_moments(symmetric_matrix)
        fig, ax = mesh3d.visualize_inertia_deformation(moments, axes, fig_size=(4, 4))
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)
        plt.close(fig)
    
    def setUp(self):
        """Configuração inicial para os testes."""
        # Caso simples: matriz diagonal
        self.diagonal_matrix = np.array([
            [2, 0],
            [0, 5]
        ])
        
        # Caso comum: matriz simétrica não-diagonal
        self.symmetric_matrix = np.array([
            [3, 1],
            [1, 2]
        ])
        
        # Caso 3D: matriz 3x3
        self.matrix_3d = np.array([
            [3, 1, 0.5],
            [1, 4, -0.2],
            [0.5, -0.2, 2]
        ])
        
        # Caso inválido: matriz não simétrica
        self.asymmetric_matrix = np.array([
            [3, 1],
            [2, 4]
        ])
        
        # Tolerância para comparações numéricas
        self.tol = 1e-10
        
        # Diretório temporário para salvar imagens de teste
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Limpeza após os testes."""
        # Limpar arquivos temporários se necessário
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
    
    def test_principal_moments_diagonal(self):
        """Testa o cálculo de momentos principais para uma matriz diagonal."""
        moments, axes = mesh3d.calculate_principal_moments(self.diagonal_matrix)
        
        # Para uma matriz diagonal, os momentos principais devem ser os elementos da diagonal
        expected_moments = np.array([2, 5])
        self.assertTrue(np.allclose(np.sort(moments), np.sort(expected_moments), atol=self.tol))
        
        # Os eixos principais devem ser alinhados com os eixos coordenados
        # Nota: os vetores próprios podem ter sinais diferentes, então comparamos os valores absolutos
        expected_axes = np.eye(2)
        # Verificamos se cada vetor próprio está alinhado com um dos eixos coordenados
        for i in range(2):
            vec = axes[:, i]
            # Procura o eixo coordenado mais próximo
            max_dot = max(abs(np.dot(vec, expected_axes[:, j])) for j in range(2))
            self.assertAlmostEqual(max_dot, 1.0, delta=self.tol)
    
    def test_principal_moments_3d(self):
        """Testa o cálculo de momentos principais para uma matriz 3D."""
        moments, axes = mesh3d.calculate_principal_moments(self.matrix_3d)
        
        # Verificar se a função pode lidar com matrizes 3x3
        self.assertEqual(len(moments), 3)
        self.assertEqual(axes.shape, (3, 3))
        
        # Verificar os vetores próprios
        reconstructed = axes @ np.diag(moments) @ axes.T
        self.assertTrue(np.allclose(reconstructed, self.matrix_3d, atol=self.tol))
    
    def test_asymmetric_matrix(self):
        """Testa se uma exceção é lançada para uma matriz não simétrica."""
        with self.assertRaises(ValueError):
            mesh3d.calculate_principal_moments(self.asymmetric_matrix)

    def test_visualization_output(self):
        """Testa se a função de visualização gera um gráfico sem erros."""
        moments, axes = mesh3d.calculate_principal_moments(self.symmetric_matrix)
        
        # Testa se a função retorna os objetos esperados
        fig, ax = mesh3d.visualize_inertia_deformation(moments, axes, fig_size=(4, 4))
        self.assertIsInstance(fig, plt.Figure)
        self.assertIsInstance(ax, plt.Axes)
        
        # Verifica se o gráfico tem os elementos esperados
        self.assertEqual(len(ax.lines), 6)  # 2 para os eixos, 2 para o círculo/elipse, 1 para o eixo z
        
        # Salva a figura para verificações visuais (opcional)
        test_file = os.path.join(self.temp_dir, 'test_plot.png')
        fig.savefig(test_file)
        self.assertTrue(os.path.exists(test_file))
        
        # Fecha a figura para liberar recursos
    def test_custom_title_and_size(self):
        """Testa se os parâmetros opcionais funcionam corretamente."""
        moments, axes = mesh3d.calculate_principal_moments(self.symmetric_matrix)
        
        title = "Teste Personalizado"
        fig_size = (8, 6)
        
        fig, ax = mesh3d.visualize_inertia_deformation(moments, axes, fig_size=fig_size, title=title)
        
        self.assertEqual(ax.get_title(), title)
        self.assertEqual(fig.get_size_inches()[0], fig_size[0])
        self.assertEqual(fig.get_size_inches()[1], fig_size[1])
        
        plt.close(fig)

    def test_orthogonality_of_eigenvectors(self):
        """Testa se os vetores próprios (eixos principais) são ortogonais."""
        for matrix in [self.diagonal_matrix, self.symmetric_matrix, self.matrix_3d]:
            _, axes = mesh3d.calculate_principal_moments(matrix)
            dim = matrix.shape[0]
            
            # Verifica ortogonalidade (produto escalar perto de 0 para vetores diferentes)
            for i in range(dim):
                for j in range(i+1, dim):
                    dot_product = np.abs(np.dot(axes[:, i], axes[:, j]))
                    self.assertAlmostEqual(dot_product, 0.0, delta=self.tol)
            
            # Verifica se cada vetor tem norma = 1
            for i in range(dim):
                norm = np.linalg.norm(axes[:, i])
                self.assertAlmostEqual(norm, 1.0, delta=self.tol)

    def test_plotting_functions_no_error(self):
        """Test that plotting functions run without errors"""
        # Create a small mesh for testing
        mesh = mesh3d.create_3d_mesh(nx=4, ny=4, nz=2)
        
        # Apply refinement
        refinement_regions = {
            0: {1: [(1, 2, 2, 2, 1)]},
            1: {2: [(1, 2, 3, 3, 3)]}
        }
        refined_mesh = mesh3d.refine_mesh(mesh, refinement_regions)
        
        # Create weight array
        weight_array = mesh3d.compute_weight_array(refined_mesh)
        
        # Test each plot function with plt.ioff() to prevent plots from showing
        plt.ioff()
        
        # Redirect standard output to capture any print statements
        original_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Test all plotting functions to ensure they don't raise errors
            
            # Test plot_weights
            fig, ax = plt.subplots()
            mesh3d.plot_weights(weight_array)
            plt.close(fig)
            
            # Test plot_3d_mesh_with_weights
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            mesh3d.plot_3d_mesh_with_weights(refined_mesh, show_refinement=False)
            plt.close(fig)
            
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            mesh3d.plot_3d_mesh_with_weights(refined_mesh, show_refinement=True)
            plt.close(fig)
            
            # Test plot_both_mesh_views
            fig = plt.figure()
            mesh3d.plot_both_mesh_views(refined_mesh)
            plt.close(fig)
            
            # Test visualize_inertia_deformation
            inertia_matrix, center_of_mass = mesh3d.compute_inertia_matrix_from_grid(weight_array)
            principal_moments, principal_axes = mesh3d.calculate_principal_moments(inertia_matrix)
            fig, ax = mesh3d.visualize_inertia_deformation(principal_moments, principal_axes)
            plt.close(fig)
            
            self.assertTrue(True)  # If we got here, no exceptions were raised
            
        finally:
            # Restore standard output
            sys.stdout = original_stdout
            plt.ion()  # Turn interactive mode back on    
    def test_single_point(self):
        """Teste com um único ponto na origem."""
        points = np.array([[0, 0, 1]])  # Um ponto na origem com peso 1
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Centro de massa deve ser na origem
        self.assertEqual(center, (0, 0))
        
        # Matriz de inércia deve ser zeros
        expected_I = np.zeros((2, 2))
        assert_array_almost_equal(I, expected_I)
    
    def test_two_equal_points(self):
        """Teste com dois pontos iguais."""
        points = np.array([[1, 1, 1], [1, 1, 1]])  # Dois pontos idênticos
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Centro de massa deve ser no ponto (1, 1)
        self.assertEqual(center, (1, 1))
        
        # Matriz de inércia deve ser zeros (ambos os pontos estão no centro de massa)
        expected_I = np.zeros((2, 2))
        assert_array_almost_equal(I, expected_I)
    
    def test_symmetric_configuration(self):
        """Teste com configuração simétrica de pontos."""
        # Pontos formando um quadrado de lado 2 centrado na origem
        points = np.array([
            [-1, -1, 1],  # Ponto inferior esquerdo
            [1, -1, 1],   # Ponto inferior direito
            [-1, 1, 1],   # Ponto superior esquerdo
            [1, 1, 1]     # Ponto superior direito
        ])
        
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Centro de massa deve ser na origem
        assert_array_almost_equal(center, (0, 0))
        
        # Para configuração simétrica, os termos não diagonais devem ser zero
        # e os termos diagonais devem ser iguais
        self.assertAlmostEqual(I[0, 1], 0)
        self.assertAlmostEqual(I[1, 0], 0)
        self.assertAlmostEqual(I[0, 0], I[1, 1])
        
        # Valor esperado para o momento de inércia (2 unidades de massa * 2 unidades de distância²)
        expected_diagonal = 4
        self.assertAlmostEqual(I[0, 0], expected_diagonal)
    
    def test_different_weights(self):
        """Teste com pontos de pesos diferentes."""
        # Dois pontos com pesos diferentes
        points = np.array([
            [0, 0, 1],   # Ponto na origem com peso 1
            [2, 0, 3]    # Ponto em (2,0) com peso 3
        ])
        
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Centro de massa: (2*3 + 0*1)/(3+1) = 6/4 = 1.5 no eixo x e 0 no eixo y
        expected_center = (1.5, 0)
        assert_array_almost_equal(center, expected_center)
        
        # Cálculo manual da matriz de inércia
        # I_xx = Σ w_i * (y_i - y_bar)² = 1*0² + 3*0² = 0
        # I_yy = Σ w_i * (x_i - x_bar)² = 1*(0-1.5)² + 3*(2-1.5)² = 1*2.25 + 3*0.25 = 2.25 + 0.75 = 3
        # I_xy = -Σ w_i * (x_i - x_bar)*(y_i - y_bar) = -[1*(0-1.5)*(0-0) + 3*(2-1.5)*(0-0)] = 0
        expected_I = np.array([[0, 0], [0, 3]])
        assert_array_almost_equal(I, expected_I)
    
    def test_general_case(self):
        """Teste com uma configuração de pontos genérica."""
        points = np.array([
            [0, 0, 2],
            [1, 2, 3],
            [3, 1, 1]
        ])
        
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Cálculo manual do centro de massa
        total_weight = 2 + 3 + 1
        x_bar = (0*2 + 1*3 + 3*1) / total_weight
        y_bar = (0*2 + 2*3 + 1*1) / total_weight
        expected_center = (x_bar, y_bar)
        
        # Verificando centro de massa
        assert_array_almost_equal(center, expected_center)
        
        # Propriedades da matriz de inércia
        # 1. Deve ser simétrica
        self.assertAlmostEqual(I[0, 1], I[1, 0])
        
        # 2. O traço da matriz deve ser positivo ou zero
        self.assertGreaterEqual(np.trace(I), 0)
        
        # 3. O determinante deve ser não-negativo
        self.assertGreaterEqual(np.linalg.det(I), 0)
    
    def test_zero_weights(self):
        """Teste com pontos de peso zero."""
        points = np.array([
            [1, 2, 0],
            [3, 4, 0]
        ])
        
        I, center = mesh3d.compute_inertia_matrix_from_points(points)
        
        # Centro de massa deve ser (0, 0) quando todos os pesos são zero
        self.assertEqual(center, (0, 0))
        
        # Matriz de inércia deve ser zeros
        expected_I = np.zeros((2, 2))
        assert_array_almost_equal(I, expected_I)

if __name__ == '__main__':
    unittest.main()
