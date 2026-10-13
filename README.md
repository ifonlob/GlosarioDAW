# Glosario personal de DAW

Glosario de **Desarrollo de Aplicaciones Web** hecho con archivos Markdown y dos
comandos de OpenCode. Todo es texto plano: puedes abrirlo con Obsidian, con un
editor cualquiera o desde una terminal.

## Lo único que necesitas recordar

Un comando para aprender, uno para repasar.

```text
/glosario Cookie
```

Así de simple. El asistente te explica qué es, te dibuja un diagrama y guarda la
ficha. Puedes añadir contexto si quieres:

```text
/glosario Cookie — contexto: el servidor manda una cookie al iniciar sesión
— duda: por qué hace falta si HTTP es sin estado
```

## Estructura

```text
Glosario/
├── AGENTS.md              reglas permanentes (pedagogía, organización, seguridad)
├── README.md              este archivo
├── Glosario.md            índice de fichas, en orden alfabético
├── Entrada/pendientes.md  bandeja opcional para apuntar en clase
├── Plantillas/termino.md  plantilla de cada ficha
├── Terminos/              una ficha por término (http.md es la de ejemplo)
├── Repasos/               un archivo por fecha de repaso
├── Recursos/Imagenes/     imágenes que aportes tú
└── .opencode/commands/    glosario.md y repasar.md
```

## `/glosario` — aprender un término

```
/glosario <término> [- contexto: Y - duda: Z]
```

Qué hace:

1. Comprueba si el término ya existe y **amplía** esa ficha en lugar de duplicarla.
2. Si hay ambigüedad importante, **te pregunta antes** de escribir nada.
3. Crea `Terminos/<termino>.md` con las 12 secciones de la plantilla y
   **al menos un diagrama Mermaid**.
4. Añade el enlace a `Glosario.md` en la lista alfabética.
5. Deja la ficha con `estado: revisado` (no hay flujo de revisión pendiente).
6. En el chat te lo explica por capas: qué es → cómo funciona → diagrama →
   ejemplo mínimo → confusiones típicas → una pregunta de repaso **sin respuesta**.

Ejemplos:

```text
/glosario API
/glosario método GET
/glosario session — contexto: en clase vimos $_SESSION
```

## `/repasar` — ponerte preguntas

```
/repasar                      → repaso global: TODOS los términos, uno a uno
/repaso <término>            → solo ese término
/repaso AAAA-MM-DD            → los términos de ese día
```

Hace **una pregunta y espera tu respuesta**. No suelta las soluciones al empezar;
después te dice qué acertaste, qué fallaste y qué sección releer. No toca las fichas.

Con `/repasar` a secas, te avisa de cuántos términos entran y va uno por uno. Puedes
parar cuando quieras con `/repasar <término>`.

## `Entrada/pendientes.md` (opcional)

Sirve para apuntar en clase un montón de términos sin parar a explicar nada.
Copia el bloque, rellénalo y pásalo tal cual al chat:

```text
/glosario Cookie — contexto: el servidor manda una cookie al
iniciar sesión. Duda: por qué hace falta si HTTP es sin estado.
```

Si no la usas, no pasa nada: `/glosario` funciona igual.

## En Obsidian

1. Abre Obsidian.
2. **Abrir carpeta como repositorio** → selecciona la carpeta `Glosario`.
3. En *Ajustes → Archivos y enlaces*, pon **Nuevo enlace** en «Ruta relativa al
   archivo actual».
4. Activa *Ajustes → Diagramas → Mermaid* para ver los diagramas.

Los enlaces son Markdown estándar (`[HTTP](Terminos/http.md)`), no enlaces
`[[...]]` de Obsidian, así que también funcionan fuera de Obsidian.

## Qué partes requieren tu intervención

- **La sección «Mis notas»** de cada ficha es tuya. No se borra ni se sobrescribe.
- **Contestar el repaso**: el comando pregunta, tú respondes.
- **El contexto de clase y tu duda** son tuyos: si no los escribes, la ficha se hace
  solo con lo que hay en la documentación.

## Comprobaciones y límites

- He comprobado que los **enlaces locales** de los archivos existentes apuntan a
  archivos que existen.
- **No he ejecutado los comandos** (una sesión no puede lanzar OpenCode): la primera
  vez, pruébalo con un término pequeño y mira el resultado.
- **Los diagramas Mermaid no se validan automáticamente.** Ábrelos en Obsidian, en
  GitHub o en <https://mermaid.live> para verlos.
- No he instalado nada ni he tocado tu configuración global. Todo está dentro de
  esta carpeta.
