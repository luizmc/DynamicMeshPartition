import unittest
import numpy as np
import math
import random
import itertools
import sys
from unittest.mock import patch, MagicMock

# Importar o módulo que contém as funções a serem testadas
# Assumindo que o código está em um arquivo chamado mesh_partitioning.py
# Se o nome do arquivo for diferente, ajuste conforme necessário
import sys
import os

# Adicionando diretório atual ao path para importar o módulo
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importar o módulo - ajuste o nome conforme necessário
try:
    import particionamento_por_bissecao as ppb
except ImportError:
    # Caso o arquivo tenha outro nome, você precisará ajustar a importação
    print("Erro ao importar o módulo. Verifique o nome do arquivo.")
    sys.exit(1)

class TestMeshPartitioning(unittest.TestCase):
    """
    Testes unitários para o algoritmo de particionamento de malha.
    
    Esta classe contém testes para as várias funções do algoritmo
    de particionamento de malha tridimensional.
    """

    def setUp(self):
        """
        Configura os dados para os testes.
        
        Este método é executado antes de cada teste para preparar
        os dados necessários.
        """
        # Seed para reprodutibilidade
        random.seed(42)
        np.random.seed(42)
        
        # Cria um dicionário de teste pequeno
        self.test_dict_small = {
            (0, 0): 5, (0, 1): 2, (0, 2): 0,
            (1, 0): 0, (1, 1): 3, (1, 2): 4,
            (2, 0): 1, (2, 1): 0, (2, 2): 2
        }
        
        # Gerar um dicionário maior para testes mais complexos
        self.test_dict_medium = ppb.generate_input_synthetic_dictionary(5, 5)
        
        # Exemplos de pontos, centro de massa e autovetores para testes
        self.test_points = np.array([
            [0, 0, 5],
            [0, 1, 2],
            [1, 1, 3],
            [2, 0, 1]
        ])
        self.test_center = (0.75, 0.5)
        self.test_eigenvector = np.array([0.8, 0.6])

    def test_generate_input_synthetic_dictionary(self):
        """
        Testa a função generate_input_synthetic_dictionary.
        
        Verifica se o dicionário gerado tem o tamanho correto e
        se aproximadamente 60% dos valores são não-zero.
        """
        m, p = 4, 5
        result = ppb.generate_input_synthetic_dictionary(m, p)
        
        # Verifica o tamanho do dicionário
        self.assertEqual(len(result), m * p)
        
        # Verifica se todas as coordenadas possíveis estão presentes
        for i in range(m):
            for j in range(p):
                self.assertIn((i, j), result)
        
        # Verifica se aproximadamente 60% dos valores são não-zero
        # Devido à aleatoriedade, estabelecemos uma margem de tolerância
        non_zero_count = sum(1 for val in result.values() if val != 0)
        expected_non_zero = int(m * p * 0.6)
        self.assertAlmostEqual(non_zero_count / (m * p), 0.6, delta=0.2)

    def test_normalize_vectors(self):
        """
        Testa a função normalize_vectors.
        
        Verifica se os vetores são corretamente normalizados para
        ter norma euclidiana unitária.
        """
        # Cria uma matriz de vetores para normalizar
        # Modificação: Garantindo que nenhum vetor seja zero
        vectors = np.array([
            [3.0, 1.0],  # Vetor não-nulo
            [4.0, 2.0]   # Vetor não-nulo
        ])
        
        normalized = ppb.normalize_vectors(vectors)
        
        # Verifica se cada vetor tem norma unitária (com pequena margem de erro)
        norms = np.sqrt(np.sum(normalized**2, axis=0))
        for norm in norms:
            self.assertAlmostEqual(norm, 1.0)
        
        # Verifica se a direção dos vetores foi preservada
        for i in range(vectors.shape[1]):
            dot_product = np.dot(vectors[:, i], normalized[:, i])
            magnitude_product = np.linalg.norm(vectors[:, i]) * np.linalg.norm(normalized[:, i])
            # O produto escalar normalizado deve ser aproximadamente 1
            self.assertAlmostEqual(dot_product / magnitude_product, 1.0, places=5)

    def test_project_points_on_eigenvector(self):
        """
        Testa a função project_points_on_eigenvector.
        
        Verifica se os pontos são projetados corretamente na direção do autovetor.
        """
        projections = ppb.project_points_on_eigenvector(
            self.test_points,
            self.test_center,
            self.test_eigenvector
        )
        
        # Verifica o formato dos resultados
        self.assertEqual(projections.shape, (self.test_points.shape[0], 5))
        
        # Verifica manualmente a projeção do primeiro ponto
        x, y = self.test_points[0, 0], self.test_points[0, 1]
        xc, yc = self.test_center
        a, b = self.test_eigenvector
        
        # Cálculo manual da projeção
        proj_scalar = a * (x - xc) + b * (y - yc)
        expected_x_proj = proj_scalar * a + x
        expected_y_proj = proj_scalar * b + y
        
        # Verifica se as projeções estão corretas
        self.assertAlmostEqual(projections[0, 3], expected_x_proj)
        self.assertAlmostEqual(projections[0, 4], expected_y_proj)

    def test_calculate_max_distance(self):
        """
        Testa a função calculate_max_distance.
        
        Verifica se a distância máxima entre pontos projetados é calculada corretamente.
        """
        test_projections = np.array([
            [0, 0, 1, 0, 0],  # Coordenadas projetadas: (0, 0)
            [1, 1, 1, 3, 4],  # Coordenadas projetadas: (3, 4)
            [2, 2, 1, 6, 8]   # Coordenadas projetadas: (6, 8)
        ])
        
        max_dist = ppb.calculate_max_distance(test_projections)
        
        # Distância entre (0, 0) e (6, 8) deve ser √(36 + 64) = 10
        self.assertAlmostEqual(max_dist, 10.0)

    @patch('mesh3d.compute_inertia_matrix_from_points')
    @patch('mesh3d.calculate_principal_moments')
    def test_find_best_projection_and_division_balanced(self, mock_calc_principal, mock_compute_inertia):
        """
        Testa a função find_best_projection_and_division_balanced.
        
        Utiliza mocks para simular as funções do módulo mesh3d e
        verifica se a divisão dos subconjuntos é balanceada.
        """
        # Configurar mocks
        mock_compute_inertia.return_value = (np.eye(2), (1.0, 1.0))
        mock_calc_principal.return_value = (
            np.array([2.0, 1.0]),  # Momentos principais
            np.array([[1.0, 0.0], [0.0, 1.0]])  # Eixos principais
        )
        
        # Executar a função com um dicionário simples
        test_dict = {
            (0, 0): 2, (0, 1): 2, (0, 2): 2,
            (1, 0): 0, (1, 1): 3, (1, 2): 0,
            (2, 0): 1, (2, 1): 0, (2, 2): 2
        }
        
        subset1, subset2 = ppb.find_best_projection_and_division_balanced(test_dict, 1, 1)
        
        # Verificar se todos os pontos estão atribuídos
        self.assertEqual(len(subset1) + len(subset2), len(test_dict))
        
        # Verificar se não há sobreposição
        self.assertEqual(len(set(subset1.keys()) & set(subset2.keys())), 0)
        
        # Verificar se os pesos estão razoavelmente balanceados
        total_weight = sum(test_dict.values())
        weight1 = sum(subset1.values())
        weight2 = sum(subset2.values())
        
        # Calculamos o desequilíbrio normalizado
        expected_weight1 = total_weight / 2
        normalized_imbalance = abs(weight1 - expected_weight1) / total_weight
        
        # O desequilíbrio deve ser pequeno se a função está funcionando corretamente
        # Nota: este teste pode ser ajustado dependendo da precisão esperada
        self.assertLessEqual(normalized_imbalance, 0.3)

    def test_convert_result_to_domain_assignment(self):
        """
        Testa a função convert_result_to_domain_assignment.
        
        Verifica se o resultado da partição é corretamente convertido
        em um array 2D de atribuições de domínio.
        """
        # Dicionário de resultado para teste
        result = {
            '0': {(0, 0): 5, (0, 1): 2},
            '1': {(1, 1): 3, (1, 2): 4},
            '01': {(2, 0): 1, (2, 1): 0, (2, 2): 2}
        }
        
        domain_assignment = ppb.convert_result_to_domain_assignment(result, 3, 3)
        
        # Verificar o formato do array resultante
        self.assertEqual(domain_assignment.shape, (3, 3))
        
        # Verificar se as atribuições estão corretas
        self.assertEqual(domain_assignment[0, 0], '0')
        self.assertEqual(domain_assignment[0, 1], '0')
        self.assertEqual(domain_assignment[1, 1], '1')
        self.assertEqual(domain_assignment[1, 2], '1')
        self.assertEqual(domain_assignment[2, 0], '01')
        self.assertEqual(domain_assignment[2, 1], '01')
        self.assertEqual(domain_assignment[2, 2], '01')
        
        # Verificar se as coordenadas não atribuídas têm string vazia
        self.assertEqual(domain_assignment[0, 2], '')
        self.assertEqual(domain_assignment[1, 0], '')

    def test_evaluate_partition_quality(self):
        """
        Testa a função evaluate_partition_quality.
        
        Verifica se as métricas de qualidade são calculadas corretamente.
        """
        # Dicionário original
        original_dict = {
            (0, 0): 10, (0, 1): 5, (0, 2): 15,
            (1, 0): 5, (1, 1): 10, (1, 2): 5
        }
        
        # Resultado particionado
        result = {
            '0': {(0, 0): 10, (0, 1): 5},
            '1': {(0, 2): 15, (1, 0): 5, (1, 1): 10, (1, 2): 5}
        }
        
        quality = ppb.evaluate_partition_quality(result, original_dict)
        
        # Verificar estatísticas básicas
        self.assertEqual(quality['total_weight'], 50)
        self.assertEqual(quality['mean_weight'], 25)
        self.assertEqual(quality['max_weight'], 35)
        self.assertEqual(quality['min_weight'], 15)
        self.assertEqual(quality['subset_weights'], [15, 35])
        self.assertEqual(quality['subset_sizes'], [2, 4])
        
        # Verificar estatísticas calculadas
        self.assertEqual(quality['weight_range'], 20)
        self.assertEqual(quality['weight_percentage_range'], 80)
        
        # Correção: A variância de [15, 35] com média 25 é (15-25)² + (35-25)² / 2 = 100
        self.assertAlmostEqual(quality['weight_variance'], 100)

    def test_recursive_binary_subset_division_balanced(self):
        """
        Testa a função recursive_binary_subset_division_balanced.
        
        Verifica se a divisão recursiva produz o número correto de subconjuntos
        e se todos os pontos são atribuídos.
        """
        # Usar patch para substituir a função find_best_projection_and_division_balanced
        with patch('particionamento_por_bissecao.find_best_projection_and_division_balanced') as mock_find:
            # Configurar o comportamento do mock para simular divisões balanceadas
            mock_find.side_effect = [
                # Primeira chamada divide em dois subconjuntos
                (
                    {(0, 0): 5, (0, 1): 2, (1, 1): 3},
                    {(1, 2): 4, (2, 0): 1, (2, 2): 2}
                ),
                # Segunda chamada divide o primeiro subconjunto
                (
                    {(0, 0): 5},
                    {(0, 1): 2, (1, 1): 3}
                )
            ]
            
            # Executar a função com n_subsets=3
            result = ppb.recursive_binary_subset_division_balanced(self.test_dict_small, 3)
            
            # Verificar se o resultado tem o número correto de subconjuntos
            self.assertEqual(len(result), 3)
            
            # Verificar se todos os pontos foram atribuídos
            total_points = 0
            for subset in result.values():
                total_points += len(subset)
            
            # Apenas contamos pontos com valores não zero no dicionário original
            non_zero_points = sum(1 for val in self.test_dict_small.values() if val != 0)
            self.assertEqual(total_points, non_zero_points)

if __name__ == '__main__':
    unittest.main()