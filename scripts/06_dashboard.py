"""
FASE 6: Crear Dashboard Interactivo
====================================

Objetivo:
- Crear visualizaciones que respondan las 8 preguntas de negocio
- Exportar a HTML interactivo con Plotly
- Generar gráficos estáticos con Matplotlib

Preguntas a responder:
1. ¿Cómo han evolucionado las ventas en el tiempo?
2. ¿Qué países o regiones generan más ingresos?
3. ¿Qué productos tienen mejor desempeño?
4. ¿Qué regiones presentan bajo rendimiento?
5. ¿Qué productos tienen menor impacto en ventas?
6. ¿Qué tipo de clientes generan mayor valor?
7. ¿Existe relación entre ubicación y comportamiento de compra?
8. ¿Qué acciones recomendarías al negocio?
"""

import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os

# Rutas
data_path = "data/analytical/fact_table.csv"
output_html_path = "output/dashboard.html"
output_plots_path = "output/plots"
os.makedirs(output_plots_path, exist_ok=True)


def load_analytical_data():
    """Cargar dataset analítico"""
    print("📊 Cargando dataset analítico...")
    sales_df = pd.read_csv(data_path)
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    print(f"   Datos cargados: {sales_df.shape}")
    return sales_df


def question_1_sales_evolution(df):
    """1. ¿Cómo han evolucionado las ventas en el tiempo?"""
    print("\n📈 Pregunta 1: Evolución temporal de ventas...")
    
    # Agrupar por mes
    temporal_df = df.groupby(df['order_date'].dt.to_period('M'))['sales'].agg(['sum', 'count', 'mean'])
    temporal_df.index = temporal_df.index.to_timestamp()
    
    return temporal_df


def question_2_top_countries_and_regions(df):
    """2. ¿Qué países o regiones generan más ingresos?"""
    print("\n🌍 Pregunta 2: Top países y regiones por ingresos...")
    
    top_countries = df.groupby('country')['sales'].sum().sort_values(ascending=False).head(10)
    top_continents = df.groupby('continent')['sales'].sum().sort_values(ascending=False)
    
    return top_countries, top_continents


def question_3_top_products(df):
    """3. ¿Qué productos tienen mejor desempeño?"""
    print("\n🏆 Pregunta 3: Top productos por ingresos...")
    
    top_products = df.groupby('product_code').agg({
        'sales': 'sum',
        'quantity_ordered': 'sum'
    }).sort_values('sales', ascending=False).head(10)
    
    return top_products


def question_4_low_performance_regions(df):
    """4. ¿Qué regiones presentan bajo rendimiento?"""
    print("\n⚠️  Pregunta 4: Regiones con bajo rendimiento...")
    
    low_performance_regions = df.groupby('region').agg({
        'sales': 'sum',
        'order_number': 'count'
    }).sort_values('sales', ascending=True).head(10)
    
    return low_performance_regions


def question_5_low_impact_products(df):
    """5. ¿Qué productos tienen menor impacto en ventas?"""
    print("\n📉 Pregunta 5: Productos con bajo impacto...")
    
    low_impact_products = df.groupby('product_code')['sales'].sum().sort_values(ascending=True).head(10)
    
    return low_impact_products


def question_6_top_customers(df):
    """6. ¿Qué tipo de clientes generan mayor valor?"""
    print("\n👤 Pregunta 6: Clientes de mayor valor...")
    
    # Top clientes
    top_customers = df.groupby('customer_id').agg({
        'sales': 'sum',
        'order_number': 'count',
        'customer_name': 'first',
        'customer_country': 'first'
    }).sort_values('sales', ascending=False).head(10)
    
    # Segmentación por país
    value_by_country = df.groupby('customer_country')['sales'].sum().sort_values(ascending=False).head(10)
    
    return top_customers, value_by_country


def question_7_location_behavior(df):
    """7. ¿Existe relación entre ubicación y comportamiento de compra?"""
    print("\n📍 Pregunta 7: Relación ubicación-comportamiento...")
    
    # Análisis por país
    location_analysis = df.groupby('country').agg({
        'sales': ['sum', 'mean', 'count'],
        'quantity_ordered': ['sum', 'mean']
    }).round(2)
    
    return location_analysis


def question_8_recommendations(df, top_countries, low_impact_products):
    """8. ¿Qué acciones recomendarías al negocio?"""
    print("\n💡 Pregunta 8: Recomendaciones de negocio...")
    
    recommendations = {
        'top_countries': top_countries.head(3),
        'low_impact_products': low_impact_products.head(3),
        'ingresos_totales': df['sales'].sum(),
        'numero_ordenes': df['order_number'].nunique(),
        'ticket_promedio': df.groupby('order_number')['sales'].sum().mean(),
    }
    
    return recommendations


