import marshal, os, telebot, json, unidecode, webbrowser
from matplotlib import pyplot
from datetime import datetime
from pathlib import Path
from playsound import playsound
from urllib.request import urlopen, Request
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='ITLA')

casosvc = []
ubi = Path("casos.txt")
if ubi.exists():
    archivo = open("casos.txt", "r")
    datos = archivo.read()
    archivo.close()
    casos = json.loads(datos)
else:
    playsound("vacio.wav")    
    input("Aún no ha añadido casos, por favor presione ENTER y empiece a registrar sus casos.")

token = '1054792785:AAELJTsBmRpFM6ZOnmBnfrGzVa3lwayB0u8'
tb = telebot.TeleBot(token)

def limpiar():
    os.system("cls")

def menu():	
    limpiar()
    playsound("bienvenido.wav")    
    print("Bienvenido al programa de Casos de Coronavirus. ")
    playsound("agregar.wav")    
    print("1- Agregar Caso")
    playsound("editar.wav")    
    print("2- Editar Casos.")
    playsound("exportar.wav")    
    print("3- Exportar un Caso.")
    playsound("exportar2.wav")    
    print("4- Exportar todos los Casos.")
    playsound("mapa.wav")    
    print("5- Ver mapa de Casos.")
    playsound("estadistica.wav")    
    print("6- Estadística Mística.")
    playsound("salir.wav")    
    print("7- Salir del programa.")
    
    e = input("\nSeleccione la opción que desea: ")
    if e == "1":
        limpiar()
        playsound("agregar1.wav")    
        print("Opción: Agregar Casos")
        c = []
        c.append(input("Ingrese su cedula: "))
        url = "http://173.249.49.169:88/api/test/consulta/"+c[0]
        date = urlopen(url)
        tmp = json.loads(date.read())

        c.append(tmp["Nombres"])
        c.append(tmp["Apellido1"])
        c.append(tmp["Apellido2"])
        c.append(tmp["FechaNacimiento"])
        c.append(tmp["LugarNacimiento"])
        c.append(input("Ingrese el sexo: "))
        c.append(input("Ingrese el estado (enfermo o recuperado): "))
        c.append(input("Ingrese el teléfono: "))
        c.append(input("Ingrese su correo: "))
        while True:
            try:
                c.append(input('Digita la latitud: '))
                c.append(input('Digita la longitud: '))

                geolocator = Nominatim(user_agent='xdxd')
                coordenadas = c[10], c[11]
                localizacion = geolocator.reverse(coordenadas)
                pais = localizacion.raw['address']['country']
                c.append(localizacion.raw['address']['state'])
                print("Las coordenadas que acaba de escribir pertenecen a esta provincia: "+c[12])
                if pais == 'República Dominicana':
                    break
                else:
                    print('Las coordenadas que ingreso no pertenece a la Republica Dominciana\nVuelva a intentarlo INTENTARLO')
            except:
                input('Error, por favor introduzca coordenadas validas, vuelva a intentarlo')
                menu()
            while True:
                provin=input('Digita la provincia: ')
                if 'ñ' in provin:
                    mi=c[12].lower()
                    if  provin==c[12]:
                        break
                    else:
                        print(f'La provincia que digito no corresponde a las coordenadas {coordenadas}\nVuelva a intentarlo.')
                        menu()
                else:
                    minu=c[12].lower()
                    if provin==unidecode.unidecode(c[12]) or provin==c[12] or provin==minu or provin==unidecode.unidecode(minu):
                        break
                    else:
                        print(f'La provincia que digito no corresponde a las coordenadas {coordenadas}\nVuleva a intentarlo.')
                        menu()

        if c[7] in ("Enfermo","enfermo", "Enferma", "enferma"):
            tb.send_message('-1001239818290',"Acaba de aparecer un nuevo caso de Coronavirus en la Provincia de: "+c[12])
        elif c[7] in ("recuperado", "Recuperado", "Recuperada", "recuperada"):
            tb.send_message('-1001239818290',"Acaba de recuperarse paciente que tenía Coronavirus en la Provincia de: "+c[12])
        signo=["Capricornio", "Acuario", "Piscis", "Aries", "Tauro", "Geminis", "Cancer", "Leo", "Virgo", "Libra", "Escorpio", "Sagitario"]
        fecha=[20,19,20,20,21,21,22,22,22,22,22,21]
        mes= int(tmp["FechaNacimiento"][5:7])
        dia= int(tmp["FechaNacimiento"][8:10])
        mes= mes - 1
        if dia > fecha[mes]:
            mes = mes +1
        if mes == 12: 
            mes=0
        fechazodiacal = signo[mes]
        casosvc.append(c)
        c.append(fechazodiacal)

        datos = json.dumps(casosvc)
        file = open("casos.txt", "w")
        file.write(datos)
        file.close()
        playsound("perfecto.wav")    
        input("El caso ha sido agregado perfectamente.")
        menu()
    
    elif e == "2":
        limpiar()
        playsound("editar2.wav")    
        print("Opción: Editar Casos")
        x=0
        for c in casosvc:
            print(str(x) + ") "+ str(c[0])+", "+ str(c[1])+ ", "+ str(c[2])+" "+str(c[3])+", "+ str(c[5])+", "+str(c[7]))
            x+=1
        editacion = int(input("Ingrese que opción desea editar: "))
        infile = "casos.txt"
        edit_list = str(casosvc)
        limpiar()
        print("1) El nombre")
        print("2) Su primer apellido")
        print("3) Su segundo apellido")
        print("4) La fecha")
        print("5) La nacionalidad")
        print("6) El sexo")
        print("7) El estado")
        print("8) Su teléfono")
        print("9) El correo")
        print("10) La latitud")
        print("11) La longitud")
        print("12) La provincia")

        p = input("\n¿Cuál de estas opciones desea usted editar?: ")
        if p == "1":
            casosvc[editacion][1] = str(input("Ingrese su nuevo nombre: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El nombre ha sido editado a: "+casosvc[editacion][1])
            menu()
        elif p == "2":
            casosvc[editacion][2] = str(input("Ingrese su primer apellido: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El primer apellido ha sido editado a: "+casosvc[editacion][2])
            menu()
        elif p == "3":
            casosvc[editacion][3] = str(input("Ingrese el nuevo 2do apellido: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El segundo apellido ha sido editado a: "+casosvc[editacion][3])
            menu()
        elif p == "4":
            casosvc[editacion][4] = str(input("Ingrese su nueva fecha de nacimiento: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("La fecha ha sido editado a: "+casosvc[editacion][4])
            menu()
        elif p == "5":
            casosvc[editacion][5] = str(input("Ingrese su nueva nacionalidad: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("Su nacionalidad ha sido editado a: "+casosvc[editacion][5])
            menu()
        elif p == "6":
            casosvc[editacion][6] = str(input("Ingrese el sexo nuevo: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("Su sexo ha sido editado a:"+casosvc[editacion][6])
            menu()
        elif p == "7":
            casosvc[editacion][7] = str(input("Ingrese el nuevo estado: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El estado ha sido editado a: "+casosvc[editacion][7])
            menu()
        elif p == "8":
            casosvc[editacion][8] = str(input("Ingrese el nuevo teléfono: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El teléfono ha sido editado a: "+casosvc[editacion][8])
            menu()
        elif p == "9":
            casosvc[editacion][9] = str(input("Ingrese el nuevo correo: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("El correo ha sido editado a: "+casosvc[editacion][9])
            menu()
        elif p == "10":
            casosvc[editacion][10] = str(input("Ingrese la nueva latitud: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("La latitud ha sido editado a: "+casosvc[editacion][10])
            menu()
        elif p == "11":
            casosvc[editacion][11] = str(input("Ingrese la nueva longitud: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("La longitud ha sido editado a: "+casosvc[editacion[11]])
            menu()
        elif p == "12":
            casosvc[editacion][12] = str(input("Ingrese la nueva provincia: "))
            datos = json.dumps(casosvc)
            file = open("casos.txt", "w")
            file.write(datos)
            file.close()
            playsound("correctamente.wav")    
            input("La provincia ha sido editado a: "+casosvc[editacion][12])
            menu()

    elif e == "3":
        limpiar()
        playsound("exportar1.wav")    
        print("Opción: Exportar un solo Caso")
        print("Seleccione el candidato o caso a exportar: ")
        x = 0
        for c in casosvc:
            print(str(x)+") "+str(c[0])+", "+str(c[1])+", "+str(c[2])+" "+str(c[3])+", "+str(c[5])+", "+str(c[7]))
            x+=1
        exportar = int(input("Introduzca el número del caso que quiera exportar: "))
        try:
            url = "http://173.249.49.169:88/api/test/consulta/"+casosvc[exportar][0]
            req = Request(url, headers = {"User-Agent": "Mozilla/5.0"})
            exportacion = urlopen(req)
            cargad = json.loads(exportacion.read())
            html = open('caso1.html','w')
            html1 = '''<!DOCTYPE html>
<html>  
<head>
    <title>Casos</title>
<style>
{
    text-align:center;
}

html{
    background:greenyellow;
}

body{
    margin:50px;
	border:solid 3px black;
	padding:10px;
	background:white;
}
h2 {
    color: black;
}
			</style>
		</head>
		<body>
			<center>
			<table border=''>
			<div id="Datos">
			<h1>Datos del Caso elegido</h1>
				<tr>
					<td>Cedula:</td>
					<td>'''+casosvc[exportar][0]+'''</td>
				</tr>
				<tr>
					<td>Nombre:</td>
					<td>'''+casosvc[exportar][1]+'''</td>
				</tr>
				<tr>
					<td>Primer Apellido:</td>
					<td>'''+casosvc[exportar][2]+'''</td>
				</tr>
				<tr>
					<td>Segundo Apellido:</td>
					<td>'''+casosvc[exportar][3]+'''</td>
				</tr>
				<tr>
					<td>Fecha de Nacimiento:</td>
					<td>'''+casosvc[exportar][4]+'''</td>
                </tr>
                <tr>
					<td>Nacionalidad:</td>
					<td>'''+casosvc[exportar][5]+'''</td>
                </tr>
                <tr>
					<td>Sexo:</td>
					<td>'''+casosvc[exportar][6]+'''</td>
                </tr>
                <tr>
					<td>Estado:</td>
					<td>'''+casosvc[exportar][7]+'''</td>
                </tr>
                <tr>
					<td>Teléfono:</td>
					<td>'''+casosvc[exportar][8]+'''</td>
                </tr>
                <tr>
					<td>Correo:</td>
					<td>'''+casosvc[exportar][9]+'''</td>
				</tr>
			</table>
			</div>
			</center>
			</br>
		</body>
	</html>'''
            html.write(html1)
            html.close()
            playsound("correctamentecaso.wav")    
            input("El caso ha sido exportado.")
            menu()
        except:
            print("El caso que acaba de seleccionar no existe, por favor vuelva a intentarlo.")
            input("Presione ENTER para seguir el programa.")
            limpiar()
            menu()

    elif e == "4":
        limpiar()
        playsound("exportaremos3.wav")    
        print("Opción: Exportar todos los Casos.")
        for k in casosvc:
            def html1():
                html.write('<div class="container">')
                html.write('<div class="card">')
                html.write('<img  class= "img" src="http://173.249.49.169:88/api/test/foto/'+k[0]+'">')
                html.write('<h4>Nombre Completo: '+k[1]+' '+k[2]+' '+k[3]+'</h4>')
                html.write('<h5>Cedula: '+k[0]+'</h5>')
                html.write('<h5>Fecha de Nacimiento: '+k[4]+'</h5>')
                html.write('<h5>Nacionalidad: '+k[5]+'</h5>')
                html.write('<h5>Estado: '+k[7]+'</h5>')
                html.write('</div>')
            folder = "Proyecto Final"
            if os.path.exists(folder) == False:
                os.mkdir(folder)

            html = open(folder+"/Casos.html","w")
            html.write('<html>')
            html.write('<head>')
            html.write('<meta charset="UTF-8">')
            html.write('<title>Casos</title>')
            html.write('<link rel="stylesheet" href="css/estilos.css">')
            html.write('<meta name="viewport" content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">')
            html.write('<style>')
            html.write('''@import url('https://fonts.googleapis.com/css?family=Open+Sans|Roboto');''')
            html.write('html, body{')
            html.write('margin: 0;')
            html.write('padding: 0;')
            html.write('}')
            html.write('body{')
            html.write('text-align: center;')
            html.write('width: 100%;')
            html.write('height: 100%;')
            html.write('font-family: sans-serif;')
            html.write('letter-spacing: 0.03em;')
            html.write('line-height: 1.6;')
            html.write('''font-family: 'Open Sans', sans-serif;''')
            html.write('}')
            html.write('.title{')
            html.write('text-align: center;')
            html.write('font-size: 40px;')
            html.write('color: #FFFFFF;')
            html.write('margin-top: 100px;')
            html.write('font-weight: 100;')
            html.write('''font-family: 'Roboto', sans-serif;''')
            html.write('}')
            html.write('.container{')
            html.write('width: 100%;')
            html.write('max-width: 1200px;')
            html.write('height: 430px;')
            html.write('display: flex;')
            html.write('flex-wrap: wrap;')

            html.write('margin: auto;')
            html.write('}')
            html.write('.esc {')
            html.write('width: 100px;')
            html.write('}')
            html.write('.container .card{')
            html.write('background-color: white;')
            html.write('width: 100%;')
            html.write('height: 100%;')
            html.write('border-radius: 8px;')
            html.write('box-shadow: 0 2px 2px rgba(0, 0, 0, 0.2);')
            html.write('overflow: hidden;')
            html.write('margin: 20px;')
            html.write('text-align: center;')
            html.write('transition: all 0.25s;')
            html.write('}')
            html.write('.container .card img{')
            html.write('padding-top: 30px;')
            html.write('width: 180px;')
            html.write('height: 170px;')
            html.write('}')
            html.write('.container .card h4{')
            html.write('font-weight: 600;')
            html.write('}')
            html.write('.container .card p{')
            html.write('padding: 0 1rem;')
            html.write('font-size: 16px;')
            html.write('font-weight: 300;')
            html.write('}')
            html.write('i {')
            html.write('color: white;')
            html.write('}')
            html.write('.container .card a {')
            html.write('font-weight: 500;')
            html.write('text-decoration: none;')
            html.write('color: #3498db;')
            html.write('}')
            html.write('</style>')
            html.write('</head>')
            html.write('<body bgcolor = black>')
            html.write('<i><h4>Republica Dominicana</h4>')
            html.write('</i>')
            for c in casosvc:
                html1()
            html.write('</div>')
            html.write('</body>')
            html.write('</html>')
            html.close()
            playsound("exportaremoscaso2.wav")    
            input("Los casos han sido exportado. Presione ENTER para continuar.")
            menu()
    
    elif e == "5":
        limpiar()
        playsound("mapacaso.wav")    
        print("Opción: Mapa de los Casos.")
        y = 0
        final = []
        for c in casosvc:
            tmp = """L.marker(["""+casosvc[y][10]+""","""+casosvc[y][11]+"""]).addTo(map)
                .bindPopup('"""+casosvc[y][1]+"""')
                .openPopup();"""
            final.append(tmp)
            y = y + 1
            sep = " "
        html = open('mapa.html','w')
        html1 = """<!DOCTYPE html>
<html>
	<head>
		<link rel="stylesheet" href="https://unpkg.com/leaflet@1.6.0/dist/leaflet.css" />
		<script src="https://unpkg.com/leaflet@1.6.0/dist/leaflet.js"></script>
	</head>
		<body>
			<h1>Mapa Meteoritos</h1>
			<div id="map" style="position: absolute; top:0; bottom:0; left:0; right:0;"></div>
			<script>
				var map = L.map('map').setView([18.45,-69.66], 8);
					
				L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
					attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
				}).addTo(map);

				{Marcador}
					
			</script>
		</body>
</html>"""
        tmp = sep.join(final)
        base = html1.replace("{Marcador}",tmp)
        html.write(base)
        html.close()
        elcaso = "mapa.html"
        webbrowser.get().open(elcaso, new=2)
        playsound("mapaabriendo.wav")    
        input("Su programa esta abriendo. Presione ENTER para continuar.")
        menu()

    elif e == "6":
        limpiar()
        playsound("mistica.wav")    
        print("Opción: Estadística Mística.")
        capricornio = 0
        acuario = 0
        piscis = 0
        aries = 0
        tauro = 0
        geminis = 0
        cancer = 0
        leo = 0
        virgo = 0
        libra = 0
        escorpio = 0
        sagitario = 0
        for sig in casosvc:
            if sig[13]=="Capricornio":
                capricornio+=1
        if sig[13]=="Acuario":
            acuario+=1
        if sig[13]=="Piscis":
            piscis+=1
        if sig[13]=="Aries":
            aries+=1
        if sig[13]=="Tauro":
            tauro+=1
        if sig[13]=="Géminis":
            geminis+=1
        if sig[13]=="Cáncer":
            cancer+=1
        if sig[13]=="Leo":
            leo+=1
        if sig[13]=="Virgo":
            virgo+=1
        if sig[13]=="Libra":
            libra+=1
        if sig[13]=="Escorpio":
            escorpio+=1
        if sig[13]=="Sagitario":
            sagitario+=1
        
        signos = ('Capricornio', 'Acuario', 'Piscis', 'Aries', 'Tauro', 'Géminis', 'Cáncer', 'Leo', 'Virgo', 'Libra', 'Escorpio','Sagitario')
        wy = (capricornio, acuario, piscis, aries, tauro, geminis, cancer, leo, virgo, libra, escorpio, sagitario)
        colour = ('purple','red','green','yellow','blue','red','cyan','pink','black','orange','green','gray')
        pyplot.title("Estadística Mística del CoronaVirus")
        pyplot.bar(signos, height=wy, color=colour, width=0.5)
        playsound("mistica2.wav")    
        pyplot.show()
        menu()  

    elif e == "7":
        playsound("salir2.wav")    
        print("\nOpción: Salir\nPresione ENTER para salir.")
        input()
menu()
limpiar()






