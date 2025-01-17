class Jogador:
    
    vida = 100
    mana = 50
    maxVida = 100
    maxMana = 50

    def verifica(self):
        if self.vida > self.maxVida:
            self.vida = self.maxVida
        if self.vida < 0:
            self.vida = 0

        if self.mana > self.maxMana:
            self.mana = self.maxMana


    def diminuir_vida(self, dano):
        self.vida -= dano
        self.verifica()

    def golpe_1(self, inimigo):
        if self.mana >= 10:
            inimigo.diminuir_vida(10)
            self.mana -= 10
        

    def golpe_2(self, inimigo):
        if self.mana >= 20:
            inimigo.diminuir_vida(20)
            self.mana -= 20

    def golpe_3(self, inimigo):
        if self.mana >= 30:
            inimigo.diminuir_vida(30)
            self.mana -= 30


    def curar(self, inimigo):
        if self.mana >= 10:
            self.vida += 15
            self.mana -= 10
        self.verifica()


    def cura_mana(self, inimigo):
        if self.mana != 50:
            self.mana += 10
        self.verifica()


    def getVida(self):
        return self.vida
    
    def getMana(self):
        return self.mana

    def __str__(self):
        return f' vida:{self.vida} || mana:{self.mana} '

