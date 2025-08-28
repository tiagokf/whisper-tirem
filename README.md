# Whisper Online - Transcrição de Áudio

🎙️ **Aplicação web para transcrição de áudio usando Whisper AI**

🌐 **Demo**: [whisper.tiremoto.com.br](https://whisper.tiremoto.com.br)

## 🚀 Funcionalidades

- ✅ Interface web moderna e responsiva
- ✅ Suporte a múltiplos formatos (MP3, WAV, M4A, OGG, FLAC, AAC, OPUS)
- ✅ Áudios do WhatsApp (.opus)
- ✅ Configurações avançadas (modelo, idioma, precisão)
- ✅ Download SRT e TXT
- ✅ Visualização de segmentos com timestamps
- ✅ Drag & drop de arquivos
- ✅ Tema escuro personalizado

## 🛠️ Deploy

### Local
```bash
git clone git@github.com:tiagokf/whisper-tirem.git
cd whisper-tirem
pip install -r requirements-flask.txt
python app_flask.py
```

### Docker
```bash
docker build -t whisper-app .
docker run -p 5000:5000 whisper-app
```

### EasyPanel
1. Conecte o repositório GitHub: `git@github.com:tiagokf/whisper-tirem.git`
2. O Dockerfile será detectado automaticamente
3. Configure a porta 5000
4. Deploy!

## ⚙️ Modelos Disponíveis

| Modelo | Velocidade | Precisão | Uso Recomendado |
|--------|------------|----------|------------------|
| tiny   | Muito rápida | Básica | Testes rápidos |
| base   | Rápida | Boa | Uso geral |
| small  | Média | Muito boa | Balanço ideal |
| medium | Lenta | Excelente | Produção |
| large  | Muito lenta | Máxima | Máxima qualidade |

## 📝 Formatos Suportados

**Entrada**: MP3, WAV, M4A, OGG, FLAC, AAC, OPUS (WhatsApp)  
**Saída**: SRT (legendas), TXT (texto)

## 🌍 Idiomas

Suporte a 90+ idiomas com detecção automática.

## 🎨 Tecnologias

- **Backend**: Flask + Faster-Whisper
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Deploy**: Docker + EasyPanel
- **IA**: OpenAI Whisper

## 📄 Licença

MIT License