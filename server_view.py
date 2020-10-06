def preguntar():
    num_con = 0
    file_to_send = ""
    print('Bienvenido al servidor TCP')

    print('Primero, ingrese el numero de conexiones')
    print('Recuerde que pueden ser entre 1 y 25, o ingrese 0 para apagar')
    num_con = int(input())
    continuar = True
    terminar = False
    if (num_con != 0 and num_con < 26):
        print('Se esperarán ' + str(num_con) + ' conexiones')
        while continuar:
            print(
                'Escoja el archivo a transmitir (escriba el número correspondiente u oprima 0 para salir):')
            print('1. video1.mkv [104.4 MB]')
            print('2. video2.webm [53.8 MB]')
            print('3. archivo3.pdf [296.3 MB]')
            num_file = int(input())
            if num_file == 1:
                file_to_send = "video1.mkv"
                continuar = False
            elif num_file == 2:
                file_to_send = "video2.webm"
                continuar = False
            elif num_file == 3:
                file_to_send = "archivo3.pdf"
                continuar = False
            elif num_file == 0:
                terminar = True
                continuar = False
                break
            else:
                print('Archivo invaldo, escoja uno nuevamente u oprima 0 para salir')
            if num_file > 0 and num_file < 4:
                print('Esperando ' + str(num_con) +
                      ' conexiones para enviar ' + file_to_send + ' ...')

    else:
        terminar = True
    return terminar, num_con, file_to_send
