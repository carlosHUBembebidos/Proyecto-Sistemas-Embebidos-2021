from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
import time, re, os
from serial import*

GPIO.setwarnings(False)
ser = Serial('/dev/ttyACM0', 9600)

#Obtengo los valores de fecha y hora actual
fecha = (time.strftime("%d/%m/%y"))
hora = (time.strftime("%I/%M"))
print(fecha)
print(hora)

reserv = "Reservaciones.txt"


Request = None
class RequestHandler_httpd(BaseHTTPRequestHandler):
    def do_GET(self):
        global Request
        messagetosend = bytes('Solicitando conexion',"utf")
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Content-Length', len(messagetosend))
        self.end_headers()
        self.wfile.write(messagetosend)
        Request = self.requestline
        Request = Request[5 : int(len(Request)-9)]
                
        cod = str(Request[0])
        print(cod)
        
        
##Codigo definitivo para el ingreso al parquedaero
        if cod == "i":
            archivoLec = open("Reservaciones.txt", "r")
            datosArchivo = archivoLec.readlines()
            archivoLec.close()
            
            datos = re.split(r'[,]', Request)
            CI = datos[1]
            
            fechaActual = (time.strftime("%d/%m/%Y"))    #obtengo la fecha atual
            horaActual = (time.strftime("%H/%M"))       #obtengo la hora actual
            datosFechaActual = re.split(r'[/]', fechaActual)    #separo la fecha en una listade strings
            diaActual = int(datosFechaActual[0])                #solamente tomo el día actual para verificar el tiempo limite paa eliminar reservaciones
            
            datosHoraActual = re.split(r'[/]', horaActual)    #separo la fecha en una listade strings
            horaActual = int(datosHoraActual[0]+"00")
            minActual = int(datosHoraActual[1])
            
            #Defino las variables para contar aquellas reservacioines que coincidan con la cedula
            contDatIni = 0
            contDatNotIn = 0
            contDatIn = 0
            diaEquivocado = 0
            diaCorrect = 0
            horaEquivocada = 0
            horaCorrect = 0
            tarde = 0
            
            for i in datosArchivo:
                contDatIni = contDatIni + 1       #Voy contando el total de datos existentes en el archivo
                if CI not in i:
                        contDatNotIn = contDatNotIn + 1    #Voy contando cuantos datos no contienen ese numero de cedula
                elif CI in i:
                    contDatIn = contDatIn + 1    #Voy contando cuantos datos contienen ese numero de cedula
                    datosList = re.split(r'[,]', i)    #Necesito tenerel string definitivo que se transmitirá de la app a la raspberry
        
                    diaReserv = int(datosList[8])
                    horaEnt = int(datosList[4])
                    horaSal = int(datosList[5])
                    parqueadero = datosList[2]
                    tarifa = int(datosList[9])
                    puesto = int(datosList[3])
                    if diaReserv == diaActual:
                        diaCorrect = diaCorrect + 1
                        if horaActual <= horaSal and (horaActual >= ((horaEnt - 100)+50)):   #Controlamos que el usuario pueda ingresar  al parqueadero hasta con 10 minutos de anticipacion y a cualquier hora hasta la hora de salida
                            horasTotales = ((horaSal/100)-(horaEnt/100))
                            valorCancelar = horasTotales*tarifa
                            horaCorrect = horaCorrect + 1
                            print("Usted ha reservado el puesto: %.0f\nTiene un tiempo de %.0f hora(s)\nSu valor a cancelar es de %.0f dolares\nPor favor, para ingresar al parqueadero cancele el monto total"% (puesto, horasTotales, valorCancelar))
                        elif horaActual <= horaEnt and minActual < 50:   #Verificamos si esta intentando ingresar con mas de 10 minutos de anticipación
                            horaEquivocada = horaEquivocada + 1
                        elif horaActual > horaSal:                    #Verificamos si esta intentado ingresar luego del tiempo reservado
                            tarde = tarde +1
                    else:
                        diaEquivocado = diaEquivocado + 1
                    
            if contDatIni == contDatNotIn and contDatIni != 0:
                print("No tiene reservaciones ingresadas")
            
            elif horaCorrect != 0:          #Si es diferente de cero indica que si esta registrada una reservacion con esa cedula
                print("Bienvenido al Parqueadero %s"% parqueadero)    #Debemos de enviar la orden de abrir la baranda a través de comunicación serial OJOJOJOJOJOJOJO
                
                try:
                    while True:
                        comando = str("e")
                        comandoBytes = comando.encode()
                        print(comandoBytes)
                        ser.write(comandoBytes)
                        time.sleep(0.1)
                        read = ser.readline()
                        print(read)

                finally:
                    ser.close()
                
            
            elif contDatIn == tarde and contDatIn != 0:
                print("Su reservación ha expirado")
                
            elif contDatIn == diaEquivocado or contDatIn == horaEquivocada:
                if contDatIn != 0:
                    print("Su reservación se guardó para el día %.0f desde las %.0f H hasta las %.0f H" %(diaReserv, horaEnt, horaSal))
             
            elif contDatIn == (diaEquivocado + tarde):
                if contDatIn != 0:
                    if tarde == 0:
                        print("Usted tiene %.0f reseraciones pendientes" %contDatIn)
                    elif tarde >= 1:
                        print("Usted tiene %.0f reservaciones expiradas y otras pendientes" %tarde)
            elif contDatIn == (diaEquivocado + horaEquivocada):
                if contDatIn != 0:
                    print("Usted tiene %.0f reseraciones pendientes" %contDatIn)
                
            