def create_plotly_dashboard(df):
    """Crear dashboard interactivo con Plotly"""
    print("\n🎨 Creando dashboard interactivo...")
    
    from plotly.subplots import make_subplots
    
    # Crear figura con subplots
    fig = make_subplots(
        rows=3, cols=2,
        subplot_titles=(
            "Sales Evolution",
            "Top 10 Países",
            "Top 10 Productos",
            "Sales by Continent",
            "Order Trend",
            "Sales Distribution"
        )
    )
    
    # 1. Evolución temporal
    df_temporal = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
    df_temporal.index = df_temporal.index.to_timestamp()
    fig.add_trace(
        go.Scatter(x=df_temporal.index, y=df_temporal.values, name='Sales', mode='lines+markers'),
        row=1, col=1
    )
    
    # 2. Top países
    top_countries = df.groupby('country')['sales'].sum().nlargest(10)
    fig.add_trace(
        go.Bar(x=top_countries.values, y=top_countries.index, orientation='h', name='Countries'),
        row=1, col=2
    )
    
    # 3. Top productos
    top_products = df.groupby('product_code')['sales'].sum().nlargest(10)
    fig.add_trace(
        go.Bar(x=top_products.index, y=top_products.values, name='Products'),
        row=2, col=1
    )
    
    # 4. Continentes
    continents = df.groupby('continent')['sales'].sum()
    fig.add_trace(
        go.Pie(labels=continents.index, values=continents.values, name='Continents'),
        row=2, col=2
    )
    
    fig.update_layout(height=1000, title="Emausoft Dashboard", showlegend=False)
    
    return fig


def create_matplotlib_plots(df):
    """Crear gráficos estáticos con Matplotlib"""
    print("📊 Creando gráficos estáticos...")
    
    # Crear figura con múltiples subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Emausoft Dashboard - Sales Analysis', fontsize=16)
    
    # 1. Top países
    top_countries = df.groupby('country')['sales'].sum().nlargest(10)
    axes[0, 0].barh(top_countries.index, top_countries.values)
    axes[0, 0].set_title('Top 10 Countries by Revenue')
    axes[0, 0].set_xlabel('Revenue ($)')
    
    # 2. Top productos
    top_products = df.groupby('product_code')['sales'].sum().nlargest(10)
    axes[0, 1].bar(range(len(top_products)), top_products.values)
    axes[0, 1].set_xticks(range(len(top_products)))
    axes[0, 1].set_xticklabels(top_products.index, rotation=45, ha='right')
    axes[0, 1].set_title('Top 10 Products by Revenue')
    axes[0, 1].set_ylabel('Revenue ($)')
    
    # 3. Continentes
    continents = df.groupby('continent')['sales'].sum()
    axes[1, 0].pie(continents.values, labels=continents.index, autopct='%1.1f%%')
    axes[1, 0].set_title('Sales Distribution by Continent')
    
    # 4. Evolución temporal
    df_temporal = df.groupby(df['order_date'].dt.to_period('M'))['sales'].sum()
    df_temporal.index = df_temporal.index.to_timestamp()
    axes[1, 1].plot(df_temporal.index, df_temporal.values, marker='o')
    axes[1, 1].set_title('Sales Evolution Over Time')
    axes[1, 1].set_xlabel('Date')
    axes[1, 1].set_ylabel('Revenue ($)')
    plt.setp(axes[1, 1].xaxis.get_majorticklabels(), rotation=45)
    
    plt.tight_layout()
    
    return fig


if __name__ == "__main__":
    # Ejecutar pipeline
    print("="*60)
    print("FASE 6: CREAR DASHBOARD")
    print("="*60 + "\n")
    
    # Cargar datos
    df = load_analytical_data()
    
    # Responder las 8 preguntas
    print("\n" + "="*60)
    print("ANALIZANDO LAS 8 PREGUNTAS DE NEGOCIO")
    print("="*60)
    
    df_temp = question_1_sales_evolution(df)
    top_countries, top_continents = question_2_top_countries_and_regions(df)
    top_products = question_3_top_products(df)
    low_performance_regions = question_4_low_performance_regions(df)
    low_impact_products = question_5_low_impact_products(df)
    top_customers, value_by_country = question_6_top_customers(df)
    location_behavior = question_7_location_behavior(df)
    recommendations = question_8_recommendations(df, top_countries, low_impact_products)
    
    print("\n✅ Análisis completado")
    
    # Crear visualizaciones
    print("\n" + "="*60)
    print("CREANDO VISUALIZACIONES")
    print("="*60)
    
    # Plotly (interactivo)
    fig_plotly = create_plotly_dashboard(df)
    fig_plotly.write_html(output_html_path)
    print(f"\n✅ Dashboard interactivo guardado: {output_html_path}")
    
    # Matplotlib (estático)
    fig_mpl = create_matplotlib_plots(df)
    plt.savefig(os.path.join(output_plots_path, "dashboard_static.png"), dpi=300, bbox_inches='tight')
    print(f"✅ Gráficos estáticos guardados: {output_plots_path}/dashboard_static.png")
    
    print("\n" + "="*60)
    print("✅ FASE 6 COMPLETADA")
    print("="*60)
