🧛‍♂️ Cofre Mágico de Doces 🎃

Um divertido e seguro sistema de armazenamento de doces criptografados, com tema de Halloween, desenvolvido em Python utilizando:

🧩 Tkinter – para a interface gráfica assustadoramente amigável

🍬 MongoDB (Atlas) – para armazenar os doces coletados pelas crianças

🔐 Criptografia Fernet (Cryptography) – para proteger os tipos de doces com segurança

👻 Animações e efeitos visuais – fantasminhas, cores piscantes e uma ambientação sombria

🎯 Funcionalidades

Adicionar doces: registra o nome da criança, tipo de doce e quantidade, salvando os dados criptografados no banco.

Listar doces: exibe todos os doces armazenados no banco em formato criptografado.

Descriptografar doces: revela o tipo real de doce, junto com data e hora de registro.

Interface interativa: botões temáticos, mensagens amigáveis e efeitos visuais de Halloween.

🧠 Tecnologias e Bibliotecas

pymongo — integração com MongoDB

cryptography.fernet — criptografia simétrica dos dados

tkinter — interface gráfica

datetime — registro de data e hora

random — efeitos visuais aleatórios (fantasminhas e luzes)

💾 Estrutura de Armazenamento

Cada registro é salvo no MongoDB com o formato:

{
  "child": "Isabella",
  "candy_type": "gAAAAABn...",  // criptografado
  "qty": 5,
  "timestamp": "2025-10-31T23:59:59Z"
}

🧙‍♀️ Experiência

O programa simula um cofre mágico de guloseimas, com uma interface lúdica e misteriosa.
É ideal para demonstrar:

Conceitos de criptografia de dados

Uso de MongoDB em Python

Criação de interfaces gráficas interativas

Integração entre segurança + design criativo

🚀 Execução

Instale as dependências:

pip install pymongo cryptography


Execute o script principal:

python cofre_magico_doces.py


Interaja com o sistema e veja a magia acontecer! 🎃

📜 Licença

Distribuído sob a licença MIT.
Feito com 🧡 e 🎃 por Isabella Gimenes, Vitor Farias e Vitor Henrique