#Código para la salida del parqueadero.
        if cod == "o":
            print(Request)
            archivoLec = open("Reservaciones.txt", "r")
            datosArchivo = archivoLec.readlines()
            archivoLec.close()
            
            datos = re.split(r'[,]', Request)
            CI = datos[1]
            
            fechaActual = (time.strftime("%d/%m/%Y"))    #obtengo la fecha atual
            horaActual = (time.strftime("%H/%M"))       #obtengo la hora actual
            datosFechaActual = re.split(r'[/]', fechaActual)    #separo la fecha en una listade strings
            diaActual = int(datosFechaActual[0])                #solamente tomo el día actual para verificar el tiempo limite paa eliminar reservaciones
            
            datosHoraActual = re.split(r'[/]', horaActual)    #separo la fecha en una listade strings
            horaActual = int(datosHoraActual[0]+"00")
            minActual = int(datosHoraActual[1])
            
            
            
            archivoEsc = open("Reservaciones.txt", "w")
            
            for i in datosArchivo:
                if CI not in i:
                        archivoEsc.write(i)
                elif CI in i:
                    datosList = re.split(r'[,]', i)
                    diaReserv = int(datosList[8])
                    horaEnt = int(datosList[4])
                    horaSal = int(datosList[5])
                    if horaActual <= horaSal and horaActual >= horaEnt:
                        print("Gracias por su visita")
                        try:
                            while True:
                                comando = str("s")
                                comandoBytes = comando.encode()
                                print(comandoBytes)
                                ser.write(comandoBytes)
                                time.sleep(0.1)
                                read = ser.readline()
                                print(read)

                        finally:
                            ser.close()
                            
                    elif horaActual > horaSal:
                        archivoEsc.write(i)
                        print("Límite de tiempo reservado sobrepasado.")
                    else:
                        archivoEsc.write(i)
            archivoEsc.close()

