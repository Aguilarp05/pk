# Para Karla 🌻

Página personal que Pablo (Juan Pablo Aguilar Varela) le hizo a Karla (Karla Alessandra Sánchez Saviñón). Empezó como un CV en 2025 y en 2026 se convirtió en una página llena de secretos, misiones y easter eggs. Es un regalo: cuidar el tono, no inventar contenido personal y preguntar antes de cambiar lo que Pablo escribió.

## Estado actual (5 de octubre de 2026)

- **Publicada el 5 oct 2026** (cumpleaños 24 de Pablo; ese día se la entregó a Karla). Repo **`Aguilarp05/pk`** (antes `para-Karla`, le cambió el nombre para que no se note). Se subió a **`main`** (Pablo lo pidió) y también a `preview-2026`. Link: https://aguilarp05.github.io/pk/. El `CLAUDE.md` se queda en el repo (decisión de Pablo).
- Los atajos temporales del sudoku (`sudokuprueba` / `sudokulisto`) ya se quitaron. Si se vuelven a necesitar para probar, agregarlos y quitarlos antes de subir.
- **Decisiones que Pablo dejó así a propósito:** "esta carta" y "el cual" en Sobre mí, los tiempos ("año y medio" / "hace dos años"), el cierre "No quiero prometerte…" en Sobre mí aunque se parece a la carta, y las partes del último párrafo de la carta tal como quedaron.
- **La carta 2026** (Agradecimiento): 10 párrafos + el último que termina en "pero quiero que sepas que" y se completa con la firma "Te quiero, siempre 🌻". Escrita el 3 y 5 de octubre.
- **Las Polaroids** (13): arreglo `POLAROIDS` en `index.html`, fotos en `img/polaroid-NN.jpg` (collages: `polaroid-NN-M.jpg`). Al abrir el sobre salen una por una en pantalla completa ("Siguiente" / "Leer la carta") y luego se quedan en un carrusel debajo de la carta. Varias fotos en un elemento = collage (hasta 6). Tocar una foto la abre en grande. `pos` = qué parte de la foto se ve en el cuadro; `fit: "contain"` = se ve completa sobre blanco. Orden: pulsera, collage de su día, sándwich del Seven, atardecer, poemas ("Todo Rima"), clase de pintura (en 2 salen los dos, pero Pablo no las cuenta porque uno sale de fondo), collage "Otro collage de fotooooos", "¿Dónde quedó tu diadema?" → "Oh, ahí está." (van juntas, es un chiste), los dos cuadros del último día del semestre del año pasado, el girasol de Pablo ("mi obra maestra"), el frasco de Mariotte y **la última: la única foto de los dos** (selfie de grupo de cuando se iban conociendo, "Aquí empezamos").
- **Experiencia:** Tortas el Ring dice "2026-20 oct 2026" (renuncia; Karla se entera por la página).
- **Pendiente para después:** carrusel de proyectos (necesita capturas de Ladder y Cáritas con datos de prueba).

## Archivos

- `index.html`: la página 2026 (casi todo vive aquí: HTML, CSS y JS).
- `original.html`: la versión 2025, **congelada**. Solo se le agregaron el botón "🌻 2026 →" y un mensaje la primera vez que se abre: *"Se me hacía feo deshacerme de las palabras de esta persona."* Sigue con la playlist vieja a propósito.
- `eras.js` / `eras.css`: eras de Taylor Swift. `eras.js` se **genera** con `python3 tools/gen_eras.py eras.js`; para cambiar una escena, editar el script y volver a correrlo (no editar el SVG a mano). Solo se descarga cuando se activa.
- `disney.js` / `disney.css`: modo Disney. Solo se descarga cuando se activa.
- `img/kass.jpg`: portada de la playlist (mosaico de Spotify). `img/noche-estrellada.jpg`: La noche estrellada de Van Gogh (dominio público, Wikimedia Commons), solo se carga al activar el fondo.
- Los archivos que se cargan aparte llevan `?v=` para que Safari no use versiones viejas.

## Reglas para trabajar

