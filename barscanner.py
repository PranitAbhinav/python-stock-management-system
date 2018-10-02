import win32com.client
import pythoncom
import time

global q
def wyto(t):
    global q
    q=t
class E:
    def OnBarcodeIn(self, _1):
        wyto(str(_1))
def barscan():
    scanner=win32com.client.DispatchWithEvents("BarcodeScanner.Reader",E)
    scanner.Visible=True
    global q
    q=""
    while q=="":
     pythoncom.PumpWaitingMessages()
     time.sleep(0.4)
    return q