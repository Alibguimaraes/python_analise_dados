class Carro:
    def __init__(self,modelo, cor):
        #atributos do carro
        self.modelo = modelo
        self.cor = cor
        self.velocidade = 0  #o carro começa parado
    
    def acelerar(self, incremento):
        self.velocidade += incremento
        print(f'O modelo de carro {self.modelo} acelerou para {self.velocidade}km/h')

    def reduzir (self, decremento):
        self.velocidade -= decremento
        print(f'O modelo de carro {self.modelo} reduziu para {self.velocidade}km/h')

    def parar (self):
        self.velocidade = 0
        print(f'O modelo de carro {self.modelo} parou {self.velocidade}km/h')

    def reduzir_velocidade(self):
        while self.velocidade > 0:
            self.velocidade -= 5
            print(f'O {self.modelo} reduziu para {self.velocidade}km/h')
        print (f'{self.modelo} está parado')
        
#criar o objetio carro

meu_carro = Carro ('Fusca','Amarelo')
outro_carro =Carro ('Jepp Compass','Azul')

#Usar os metodos 
meu_carro.acelerar(20)
meu_carro.acelerar(30)
outro_carro.acelerar(100)
outro_carro.reduzir(30)
outro_carro.reduzir_velocidade()
outro_carro.parar ()
desacelerar =int(input("Quero reduzir a velocidade para quanto:"))
outro_carro.reduzir_velocidade(de)
