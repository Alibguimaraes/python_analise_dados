
import meu_modulo as mm

usnasc_a = int(input('Qual o seu ano de nascimento ?'))
usatual_b = int(input('Informe o ano atual'))

print(mm.calcularIdade (usnasc_a ,usatual_b))

idade = mm.calcularIdade (usnasc_a ,usatual_b)

print(f'Voce tem {idade} anos')