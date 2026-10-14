---
titulo: Spring Boot y controladores REST
tema: Controladores REST
fecha_creacion: 2026-10-14
fecha_actualizacion: 2026-10-14
estado: revisado
etiquetas: [spring-boot, controladores, api-rest, responseentity, java]
bloque: spring
fuente: 03-controladores-rest.pdf
paginas: 6
---

# Spring Boot y controladores REST

> **Resumen de material de clase.** Viene del PDF `03-controladores-rest.pdf`
> (6 páginas), que aportó la estudiante. Lo marcado como **material de clase** es lo que
> dice el PDF; el resto es explicación propia.

## 1. De qué va (resumen en cinco líneas)

1. Qué es un **controlador** en Spring: recibe peticiones HTTP, ejecuta la lógica y
   devuelve una respuesta.
2. `@RestController` devuelve **JSON**, `@Controller` devuelve vistas HTML: no es lo
   mismo.
3. Las cuatro formas de recibir datos: `@PathVariable`, `@RequestParam`,
   `@RequestHeader` y `@RequestBody`.
4. `ResponseEntity` deja controlling **estado, cabeceras y cuerpo** de la respuesta.
5. Sirve para construir una API REST con rutas, verbos y códigos HTTP correctos, que es
   el entregable práctico del capítulo.

## 2. Explicación paso a paso

**El guion del PDF, de principio a fin:**

1. **Clase principal** con `@SpringBootApplication` y `SpringApplication.run(...)`: es lo
   que arranca la aplicación.
2. **Objeto de dominio** `Task` con sus getters.
3. **Controlador** `@RestController` con `@RequestMapping("/api/tasks")` y los métodos
   `list`, `create` y `get`.
4. **Probar la API** con `./mvnw spring-boot:run` y los endpoints.
5. **Aprender** cómo se arrancan, cómo se declara un controlador, cómo se devuelve JSON y
   qué hace `ResponseEntity`.

**Los conceptos que introduce el PDF**, uno a uno:

- `@RestController`: devuelve datos JSON, no vistas.
- `@RequestMapping("/api/tasks")`: el punto de entrada de la API.
- `@GetMapping` y `@PostMapping`: los verbos HTTP GET y POST.
- `@RequestBody`: convierte el JSON de entrada en un objeto Java.
- `@PathVariable`: recoge un valor dinámico de la ruta.
- `ResponseEntity`: devuelve la respuesta completa (estado, cabeceras, cuerpo).

**La tabla de códigos que da el material**, y su uso habitual:

| Código | Significado | Uso habitual |
|---|---|---|
| 200 | OK | Petición correcta |
| 201 | Created | Recurso creado (POST) |
| 204 | No Content | Eliminación o actualización sin cuerpo |
| 400 | Bad Request | Error de validación o de formato |
| 404 | Not Found | Recurso inexistente |
| 409 | Conflict | Conflicto de estado o duplicado |
| 422 | Unprocessable Entity | Error semántico |

**Clases vs records**, que el PDF repite como conclusión: entidades con `class`
(mutables, con constructor vacío, para JPA) y DTOs con `record` (inmutables, para
transportar datos).

## 3. Ideas clave del tema

- **En REST la «vista» es el cuerpo JSON.** No hay plantillas: Jackson convierte tus
  objetos Java en JSON automáticamente.
- **Cada método del controlador responde a un verbo HTTP**, y el verbo decide si la
  operación cambia algo (`POST`, `PATCH`, `DELETE`) o solo lo consulta (`GET`).
- **Devolver el objeto directamente es un `200` implícito.** Si necesitas código distinto,
  cabecera `Location` o cuerpo vacío, usa `ResponseEntity`.
- **Los parámetros viajan por sitios distintos**: la ruta (`@PathVariable`), la query
  (`@RequestParam`), las cabeceras (`@RequestHeader`) y el cuerpo (`@RequestBody`).
- **Errores con `@ControllerAdvice` + `@ExceptionHandler`**, para devolver siempre un
  JSON de error uniforme en vez de una página de error genérica.
- **Entregable del capítulo**, según el PDF: 3 endpoints funcionales, `201` en creación,
  `404` en no encontrado, y una colección de pruebas en Insomnia o Postman.

## 4. Ejemplo práctico relacionado con DAW

El controlador mínimo del PDF, reducido a lo esencial:

```java
@RestController
@RequestMapping("/api/tasks")
public class TaskController {

  private final List<Task> tasks = new ArrayList<>();
  private long nextId = 1;

  @GetMapping("/{id}")
  public ResponseEntity<Task> get(@PathVariable Long id) {
      return tasks.stream()
              .filter(t -> t.getId().equals(id))
              .findFirst()
              .map(ResponseEntity::ok)          // encontrado → 200 con la tarea
              .orElse(ResponseEntity.notFound().build());  // no → 404 sin cuerpo
  }
}
```

Esa última línea es la que más cuesta al principio: `.map(...)` + `.orElse(...)` es la
forma de decir «si está, devuélvelo con 200; si no, devuelve 404».

## 5. Código o comandos pequeños comentados

```java
// Clase principal: arranca todo
@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);  // arranque
    }
}
```

```java
// Las cuatro formas de recibir datos, según el PDF
@GetMapping("/{id}")          // @PathVariable: /api/tasks/7
public Task get(@PathVariable Long id) { ... }

@GetMapping                   // @RequestParam: /api/tasks?page=1
public List<Task> list(@RequestParam int page) { ... }

@GetMapping                   // @RequestHeader: lee una cabecera HTTP
public String ua(@RequestHeader("User-Agent") String ua) { ... }

@PostMapping                  // @RequestBody: el JSON de la petición
public Task create(@RequestBody Task t) { ... }
```

```bash
# Arrancar y probar
./mvnw spring-boot:run
curl -s http://localhost:8080/api/tasks
```

Formas de construir una respuesta, tal como las lista el PDF:

```java
ResponseEntity.ok(body);                 // 200 OK
ResponseEntity.status(HttpStatus.CREATED); // 201 Created
ResponseEntity.noContent().build();      // 204 No Content
ResponseEntity.badRequest().body(errorMsg); // 400 Bad Request
```

## 6. Diagrama (Mermaid)

```mermaid
flowchart TD
  A[Cliente: curl, Insomnia, Postman<br/>o el navegador] -->|GET /api/tasks/7| B[Controlador REST]
  A -->|POST /api/tasks + JSON| B
  B --> C{De dónde vienen los datos?}
  C -->|@PathVariable| D[id de la ruta]
  C -->|@RequestParam| E[query: ?done=true]
  C -->|@RequestHeader| F[cabecera HTTP]
  C -->|@RequestBody| G[cuerpo JSON]
  B --> H[ResponseEntity: estado + cabeceras + cuerpo]
  H --> I[200 con datos]
  H --> J[201 + Location al crear]
  H --> K[404 si no existe]
  H --> L[400 si los datos no valen]
```

Y dónde encaja un controlador dentro de la aplicación:

```mermaid
flowchart LR
  A[main] --> B[@SpringBootApplication]
  B --> C[Cliente HTTP]
  C --> D[Controlador REST<br/>@RestController]
  D --> E[Servicio<br/>lógica de negocio]
  E --> F[Repositorio JPA]
  F --> G[(Base de datos)]
  D -->|JSON + código| C
```

## 7. Conceptos con los que se suele confundir

- **`@RestController` ≠ `@Controller`**: el primero devuelve JSON, el segundo devuelve
  vistas (Thymeleaf).
- **`@PathVariable` ≠ `@RequestParam`**: el primero va en la ruta (`/tasks/{id}`), el
  segundo en la query (`?done=true`).
- **`@RequestBody` ≠ `@RequestParam`**: el primero es el cuerpo completo en JSON; el
  segundo, un valor suelto de la query.
- **`ResponseEntity` ≠ devolver el objeto**: devolver el objeto es siempre un `200`
  implícito; `ResponseEntity` te deja elegir código, cabeceras y cuerpo.
- **`201` ≠ `200` al crear**: el `201` además dice dónde está lo creado (`Location`).
- **`404` ≠ `empty`**: si el recurso no existe, es `404`, no un `200` con una lista
  vacía.

## 8. Errores frecuentes

- **Devolver siempre `200`**: obliga al cliente a interpretar el cuerpo para saber qué
  pasó.
- **Olvidarse del `Location` en el `201`**: el cliente no sabe cómo pedir lo que acaba
  de crear.
- **Devolver el `404` con el cuerpo vacío sin querer**: `ResponseEntity.notFound().build()`
  es intencionado; conviene saber cuándo se usa.
- **Usar `@Controller` pensando que devuelve JSON**: devuelve el nombre de una vista y
  falla al serializar.
- **Cargar en el controlador la lógica de negocio**: el PDF separa las responsabilidades
  en capas precisamente para que el controlador sea pequeño y reutilizable.
