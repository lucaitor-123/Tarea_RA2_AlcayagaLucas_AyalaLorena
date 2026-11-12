"""Genera tablas estadísticas y gráficos a partir de mediciones verificadas."""
from pathlib import Path
import argparse
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

NOMBRE_CSV = "datos_experimentales_AlcayagaLucas_AyalaLorena.csv"
RESUMEN_CSV = "resumen_estadistico_AlcayagaLucas_AyalaLorena.csv"
DISTRIBUCIONES = ["Aleatorio", "Ordenado Ascendente", "Ordenado Descendente", "Con Repetidos"]
KS = ["k=1", "k=n/2", "k=n"]


def cargar_y_procesar_datos(archivo=NOMBRE_CSV):
    df = pd.read_csv(archivo)
    columnas = {"algoritmo", "n", "tipo_datos", "k_etiqueta", "repeticion", "tiempo_ms", "comparaciones", "orden_teorico", "validado"}
    faltan = columnas - set(df.columns)
    if faltan:
        raise ValueError(f"El CSV no es el nuevo protocolo; faltan columnas: {sorted(faltan)}")
    if not df["validado"].astype(str).str.lower().eq("true").all():
        raise ValueError("Hay mediciones no validadas")
    claves = ["algoritmo", "n", "tipo_datos", "k_etiqueta"]
    resumen = df.groupby(claves, as_index=False).agg(
        repeticiones=("tiempo_ms", "size"),
        tiempo_prom_ms=("tiempo_ms", "mean"),
        tiempo_std_ms=("tiempo_ms", "std"),
        comparaciones_prom=("comparaciones", "mean"),
        comparaciones_std=("comparaciones", "std"),
        orden_teorico=("orden_teorico", "first"),
    )
    return df, resumen


def _grafico(sub, campo, titulo, etiqueta, destino):
    if sub.empty:
        return
    fig, ax = plt.subplots(figsize=(9, 5.5))
    sns.lineplot(data=sub, x="n", y=campo, hue="algoritmo", marker="o", ax=ax, linewidth=2)
    ax.set_xscale("log")
    if (sub[campo] > 0).all():
        ax.set_yscale("log")
    ax.set_title(titulo)
    ax.set_xlabel("Tamaño de entrada n (escala logarítmica)")
    ax.set_ylabel(etiqueta)
    ax.grid(True, which="both", ls="--", alpha=.35)
    fig.tight_layout()
    fig.savefig(destino, dpi=180)
    plt.close(fig)
    print("Guardado:", destino)


def generar_graficos(resumen):
    sns.set_theme(style="whitegrid")
    for dist in DISTRIBUCIONES:
        for k in KS:
            sub = resumen[(resumen["tipo_datos"] == dist) & (resumen["k_etiqueta"] == k)]
            sufijo = f"{dist.lower().replace(' ', '_')}_{k.replace('=', '').replace('/', '_')}"
            _grafico(sub, "tiempo_prom_ms", f"Tiempo vs n | {dist} | {k}",
                     "Tiempo promedio (ms)", f"grafico_tiempo_{sufijo}.png")
            _grafico(sub, "comparaciones_prom", f"Comparaciones reales vs n | {dist} | {k}",
                     "Comparaciones promedio", f"grafico_comparaciones_{sufijo}.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--archivo", default=NOMBRE_CSV, help="Archivo de datos validados")
    args = parser.parse_args()
    if not Path(args.archivo).exists():
        raise SystemExit(f"No existe {args.archivo}. Ejecuta primero python experimento.py")
    df, resumen = cargar_y_procesar_datos(args.archivo)
    resumen.to_csv(RESUMEN_CSV, index=False)
    print(f"Filas: {len(df)} | combinaciones: {len(resumen)} | repeticiones: {sorted(resumen.repeticiones.unique())}")
    if len(resumen) < 180 or not (resumen.repeticiones == 10).all():
        print("AVISO: protocolo incompleto para entrega (se esperan 180 combinaciones y 10 repeticiones).")
    generar_graficos(resumen)
