import sqlite3
import sys
import mail
import time


# schermata iscritti
def addiscritti(lista):
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.executemany("INSERT OR IGNORE INTO Iscritti(mail, sent) VALUES(?, ?);", ((i, 0) for i in lista))
    conn.commit()
    conn.close()
    return


def _getalliscritti():  # fornisce tutti gli iscritti
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.execute("SELECT mail, sent FROM Iscritti")
    lista = cur.fetchall()
    conn.close()
    return lista


def getiscritti():  # fornisce gli iscritti che non hanno ricevuto la newsletter
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.execute("SELECT mail FROM Iscritti WHERE sent=0")   # prendiamo dal databse solo le mail che non abbiamo
    lista = list( i[0] for i in cur.fetchall() )            # ancora inviato
    conn.close()
    return lista


def updatesubs(mail_list):
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.executemany('UPDATE Iscritti SET sent=1 WHERE mail=?', mail_list)
    conn.commit()
    conn.close()
    return


# schermata iscritti
def _resetiscritti():
    start_time = time.time()
    print('Resetting all subscribers...')
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.execute('UPDATE Iscritti SET sent=0')
    conn.commit()
    conn.close()
    print('Done!------------- Time elapsed : ', round(time.time() - start_time, 6), '\n')
    return

#schermata iscritti
def deleteiscritto(mail):
    print('deleting sub :', mail)
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM Iscritti WHERE mail=?', (mail,))
    if cur.rowcount > 0:
        print(mail, ' found in subs')
        print('deleted')
    else :
        print(mail, ' not in subs')
        print('Nothing to delete')
    conn.commit()
    conn.close()
    print('closed db connection')
    return


def _resetdb():
    conn = sqlite3.connect('iscritti.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM Iscritti')
    conn.commit()
    conn.close()
    return


def checkend(username, password, subject, filecont):

    lista = getiscritti()

    if lista :  # Non ha finito qualcuno non ha ricevuto la notizia
        mail.mailer(username, password, subject, filecont)
    else :  # Ha finito
        # _resetiscritti()
        pass
    return


def main():
    #_resetdb()
    print(_getalliscritti())


if __name__ == "__main__":
    sys.exit(main())