- **El texto de versiones anteriores no se toca.** `original.html` se queda como está.
- **Al escribir texto que dicte Pablo:** ponerle acentos y puntuación, pero **no cambiar su redacción ni su sentido**. Si algo es ambiguo o se podría mejorar, **proponerlo y preguntar** antes de cambiarlo. Palabras suyas como "jajaj", "lit", "ntp", "chingo", "favs", "vdd" se respetan.
- **Retro:** Pablo pidió opinión honesta después de cada texto (qué transmite, si se puede malinterpretar, cómo conecta con otras partes de la página).
- **Sin emojis** en las pistas de misiones, el botón "El porqué de cada canción", el reto del sudoku ni textos donde él lo pidió. Preguntar antes de agregar emojis nuevos a textos.
- **Estilo:** CV de una sola hoja (sin tarjetas separadas), secciones con líneas finas, colores girasol, girasol arriba a la derecha y peonía abajo a la izquierda. Tipografías: Fraunces (títulos) y Source Sans 3 (texto).
- **Probar** cada cambio con Chrome headless (capturas y `document.title` con resultados). En headless: el scroll suave no avanza, así que usar ventanas altas para capturas; las animaciones se congelan con `getAnimations()`.
- **Todo lo desbloqueado se guarda en `localStorage`** con prefijo `para-karla-`. El botón "↺ Reiniciar todo" (al final de la ventana de misiones) borra todo para probar desde cero.

## Flujo de la página (lo que vive Karla)

1. **Mensaje de bienvenida** (solo la primera vez): "Hello 👋 La página recibió una actualización. ¿La quieres ver?" con opciones 1.- Sí / 2.- 1 / 3.- 2 / 4.- ¿Por qué estás buscando otra opción que no sea sí? (todas son sí). La página está oculta hasta responder.
2. **Página CV** con Sobre mí, Experiencia, Educación, Intereses. Al final una nota: hay **6 Hidden Mickeys** + pista del girasol + botón "💡 Pistas de los otros" (acertijos que se revelan uno por uno; los encontrados se tachan). La nota desaparece al encontrar los 6.
3. **Hidden Mickeys** (6, atributo `data-hm`): girasol, peonía, Kinder "Mi Casita", título "Videojuegos", título "Cine" y pie de página. **Ninguno puede estar dentro de una sección bloqueada.** Al encontrar los 6: sube la página al inicio, se activa el **modo Disney** y se desbloquea el botón de **misiones** (Llave Espada).
4. **Misiones secretas** (21 en total, arreglo `MISSIONS` en `index.html`). Cada una tiene pregunta, pista (todas tienen, sin emojis), respuestas válidas (sin importar mayúsculas ni acentos), un código o recompensa y la frase de Pablo (`reason`).
5. **Misión 21** es secreta: no aparece ni cuenta hasta completar las 20. Al completar la 20 sale "Wowowow, si eran 20… ¿por qué ahora dice 21? 👀" y aparece. Pregunta: "¿Cuál es tu nombre?" → Karla. Frase: "Siempre te he dicho que es un nombre muy lindo."
6. Al resolver la 21: pantalla estilo Smash "¡Un nuevo retador se acerca!" / "¿Pensaste que sería tan fácil?" → **sudoku** → pantalla "¡Felicidades! Tu tiempo" + comparación con el de Pablo → botón "Abrir la carta" → animación del sobre (sello de girasol) → se desbloquea la sección **Agradecimiento** con la carta.

## Misiones (orden fijo)

**La misión 10 SIEMPRE debe ser "¿En qué año y mes nos conocimos?"** (le importa a Pablo).

