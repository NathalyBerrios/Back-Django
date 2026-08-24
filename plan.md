Inscripción para chequeo veterinario municipal para perros de razas pequeñas y medianas.

1) Apartado de NegocioProblema:
Actualmente, en las jornadas de atención veterinaria municipal, las personas hacen largas filas con sus mascotas solo para descubrir en la puerta que ya no quedan cupos o que el perro excede el peso permitido por ser de raza grande. Esto causa molestia a los dueños y estrés a los animales.  
Solución:
Un programa en consola que evalúa en el instante si la mascota puede ser ingresada basándose en su peso y en los cupos del día, entregando un veredicto con el motivo exacto si es rechazada.  
Alcance:
El sistema solo procesará las admisiones del día y registrará los resultados. No administrará historiales médicos ni agendará horas para el futuro.  
MoSCoW:
Must: Pedir los datos de la mascota, decidir entre 4 opciones, mostrar el motivo exacto, guardar en JSON y mostrar el resumen final.  
Should: Validar que el usuario no deje el nombre en blanco.  
Could: Mostrar cuántos cupos sobraron al final. 
Won't: Cuentas de usuario con contraseña y base de datos fara futuros chequeos.  

2) Apartado Técnico
Datos de entrada:
Nombre de la mascota: Texto (ingresado con input()).  
Peso de la mascota (kilos): Número entero (convertido con int()).
Cupos disponibles: Número entero (convertido con int()).  
Regla de decisión (4 resultados):Dato inválido: Si el peso ingresado es 0 o negativo.  Rechazo 1: Si los cupos disponibles son 0 (no hay espacio).  Rechazo 2: Si el peso de la mascota es mayor a 15 kilos (excede la capacidad del canil).  
Aceptado: Si hay cupos mayores a 0 y el peso es menor o igual a 15 kilos.  
Paquete externo:
Se utilizará el paquete tabulate para formatear y pasar los registros del JSON a una tabla ordenada en la consola.  
Pantalla web:
Tendrá una sola vista en Django que leerá el archivo datos.json y mostrará en una tabla web el listado final de mascotas aceptadas y rechazadas. 