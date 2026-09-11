# Diccionario de datos de FestivalOps

La fuente es sintética: describe un festival imaginario y no contiene datos personales. El archivo `data/source/festival.sql` permite reconstruir la misma base en cualquier equipo.

## Cómo se relacionan las tablas

```text
stages 1 ─── N events N ─── 1 artists
                 │
                 ├─── N ticket_sales
                 └─── N incidents
```

Una actuación pertenece a un escenario y a un artista. Una actuación puede tener varias ventas y varias incidencias. Esa última relación es importante: unir ventas e incidencias directamente puede multiplicar filas.

## Tablas

### `stages`

Una fila por escenario.

| Columna | Significado |
|---|---|
| `stage_id` | Identificador único del escenario. |
| `name` | Nombre visible. |
| `capacity` | Aforo máximo. |

### `artists`

Una fila por artista o grupo.

| Columna | Significado |
|---|---|
| `artist_id` | Identificador único. |
| `name` | Nombre visible; uno contiene una coma para probar el CSV. |
| `genre` | Género musical usado en filtros y gráficos. |

### `events`

Una fila por actuación programada.

| Columna | Significado |
|---|---|
| `event_id` | Identificador único de la actuación. |
| `stage_id` | Escenario donde se celebra. |
| `artist_id` | Artista programado. |
| `starts_at` | Fecha y hora de inicio en formato ISO. |
| `ends_at` | Fecha y hora de fin en formato ISO. |

### `ticket_sales`

Una fila por lote de entradas vendido para una actuación.

| Columna | Significado |
|---|---|
| `sale_id` | Identificador único de la venta. |
| `event_id` | Actuación a la que pertenece. |
| `quantity` | Número de entradas del lote. |
| `unit_price` | Precio unitario guardado como texto; existe punto y coma decimal. |

### `incidents`

Una fila por incidencia operativa asociada a una actuación.

| Columna | Significado |
|---|---|
| `incident_id` | Identificador único. |
| `event_id` | Actuación afectada. |
| `severity` | Nivel de impacto. |
| `status` | Estado de seguimiento. |
| `summary` | Descripción breve. |

## Reglas que se deben proteger

- las claves primarias no se repiten;
- las claves externas apuntan a filas existentes;
- la fuente SQL permanece intacta;
- la base generada se puede borrar y reconstruir;
- una métrica de ventas no cambia por añadir incidencias;
- fecha y hora completas determinan el orden del programa.
