#Sistemde aktivasyon kodu uyeliksistemi.py dosyasının olduğu yerde otomatik açılıyor
import json
from random import randint

class Sistem:
    def __init__(self):
        self.durum = True
        self.veriler = self.verileriAl()
    def calistir(self):
        self.menuGoster()
        secim = self.menuSecimYap()

        if secim == 1:
            self.girisYap()
        if secim == 2:
            self.kayitOl()
        if secim == 3:
            self.sifremiUnuttum()
        if secim == 4:
            self.cikis()

    def menuGoster(self):
        print("""
1-Giris Yap
2-Kayit Ol
3-Sifremi Unuttum
4-Cikis

        """)

    def menuSecimYap(self):
        while True:
            try:
                secim = int(input("Seciminizi giriniz: "))
                while secim < 1 or secim > 4:
                    secim = int(input("Lutfen 1-4 arasi deger giriniz: "))
                break
            except ValueError:
                print("Lutfen sayi giriniz!\n")
        
        return secim
    def verileriAl(self):
        try:
            with open("kullanicilar.json","r") as dosya:
                veriler = json.load(dosya)
        except FileNotFoundError:
            with open("kullanicilar.json","w") as dosya:
                dosya.write("{}")
            with open("kullanicilar.json","r") as dosya:
                veriler = json.load(dosya)
        return veriler

    def girisYap(self):
        kadi = input("Kullanici adinizi giriniz: ")
        sifre = input("Sifrenizi giriniz: ")
        

        durum = self.kontrolEt(kadi,sifre)


        if durum:
            self.girisBasarili()
            print("Bu kullanici adi veya sifre sistemde kayitli!")
        else:

            aktivasyonKodu = self.aktivasyonKoduGonder()
            akdurum = self.aktivasyonKontrolEt(aktivasyonKodu)
            if akdurum:
                
                print("Aktivasyon dogru!")
            else:
                print("Aktivasyon gecersiz!")
            self.girisBasarisiz("Bilgiler yanlış!")
       

    def kayitOl(self):
        kadi = input("Kullanici adinizi giriniz: ")
        while True:
            sifre = input("Sifrenizi giriniz: ")
            tsifre = input("Sifrenizi tekrar giriniz: ")

            if sifre == tsifre:
                break
            else:
                print("Sifreler eslesmiyor.Lutfen tekrar giriniz: ")
        
        email = input("E-posta adresinizi giriniz: ")

        durum =self.kayitVarMi(kadi,email)
        
        if durum:
            print("Bu kullanici adi veya e-posta sistemde kayitli!")
        else:
            aktivasyonKodu = self.aktivasyonKoduGonder()
            akdurum = self.aktivasyonKontrolEt(aktivasyonKodu)

            if akdurum:
                self.kaydet(kadi,sifre,email)
            else:
                print("Aktivasyon gecersiz!")

    def sifremiUnuttum(self):
        mail = input("E-posta adresini giriniz: ")

        if self.mailVarMi(mail):
            with open("aktivasyon.txt","w") as dosya:
                aktivasyon = str(randint(1000,9999))
                dosya.write(aktivasyon)
        

            aktgir = input("Sifrenizi degistirmek icin aktivasyonu giriniz!: ")
    
            if aktgir == aktivasyon:
                while True:
                    yeniSifre= input("Yeni sifrenizi giriniz: ")
                    yeniSifreTekrar= input("Yeni sifrenizi tekrar giriniz: ")
    
                    if yeniSifre == yeniSifreTekrar:
                        
                        break
                    else:
                        print("Girdiginiz sifre uyusmuyor.Tekrar giriniz!!")
    
            self.veriler = self.verileriAl()
    
            for kullanici in self.veriler["kullanicilar"]:

                if kullanici["mail"] == mail:
                    kullanici["sifre"] = str(yeniSifre)
                

            with open("kullanicilar.json","w") as dosya:
                json.dump(self.veriler,dosya)
                print("Sifre basari ile degisti!")
        else:
            print("Boyle bir mail sistemimizde kayitli degil.")

        
    def mailVarMi(self,mail):
        self.veriler = self.verileriAl()

        for kullanici in self.veriler["kullanicilar"]:
            if kullanici["mail"] == mail:
                return True

        return False

    def cikis(self):
        self.durum = False
        print("Cikis yapildi!!!")

    def kontrolEt(self,kadi,sifre):
        self.veriler = self.verileriAl()

        for kullanici in self.veriler["kullanicilar"]:
            if kullanici["kadi"] == kadi and kullanici["sifre"] == sifre and kullanici["timeout"] == "0" and kullanici["aktivasyon"] == "Y":
                
                return True
            
            return False


    def girisBasarisiz(self,sebep):
        print(sebep)

    def girisBasarili(self):
        print("Hos geldiniz!")

        self.durum = False

    def kayitVarMi(self,kadi,mail):
        self.veriler = self.verileriAl()
        try:
            for kullanici in self.veriler["kullanicilar"]:
                if kullanici["kadi"] == kadi and kullanici["email"] == mail and kullanici["mail"] == mail:
                    return True
        except KeyError:
            return False
        return False



    def kayitBasarisiz(self,sebep):
        pass

    def aktivasyonKoduGonder(self):
        with open("aktivasyon.txt","w") as dosya:
            aktivasyon = str(randint(1000,9999))
            dosya.write(aktivasyon)

        return aktivasyon
            

    def aktivasyonKontrolEt(self,aktivasyon):
        aktivasyonKoduAl = input("Aktivasyon kodunuzu giriniz: ")
        if aktivasyon == aktivasyonKoduAl:
            return True
        else:
            return False
        

    def kaydet(self,kadi,sifre,mail):
        self.veriler = self.verileriAl()
        try:
            self.veriler["kullanicilar"].append({"kadi" : kadi,"sifre" : sifre,"mail": mail,"aktivasyon":"Y","timeout" : "0"})
        except KeyError:
            self.veriler["kullanicilar"] = []
            self.veriler["kullanicilar"].append({"kadi" : kadi,"sifre" : sifre,"mail": mail,"aktivasyon":"Y","timeout" : "0"})

        with open("kullanicilar.json","w") as dosya:
            json.dump(self.veriler,dosya)
            print("Kayit basarıyla olusturuldu!")


    

    

sistem = Sistem()

while sistem.durum:
    sistem.calistir()
               