###Código para eliminar reservaciones hasta con 2 horas de anticipación
        if cod == 'e':
            fechaActual = (time.strftime("%d/%m/%Y"))    #obtengo la fecha atual
            horaActual = (time.strftime("%H/%M"))       #obtengo la hora actual
            
            datosFechaActual = re.split(r'[/]', fechaActual)    #separo la fecha en una listade strings
            diaActual = int(datosFechaActual[0])                #solamente tomo el día actual para verificar el tiempo limite paa eliminar reservaciones
            
            datosHoraActual = re.split(r'[/]', horaActual)    #separo la fecha en una listade strings
            horaActual = int(datosHoraActual[0]+"00")
            print(horaActual)
            
            archivoLec = open("Reservaciones.txt", "r")
            datosArchivo = archivoLec.readlines()
            archivoLec.close()
            
            datos = re.split(r'[,]', Request)
            CI = datos[1]
            placa = datos[2]
            
            archivoEsc = open("Reservaciones.txt", "w")
            contDatIni = 0     #Cuento cuantos datos voy leyendo
            contDatFin = 0     #Cuento cuantos datos han sido leiodos y dejados intactos
            contResElim = 0    #Cuento cuantas reservaciones que cuentan con ese numero de cedula y placa hansido eliminadas
            
            for i in datosArchivo:
                contDatIni = contDatIni + 1
                if CI not in i:
                    if placa not in i:
                        archivoEsc.write(i)
                        contDatFin = contDatFin + 1
                    elif placa in i:
                        archivoEsc.write(i)
                        contDatFin = contDatFin + 1
                elif CI in i and placa not in i:
                    archivoEsc.write(i)
                    contDatFin = contDatFin + 1
                elif CI in i and placa in i:
                    i = i.split(",")                    
                    if int(i[8]) == diaActual:
                        if horaActual <= (int(i[4])-200):
                            contResElim = contResElim + 1
                        elif horaActual > (int(i[4])-200):
                            print("Puede eliminar su reservación hasta 2 horas antes de la hora de entrada")
                            archivoEsc.write(','.join(i))
                            contDatFin = contDatFin + 1
                    elif int(i[8]) <= diaActual:
                        contResElim = contResElim + 1
                        
            if contResElim != 0:
                print("Se ha eliminado: %.0f Reservacion" % (contResElim))
            elif contDatFin == contDatIni and contDatFin != 0:
                print("No se ha podido eliminar su reservación")
            archivoEsc.close()

