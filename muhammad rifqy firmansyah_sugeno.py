#Nama   : Muhammad Rifqy Firmansyah
#NIM    : 191011402526
#Kelas  : 06TPLE025 

#Fuzzy Sugeno
#Studi Kasus : putaran mesin CPT

#Kecepatan Putaran Mesin : min 300 rpm dan max 600 rpm.
#Banyaknya roller  : sedikit 3 dan banyak 6.
#Tingkat Kerusakan  : rendah 20, sedang 40, dan 60 tinggi.

def down(x, xmin, xmax):
    return (xmax- x) / (xmax - xmin)

def up(x, xmin, xmax):
    return (x - xmin) / (xmax - xmin)

class roller():
    minimum = 3
    maximum = 6

    def sedikit(self, x):
        if x >= self.maximum:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.maximum)

    def banyak(self, x):
        if x <= self.minimum:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.minimum, self.maximum)

class Kerusakan():
    minimum = 20
    medium = 40
    maximum = 60

    def rendah(self, x):
        if x >= self.medium:
            return 0
        elif x <= self.minimum:
            return 1
        else:
            return down(x, self.minimum, self.medium)
    
    def sedang(self, x):
        if self.minimum < x < self.medium:
            return up(x, self.minimum, self.medium)
        elif self.medium < x < self.maximum:
            return down(x, self.medium, self.maximum)
        elif x == self.medium:
            return 1
        else:
            return 0

    def tinggi(self, x):
        if x <= self.medium:
            return 0
        elif x >= self.maximum:
            return 1
        else:
            return up(x, self.medium, self.maximum)

class Putaran():
    minimum = 300
    maximum = 600
    
    def lambat(self, α):
        if α >= self.maximum:
            return 0
        elif α <= self.minimum:
            return 1

    def cepat(self, α):
        if α <= self.minimum:
            return 0
        elif α >= self.maximum:
            return 1

    # 2 permintaan 3 persediaan
    def inferensi(self, jumlah_roller, jumlah_kerusakan):
        rll = roller()
        krs = Kerusakan()
        result = []
        
        # [R1] Jika Roller SEDIKIT, dan kerusakan RENDAH, 
        #     MAKA Putaran = 300
        α1 = min(rll.sedikit(jumlah_roller), krs.rendah(jumlah_kerusakan))
        z1 = self.minimum
        result.append((α1, z1))

        # [R2] Jika Roller SEDIKIT, dan kerusakan SEDANG, 
        #     MAKA Putaran = 10 * jumlah_kerusakan + 100
        α2 = min(rll.sedikit(jumlah_roller), krs.sedang(jumlah_kerusakan))
        z2 = 10 * jumlah_kerusakan + 100
        result.append((α2, z2))

        # [R3] Jika Roller SEDIKIT, dan Kerusakan TINGGI, 
        #     MAKA Putaran = 10 * jumlah_kerusakan + 200
        α3 = min(rll.sedikit(jumlah_roller), krs.tinggi(jumlah_kerusakan))
        z3 = 10 * jumlah_kerusakan + 200
        result.append((α3, z3))

        # [R4] Jika Roller BANYAK, dan Kerusakan RENDAH,
        #     MAKA Putaran = 5 * jumlah_pakaian + 2 * jumlah_kerusakan
        α4 = min(rll.banyak(jumlah_roller), krs.rendah(jumlah_kerusakan))
        z4 = 5 * jumlah_roller + 2 * jumlah_kerusakan
        result.append((α4, z4))

        # [R5] Jika Roller BANYAK, dan Kerusakan SEDANG,
        #     MAKA Putaran = 5 * jumlah_pakaian + 4 * jumlah_Kerusakan + 100
        α5 = min(rll.banyak(jumlah_roller), krs.sedang(jumlah_kerusakan))
        z5 = 5 * jumlah_roller + 4 * jumlah_kerusakan + 100
        result.append((α5, z5))

        # [R6] Jika Roller BANYAK, dan Kerusakan TINGGI,
        #     MAKA Putaran = 5 * jumlah_roller + 5 * jumlah_kerusakan + 300
        α6 = min(rll.banyak(jumlah_roller), ktr.tinggi(jumlah_kerusakan))
        z6 = 5 * jumlah_roller + 5 * jumlah_kerusakan + 300
        result.append((α6, z6))

        return result
    
    def defuzifikasi(self, jumlah_roller, jumlah_kerusakan):
        inferensi_values = self.inferensi(jumlah_roller, jumlah_kerusakan)
        return sum([(value[0]* value[1]) for value in inferensi_values]) / sum([value[0] for value in inferensi_values])