from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from slugify import slugify, SLUG_OK
#import slugify
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from reportlab.lib.units import mm
from reportlab_qrcode import QRCodeImage
import time
import ftplib
import secrets
import string
from datetime import date
import locale
locale.setlocale(locale.LC_TIME, "pt_BR")

from datetime import datetime

datetime_str = '23/01/23 13:55:26'
datetime_object = datetime.strptime(datetime_str, '%d/%m/%y %H:%M:%S')

print (datetime_str)

def gentoken():
    alphabet = string.ascii_letters + string.digits
    pw1 = ''.join(secrets.choice(alphabet) for i in range(4)).upper()  # for a 20-character password
    pw2 = ''.join(secrets.choice(alphabet) for i in range(4)).upper()  # for a 20-character password
    pw3 = ''.join(secrets.choice(alphabet) for i in range(4)).upper()  # for a 20-character password
    pw4 = ''.join(secrets.choice(alphabet) for i in range(4)).upper()  # for a 20-character password
    password = '%s-%s-%s-%s'%(str(pw1),str(pw2),str(pw3),str(pw4))
    return password




escola='Colégio Guilherme Dumont Villares'
subdominio='GDV'
emissao = date.today()
emissao = datetime_object




#Informações do Curso
titulo= ['Certificado',418,440]
intro= ['A escola certifica que',418,403]
participacao=['concluiu o curso',418,343]
curso= ['Nome do curso',420,325]
apelido_curso='youraccessformacao'
duracao= ['com uma carga horária total de 2 Horas',418,309]
local = 'São Paulo'
assinatura1=['Nome do responsavel',628,190]
cargo1=['Nome da escola',628,175]






sender_address = 'email_remetente'
sender_pass = 'senha'





def sendserver(path,key):
    session = ftplib.FTP()
    session.encoding = "utf-8"
    host = "ftp.suaurl.com"
    port = 21
    session.connect(host, port)
    print (session.getwelcome())
    try:
        
        session.login('user','pass')
        print ("Logging in...")
    except:
         "failed to login"


    #with open(path, "rb") as file:
    # use FTP's STOR command to upload the file
        #session.storbinary(f"STOR {path}", file)
    currentDir = '/public_html/certificados/%s/%s/%s/'%(subdominio,emissao.strftime("%Y"),apelido_curso)
    
    
    print (currentDir + key+'.pdf')
    session.storbinary('STOR ' + currentDir + key+'.pdf', open(path, 'rb'))

    

    
   # file = open(path,'rb')                  # file to send
   # session.storbinary('%s.pdf'%(key), file)     # send the file
    print ('carregou')
    #file.close()                                    # close file and FTP
    session.quit()




def envia_cert (destinatario,anexo):
    
    #The mail addresses and password
    
    receiver_address = destinatario

    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Certificado YourAccess'


    mail_content = '''



Emissão de certificado de conclusão.


    
    
    '''

    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    attach_file_name = anexo
    attach_file = open(attach_file_name, 'rb') # Open the file as binary mode
    payload = MIMEBase('application', 'octat-stream')
    payload.set_payload((attach_file).read())
    encoders.encode_base64(payload) #encode the attachment

    #add payload header with filename
    payload.add_header('Content-Disposition', 'attachment', filename=attach_file_name)
    message.attach(payload)
    text = message.as_string()


    session.sendmail(sender_address, receiver_address, text)

def qrcode (can,key):
    currentDir = 'https://seusite/certificados/%s/%s/%s/'%(subdominio,emissao.strftime("%Y"),apelido_curso)+key+".pdf"
    qr = QRCodeImage(currentDir, size=30 * mm)
    qr.drawOn(can, 418-15*mm, 150)
    can.drawCentredString(418, 130, key)
    

