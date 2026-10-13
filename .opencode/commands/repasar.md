---
description: Repaso interactivo de términos del glosario
agent: build
---

Repaso guiado por turnos con la estudiante.

## Selección

$ARGUMENTS

## Pasos

1. **Lee `AGENTS.md`**.
2. Interpreta $ARGUMENTS para acotar el repaso:
   - **Sin argumentos (por defecto): repaso global de todos los términos.**
     Lee todas las fichas de `Terminos/` y repasa todas.
   - Un **término** concreto (por ejemplo `/repasar HTTP`).
   - Una **fecha** (por ejemplo `/repasar 2026-10-01`), leyendo `Repasos/AAAA-MM-DD.md`.
3. Si el filtro no coincide con ninguna ficha, dilo y no inventes términos.
   Si solo hay una ficha en `Terminos/`, el repaso global es esa ficha.
4. **Anuncia el alcance** antes de empezar: cuántos términos entran y cuáles.
5. **No muestres todas las soluciones al empezar.** Empieza solo con las preguntas,
   una cada vez.
6. **Haz una pregunta y espera su respuesta.** No sigas hasta que conteste.
   - Si la respuesta es ambigua, pide que la precise.
   - Si no responde, ofrece una pista, no la respuesta.
   - En el repaso global, una pregunta por término. Si son muchos, anuncia el total
     y avanza en el orden de los archivos; puedes recordarle que puede parar cuando
     quiera con `/repasar <término>`.
7. Después de cada respuesta, explica de forma didáctica **qué acertó y qué falló**,
   sin burla, y remite a la sección exacta de la ficha para repasarla.
8. Al final, resumen breve con los puntos fuertes y los que conviene volver a mirar.

## Límites

- **No modifiques ninguna ficha** salvo que la estudiante lo pida expresamente.
- Conserva siempre la sección «Mis notas».
