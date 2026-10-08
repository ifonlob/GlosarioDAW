# Glosario

Índice de todas las fichas, en orden alfabético. Los enlaces son Markdown
relativos, así que funcionan en Obsidian y en cualquier otro editor.

- [Backlog](Terminos/backlog.md) — lista ordenada de todo lo que falta por hacer en un proyecto.
- [CI/CD](Terminos/ci-cd.md) — comprobar y publicar el código automáticamente en cada cambio.
- [Evolución del protocolo HTTP](Terminos/versiones-http.md) — qué cambió entre HTTP/0.9, 1.0, 1.1, 2 y 3.
- [HTTP](Terminos/http.md) — ficha de demostración, marcada como ejemplo.
- [Linter](Terminos/linter.md) — programa que analiza el código y avisa de problemas.
- [Merge](Terminos/merge.md) — juntar dos ramas conservando el historial.
- [ORM](Terminos/orm.md) — capa que traduce entre objetos y tablas de la base de datos.
- [Rebase](Terminos/rebase.md) — reaplicar tus commits sobre otra rama; reescribe la historia.
- [Refactorización](Terminos/refactorizacion.md) — mejorar la estructura interna sin cambiar lo que hace.

## Para crear una ficha nueva

Escribe en el chat:

```text
/glosario <término> — contexto: <lo que pasó en clase> — duda: <tu duda>
```

El comando comprueba el índice, crea o amplía `Terminos/<termino>.md`, actualiza
esta lista y te explica el término en el chat con un diagrama.

## Para repasar

```text
/repaso                       → global: todos los términos, uno a uno
/repaso <término | AAAA-MM-DD>
```

Entrada opcional en [Entrada/pendientes.md](Entrada/pendientes.md) para apuntar
en clase sin parar a explicar nada.
