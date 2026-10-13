# Glosario

Índice de todas las fichas, en orden alfabético. Los enlaces son Markdown
relativos, así que funcionan en Obsidian y en cualquier otro editor.

- [Angular standalone vs Ng Module](Terminos/angular-standalone-vs-ngmodule.md) — las dos formas de organizar el código de Angular.
- [Backlog](Terminos/backlog.md) — lista ordenada de todo lo que falta por hacer en un proyecto.
- [Bean (Spring Boot)](Terminos/beans-spring.md) — objeto Java que Spring crea y gestiona por ti.
- [CI/CD](Terminos/ci-cd.md) — comprobar y publicar el código automáticamente en cada cambio.
- [Códigos de estado HTTP](Terminos/codigos-estado.md) — número de tres cifras que resume la respuesta del servidor.
- [Directivas de Angular (resumen)](Terminos/directivas-angular.md) — qué son y cuáles se usan a diario, con los bloques `@if`, `@for` y `@switch`.
- [DTO (Data Transfer Object)](Terminos/dtos.md) — clase simple que solo transporta datos.
- [Evolución del protocolo HTTP](Terminos/versiones-http.md) — qué cambió entre HTTP/0.9, 1.0, 1.1, 2 y 3.
- [HTTP](Terminos/http.md) — ficha de demostración, marcada como ejemplo.
- [@Input y @Output con EventEmitter en Angular](Terminos/input-output-eventemitter-angular.md) — cómo un hijo recibe datos del padre y le avisa.
- [Linter](Terminos/linter.md) — programa que analiza el código y avisa de problemas.
- [Merge](Terminos/merge.md) — juntar dos ramas conservando el historial.
- [Merge vs Rebase](Terminos/merge-vs-rebase.md) — las dos formas de juntar ramas y en qué se diferencian.
- [ORM](Terminos/orm.md) — capa que traduce entre objetos y tablas de la base de datos.
- [Pipes en Angular](Terminos/pipes-angular.md) — transformar y formatear valores con el operador `|`.
- [Rebase](Terminos/rebase.md) — reaplicar tus commits sobre otra rama; reescribe la historia.
- [Refactorización](Terminos/refactorizacion.md) — mejorar la estructura interna sin cambiar lo que hace.
- [Signals en Angular](Terminos/signals-angular.md) — estado que avisa a la pantalla cuando cambia.
- [Sniffing](Terminos/sniffing.md) — leer el tráfico de red o generar la documentación de una API.

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
