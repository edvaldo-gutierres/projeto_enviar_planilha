# Nome do arquivo de entrada
input_file_name = 'requirements.txt'
# Nome do arquivo de saída
output_file_name = 'requirements.txt'

# Abrir o arquivo de entrada para leitura e o arquivo de saída para escrita
with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
    # Ler cada linha do arquivo de entrada
    for line in input_file:
        # Verificar se a linha contém o caractere '@'
        if '@' not in line:
            # Se não contiver, escrever a linha no arquivo de saída
            output_file.write(line)

print(f"Linhas com '@' removidas do arquivo '{input_file_name}' e salvas em '{output_file_name}'.")