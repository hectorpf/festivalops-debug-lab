from pathlib import Path
import sys
from contextlib import closing
sys.path.insert(0, str(Path(__file__).parent / "src"))
import pandas as pd
import plotly.express as px
import streamlit as st
from festivalops.database import connect_database
from festivalops.exports import export_csv
from festivalops.filters import filter_by_stage
from festivalops.metrics import (event_rows, next_event_label, capacity_status,
    occupancy_ratio, revenue_for_selection, incident_counts)

st.set_page_config(page_title="FestivalOps", page_icon="🎪", layout="wide")
st.title("FestivalOps · Centro de control")
st.caption("Actuaciones, ocupación, ingresos e incidencias del festival.")
with closing(connect_database()) as connection:
    events = event_rows(connection)
st.subheader("Buscar actuaciones por nombre de escenario")
st.caption("Escribe el nombre completo. Esta búsqueda usa filter_by_stage, igual que la demo D01. No cambia la selección del panel inferior.")
requested_stage = st.text_input("Nombre del escenario", value="Escenario Principal")
searched_events = filter_by_stage(events, requested_stage)
st.write(f"Actuaciones encontradas: {len(searched_events)}")
if searched_events:
    st.dataframe(pd.DataFrame(searched_events)[["artist", "stage", "starts_at"]], hide_index=True)
else:
    st.info("No se encontraron actuaciones con ese nombre.")
st.subheader("Panel por selección de escenarios")
stage_names = sorted({str(row["stage"]) for row in events})
selected = st.multiselect("Escenarios", stage_names, default=stage_names)
filtered = [row for row in events if row["stage"] in selected]
with closing(connect_database()) as connection:
    revenues = revenue_for_selection(connection, selected)
    incidents = incident_counts(connection, [r["event_id"] for r in filtered])
ratio = occupancy_ratio(filtered)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Entradas", f"{sum(r['sold'] for r in filtered):,}".replace(",", "."))
col2.metric("Ingresos", f"{sum(r['revenue'] for r in filtered):,.2f} €")
col3.metric("Ocupación conjunta", "Sin aforo" if ratio is None else f"{ratio:.1f} %")
col4.metric("Próxima actuación", next_event_label(filtered))

st.subheader("Horario y ocupación")
if True:  # Bloque de visualización
    frame = pd.DataFrame(filtered)
    timeline = px.timeline(frame, x_start="starts_at", x_end="ends_at",
                           y="stage", color="genre", hover_name="artist")
    st.plotly_chart(timeline, width="stretch")
    occupancy = frame[["artist", "stage", "sold", "capacity"]].copy()
    occupancy["estado"] = [capacity_status(r["sold"], r["capacity"]) for r in filtered]
    st.dataframe(occupancy, width="stretch", hide_index=True)
else:
    st.info("Sin actuaciones para la selección")
st.subheader("Ingresos por escenario seleccionado")
st.dataframe(pd.DataFrame(revenues, columns=["stage", "revenue"]), width="stretch", hide_index=True)
st.subheader("Incidencias por actuación")
st.dataframe(pd.DataFrame([{"event_id": k, "incidencias": v} for k, v in incidents.items()],
                         columns=["event_id", "incidencias"]), hide_index=True)
st.download_button("Descargar actuaciones filtradas", export_csv(filtered),
                   file_name="festivalops_actuaciones.csv", mime="text/csv")