- **Filtrar datos privados de la entidad**: el material propone un DTO de salida para no
  exponer la entidad tal cual.

## 9. Tres preguntas de repaso

1. ¿Qué diferencia hay entre `@RestController` y `@Controller`, y cuándo se usa cada uno?
2. ¿Para qué sirven `@PathVariable`, `@RequestParam`, `@RequestHeader` y `@RequestBody`?
3. ¿Qué ventaja tiene devolver `ResponseEntity` en lugar de devolver el objeto
   directamente?

### Respuestas

1. `@RestController` devuelve los datos serializados en JSON, así que es lo que se usa en
   una API REST. `@Controller` devuelve el **nombre de una vista** que se resuelve con un
   motor de plantillas como Thymeleaf, y por eso se usa en aplicaciones web con HTML.
   Cuando el PDF dice que «en REST la vista es el cuerpo JSON», quiere decir eso: no hay
   plantilla, el JSON es el resultado.
2. `@PathVariable` recoge un valor que forma parte de la ruta (`/users/{id}`),
   `@RequestParam` un parámetro de la query (`?page=1`), `@RequestHeader` una cabecera
   HTTP, y `@RequestBody` el cuerpo de la petición convertido en objeto Java a partir
   del JSON.
3. Devolver el objeto directamente produce siempre un `200 OK` y una cabecera de
   contenido estándar. `ResponseEntity` te permite decidir **el código, las cabeceras y
   el cuerpo**: por ejemplo `201 Created` con la cabecera `Location` al crear, `204` sin
   cuerpo al borrar, o `404` cuando el recurso no existe. Con eso la respuesta cumple el
   contrato HTTP en vez de parecer siempre igual.

## 10. Términos relacionados

- [Códigos de estado HTTP](../Terminos/codigos-estado.md) — la tabla de códigos del PDF con
  su ficha completa.
- [Métodos HTTP](metodos-http.md) — qué significa exactamente cada verbo que usa el
  controlador.
- [HTTP](../Terminos/http.md) — las peticiones y respuestas que el controlador traduce a
  Java.
- [DTO (Data Transfer Object)](../Terminos/dtos.md) — el `TaskDTO` de salida que evita
  exponer la entidad.
- [Introducción a Spring Boot](introduccion-spring-boot.md) — el mismo proyecto Tasks,
  con servicio y repositorio ya añadidos.
- [Capa de servicio](capa-servicios.md) — el eslabón que va entre el controlador y los
  datos.
- [TDD y MockMvc en la mini API Tasks](tdd-primeros-pasos.md) — cómo se prueban estos
  controladores.

*(Aparecen en el PDF pero aún no tienen ficha: Spring Boot, controlador REST,
`@RestController`, `@Controller`, `@RequestMapping`, `@PathVariable`, `@RequestParam`,
`@RequestHeader`, `@RequestBody`, `ResponseEntity`, `@ControllerAdvice`, JSON, Jackson,
Spring Initializr, capa de servicio.)*

## 11. Fuentes y límites del resumen

- Fuente: PDF `03-controladores-rest.pdf`, «Capítulos 2 bis y 3 – Spring Boot y Controladores
  REST» (páginas 1-6, leídas las 6), aportado por la estudiante. Módulo profesional DWES,
  con una duración estimada de 12-14 horas.
- Fuentes externas: **no consultadas** para este resumen.
- Límites:
  - El PDF se ha leído **extrayendo el texto** con `pdftotext`, sin ver las páginas
    originales: si hay capturas o diagramas, **no los he visto**. El PDF además anuncia
    que tiene una navegación lateral generada automáticamente, que no es relevante aquí.
  - **No he ejecutado** nada: ni la aplicación, ni `curl`, ni las peticiones de prueba. Los
    fragmentos son transcripciones del PDF.
  - Dos líneas de código aparecen **cortadas al extraer el texto**: el `POST` de ejemplo con
    `@Valid` termina en `save` y el apartado de «oti`as formas» empieza con «yas». Es un
    problema de formato del PDF, no del resumen; no he inventado el final.
  - El PDF anuncia que los apartados `service/` y `repo/` se verán más adelante: aquí no se
    desarrollan, solo se mencionan.
  - El diagrama Mermaid **no se ha validado automáticamente**: requiere comprobación
    visual.

## 12. Mis notas

<!-- Sección reservada para la estudiante. No borrar ni sobrescribir. -->