| # | Pregunta | Respuesta | Recompensa / código |
|---|---|---|---|
| 1 | Encuentra los Hidden Mickeys | (automática) | modo Disney (`disney`) |
| 2 | ¿Cuál es mi número favorito? | 25 | desfile de personajes (`25`) |
| 3 | ¿Cuál es mi anime favorito? (siglas) | fmab | círculo de transmutación (`fmab`) |
| 4 | ¿Cuál es mi constelación favorita? | Orión | cielo nocturno (`orion`) |
| 5 | ¿Qué es lo primero que escribe todo programador? | hello world | página en binario (`hello world`) |
| 6 | ¿Quién es tu artista favorita? | Taylor | eras de Taylor (`taylor`, varias veces cambia de era) |
| 7 | ¿Cómo se les dice a las horas como las 11:11? | espejo | tarjeta de hora espejo (`espejo`) |
| 8 | Mi número favorito + 8 | 33 | caparazón azul (`33`) |
| 9 | ¿Cuál es mi comida favorita? | hamburguesa | desbloquea **Planes a futuro** + lluvia de hamburguesas (`hamburguesa`) |
| 10 | ¿En qué año y mes nos conocimos? | septiembre 2023 | desbloquea la **carta de 2025** (`original.html`) |
| 11 | ¿Cuál es mi equipo europeo favorito? | Arsenal | cañón contra el gallo del Tottenham (`arsenal`) |
| 12 | ¿Canción en la que me basé para el nombre? | Für Elise | toca las primeras notas de Für Elise |
| 13 | ¿Cuál es mi artista favorito? | Mac Miller | desbloquea la **Playlist** |
| 14 | ¿Cuál es mi pintura favorita? | La noche estrellada | fondo de Van Gogh (`vangogh`); frase es un mensaje de Karla del 19 de enero de 2026 |
| 15 | ¿Canción de Taylor que es "mi canción"? | exile | era folklore + Taylor y Bon Iver cantando + Spotify (`exile`) |
| 16 | ¿Cuál es mi libro favorito? | The Outsiders | amanecer + poema "Nothing Gold Can Stay" (`staygold`) |
| 17 | ¿Cuál es mi película favorita? | cualquiera de sus 4 | carrete de Letterboxd (`letterboxd`) |
| 18 | ¿Cuál es mi signo zodiacal? | Libra | tarjeta de Libra + cosas en común con Géminis (`libra`) |
| 19 | ¿Dónde nací? | San Luis Río Colorado | desierto de Sonora (`sonora`) |
| 20 | ¿Cuál es mi planeta favorito? | Neptuno | tarjeta de Neptuno (`neptuno`) |
| 21 | ¿Cuál es tu nombre? (secreta) | Karla | retador + sudoku + carta |

Todas las misiones ya tienen su frase.

## Detalles de cada cosa

- **Secciones bloqueadas:** `<section data-lock="clave">` no se muestra hasta resolver la misión con ese `code`. Hoy: Planes a futuro (`hamburguesa`), Playlist (`macmiller`) y Agradecimiento (`karla`). Al inicio la página termina en Intereses.
- **Desfile de personajes:** apagado hasta escribir "25" (la primera vez salen todos en fila; luego uno por minuto). Personajes: Sora y Pikachu, Isaac, Ed y Al, Luffy (se estira), Anakin→Vader, Ichigo (Bankai), Ted Mosby, Spider-Man, Koro-sensei, Snoopy, Mia y Sebastian (La La Land), Ponyboy/Johnny/Dally. En modo Disney: Mickey, Stitch, Buzz, Olaf, Nemo y Dory, Alegría.
- **Caparazón azul:** se desbloquea con "33"; después 33% de probabilidad en cada desfile. Persigue al personaje que va adelante.
- **Nota de la peonía:** flecha a mano (tipografía Caveat) "Es una peonía, por si cualquier cosa jajaj".
- **Otros easter eggs:** tocar el girasol (gira y suelta pétalos), tocar la peonía (pétalos rosas), cielo nocturno automático de 7 pm a 6 am, horas espejo automáticas, cañón al tocar Londres en el mapa.
- **Modo Disney:** castillo, fuegos artificiales, arco de polvo de hadas, linternas de Enredados, casa de Up, esferas de memoria de Intensamente 1 y 2 (se tocan y dicen la emoción), nenúfares con Tiana y Naveen, Evangeline y el gorro de mago de Mickey sobre el nombre.
- **Fondos que se apagan entre sí:** eras, Disney, Van Gogh, Stay gold y Sonora.
- **Tatuajes a futuro** (en Planes a futuro, debajo del mapa): arreglo `TATTOOS` en `index.html`, mismo carrusel que las Polaroids (fotos de referencia en `img/tatuaje-NN-M.jpg`). Hoy: FMAB (ouroboros / reloj de Ed "Don't forget 3.Oct.10"), Mac Miller (portada de The Divine Feminine), "Algo así, definitivamente." (calavera roja con flores y hongos), "I love you dude. Let it rip" (The Bear, en la mano) y flores en la pierna derecha. Pendientes que mencionó: los de The Bear ("Let it rip").
- **Mi plan** (en Planes a futuro, debajo de los tatuajes): línea de tiempo con el mismo estilo que Experiencia. 2026-2027 trabajar en Ladder y otra app en lo que termina el Tec (conseguir clientes para Ladder); 2026-2027 juntar para un carro; 2026-2030 trabajo que le permita estudiar una maestría y juntar para pagarla.
- **Algún día** (en Planes a futuro, debajo de "Mi plan"): lista sin fecha: viajar a uno de los países (al menos uno antes de 2028), publicar un libro, llevar a su papá a Italia y a un partido de la NFL, ir a todos los conciertos posibles, abrir un restaurante, ser feliz (el último en negritas).
- **Mapa de viajes:** conocidos México y EE. UU.; quiere conocer Alemania, España, Italia, Ecuador y Colombia; Reino Unido en rojo Arsenal ("E IR A UN PARTIDO DEL ARSENAL", punto en Londres). Para un país nuevo: cambiar `wish` a `visited` en `places`.
- **Letterboxd:** perfil `letterboxd.com/juanav5`. Sus 4: La La Land, Spider-Man: Into the Spider-Verse, Good Will Hunting, Star Wars Ep. II. Mención especial: The Holdovers. Cada portada muestra una frase al tocarla. Las portadas se cargan del CDN de Letterboxd.
- **Sudoku:** `PUZZLE`/`SOLUTION` en `index.html` (26 pistas, solución única, resoluble con lógica). Marca en rojo los números que no van (contra la solución), 3 errores = se reinicia todo, los números completos se apagan, botón de pausa que tapa el tablero, cronómetro que solo corre con el sudoku abierto y se guarda. "Empezar de nuevo" reinicia tablero, errores y tiempo. **Tiempo a vencer: 07:07 (el de Pablo)**, en `PABLO`; su captura (`img/sudoku-pablo.jpg`) sale en los resultados y solo se descarga al terminar. Frases: gana Karla "Alaaaaa, ¿cómo le hiciste? Trampa, ¿verdad?", empate "Bruh, qué casualidad.", gana Pablo "Qué te puedo decir, soy bueno en todo.". La nota de Hidden Mickeys dice "6 objetos perdidos" y el contador "Mickeys ocultos" (nunca "Hidden Mickeys" ni emojis en esos textos).

