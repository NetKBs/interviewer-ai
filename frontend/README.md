# Frontend

Interfaz Streamlit para consumir el backend de CIM.

## Ejecutar

Desde la raíz del proyecto:

```bash
streamlit run frontend/app.py
```

## Qué hace

- Sube audio y video de una entrevista.
- Extrae frames del video para el análisis de visión.
- Ejecuta `CIMBackend.process_interview_session`.
- Muestra contacto visual, WPM, transcripción y feedback estructurado.

## Modo demo

Si existen `sample/test_audio.mp3` y `sample/test_video.mp4`, puedes activar el modo demo desde la barra lateral.