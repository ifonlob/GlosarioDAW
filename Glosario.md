# Glosario

Índice de todas las fichas, en orden alfabético. Los enlaces son Markdown
relativos, así que funcionan en Obsidian y en cualquier otro editor.

- [Angular standalone vs Ng Module](Terminos/angular-standalone-vs-ngmodule.md) — las dos formas de organizar el código de Angular.
- [Backlog](Terminos/backlog.md) — lista ordenada de todo lo que falta por hacer en un proyecto.
- [CI/CD](Terminos/ci-cd.md) — comprobar y publicar el código automáticamente en cada cambio.
<<<<<<< HEAD
- [Directivas de Angular (resumen)](Terminos/directivas-angular.md) — qué son y cuáles se usan a diario, con los bloques `@if`, `@for` y `@switch`.
- [HTTP](Terminos/http.md) — ficha de demostración, marcada como ejemplo.
- [@Input y @Output con EventEmitter en Angular](Terminos/input-output-eventemitter-angular.md) — cómo un hijo recibe datos del padre y le avisa.
- [ORM](Terminos/orm.md) — capa que traduce entre objetos y tablas de la base de datos.
- [Pipes en Angular](Terminos/pipes-angular.md) — transformar y formatear valores con el operador `|`.
- [Signals en Angular](Terminos/signals-angular.md) — estado que avisa a la pantalla cuando cambia.

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
