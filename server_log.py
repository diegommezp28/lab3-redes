import time


def format_filename(addr, now):
    conn_id = str(addr)
    conn_id = conn_id.replace(', ', '-')
    conn_id = conn_id.replace(' ', '_')
    conn_id = conn_id.replace('.', '_')
    conn_id = conn_id.replace('(', '')
    conn_id = conn_id.replace(')', '')
    conn_id = conn_id.replace("'", '')
    dt_string = now.strftime("%Y_%M_%d_%H_%M_%S")
    filename = "log_" + conn_id + "_" + dt_string + ".txt"
    return filename


def log(addr, now, exitosa, tiempo_tot, file_to_send, file_size, enviados, recibidos, benviados, brecibidos):
    filename = format_filename(addr, now)
    f = open("log/" + filename, "x")
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    f.write("Fecha y hora de inicio: " + dt_string + "\n")
    f.write("Archivo enviado: " + file_to_send + " - " + file_size + "\n")
    f.write("Cliente: " + str(addr) + "\n")
    string_estado = "Si" if exitosa else "No"
    f.write("Exitosa: " + string_estado + "\n")
    f.write("Tiempo [s]: " + str(tiempo_tot) + "\n")
    f.write("Cantidad de paquetes enviados: " + enviados + "\n")
    f.write("Cantidad de paquetes recibidos: " + recibidos + "\n")
    f.write("Bytes enviados: " + benviados + "\n")
    f.write("Bytes recibidos: " + brecibidos + "\n")
    f.close()
    return filename
