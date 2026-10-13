---
description: Explicar un término del glosario y crear o ampliar su ficha
agent: build
---

Explica el término indicado y deja su ficha al día.

## Término

$ARGUMENTS

## Pasos

1. **Lee `AGENTS.md`** y respétalo (reglas pedagógicas, de organización y seguridad).
2. **Interpreta $ARGUMENTS**. Debe aparecer el **término**. Todo lo demás es opcional:
   - El resto del texto → **contexto de clase** (cítalo como tuyo, nunca como
     afirmación del profesor) o **duda** concreta.
   - **No uses campos de asignatura**: el glosario no los lleva.
   - Si no se entiende qué término es, **pregunta** antes de hacer nada.
3. **Comprueba si el término ya existe** en `Glosario.md` y en `Terminos/`.
   - Si existe, **amplía** esa ficha (no crees otra).
   - Si no existe, créala en `Terminos/nombre-corto-minúsculas-sin-tildes.md`.
4. **Si hay ambigüedad importante** (el mismo término con distinto significado según
   el contexto, o un término demasiado vago), **pregunta antes de escribir**.
5. **Obtén la fecha real del entorno** (por ejemplo `date +%F`) para `fecha_creacion`
   y `fecha_actualizacion`. No la inventes.
6. **Escribe la ficha** siguiendo `Plantillas/termino.md`: frontmatter YAML con las
   5 claves (sin `asignatura`) y las 12 secciones, en ese orden. Reglas de estilo:
   - frases cortas, vocabulario de principiante,
   - **un diagrama Mermaid siempre** (mínimo uno que aporte claridad; si de verdad no
     cabe ninguno, explica por qué en la sección),
   - ejemplo mínimo de 5-10 líneas,
   - tres preguntas de repaso con sus respuestas al final,
   - enlaces a términos relacionados en Markdown relativo.
7. **Actualiza `Glosario.md`**: añade el enlace en la lista alfabética de fichas.
8. **Estado**: usa siempre `estado: revisado`; las fichas no pasan por revisión.
9. **No toques la sección «Mis notas»** de ninguna ficha.
10. Comprueba que los enlaces relativos que has añadido apuntan a archivos existentes.

## Lo que respondes en el chat

Explica el término **en el chat**, de forma didáctica y por capas:

1. **Qué es**, en una frase.
2. **Cómo funciona**, en 3-5 pasos numerados.
3. **El diagrama Mermaid**, mostrando el bloque de código para que lo veas.
4. **Un ejemplo mínimo** relacionado con DAW.
5. **Confusiones típicas**, en dos líneas.
6. **Una pregunta de repaso** para que la pruebes tú (sin respuesta todavía).

Si has consultado fuentes, pon los enlaces al final. Si no has consultado ninguna,
dilo. No inventes referencias, citas ni comprobaciones.

Al final indica: archivo creado o ampliado y si el diagrama necesita comprobación
visual (no se valida automáticamente).