def emite_certificado (certificado):
    key=gentoken()
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #can.setFillColorRGB(0.36, 0.41, 0.57) #choose your font colour
    can.setFillColorRGB(0.27, 0.27, 0.27) #choose your font colour
    #can.setFont("Courier", 30) #choose your font type and font size
    
    can.setFont("Helvetica", 39) #choose your font type and font size
    can.drawCentredString(certificado['titulo'][1], certificado['titulo'][2], certificado['titulo'][0])


    can.setFillColorRGB(0.165, 0.207, 0.235) #choose your font colour
    can.setFont("Helvetica-Bold", 24) #choose your font type and font size    
    can.drawCentredString(418, 375, certificado['nome'])

    can.setFont("Helvetica-Bold", 14.4) #choose your font type and font size
    can.drawCentredString(certificado['curso'][1], certificado['curso'][2], certificado['curso'][0])


    #can.setFillColorRGB(0.9, 0, 0) #choose your font colour
    can.setFont("Helvetica", 11.1) #choose your font type and font size  
    can.drawCentredString(certificado['intro'][1], certificado['intro'][2], certificado['intro'][0])
    can.drawCentredString(certificado['participacao'][1], certificado['participacao'][2], certificado['participacao'][0])
    can.drawCentredString(certificado['duracao'][1], certificado['duracao'][2], certificado['duracao'][0])
    can.drawCentredString(certificado['localidade'][1], certificado['localidade'][2], certificado['localidade'][0])
    can.drawCentredString(certificado['cargo1'][1], certificado['cargo1'][2], certificado['cargo1'][0])
    #can.drawCentredString(certificado['cargo2'][1], certificado['cargo2'][2], certificado['cargo2'][0])
    can.setFont("Helvetica-Bold", 11.1) #choose your font type and font size  
    can.drawCentredString(certificado['assinatura1'][1], certificado['assinatura1'][2], certificado['assinatura1'][0])
    #Assinatura 2
    #can.drawCentredString(certificado['assinatura2'][1], certificado['assinatura2'][2], certificado['assinatura2'][0])
    
    qrcode(can,key)
    
  



    can.save()

    

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # read your existing PDF
    existing_pdf = PdfFileReader(open("template.pdf", "rb"))
    output = PdfFileWriter()

    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    try:
        os.mkdir('.\Certificados')
    except:
        pass
        
    
    # finally, write "output" to a real file
    path_certificado = "Certificados\%s\%s-"%(subdominio,key)+slugify(nome.replace(" ", "_"))+".pdf"
    outputStream = open(path_certificado, "wb")
    output.write(outputStream)
    outputStream.close()

    
    sendserver(path_certificado,key)
    return path_certificado


f = open('lista_gdv.txt', 'r', encoding="UTF-8")


for linha in f:
    # conectaremos de forma segura usando SSL
    session = smtplib.SMTP_SSL('youraccess.online', 465)

    # fazer login nele
    session.login(sender_address, sender_pass)


    a=linha.split(",")
    nome=a[0]
    print ("nome")
    print (nome)
    destinatario=a[1]
    print (destinatario)
    

    localidade= ['%s, %s de %s de %s'%(local,emissao.strftime("%d"),emissao.strftime("%B").capitalize(),emissao.strftime("%Y")),418,265]
    
    certificado = {
    'titulo': titulo,
    'nome':nome,
    'intro':intro,
    'participacao':participacao,
    'curso': curso,
    'duracao': duracao,
    'localidade': localidade,
    'assinatura1':assinatura1,
    'cargo1':cargo1,
    #'assinatura2':assinatura2,
    #'cargo2':cargo2,
    }

    path_certificado = emite_certificado (certificado)

    try:
        #envia_cert (destinatario,path_certificado)
	  
        print('1a tentativa')
    except:
        time.sleep(10)
        print ("esperou 10 segundos")
        try:
            #envia_cert (destinatario,path_certificado)
            print ('ok')
        except:
            print ("erro no certificado: "+nome)
            pass
        
  

session.quit()

print('ok')