## Playlist "KASS"

- ID: `0cb93Fm3M2uNvASQTl4krv` (reproductor y vinilo conectados con la API de Spotify: el disco gira con la música).
- **El reproductor de Spotify se actualiza solo; la nota del porqué (arreglo `SONGS`) y la portada NO.** Cuando Pablo cambie la playlist: leer la lista con `curl` a `https://open.spotify.com/embed/playlist/<id>` (JSON en `__NEXT_DATA__`, `trackList` y `coverArt`), reconstruir `SONGS` **en el orden de Spotify conservando los porqués existentes**, y si cambió la portada, descargarla a `img/kass.jpg` y subir el `?v=` en el `<img>`.
- Las 18 canciones ya tienen su porqué: Paint By Numbers, BAILE INoLVIDABLE, Se fue la luz, El Tiempo Que Necesites, Stop Crying Your Heart Out, Tenemos Que Hablar, Somewhere Only We Know, Coming Up Roses, Two Ghosts, Come Back to Earth (la primera que intercambiaron, "te pertenece a ti"), tolerate it (la que ella le mandó), Oh, Gemini, fantasmas (Humbe), No Dejes Que…, Please Please Please, DtMF, Matilda, Carla's Song (cierra).
- *Two Ghosts* es delicada (amor platónico que no llegó a nada); el texto quedó en tono de cariño, sin reproche.

## Ideas a futuro

- **Carrusel de proyectos** (sección "Proyectos" después de Educación): Ladder POS (destacado, en uso en Tortas El Ring), App de Brigadas Médicas Cáritas y Para Karla. Captura dentro de un marco (laptop / iPad / navegador), ícono en una esquina, descripción y etiquetas. Íconos: `POS-Ladder/electron/assets/Ladder_logo.ico` y `RetoCaritasmTC2007B/Reto/Reto/Assets.xcassets/LogoCaritas.imageset/LogoCaritas.png`. Faltan capturas con datos de prueba.
- **Versión de cada año:** copiar `index.html` a `2026.html` al empezar la de 2027; el botón de versión se vuelve selector 2025 · 2026 · 2027. Cada versión con su edad y © fijos. Revisar cada año: edad, trabajos, educación (el Tec termina en 2027), canciones, películas, países, playlist.
- Imagen de vista previa (`og:image`) para WhatsApp.
- Cuando conozca un país nuevo, pasarlo a amarillo; si va a un partido del Arsenal, festejarlo en la página.
