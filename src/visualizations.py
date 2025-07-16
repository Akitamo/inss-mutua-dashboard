"""
Gestor de Visualizaciones - Dashboard INSS vs Mutua
==================================================

Módulo para crear visualizaciones interactivas del dashboard.
Incluye gráficos matplotlib y plotly, configuración de estilos y leyendas.
"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from typing import Optional, List, Dict, Any
import logging
from config import CONFIG, COLORMAP_CONFIG, TEXTS, MATPLOTLIB_CONFIG

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VisualizationManager:
    """Clase para gestionar visualizaciones del dashboard"""
    
    def __init__(self):
        self.config = CONFIG
        self.colormap_config = COLORMAP_CONFIG
        self.texts = TEXTS
        self.matplotlib_config = MATPLOTLIB_CONFIG
        self._setup_matplotlib()
    
    def _setup_matplotlib(self):
        """Configurar matplotlib con estilos personalizados"""
        plt.rcParams.update(self.matplotlib_config)
    
    def create_comparative_chart(self, df: pd.DataFrame) -> Optional[plt.Figure]:
        """
        Crear gráfico comparativo principal
        
        Args:
            df: DataFrame con datos procesados
            
        Returns:
            Figura de matplotlib o None si hay error
        """
        try:
            if df.empty:
                st.warning("No hay datos para visualizar")
                return None
            
            # Configurar figura
            fig, ax = plt.subplots(figsize=self.config['FIGURE_SIZE'])
            
            # Configurar colormap
            cmap = plt.cm.get_cmap(self.colormap_config['name'])
            
            # Calcular límites
            percentile_cols = ['Minmin', 'P20min', 'P40min', 'P60min', 'P80min', 'P99min']
            available_cols = [col for col in percentile_cols if col in df.columns]
            
            if not available_cols:
                st.error("No se encontraron columnas de percentiles")
                return None
            
            x_min = df[available_cols].min().min()
            x_max = df[available_cols].max().max()
            
            # Márgenes
            left_margin = self.config['LEFT_MARGIN']
            right_margin = self.config['RIGHT_MARGIN']
            ax.set_xlim(x_min - left_margin, x_max + right_margin)
            
            # Calcular alturas proporcionales
            heights = self._calculate_bar_heights(df)
            
            # Crear barras para cada registro
            for idx, (_, row) in enumerate(df.iterrows()):
                self._create_percentile_bars(ax, row, idx, heights[idx], cmap, available_cols)
                self._add_inss_lines(ax, row, idx, heights[idx])
                self._add_labels(ax, row, idx, x_min, x_max, left_margin, right_margin)
            
            # Configurar eje Y invertido
            ax.invert_yaxis()
            
            # Añadir sombreado por diagnóstico
            self._add_diagnosis_shading(ax, df)
            
            # Personalizar gráfico
            self._customize_chart(ax, fig)
            
            # Añadir leyenda
            self._add_legend(ax, cmap)
            
            plt.tight_layout()
            return fig
            
        except Exception as e:
            logger.error(f"Error al crear gráfico: {str(e)}")
            st.error(f"Error al crear visualización: {str(e)}")
            return None
    
    def _calculate_bar_heights(self, df: pd.DataFrame) -> np.ndarray:
        """Calcular alturas proporcionales de barras"""
        if 'Count Episodios' not in df.columns:
            return np.full(len(df), (self.config['MIN_BAR_HEIGHT'] + self.config['MAX_BAR_HEIGHT']) / 2)
        
        counts = df['Count Episodios']
        range_counts = counts.max() - counts.min()
        
        if range_counts == 0:
            return np.full(len(counts), (self.config['MIN_BAR_HEIGHT'] + self.config['MAX_BAR_HEIGHT']) / 2)
        
        scaled_heights = (
            self.config['MIN_BAR_HEIGHT'] + 
            (counts - counts.min()) / range_counts * 
            (self.config['MAX_BAR_HEIGHT'] - self.config['MIN_BAR_HEIGHT'])
        )
        
        return scaled_heights.values
    
    def _create_percentile_bars(self, ax: plt.Axes, row: pd.Series, idx: int, 
                               height: float, cmap: Any, available_cols: List[str]):
        """Crear barras de percentiles para una fila"""
        percentiles = [row[col] for col in available_cols if pd.notna(row[col])]
        
        if len(percentiles) < 2:
            return
        
        # Verificar si hay variación
        if hasattr(row, 'percentiles_iguales') and row.percentiles_iguales:
            # Sin variación - barra gris
            ax.barh(idx, 1, left=percentiles[0]-0.5, height=height, 
                   color=self.config['COLORS']['light_gray'])
            ax.text(percentiles[0] + 1, idx, self.texts['no_variation'], 
                   va='center', fontsize=7, color=self.config['COLORS']['dark_gray'])
        else:
            # Con variación - barras de color
            norm = mcolors.Normalize(vmin=min(percentiles), vmax=max(percentiles))
            
            for i in range(len(percentiles)-1):
                if pd.notna(percentiles[i]) and pd.notna(percentiles[i+1]):
                    color = cmap(norm((percentiles[i] + percentiles[i+1]) / 2))
                    width = percentiles[i+1] - percentiles[i]
                    if width > 0:
                        ax.barh(idx, width, left=percentiles[i], height=height, color=color)
    
    def _add_inss_lines(self, ax: plt.Axes, row: pd.Series, idx: int, height: float):
        """Añadir líneas de INSS (estándar y óptima)"""
        # Línea estándar INSS
        if 'Durestd Inss min' in row.index and pd.notna(row['Durestd Inss min']):
            ax.plot([row['Durestd Inss min']] * 2, [idx - height/2, idx + height/2], 
                   color=self.config['COLORS']['black'], linewidth=1.4)
        
        # Punto óptimo INSS
        if 'Duropt Inss min' in row.index and pd.notna(row['Duropt Inss min']):
            ax.plot(row['Duropt Inss min'], idx, 'o', 
                   color=self.config['COLORS']['blue'], markersize=6)
    
    def _add_labels(self, ax: plt.Axes, row: pd.Series, idx: int, 
                   x_min: float, x_max: float, left_margin: float, right_margin: float):
        """Añadir etiquetas de diagnóstico y caso"""
        # Etiqueta de diagnóstico (izquierda)
        if 'Diagnóstico' in row.index:
            ax.text(x_min - left_margin + 2, idx, row['Diagnóstico'], 
                   va='center', ha='right', fontsize=7)
        
        # Etiqueta de caso y episodios (derecha)
        caso_text = ""
        if 'Caso' in row.index:
            caso_text = str(row['Caso'])
        
        if 'Count Episodios' in row.index and pd.notna(row['Count Episodios']):
            episodios = int(row['Count Episodios'])
            caso_text += f" ({episodios})" if caso_text else f"({episodios})"
        
        if caso_text:
            ax.text(x_max + 5, idx, caso_text, va='center', ha='left', fontsize=7)
    
    def _add_diagnosis_shading(self, ax: plt.Axes, df: pd.DataFrame):
        """Añadir sombreado alterno por diagnóstico"""
        if 'Diagnóstico' not in df.columns:
            return
        
        labels = df['Diagnóstico']
        bounds = labels.ne(labels.shift()).cumsum()
        sizes = df.groupby(bounds).size()
        starts = sizes.cumsum() - sizes
        ends = sizes.cumsum()
        
        for i, (start, end) in enumerate(zip(starts, ends)):
            color = self.config['COLORS']['light_gray'] if i % 2 == 0 else 'white'
            ax.axhspan(start - 0.2, end - 0.2, color=color, alpha=0.2)
            
            if i != 0:
                ax.axhline(start - 0.2, color='gray', linestyle='--', linewidth=0.6)
    
    def _customize_chart(self, ax: plt.Axes, fig: plt.Figure):
        """Personalizar apariencia del gráfico"""
        ax.set_yticks([])
        ax.set_xlabel(self.texts['xlabel'])
        ax.set_title(
            f"{self.texts['main_title']}\n{self.texts['subtitle']}", 
            loc='left'
        )
        
        # Configurar grid
        ax.grid(True, alpha=0.3)
        ax.set_axisbelow(True)
    
    def _add_legend(self, ax: plt.Axes, cmap: Any):
        """Añadir leyenda personalizada"""
        legend_elements = [
            Patch(facecolor=cmap(0.0), label=self.texts['legend_labels']['min']),
            Patch(facecolor=cmap(0.2), label=self.texts['legend_labels']['p20']),
            Patch(facecolor=cmap(0.4), label=self.texts['legend_labels']['p40']),
            Patch(facecolor=cmap(0.6), label=self.texts['legend_labels']['p60']),
            Patch(facecolor=cmap(0.8), label=self.texts['legend_labels']['p80']),
            Patch(facecolor=cmap(1.0), label=self.texts['legend_labels']['p99']),
            Patch(facecolor=self.config['COLORS']['light_gray'], 
                  label=self.texts['legend_labels']['constant']),
            Line2D([0], [0], color=self.config['COLORS']['black'], 
                   linestyle='-', label=self.texts['legend_labels']['standard']),
            Line2D([0], [0], marker='o', color=self.config['COLORS']['blue'], 
                   linestyle='None', markersize=6, label=self.texts['legend_labels']['optimal'])
        ]
        
        ax.legend(handles=legend_elements, loc='lower center', 
                 bbox_to_anchor=(0.5, -0.05), ncol=3)
    
    def create_summary_charts(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Crear gráficos resumen adicionales
        
        Args:
            df: DataFrame con datos procesados
            
        Returns:
            Diccionario con figuras de gráficos resumen
        """
        charts = {}
        
        try:
            # Gráfico de distribución por diagnóstico
            if 'Diagnóstico' in df.columns:
                charts['diagnosticos'] = self._create_diagnosis_distribution(df)
            
            # Gráfico de distribución por género
            if 'Cod Genero' in df.columns:
                charts['genero'] = self._create_gender_distribution(df)
            
            # Gráfico de distribución por edad
            if 'Gr Edad 10' in df.columns:
                charts['edad'] = self._create_age_distribution(df)
            
            # Gráfico de correlación duraciones
            duration_cols = ['Durestd Inss min', 'Duropt Inss min', 'P60min']
            available_duration_cols = [col for col in duration_cols if col in df.columns]
            if len(available_duration_cols) >= 2:
                charts['correlacion'] = self._create_correlation_chart(df, available_duration_cols)
            
        except Exception as e:
            logger.error(f"Error al crear gráficos resumen: {str(e)}")
        
        return charts
    
    def _create_diagnosis_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Crear gráfico de distribución por diagnóstico"""
        diagnosis_counts = df['Diagnóstico'].value_counts().head(10)
        
        fig = go.Figure(data=[
            go.Bar(
                x=diagnosis_counts.values,
                y=diagnosis_counts.index,
                orientation='h',
                marker_color=self.config['COLORS']['primary']
            )
        ])
        
        fig.update_layout(
            title="Top 10 Diagnósticos",
            xaxis_title="Número de Casos",
            yaxis_title="Diagnóstico",
            height=400
        )
        
        return fig
    
    def _create_gender_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Crear gráfico de distribución por género"""
        gender_counts = df['Cod Genero'].value_counts()
        
        fig = go.Figure(data=[
            go.Pie(
                labels=gender_counts.index,
                values=gender_counts.values,
                hole=0.3
            )
        ])
        
        fig.update_layout(
            title="Distribución por Género",
            height=400
        )
        
        return fig
    
    def _create_age_distribution(self, df: pd.DataFrame) -> go.Figure:
        """Crear gráfico de distribución por edad"""
        age_counts = df['Gr Edad 10'].value_counts()
        
        fig = go.Figure(data=[
            go.Bar(
                x=age_counts.index,
                y=age_counts.values,
                marker_color=self.config['COLORS']['secondary']
            )
        ])
        
        fig.update_layout(
            title="Distribución por Grupo de Edad",
            xaxis_title="Grupo de Edad",
            yaxis_title="Número de Casos",
            height=400
        )
        
        return fig
    
    def _create_correlation_chart(self, df: pd.DataFrame, cols: List[str]) -> go.Figure:
        """Crear gráfico de correlación entre duraciones"""
        fig = go.Figure()
        
        # Scatter plot para cada par de variables
        if len(cols) >= 2:
            fig.add_trace(
                go.Scatter(
                    x=df[cols[0]],
                    y=df[cols[1]],
                    mode='markers',
                    name=f'{cols[0]} vs {cols[1]}',
                    marker=dict(color=self.config['COLORS']['primary'])
                )
            )
        
        fig.update_layout(
            title="Correlación entre Duraciones",
            xaxis_title=cols[0] if cols else "X",
            yaxis_title=cols[1] if len(cols) > 1 else "Y",
            height=400
        )
        
        return fig