###Código definitivo para agregar reservaciones###
        if cod == 'c':
            archivo = open("Reservaciones"+".txt", "a")
            archivo.close()
            datos = re.split(r'[,]', Request)
            
            fechaActual = (time.strftime("%d/%m/%Y"))    #obtengo la fecha atual
            horaActual = (time.strftime("%I/%M"))       #obtengo la hora actual
            
            datosFechaActual = re.split(r'[/]', fechaActual)    #separo la fecha en una listade strings
            anoActual = int(datosFechaActual[2])
            mesActual = int(datosFechaActual[1])
            diaActual = int(datosFechaActual[0])
            diaMax = diaActual + 1
            
            CI = datos[1]
            placa = datos[2]
            sitio = datos[3]
            puesto = datos[4]
            entrada = int(datos[5])
            salida = int(datos[6])
            fechaA = int(datos[7])
            fechaM = int(datos[8])
            fechaD = int(datos[9])
            tarifa = int(datos[10])
            
            lectura = open("Reservaciones.txt", "r")   #abro mi archivo en modo lectura para leer las reservaciones ingresadas
                    
            contGeneral = 0
            contSitioDisp = 0
            contHorarioOcu = 0
            contSitioExistente = 0
            contadorHorarioDisp = 0
            contTotPuestosEx = 0
            contTotPuestosDisp = 0
            noHayReserv = 0
            contGeneral1 = 0
            
            if anoActual == fechaA:
                if mesActual == fechaM:
                    if fechaD == diaActual or fechaD == diaMax:    #Pimero verifico que la reservación se este intentando realizar para el mismo año, mes y hasta con un día de anticipación
                        for i in lectura:                          #Recorro losdatos de mi archivo para comparar las reservaciones ealizadas con la nueva
                            i = i.split(",")
                            contGeneral1 = contGeneral1 + 1        #Voy contando uantos datostotales voy recorriendo
                            if fechaD == int(i[8]):                #comparo con las reservaciones por fecha
                                contGeneral = contGeneral + 1      #Cuento cuantas reservaciones son para un dia en especifico
                                if sitio == i[2]:                  #Verifico si un sitio ya tiene reservaciones
                                    contSitioExistente = contSitioExistente + 1       #Cuento cuantos sitios ya tienen resevaciones
                                    if i[3] == puesto:                                #si un sitios ya tiene reservaciones, comruebo si un puesto ya esta ocupado
                                        contTotPuestosEx = contTotPuestosEx + 1       #Cuento cuantas veces es puesto ya esta ocupado
                                        if entrada < int(i[4]) and salida <= int(i[4]):        #verifico si que el horario elegido no este ocupado o se cruce con otro
                                            contadorHorarioDisp = contadorHorarioDisp + 1      #Cento cuantos estan disponibles
                                        elif entrada >= int(i[5]) and salida > int(i[5]):
                                            contadorHorarioDisp = contadorHorarioDisp + 1
                                        else:
                                            contHorarioOcu = contHorarioOcu + 1
                                    else:
                                        contTotPuestosDisp = contTotPuestosDisp + 1
                                else:
                                    contSitioDisp = contSitioDisp + 1
                            else:
                                noHayReserv = noHayReserv + 1
                    else:
                        print("Solo puede reservar puestos hasta con un día de anticipación")
                else:
                    print("Solo puede agregar reservaciones para el mes en curso")
            else:
                print("Solo puede agregar reservaciones para el año en curso")

            lectura.close()
            
            if noHayReserv == contGeneral1 and noHayReserv != 0:
                datoGuardar = [CI, placa, sitio, puesto, str(entrada), str(salida), str(fechaA), str(fechaM), str(fechaD), str(tarifa)]
                datoGuardar = ','.join(datoGuardar)
                print(datoGuardar)
                f = open("Reservaciones.txt", "a")
                f.write("\n")
                f.write(datoGuardar)
                f.close()
                print("Se registró su reservación con éxito")

            elif contSitioDisp == contGeneral and contGeneral != 0:
                datoGuardar = [CI, placa, sitio, puesto, str(entrada), str(salida), str(fechaA), str(fechaM), str(fechaD), str(tarifa)]
                datoGuardar = ','.join(datoGuardar)
                print(datoGuardar)
                f = open("Reservaciones.txt", "a")
                f.write("\n")
                f.write(datoGuardar)
                f.close()
                print("Se registró su reservación con éxito")
                
            elif contTotPuestosDisp == contSitioExistente and contTotPuestosDisp != 0:
                datoGuardar = [CI, placa, sitio, puesto, str(entrada), str(salida), str(fechaA), str(fechaM), str(fechaD), str(tarifa)]
                datoGuardar = ','.join(datoGuardar)
                print(datoGuardar)
                f = open("Reservaciones.txt", "a")
                f.write("\n")
                f.write(datoGuardar)
                f.close()
                print("Se registró su reservación con éxito")
                
            elif contTotPuestosEx == contadorHorarioDisp and contadorHorarioDisp != 0 and contHorarioOcu == 0:
                datoGuardar = [CI, placa, sitio, puesto, str(entrada), str(salida), str(fechaA), str(fechaM), str(fechaD), str(tarifa)]
                datoGuardar = ','.join(datoGuardar)
                print(datoGuardar)
                f = open("Reservaciones.txt", "a")
                f.write("\n")
                f.write(datoGuardar)
                f.close()
                print("Se registró su reservación con éxito")
            
            else:
                print("No se pudo registrar su reservación")
        return

server_address_httpd = ('192.168.100.63',8080)
httpd = HTTPServer(server_address_httpd, RequestHandler_httpd)
print('Conectado a servidor')
httpd.serve_forever()