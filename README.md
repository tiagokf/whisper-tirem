# Whisper Online - Transcrição de Áudio

Uma aplicação web para transcrição de áudio usando Whisper AI.

## 🚀 Funcionalidades

- ✅ Interface web moderna e responsiva
- ✅ Suporte a múltiplos formatos (MP3, WAV, M4A, OGG, FLAC, AAC, OPUS)
- ✅ Áudios do WhatsApp (.opus)
- ✅ Configurações avançadas (modelo, idioma, precisão)
- ✅ Download SRT e TXT
- ✅ Visualização de segmentos com timestamps
- ✅ Drag & drop de arquivos

## 🛠️ Deploy

### Local
```bash
git clone https://github.com/seu-usuario/whisper-tirem.git
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
1. Conecte seu repositório GitHub
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

## 📄 Licença

MIT License