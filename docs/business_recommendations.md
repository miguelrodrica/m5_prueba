# Recomendaciones de Negocio
**Fecha:** 20 de abril de 2026

## Propósito
Documento de síntesis con recomendaciones y decisiones estratégicas basadas en análisis de datos.

## Respuestas a las 8 Preguntas

### 1. ¿Cómo han evolucionado las ventas en el tiempo?
**Hallazgo:**
- La tendencia general es creciente entre 2003 y 2005.
- Primer mes del histórico (2003-01): 129,753.60.
- Último mes disponible (2005-05): 457,861.06.
- Pico de ventas mensual: 1,089,048.01 en 2004-11.

**Interpretación:**
- El negocio muestra crecimiento con estacionalidad marcada, especialmente en el cierre de 2004.
- Conviene planificar inventario y campañas para meses de alta demanda.

---

### 2. ¿Qué países o regiones generan más ingresos?
**Hallazgo:**
- Top países por ingresos:
	- United States: 3,627,982.83
	- Spain: 1,215,686.92
	- France: 1,110,916.52
	- Australia: 630,623.10
	- United Kingdom: 478,880.46
- Top regiones por ingresos:
	- Europe: 4,979,272.41
	- Americas: 3,852,061.39
	- Oceania: 630,623.10
	- Asia: 570,671.95

**Implicación:**
- Existe alta concentración en United States y Europe.
- Hay oportunidad de crecimiento en Asia y Oceania con estrategias comerciales locales.

---

### 3. ¿Qué productos tienen mejor desempeño?
**Hallazgo:**
- Top productos por ingresos:
	- S18_3232: 288,245.42
	- S10_1949: 191,073.03
	- S10_4698: 170,401.07
	- S12_1108: 168,585.32
	- S18_2238: 154,623.95

**Implicación:**
- Estos productos deben tener prioridad en stock, promoción y estrategia comercial.
- Son candidatos para bundles y campañas de alto margen.

---

### 4. ¿Qué regiones presentan bajo rendimiento?
**Hallazgo:**
- Regiones con menor ingreso total:
	- Asia: 570,671.95
	- Oceania: 630,623.10

**Recomendación:**
- Ejecutar campañas segmentadas por región para aumentar conversión.
- Revisar portafolio de productos por región y ajustar oferta local.

---

### 5. ¿Qué productos tienen menor impacto en ventas?
**Hallazgo:**
- Productos con menor ingreso:
	- S24_3969: 33,181.66
	- S32_2206: 41,353.43
	- S24_2022: 44,667.16
	- S24_2972: 46,515.92
	- S24_1628: 46,676.51

**Decisión Propuesta:**
- Mantenerlos bajo observación.
- Probar mejora comercial (precio, bundle, promoción) por un periodo definido.
- Si no mejoran, considerar descontinuación gradual.

---

### 6. ¿Qué tipo de clientes generan mayor valor?
**Hallazgo:**
- Los clientes de mayor valor superan 120,000 en ventas acumuladas.
- Top 5 clientes por valor:
	- customer_id 71 (Turkey): 140,950.09
	- customer_id 98 (Serbia): 134,319.04
	- customer_id 90 (Finland): 131,090.50
	- customer_id 31 (Spain): 129,916.78
	- customer_id 32 (Mexico): 126,840.96

**Recomendación:**
- Diseñar estrategia de retención para clientes top.
- Implementar beneficios por valor (ofertas exclusivas, seguimiento preferente).

---

### 7. ¿Existe relación entre ubicación y comportamiento de compra?
**Hallazgo:**
- Sí, hay relación entre ubicación e ingreso acumulado.
- Países con mayor ingreso también concentran más órdenes.
- El ticket promedio por país es relativamente estable entre mercados líderes, con mayor diferencia en volumen total.

**Insight:**
- La principal diferencia viene por cantidad de órdenes y escala de mercado, no por ticket promedio extremo.
- Se recomienda estrategia geográfica basada en volumen y penetración.

---

### 8. ¿Qué acciones recomendarías al negocio?

#### Acciones Inmediatas (0-3 meses)
1. Asegurar stock y campañas para productos top (S18_3232, S10_1949, S10_4698).
2. Lanzar plan de retención para clientes de mayor valor.
3. Crear acciones comerciales específicas en Asia y Oceania.

#### Acciones a Mediano Plazo (3-6 meses)
1. Optimizar portafolio por región según desempeño de productos.
2. Definir metas por país con foco en crecimiento fuera de mercados concentrados.

#### Acciones Estratégicas (6+ meses)
1. Consolidar operación analítica sobre modelo estrella en PostgreSQL.
2. Implementar monitoreo continuo de KPIs con dashboard y alertas.

---

## Métricas Clave

| Métrica | Valor | Tendencia |
|---------|-------|-----------|
| Ingresos Totales | 10,032,628.85 | Creciente con estacionalidad |
| Número de Órdenes | 307 | Estable en periodo analizado |
| Ticket Promedio | 32,679.57 | Estable |
| Productos Activos | 109 | Estable |
| Clientes Activos | 100 | Estable |

---

**Nota:** Resultados calculados desde `data/analytical/fact_table.csv`.
