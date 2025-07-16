"""
Tests para DataProcessor - Dashboard INSS vs Mutua
=================================================

Tests unitarios para validar el funcionamiento del procesador de datos.
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import Mock, patch
import sys
import os

# Añadir el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processor import DataProcessor
from config import COLUMN_MAPPING, NUMERIC_COLUMNS

class TestDataProcessor:
    """Clase de tests para DataProcessor"""
    
    def setup_method(self):
        """Configurar antes de cada test"""
        self.processor = DataProcessor()
        
        # Datos de ejemplo
        self.sample_data = {
            'Des Cie9 3dig': ['Lumbalgia', 'Cervicalgia', 'Tendinitis'],
            'Gr Ocupac': ['Administrativo', 'Operario', 'Técnico'],
            'Cod Genero': ['M', 'F', 'M'],
            'Gr Edad 10': ['36-45', '26-35', '46-55'],
            'CASO': ['C001', 'C002', 'C003'],
            'Count (Id Episodio)': [15, 8, 12],
            'Durestd Inss min': [30, 20, 25],
            'Duropt Inss min': [25, 18, 22],
            'Minmin': [10, 8, 12],
            'P20min': [15, 12, 16],
            'P40min': [20, 16, 20],
            'P60min': [25, 20, 24],
            'P80min': [30, 24, 28],
            'P99min': [35, 28, 32]
        }
        
        self.sample_df = pd.DataFrame(self.sample_data)
    
    def test_init(self):
        """Test inicialización del procesador"""
        assert self.processor.column_mapping == COLUMN_MAPPING
        assert self.processor.numeric_columns == NUMERIC_COLUMNS
        assert self.processor.edad_orden == ['16-25', '26-35', '36-45', '46-55', '56-65']
    
    def test_validate_columns_success(self):
        """Test validación exitosa de columnas"""
        result = self.processor._validate_columns(self.sample_df)
        assert result is True
    
    def test_validate_columns_missing(self):
        """Test validación con columnas faltantes"""
        incomplete_df = self.sample_df.drop(columns=['Des Cie9 3dig'])
        result = self.processor._validate_columns(incomplete_df)
        assert result is False
    
    def test_rename_columns(self):
        """Test renombrado de columnas"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        
        # Verificar que las columnas se renombraron correctamente
        assert 'Diagnóstico' in renamed_df.columns
        assert 'Count Episodios' in renamed_df.columns
        assert 'Des Cie9 3dig' not in renamed_df.columns
    
    def test_clean_data(self):
        """Test limpieza de datos"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        cleaned_df = self.processor._clean_data(renamed_df)
        
        # Verificar que los tipos son correctos
        for col in ['Durestd Inss min', 'Duropt Inss min', 'Count Episodios']:
            assert pd.api.types.is_numeric_dtype(cleaned_df[col])
        
        # Verificar que no hay valores nulos en columnas críticas
        assert cleaned_df[NUMERIC_COLUMNS].isnull().sum().sum() == 0
    
    def test_sort_data(self):
        """Test ordenamiento de datos"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        sorted_df = self.processor._sort_data(renamed_df)
        
        # Verificar que los datos están ordenados
        assert sorted_df['Diagnóstico'].iloc[0] == 'Cervicalgia'  # Orden alfabético
        
        # Verificar que la columna de edad es categórica
        assert sorted_df['Gr Edad 10'].dtype.name == 'category'
    
    def test_calculate_additional_fields(self):
        """Test cálculo de campos adicionales"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        calculated_df = self.processor._calculate_additional_fields(renamed_df)
        
        # Verificar que se calculó el campo percentiles_iguales
        assert 'percentiles_iguales' in calculated_df.columns
        assert calculated_df['percentiles_iguales'].dtype == bool
        
        # Verificar diferencias calculadas
        if 'diferencia_estandar' in calculated_df.columns:
            expected_diff = calculated_df['Durestd Inss min'] - calculated_df['P60min']
            assert (calculated_df['diferencia_estandar'] == expected_diff).all()
    
    def test_apply_filters(self):
        """Test aplicación de filtros"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        
        # Aplicar filtros
        filtered_df = self.processor.apply_filters(
            renamed_df,
            diagnosticos=['Lumbalgia', 'Cervicalgia'],
            genero='M',
            edad_grupos=['36-45'],
            episodios_range=(10, 20)
        )
        
        # Verificar que los filtros funcionaron
        assert len(filtered_df) == 1
        assert filtered_df['Diagnóstico'].iloc[0] == 'Lumbalgia'
        assert filtered_df['Cod Genero'].iloc[0] == 'M'
    
    def test_get_summary_stats(self):
        """Test estadísticas resumen"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        stats = self.processor.get_summary_stats(renamed_df)
        
        # Verificar estadísticas básicas
        assert stats['total_registros'] == 3
        assert stats['diagnosticos_unicos'] == 3
        assert stats['total_episodios'] == 35  # 15 + 8 + 12
        assert isinstance(stats['duracion_media_inss'], float)
    
    def test_validate_data_quality(self):
        """Test validación de calidad de datos"""
        renamed_df = self.processor._rename_columns(self.sample_df)
        quality_report = self.processor.validate_data_quality(renamed_df)
        
        # Verificar estructura del reporte
        assert 'total_rows' in quality_report
        assert 'missing_values' in quality_report
        assert 'duplicates' in quality_report
        assert 'outliers' in quality_report
        assert 'data_types' in quality_report
        
        # Verificar valores
        assert quality_report['total_rows'] == 3
        assert quality_report['duplicates'] == 0
    
    @patch('pandas.read_excel')
    def test_load_and_process_data_success(self, mock_read_excel):
        """Test carga exitosa de datos"""
        mock_read_excel.return_value = self.sample_df
        mock_file = Mock()
        
        result = self.processor.load_and_process_data(mock_file)
        
        # Verificar que se procesaron los datos correctamente
        assert result is not None
        assert len(result) == 3
        assert 'Diagnóstico' in result.columns
        assert 'percentiles_iguales' in result.columns
    
    @patch('pandas.read_excel')
    def test_load_and_process_data_error(self, mock_read_excel):
        """Test manejo de errores en carga de datos"""
        mock_read_excel.side_effect = Exception("Error de lectura")
        mock_file = Mock()
        
        result = self.processor.load_and_process_data(mock_file)
        
        # Verificar que retorna None en caso de error
        assert result is None
    
    def test_validate_ranges(self):
        """Test validación de rangos"""
        # Crear datos con valores negativos
        bad_data = self.sample_data.copy()
        bad_data['Durestd Inss min'] = [-5, 20, 25]
        bad_data['Count (Id Episodio)'] = [15, -2, 12]
        
        bad_df = pd.DataFrame(bad_data)
        renamed_df = self.processor._rename_columns(bad_df)
        
        # Convertir a numérico para simular el proceso
        for col in self.processor.numeric_columns:
            if col in renamed_df.columns:
                renamed_df[col] = pd.to_numeric(renamed_df[col], errors='coerce')
        
        validated_df = self.processor._validate_ranges(renamed_df)
        
        # Verificar que se eliminaron los valores negativos
        assert len(validated_df) < len(renamed_df)
        assert all(validated_df['Durestd Inss min'] >= 0)

if __name__ == "__main__":
    pytest.main([__file__])
