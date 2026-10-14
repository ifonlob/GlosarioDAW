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

## Resúmenes de clase

Un archivo por PDF de `Entrada/PDF/`. Todos son resúmenes de material de clase.

- [Cliente, servidor y contenido dinámico](Resumenes/cliente-servidor-contenido-dinamico.md) — quién hace qué y por qué validar en el navegador no protege nada.
- [Versiones y estructura de los mensajes HTTP](Resumenes/versiones-y-mensajes-http.md) — petición, respuesta y qué cambia entre HTTP/1.1, 2 y 3.
- [Métodos HTTP](Resumenes/metodos-http.md) — GET, POST, PUT, PATCH, DELETE, HEAD y OPTIONS, con seguridad e idempotencia.
- [Estados de respuesta HTTP](Resumenes/estados-http.md) — elegir el código correcto y saber qué poner en el cuerpo de error.
- [Cabeceras HTTP, contenido, caché y negociación](Resumenes/cabeceras-http-contenido-y-cache.md) — `Accept` frente a `Content-Type`, caché, cookies y CORS.
- [Método HTTP QUERY](Resumenes/query-http.md) — consultas con contenido en lugar de parámetros en la URL.
- [Mecanismos de ejecución del servidor](Resumenes/mecanismos-ejecucion-servidor.md) — CGI, FastCGI, PHP-FPM y proceso persistente.
- [Infraestructura web](Resumenes/infraestructura-web.md) — servidor web, proxy inverso, balanceador y contenedores.
- [Tecnologías e integración](Resumenes/tecnologias-e-integracion.md) — cómo elegir framework y cómo integrar respuestas.
- [TDD mínimo](Resumenes/tdd-minimo.md) — red, green, refactor, fixtures y JUnit.
- [Introducción a Spring Boot](Resumenes/introduccion-spring-boot.md) — starters, autoconfiguración, perfiles y la API Tasks completa.
- [Controladores REST](Resumenes/controladores-rest.md) — `@RestController`, anotaciones de parámetros, `ResponseEntity` y códigos HTTP.
- [Capa de servicio](Resumenes/capa-servicios.md) — dónde vive la lógica de negocio y cómo se traducen sus errores.
- [TDD y MockMvc en la mini API Tasks](Resumenes/tdd-primeros-pasos.md) — probar la capa web con MockMvc y tests de integración.
- [Tests de errores y respuestas coherentes](Resumenes/tdd-manejo-errores.md) — `@ControllerAdvice` y el payload `{ error, message, timestamp }`.

## Para crear una ficha nueva

Escribe en el chat:

```text
/glosario <término> — contexto: <lo que pasó en clase> — duda: <tu duda>
```

El comando comprueba el índice, crea o amplía `Terminos/<termino>.md`, actualiza
esta lista y te explica el término en el chat con un diagrama.

## Para resumir un PDF de clase

Adjunta el PDF al chat y escribe:

```text
/resumir                    → usa el PDF adjunto
/resumir — tema: Nombre del tema
```

El PDF se copia a [Entrada/PDF/](Entrada/PDF/leeme.md), y el comando crea
`Resumenes/<tema>.md` con las 12 secciones, un diagrama Mermaid y tres preguntas de
repaso. Los resúmenes se publican en el apartado **Resúmenes** del sitio.

## Para repasar

```text
/repaso                       → global: todos los términos, uno a uno
/repaso <término | AAAA-MM-DD>
```

Entrada opcional en [Entrada/pendientes.md](Entrada/pendientes.md) para apuntar
en clase sin parar a explicar nada.
