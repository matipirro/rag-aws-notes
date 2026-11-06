# 📘 AWS Cloud Practitioner Essentials — Notas de estudio

> Curso oficial: AWS Skill Builder · AWS Cloud Practitioner Essentials
> Autor: Matías Pirrone Bruni
> Notas de estudio en progreso.

---

## 🗂️ Índice

- [Módulo 1: Introducción a la nube](#módulo-1-introducción-a-la-nube) ✅
- [Módulo 2: Computación en la nube](#módulo-2-computación-en-la-nube) ✅
- [Módulo 3: Exploración de los servicios de computación](#módulo-3-exploración-de-los-servicios-de-computación) ✅
- Módulos 4-13: pendientes

---

## MÓDULO 1: Introducción a la nube

### Conceptos clave

**Modelo cliente-servidor**
- Cliente envía solicitud (request) → servidor responde (response)
- Es la base de TODAS las APIs REST (lo que ya haces en FastAPI y Spring Boot)
- La nube no reemplaza este modelo, solo da servidores escalables accesibles por internet

**Computación en la nube — definición oficial**
> "Entrega bajo demanda de recursos de las TI a través de internet con precios de pago por uso."

Las 4 partes de la definición:
1. **Entrega bajo demanda** → recursos disponibles en segundos, sin aprovisionamiento largo
2. **Recursos de las TI** → servidores, almacenamiento, bases de datos, redes, AI/ML, etc.
3. **A través de internet** → accedes remoto, no necesitas hardware físico tuyo
4. **Pago por uso** → pagas solo lo que consumes, no contratos fijos largos

### Tipos de despliegue

| Tipo | Qué es | Cuándo usar |
|---|---|---|
| **En la nube** | Todo en AWS | Nuevo producto, flexibilidad total |
| **Local** (on-premise) | Todo en tus servidores físicos | Latencia muy baja, control total |
| **Híbrido** | Mezcla cloud + local | Datos sensibles locales + escalado cloud |

Ejemplo examen: "organismo gubernamental quiere control total pero usar AWS para apps específicas" → **Híbrido**.

### 6 beneficios de la nube de AWS (memorizar)

1. **Pasar de gastos fijos a gastos variables** → pagas por uso real
2. **Beneficiarse de las grandes economías de escala** → AWS compra barato por volumen y te lo pasa
3. **Dejar de hacer conjeturas sobre la capacidad** → escalas según demanda real
4. **Aumentar velocidad y agilidad** → despliegues en minutos vs meses
5. **Dejar de gastar en mantener centros de datos** → AWS gestiona hardware físico
6. **Adoptar enfoque global en minutos** → desplegar en regiones mundo entero sin instalar nada

### Infraestructura global

**Jerarquía (CLAVE para examen):**

```
Región (ubicación geográfica, ej: eu-south-2 Zaragoza)
  └── Zonas de Disponibilidad (AZ, mínimo 3 por región)
        └── Centros de datos físicos (1 o más por AZ)
```

- **Región** = área geográfica grande con mínimo 3 AZs
- **Zona de Disponibilidad (AZ)** = ubicación diferenciada dentro de región, con 1+ data centers con alimentación/redes/conectividad propias
- **Códigos típicos**: `eu-west-1` (Irlanda), `ap-southeast-1` (Singapur), `us-east-1` (N. Virginia), `eu-south-2` (Zaragoza España)

**Alta disponibilidad + Tolerancia a errores:**
- Desplegar en varias AZs → si una AZ cae, las otras siguen
- Desplegar en varias regiones → protección aún mayor (ante catástrofe geográfica)
- "Baja latencia" = responder rápido al usuario porque el servidor está físicamente cerca

### Modelo de responsabilidad compartida (MUY IMPORTANTE)

**AWS es responsable de la "seguridad DE la nube":**
- Hardware físico
- Edificios, data centers
- Red global
- Software de computación/almacenamiento/BBDD/redes

**TÚ eres responsable de la "seguridad EN la nube":**
- Tus datos y quién accede a ellos
- Cifrado de datos en el cliente
- Configuración de IAM (usuarios/permisos)
- Parches del SO SI usas EC2 (IaaS)
- Configuración firewall de tu VPC

**Zona gris: "Varía según el servicio":**
- IaaS (EC2) → TÚ parchas el SO
- PaaS (Lambda, RDS) → AWS parcha el SO
- SaaS (WorkMail, Connect) → AWS gestiona todo

**Regla mental**: cuanto más control tienes tú, más responsabilidad tienes tú.

### Conexión con tu stack real

- APIs REST que haces (FastAPI, Spring Boot) = modelo cliente-servidor puro
- Tu VPS Debian 12 en OVH = concepto equivalente a "instancia" en nube
- Migración BD a Azure (prácticas Gomez Group) = ejemplo real de pasar de local a cloud

---

## MÓDULO 2: Computación en la nube

### Amazon EC2 (Elastic Compute Cloud)

**Qué es**: servicio de servidores virtuales bajo demanda. Las unidades individuales se llaman **instancias**.

**Comparación local vs EC2 (CLAVE para examen):**

| Local tradicional | Amazon EC2 |
|---|---|
| Comprar hardware por adelantado | Lanzar instancia en minutos |
| Esperar entrega física | Disponible inmediatamente |
| Pagar aunque no uses | Pagas solo tiempo de computación activa |
| Capacidad fija | Escalar/desescalar según demanda |
| Tú gestionas instalación/configuración | AWS gestiona el hardware |

### Beneficios de EC2

- **Iniciar, escalar y detener instancias rápidamente**
- **Pagar solo por tiempo de uso activo**
- **Aprovisionar en minutos** (vs semanas de local)
- **Configurar seguridad, redes y almacenamiento** según necesites

### Cómo funciona EC2 (3 pasos)

**PASO 1: Iniciar la instancia (Launch)**

Dos decisiones clave al iniciar una instancia:

| Decisión | Qué define | Ejemplo |
|---|---|---|
| **AMI** (Amazon Machine Image) | Sistema operativo + software preinstalado | Ubuntu 22.04, Amazon Linux, Windows Server, imagen custom con tu stack |
| **Tipo de instancia** | Hardware subyacente: CPU, memoria, red, almacenamiento | `t2.micro` (gratis Free Tier), `m5.large`, `c5.xlarge` |

- La AMI es la **plantilla** del software (equivalente a elegir "qué sistema instalo")
- El tipo de instancia es el **tamaño** del hardware virtual (equivalente a "qué portátil me compro")

**PASO 2: Conectar con la instancia (Connect)**

Tres formas de conectarse (importante para examen):

| Método | Para qué | Caso de uso |
|---|---|---|
| **SSH** (Secure Shell) | Instancias Linux | Lo mismo que haces en tu VPS Debian OVH |
| **RDP** (Remote Desktop Protocol) | Instancias Windows | Acceso gráfico escritorio Windows |
| **AWS Systems Manager** | Linux o Windows | Método seguro y simplificado de AWS, no requiere puertos SSH/RDP abiertos |

- Las aplicaciones también pueden interactuar con los servicios en la instancia a **través de la red** (HTTP, HTTPS, etc.) sin "conectarse" literalmente — por ejemplo, tu API REST que recibe peticiones.
- Systems Manager es la opción recomendada por AWS para producción porque reduce superficie de ataque (no expone SSH/RDP a internet).

**PASO 3: Usar la instancia (Use)**

Una vez conectado puedes:
- Ejecutar comandos
- Instalar software
- Añadir almacenamiento
- Organizar archivos
- Correr tu servidor web, API, base de datos, lo que sea

Es exactamente lo mismo que haces en tu Debian OVH tras hacer SSH.

### Vocabulario clave Módulo 2

| Término | Significado |
|---|---|
| **Instancia** | Servidor virtual individual en EC2 |
| **AMI (Amazon Machine Image)** | Plantilla con SO preinstalado para lanzar instancias |
| **Tipo de instancia** | Tamaño: cuántos CPUs, RAM, red (ej: t2.micro, m5.large) |
| **Tenencia múltiple (multi-tenancy)** | Varias VMs de distintos clientes comparten el mismo hardware físico, aisladas lógicamente. Por defecto en EC2. |
| **Dedicated instances / Dedicated hosts** | Instancias con hardware físico solo para ti (más caro, para compliance) |
| **Stop** | Apagar la instancia. No pagas computación. Puedes volver a arrancarla con mismos datos. |
| **Terminate** | Eliminar la instancia definitivamente. No se recupera. |

### Los 5 tipos de instancias EC2 (TEMA ESTRELLA EXAMEN)

| Tipo | Qué equilibra | Casos de uso típicos |
|---|---|---|
| **Uso general** | CPU + memoria + red (equilibrado) | Servicios web, repositorios de código, cargas impredecibles |
| **Optimizadas para computación** | Mucho CPU | Servidores de juegos, HPC, machine learning, modelado científico |
| **Optimizadas para memoria** | Mucha RAM | Procesamiento datos grandes, análisis, BDs en memoria |
| **Computación acelerada** | GPUs / aceleradores hardware | Cálculos punto flotante, gráficos, deep learning (entrenar modelos) |
| **Optimizadas para almacenamiento** | Alta E/S de disco local | BDs grandes, data warehouses, apps con mucha lectura/escritura disco |

**Truco mental para recordar casos de examen:**

- "Web app básica" / "no sé qué carga" → **Uso general**
- "Videojuegos online" / "cálculo científico" → **Optimizada computación**
- "Base de datos SQL grande" / "analítica" → **Optimizada memoria**
- "Entrenar modelos ML" / "renderizado 3D" → **Computación acelerada**
- "Data warehouse" / "mucho acceso disco" → **Optimizada almacenamiento**

### ⚠️ Trampas típicas en preguntas de tipos de instancia

**Confusión memoria vs almacenamiento:**
- "en tiempo real" / "procesar RÁPIDO" / "consultas rápidas" → **Memoria** (RAM)
- "rendimiento de DISCO" / "almacenado LOCALMENTE" / "data warehouse" → **Almacenamiento** (I/O disco)

**Computación acelerada NO es para analizar datos:**
- Si dice "analizar datos" → nunca es acelerada
- Acelerada = GPUs = entrenar modelos ML, renderizado 3D, cálculos punto flotante

**Palabras literales que te dan la respuesta:**
- Si dice "**disco**" o "**almacenado localmente**" → Almacenamiento
- Si dice "**RAM**" o "**en memoria**" → Memoria
- Si dice "**GPU**" o "**entrenar modelo**" → Acelerada
- Si dice "**procesamiento intensivo**" o "**HPC**" → Computación

### ⚠️ TRAMPA EXAMEN: "Los 3 pilares para lanzar una instancia EC2"

**Respuesta correcta AWS**: AMI + Tipo de instancia + **Almacenamiento**

- ✅ **AMI** → el SO y software base
- ✅ **Tipo de instancia** → CPU, memoria, red
- ✅ **Almacenamiento** → el volumen EBS donde vive el SO (OBLIGATORIO, toda instancia necesita disco para arrancar)

**NO entran como "pilares de lanzamiento"**:
- ❌ Equilibrio de carga (es un servicio aparte, ELB)
- ❌ Permisos (se gestionan después con security groups)
- ❌ Comportamiento de terminación (opcional)

**Error típico de alumno**: pensar que "Permisos" entra en los 3. NO. Para el launch básico son AMI + Tipo + Almacenamiento.

### AMI (Amazon Machine Image) con más detalle

**Qué contiene una AMI:**
- Sistema operativo
- Configuración del almacenamiento
- Tipo de arquitectura (x86, ARM...)
- Permisos de inicio
- Software adicional preinstalado

**3 formas de obtener una AMI (importante examen):**

| Fuente | Qué es | Caso de uso |
|---|---|---|
| **AMI personalizada** | Creada por ti con tus configs + software específico | Tu stack listo para clonar |
| **AMI de AWS preconfigurada** | AWS ofrece imágenes estándar (Amazon Linux, Ubuntu, Windows Server...) | Arranque rápido con SO conocido |
| **AMI de AWS Marketplace** | Proveedores externos venden AMIs con software específico | Soluciones comerciales listas (WordPress optimizado, bases datos, etc.) |

**Beneficio clave: repetibilidad**
- Una vez creada una AMI, puedes lanzar N instancias idénticas
- Entorno uniforme → desarrollo y pruebas coherentes
- Automatización + escalado + menos errores humanos
- Equivalente a: Docker image, pero a nivel máquina virtual completa

### Las 3 formas de aprovisionar recursos AWS (CLAVE EXAMEN)

Todas las interacciones con AWS pasan por **API**. Hay 3 formas de llamarlas:

| Método | Qué es | Ideal para |
|---|---|---|
| **AWS Management Console** | Interfaz web del navegador | Usuarios que prefieren interfaz visual, administración manual |
| **AWS CLI** | Comandos en terminal (Windows/macOS/Linux) | Devs y usuarios avanzados que **automatizan tareas con scripts** |
| **AWS SDK** | Librerías para lenguajes de programación (Python, Java, C++, .NET, etc.) | Devs que **integran AWS dentro de su aplicación** |

**Resumen rápido:**
- "Lo hago yo clicando" → **Console** (web)
- "Lo automatizo con script bash" → **CLI**
- "Lo meto en mi código Python/Java" → **SDK**

### Servicios administrados (managed) vs no administrados (unmanaged)

**Servicios NO administrados (unmanaged)**: EC2 es el ejemplo clásico.
- TÚ gestionas: SO, parches, firewall (Security Groups), configuración, aplicaciones
- AWS gestiona: hardware físico, red, hipervisor
- Más control, más responsabilidad

**Servicios ADMINISTRADOS (managed)**: Lambda, RDS, DynamoDB, S3.
- AWS gestiona: SO, parches, mantenimiento, escalado
- TÚ gestionas: tus datos, código, accesos
- Menos control, menos responsabilidad

**Regla mental**: cuanto más abajo en la pila manda tú, más "no administrado" es.

### 💰 Precios EC2 (TEMA ESTRELLA DEL EXAMEN)

**Las 6 opciones de precios de EC2:**

| Opción | Ahorro vs On-Demand | Cuándo usarla | Trampa clave |
|---|---|---|---|
| **Bajo demanda (On-Demand)** | 0% (precio normal) | Cargas impredecibles, pruebas, desarrollo | Sin compromisos, pagas por uso real |
| **Instancias Reservadas (RI)** | Hasta **75%** | Cargas predecibles 1 o 3 años | Compromiso de familia + región |
| **Instancias Spot** | Hasta **90%** | Cargas tolerantes a interrupción (batch, procesado offline) | AWS puede matarte la instancia cuando quiera |
| **Savings Plans** | Hasta **72%** | Uso regular, flexibilidad entre tipos de instancia | Compromiso $/hora de computación, no instancia específica |
| **Hosts Dedicados** | — | Compliance estricto, licencias que necesitan servidor físico | Servidor físico ENTERO para ti (control total) |
| **Instancias Dedicadas** | — | Aislamiento sin tanto control | Hardware aislado de otras cuentas pero sin elegir servidor |

### 🎯 Trucos para elegir en examen

**"Cargas impredecibles / pruebas / corto plazo"** → **Bajo demanda**

**"Carga constante, misma familia 1-3 años, máximo ahorro"** → **Instancias Reservadas (75%)**

**"Carga que puedo pausar / resumir / batch processing / barato pero puede interrumpirse"** → **Spot (90%)**

**"Quiero ahorro pero con flexibilidad para cambiar tipo de instancia"** → **Savings Plans (72%)**

**"Compliance / licencia por servidor físico"** → **Hosts dedicados**

**"Aislamiento del hardware por otras cuentas pero sin tanto control"** → **Instancias dedicadas**

### 🔄 Hosts Dedicados vs Instancias Dedicadas (confusión típica)

| Aspecto | Hosts Dedicados | Instancias Dedicadas |
|---|---|---|
| Servidor físico | ENTERO para ti | Compartes hardware físico aislado |
| Control ubicación | Total (sabes dónde están tus instancias) | AWS decide dónde |
| Uso típico | Licencias que requieren servidor físico específico (Oracle, Windows BYOL) | Aislamiento de otras cuentas por compliance básico |

### 📋 Las 3 opciones de optimización profunda

1. **Savings Plans** → compromiso $/hora durante 1-3 años. Aplica a EC2 + Fargate + Lambda + SageMaker. Flexible entre tipos de instancia y regiones.

2. **Reservas de capacidad (EC2 Capacity Reservations)** → reservar capacidad en una AZ específica para cargas críticas. **Pagas tarifa bajo demanda** (no es un descuento, es garantía de disponibilidad). Útil para asegurar que puedes lanzar instancias cuando las necesitas.

3. **Instancias Reservadas (RI)** → hasta 75% ahorro con compromiso 1-3 años. AWS aplica descuentos automáticamente a otros tamaños de la misma familia + varias AZs dentro de la región.

### 📈 Escalado EC2 (TEMA ESTRELLA EXAMEN)

**Escalabilidad vs Elasticidad (diferencia clave que preguntan)**

| Concepto | Qué es | Ejemplo |
|---|---|---|
| **Escalabilidad** | Capacidad del sistema para CRECER con el tiempo (planificación largo plazo) | "Preparamos infra para 10x usuarios en 2 años" |
| **Elasticidad** | Ajustar recursos AUTOMÁTICAMENTE en TIEMPO REAL según demanda | "Añadir 5 servidores a las 20:00 cuando sube el tráfico, quitarlos a las 3:00" |

**Tipos de escalado:**

| Tipo | Qué hace | Ejemplo |
|---|---|---|
| **Vertical (scale up)** | Hacer la máquina más POTENTE (más CPU, RAM) | Pasar de t2.micro a m5.large |
| **Horizontal (scale out)** | Añadir MÁS máquinas iguales | Pasar de 2 instancias a 10 instancias |

**En AWS se favorece el escalado HORIZONTAL** porque es más flexible y tolerante a errores (si una muere, las otras siguen).

### 🤖 Amazon EC2 Auto Scaling

Servicio que ajusta automáticamente el número de instancias EC2 según demanda.

**Dos modos de escalado:**

- **Dinámico**: ajusta en tiempo real a las fluctuaciones de la demanda (reactivo)
- **Predictivo**: programa preventivamente las instancias en función de la demanda prevista (proactivo, usa ML)

### Los 3 ajustes del Auto Scaling Group (MEMORIZAR)

| Ajuste | Qué define | Si no lo pones |
|---|---|---|
| **Capacidad mínima** | Nunca bajar de este número de instancias (garantía mínima) | Son las instancias que arrancan al crear el grupo |
| **Capacidad deseada** | Número ideal de instancias para la carga actual | Si no la especificas, por defecto = capacidad mínima |
| **Capacidad máxima** | Límite superior, evita escalar sin control (protege coste) | Auto Scaling nunca lanzará más que esto |

**Ejemplo oficial del curso**: min=4, deseada=6, max=12. Auto Scaling mantiene 6, puede subir hasta 12 si hay picos, nunca baja de 4 (ni siquiera en madrugada).

### 💡 Beneficio clave de Auto Scaling

Como usa instancias EC2 bajo demanda, **solo pagas por las que están corriendo**. En horas valle solo pagas por las mínimas, en horas pico pagas por las de pico. Mejor experiencia + menor coste.

### ⚖️ Elastic Load Balancing (ELB)

**Qué hace**: distribuye automáticamente el tráfico de entrada entre múltiples instancias EC2 (o recursos) para optimizar rendimiento y fiabilidad.

**El punto clave**: es el **único punto de contacto** para todo el tráfico que entra a tu grupo de Auto Scaling. Las peticiones llegan al ELB, y él decide a qué instancia enviarlas.

### 🔗 Relación ELB + EC2 Auto Scaling (confusión típica)

Son **servicios distintos pero complementarios**:

| Servicio | Qué hace |
|---|---|
| **EC2 Auto Scaling** | Ajusta la CANTIDAD de instancias según demanda |
| **ELB** | Distribuye el TRÁFICO entre las instancias que existan |

Trabajan juntos: Auto Scaling añade/quita instancias, ELB redirige tráfico a las instancias disponibles automáticamente.

### 📊 3 beneficios clave de ELB

1. **Distribución eficiente del tráfico** → evita sobrecarga en una sola instancia
2. **Escalado automático** → se ajusta solo cuando Auto Scaling añade/quita backends
3. **Administración simplificada** → separa frontend/backend, gestiona failover y mantenimiento

### 🎯 Métodos de enrutamiento de ELB (pueden preguntar)

| Método | Cómo decide |
|---|---|
| **Round robin** | Reparte cíclicamente (1-2-3-1-2-3...) |
| **Conexión mínima** | Envía al servidor con MENOS conexiones activas |
| **Hash de IP** | Mismo usuario siempre al mismo servidor (sticky sessions por IP) |
| **Tiempo de respuesta mínimo** | Al servidor que responde más rápido |

### 📬 Mensajería y colas: EventBridge, SQS, SNS

#### Monolito vs Microservicios (concepto base)

| Enfoque | Qué es | Problema / Ventaja |
|---|---|---|
| **Monolito** | Todos los componentes acoplados (DB + lógica + UI juntos) | Si uno falla, puede caer TODO. "Acoplamiento estrecho" |
| **Microservicios** | Componentes separados que se comunican por mensajes | Si uno falla, los demás siguen. "Acoplamiento débil" |

AWS promueve microservicios con 3 servicios de mensajería/eventos:

### Los 3 servicios de mensajería (DIFERENCIA CLAVE EXAMEN)

| Servicio | Qué es | Modelo | Caso de uso típico |
|---|---|---|---|
| **Amazon SQS** (Simple Queue Service) | Cola de mensajes punto a punto | 1 productor → cola → 1 consumidor | Procesamiento asíncrono de tareas (tickets de soporte, pedidos) |
| **Amazon SNS** (Simple Notification Service) | Publicación/suscripción (pub/sub) | 1 publicador → tema → N suscriptores | Notificaciones a muchos destinatarios (emails, SMS, Lambda) |
| **Amazon EventBridge** | Enrutador de eventos (bus de eventos) | Eventos de muchas fuentes → reglas → múltiples destinos | Arquitecturas event-driven complejas, integración entre apps |

### 🎯 Cuándo usar cuál (trampa típica examen)

- **Necesito encolar tareas para procesar DESPUÉS** → **SQS**
  (ej: "los tickets llegan rápido, el especialista los va procesando a su ritmo")

- **Necesito notificar a MÚLTIPLES destinatarios lo mismo** → **SNS**
  (ej: "cuando se publica una oferta, notificar a email, SMS y Lambda")

- **Necesito enrutar eventos a diferentes servicios SEGÚN REGLAS** → **EventBridge**
  (ej: "cuando llega un pedido, mandar a pago, inventario, restaurante Y delivery, cada uno en su cola")

### 📝 Analogías que ayudan

- **SQS = buzón de correo**: el cartero deja las cartas, el destinatario las recoge cuando puede. 1 a 1.
- **SNS = megafonía del aeropuerto**: alguien grita por el altavoz y todos los que escuchan reciben el mensaje. 1 a muchos.
- **EventBridge = central de dispatch de policía**: llega un evento (incendio), el dispatcher decide quién va (bomberos + ambulancia + policía) con sus propias reglas.

### 💡 Beneficio común de los 3

**Desacoplamiento**: cada parte de la app puede fallar o estar ocupada SIN bloquear a las otras. Los mensajes se encolan/guardan y se procesan cuando el consumidor esté listo. Esto es la base de "aplicaciones resilientes" en AWS.

### Conexión con tu stack real

- Tu VPS Debian 12 en OVH ≈ instancia EC2 Linux
- Diferencia clave: OVH cobra mensual fijo, EC2 cobra por hora/segundo de uso real
- Cuando despliegues un proyecto RAG en AWS Free Tier, se usa literalmente EC2 bajo demanda (gratis durante 12 meses hasta cierto límite)
- SSH que ya haces en tu VPS → mismo flujo en EC2
- Si usas Lambda para el endpoint RAG en vez de EC2, estarías usando un servicio **administrado** (no tocas SO)

---

---

## MÓDULO 3: Exploración de los servicios de computación

### Los 3 niveles de servicios de computación AWS (CLAVE EXAMEN)

| Nivel | Qué administra AWS | Qué administras tú | Ejemplo |
|---|---|---|---|
| **Sin administrar** (Unmanaged) | Hardware físico + hipervisor | SO, parches, red, firewall, aplicación | **EC2** (máquina virtual pelada) |
| **Administrados** (Managed) | Hardware + SO + parches + mantenimiento (parcial) | Aplicación + algo de configuración | RDS, Elastic Beanstalk |
| **Totalmente administrados / Sin servidor** (Serverless) | TODO incluido el escalado y disponibilidad | SOLO tu código + seguridad del código | **AWS Lambda** |

**Regla mental**: cuanto más "administrado" el servicio, **menos tocas tú pero menos control tienes**.

### 🎯 Concepto Serverless (sin servidor)

**NO significa "sin servidor"** literalmente. Significa que **tú no gestionas servidores** — AWS los pone y los administra por ti, totalmente invisible.

Lo que AWS gestiona en serverless:
- Infraestructura física
- Sistema operativo
- Parches
- Escalado automático (de 0 a miles de instancias según demanda)
- Disponibilidad
- Red

Lo que tú sigues gestionando:
- Tu código
- La seguridad del código
- IAM / permisos del servicio

### Comparación con tu VPS

- Tu VPS Debian 12 OVH = "sin administrar" (tocas SO, parches, firewall)
- EC2 bajo demanda = "sin administrar" (igual que tu VPS pero en AWS)
- Lambda = "serverless" → subes tu función Python, AWS la ejecuta cuando le llamen, no tocas nada más

### 🔥 AWS Lambda (TEMA ESTRELLA EXAMEN)

**Qué es**: servicio de computación serverless (FaaS = Function as a Service). Ejecuta tu código **en respuesta a eventos** sin que tengas que aprovisionar NI administrar servidores.

**Flujo de 4 pasos (memorizar):**

1. **Subes el código** a Lambda → se convierte en una "función Lambda"
2. **Configuras un trigger** (desencadenador): servicios AWS, HTTP, apps móviles, S3 upload, SNS message, API Gateway, EventBridge, etc.
3. **Lambda ejecuta el código** cuando el trigger se dispara. Gestiona TODO: infraestructura, escalado, concurrencia
4. **Pagas solo por tiempo de computación usado** (al milisegundo)

### 💰 Modelo de precios Lambda

- Pagas **al milisegundo** de ejecución
- El coste depende de **cuánta memoria asignas** a tu función (más RAM = más caro pero más rápido)
- **Si no se ejecuta, no pagas nada** (vs EC2 que paga aunque esté idle)
- Primeras **1M peticiones/mes son GRATIS** (Free Tier perpetuo, no solo 12 meses)

### 🎯 Casos de uso típicos Lambda (para examen)

- Procesamiento de archivos cuando se suben a **S3** (ej: redimensionar imágenes)
- Backend de API REST + API Gateway (serverless HTTP API)
- Procesar eventos de **DynamoDB** (streams)
- Tareas programadas con **EventBridge** (cron en la nube)
- Procesamiento asíncrono desde colas **SQS**
- Chatbots (Alexa Skills, Slack bots)
- **Endpoints Claude API** sin servidor (relevante para tu proyecto RAG futuro)

### 📦 Contenedores y orquestación AWS (TEMA ESTRELLA EXAMEN)

**Contenedores vs Máquinas Virtuales:**

| Aspecto | Contenedor (Docker) | Máquina Virtual |
|---|---|---|
| **Qué contiene** | App + dependencias | SO completo + app |
| **Qué comparte** | SO del host | Hipervisor (SO aislado) |
| **Tamaño** | Ligero (MBs) | Pesado (GBs) |
| **Tiempo arranque** | Segundos | Minutos |
| **Portabilidad** | "Funciona igual en todas partes" | Depende del hipervisor |

**Ventaja clave de contenedores**: resuelven el "en mi máquina funciona" porque empaquetan la app con todas sus dependencias, uniforme en dev / test / producción.

### Los 4 servicios AWS de contenedores (CLAVE EXAMEN)

AWS los agrupa en **3 categorías**: orquestación, registro, computación.

| Servicio | Categoría | Qué es |
|---|---|---|
| **Amazon ECS** (Elastic Container Service) | Orquestación | Servicio propio AWS para orquestar contenedores Docker |
| **Amazon EKS** (Elastic Kubernetes Service) | Orquestación | Kubernetes gestionado (open source estándar) |
| **Amazon ECR** (Elastic Container Registry) | Registro | Almacén de imágenes de contenedores (como Docker Hub pero AWS) |
| **AWS Fargate** | Computación | Motor serverless para contenedores (no gestionas servidores) |

### 🎯 ECS vs EKS: diferencia clave

- **ECS** = **propio de AWS** (más simple, buena integración AWS)
- **EKS** = **Kubernetes gestionado** (estándar open source, más complejo pero portátil)

### 🔥 Tipos de inicio ECS y EKS (confusión típica examen)

Tanto ECS como EKS pueden ejecutarse sobre **2 bases**:

| Base | Qué significa | Caso de uso |
|---|---|---|
| **EC2** | Tú gestionas las máquinas donde corren los contenedores | Control total, configuraciones específicas, PYMES |
| **Fargate** | AWS gestiona los servidores (serverless) | Startups, tráfico variable, "quiero olvidarme de servidores" |

**Combinaciones posibles:**
- ECS + EC2 → orquesta tus contenedores en tus EC2
- ECS + Fargate → orquesta sin gestionar servidores
- EKS + EC2 → Kubernetes con tus EC2
- EKS + Fargate → Kubernetes sin gestionar servidores

### 🚢 AWS Fargate (importante)

- Es un **motor de computación serverless** para contenedores
- **NO es un orquestador** (eso es ECS/EKS)
- Funciona CON ECS o EKS
- Pagas solo por los recursos que usan tus contenedores
- No aprovisionas ni administras servidores

**Diferencia clave con Lambda**:
- **Lambda** = ejecuta funciones (código suelto, trigger-based)
- **Fargate** = ejecuta contenedores (apps completas en Docker)

### Conexión con tu stack real

- Ya usas Docker (taskmanager-python con docker-compose + PostgreSQL dockerizado)
- Si subes el proyecto a AWS:
  - **ECS + Fargate**: subes tu imagen Docker a ECR, ECS la orquesta, Fargate corre el contenedor → cero servidores que gestionar
  - **EKS + Fargate**: lo mismo pero con Kubernetes (más complejo, no necesario para tu escala)
- Es el siguiente nivel después de EC2 cuando quieres multiples servicios conectados sin tocar hardware

### 🛠️ 4 Servicios de computación "adicionales" (caen en examen)

| Servicio | Qué hace | Caso de uso típico |
|---|---|---|
| **AWS Elastic Beanstalk** | Despliegue completo de apps web (PaaS). Subes código → auto gestiona infra, escalado, balanceo, salud | Apps web, APIs REST, backends móviles. "Heroku dentro de AWS" |
| **AWS Batch** | Ejecuta trabajos por lotes a gran escala. Programa, escala y asigna recursos automáticamente | Computación científica, análisis financiero, procesado video masivo, entrenar ML, genómica |
| **Amazon Lightsail** | VPS simplificado con precio mensual **predecible** (compute + storage + BD + red) | PYMES, blogs, WordPress, dev/test, aprendizaje cloud. "AWS para principiantes" |
| **AWS Outposts** | Extiende AWS a tu centro de datos LOCAL (nube híbrida). Experiencia AWS idéntica en tu edificio | Compliance estricta, baja latencia local, data residency, modernizar legacy |

### 🎯 Trucos para identificar en examen

- **"Despliegue rápido de app web sin gestionar infra"** → **Elastic Beanstalk**
- **"Procesar millones de archivos / trabajos paralelos"** → **AWS Batch**
- **"Pequeña empresa + precio mensual fijo + VPS simple"** → **Amazon Lightsail**
- **"AWS en mi centro de datos físico / híbrido / cumplir residencia datos"** → **AWS Outposts**

### 💡 Diferencia Elastic Beanstalk vs Lambda vs ECS/Fargate

- **Lambda** = funciones individuales trigger-based (eventos)
- **ECS/Fargate** = contenedores Docker completos
- **Elastic Beanstalk** = aplicación web completa (gestiona TODO: EC2, scaling, LB, monitoring, deploy)
- Elastic Beanstalk es más "mágico": tú solo subes código, él decide qué EC2/LB/Auto Scaling necesitas

### 3 ejemplos reales de uso Lambda (del curso, para examen)

1. **Procesamiento imágenes red social** → usuario sube foto → trigger Lambda → redimensiona + aplica filtros + guarda optimizada en S3
2. **Agregador de noticias personalizado** → usuario abre app → Lambda recupera artículos + aplica lógica personalización + devuelve recomendaciones
3. **Juego online tiempo real** → acción jugador (puntos, logros) → Lambda actualiza tabla clasificación + estado juego → gestiona miles de eventos sin servidores

**Patrón común en los 3**:
- Hay un **evento** que dispara la función
- Carga **variable** (picos imprevisibles)
- Pagar solo por **uso real** = ahorro masivo vs servidor 24/7

### Conexión con tu stack real

- Tu endpoint `/suggest` de taskmanager-python (FastAPI en EC2 teórico) **podría ir en Lambda** → cuando una task llega, Lambda llama a Claude API y responde. No pagas por servidor idle.
- Trade-off: cold start (primera ejecución más lenta ~500ms-1s) + límite de 15 min de ejecución máxima.

---

## 📝 Preguntas tipo examen vistas

### Módulo 1

**Q**: ¿Qué describe mejor el modelo cliente-servidor?
**A**: El cliente envía solicitudes al servidor que las procesa y devuelve respuestas. La nube proporciona recursos de servidor escalables accesibles por internet.

**Q**: Organismo gubernamental quiere control total pero usar AWS para apps específicas.
**A**: Híbrido.

**Q**: Beneficio clave para startup que no puede predecir capacidad del servidor.
**A**: Dejar de hacer conjeturas sobre la capacidad.

**Q**: Infraestructura global AWS para alta disponibilidad (elegir 2).
**A**: Alta disponibilidad + Tolerancia a errores.

**Q**: Diferencia región vs AZ.
**A**: Región = ubicación geográfica con 3+ AZs. AZ = ubicación diferenciada dentro de la región con 1+ data centers.

**Q**: Responsabilidades del cliente según modelo compartido (elegir 2).
**A**: Administración de parches del SO + Cifrado de datos en el cliente.

**Q**: Reducir costes operativos eliminando mantenimiento infraestructura.
**A**: Dejar de gastar dinero en ejecutar y mantener centros de datos.

**Q**: CFO preocupado por costes fijos de la nube.
**A**: La computación en la nube es modelo pay-per-use que reduce costes fijos y da flexibilidad presupuestaria.

---

## 🎯 Trucos para memorizar

**Los 6 beneficios de la nube** → mnemotécnico:
- **GAST**os variables
- **ESCA**lar economías
- **CON**jeturas fuera
- **VEL**ocidad
- **MANT**enimiento fuera
- **GLOB**al en minutos

**Responsabilidad compartida** → regla de 3:
- Hardware/edificio = AWS siempre
- SO/parches/firewall = depende del servicio
- Datos/cifrado/IAM = TÚ siempre

---

## 📅 Progreso

- [x] Módulo 1: Introducción a la nube (23-oct)
- [x] Módulo 2: Computación en la nube (28-oct) ✅
- [x] Módulo 3: Exploración de los servicios de computación (30-oct) ✅
- [ ] Módulo 4: Expansión global
- [ ] Módulo 5: Creación de redes
- [ ] Módulo 6: Almacenamiento
- [ ] Módulo 7: Bases de datos
- [ ] Módulo 8: IA/ML y análisis de datos
- [ ] Módulo 9: Seguridad
- [ ] Módulo 10: Supervisión, conformidad y gobernanza
- [ ] Módulo 11: Precios y soporte
- [ ] Módulo 12: Migración a la nube
- [ ] Módulo 13: Soluciones Well-Architected

---

*Última actualización: 30-oct-2026*
